from cli.kuro import cmd_build
from cli.kuro import cmd_bundle
from cli.kuro import cmd_exec
from cli.kuro import cmd_native_artifact
from cli.kuro import cmd_artifact_verify
from cli.kuro import cmd_artifact_pack
import json
import subprocess
from compiler.artifacts import ArtifactError, read_program


def test_build_writes_validated_ir_artifact(tmp_path, capsys):
    source = tmp_path / "hello.kuro"
    output = tmp_path / "build" / "hello.kuro.ir"
    source.write_text('Print "hello".', encoding="utf-8")

    assert cmd_build(str(source), str(output)) == 0
    assert "PRINT" in output.read_text(encoding="utf-8")
    assert "built IR" in capsys.readouterr().out


def test_exec_runs_serialized_ir_artifact(tmp_path, capsys):
    source = tmp_path / "hello.kuro"
    output = tmp_path / "hello.kuro.ir"
    source.write_text('Print "hello artifact".', encoding="utf-8")

    assert cmd_build(str(source), str(output)) == 0
    capsys.readouterr()
    assert cmd_exec(str(output)) == 0
    assert capsys.readouterr().out == "hello artifact\n"


def test_build_rejects_invalid_source(tmp_path, capsys):
    source = tmp_path / "bad.kuro"
    output = tmp_path / "bad.ir"
    source.write_text("Print Missing.", encoding="utf-8")

    assert cmd_build(str(source), str(output)) == 1
    assert not output.exists()
    assert "E4001" in capsys.readouterr().err


def test_bundle_writes_portable_application_artifact(tmp_path):
    source = tmp_path / "hello.kuro"
    output = tmp_path / "dist" / "hello.kuro.app"
    source.write_text('Print "hello".', encoding="utf-8")
    assert cmd_bundle(str(source), str(output)) == 0
    bundle = json.loads(output.read_text(encoding="utf-8"))
    assert bundle["format"] == "kuro.app/1"
    assert bundle["language"] == "kuro"
    assert bundle["artifact"] == "validated-ir"
    assert "PRINT" in bundle["ir"]


def test_exec_runs_portable_application_bundle(tmp_path, capsys):
    source = tmp_path / "hello.kuro"
    output = tmp_path / "dist" / "hello.kuro.app"
    source.write_text('Print "hello bundle".', encoding="utf-8")
    assert cmd_bundle(str(source), str(output)) == 0
    capsys.readouterr()
    assert cmd_exec(str(output)) == 0
    assert capsys.readouterr().out == "hello bundle\n"


def test_artifact_contains_canonical_integrity_metadata(tmp_path, capsys):
    source = tmp_path / "hello.kuro"
    artifact = tmp_path / "hello.kuro.ir"
    source.write_text('Print "integrity".', encoding="utf-8")
    assert cmd_build(str(source), str(artifact)) == 0
    capsys.readouterr()
    document = json.loads(artifact.read_text(encoding="utf-8"))
    assert document["schema"] == "kuro.artifact/1"
    assert len(document["bytecode_sha256"]) == 64


def test_artifact_integrity_rejects_tampering(tmp_path, capsys):
    source = tmp_path / "hello.kuro"
    artifact = tmp_path / "hello.kuro.ir"
    source.write_text('Print "integrity".', encoding="utf-8")
    assert cmd_build(str(source), str(artifact)) == 0
    capsys.readouterr()
    document = json.loads(artifact.read_text(encoding="utf-8"))
    document["bytecode"]["main"][0]["args"][0] = "tampered"
    artifact.write_text(json.dumps(document), encoding="utf-8")
    try:
        read_program(artifact)
    except ArtifactError as error:
        assert "integrity" in str(error)
    else:
        raise AssertionError("tampered artifact was accepted")


def test_artifact_verify_rejects_wrong_schema_and_language(tmp_path):
    source = tmp_path / "hello.kuro"
    artifact = tmp_path / "hello.kuro.ir"
    source.write_text('Print "metadata".', encoding="utf-8")
    assert cmd_build(str(source), str(artifact)) == 0
    document = json.loads(artifact.read_text(encoding="utf-8"))
    document["schema"] = "kuro.artifact/0"
    artifact.write_text(json.dumps(document), encoding="utf-8")
    try:
        read_program(artifact)
    except ArtifactError as error:
        assert "schema" in str(error)
    else:
        raise AssertionError("invalid artifact schema was accepted")


def test_artifact_verify_is_a_non_executing_ci_gate(tmp_path, capsys):
    source = tmp_path / "hello.kuro"
    artifact = tmp_path / "hello.kuro.ir"
    source.write_text('Print "verified".', encoding="utf-8")
    assert cmd_build(str(source), str(artifact)) == 0
    capsys.readouterr()
    assert cmd_artifact_verify(str(artifact)) == 0
    assert "valid Kuro artifact" in capsys.readouterr().out


def test_binary_artifact_is_reusable_by_exec_and_rejects_corruption(tmp_path, capsys):
    source = tmp_path / "hello.kuro"
    json_artifact = tmp_path / "hello.kuro.ir"
    binary_artifact = tmp_path / "hello.kuro.bin"
    source.write_text('Print "binary artifact".', encoding="utf-8")
    assert cmd_build(str(source), str(json_artifact)) == 0
    capsys.readouterr()
    assert cmd_artifact_pack(str(json_artifact), str(binary_artifact)) == 0
    capsys.readouterr()
    assert binary_artifact.read_bytes().startswith(b"KRA\x01")
    assert cmd_artifact_verify(str(binary_artifact)) == 0
    capsys.readouterr()
    assert cmd_exec(str(binary_artifact)) == 0
    assert capsys.readouterr().out == "binary artifact\n"
    data = bytearray(binary_artifact.read_bytes())
    data[-1] ^= 1
    binary_artifact.write_bytes(data)
    assert cmd_artifact_verify(str(binary_artifact)) == 1
    assert "integrity" in capsys.readouterr().err


def test_binary_pack_preserves_application_format_and_entry(tmp_path, capsys):
    source = tmp_path / "hello.kuro"
    bundle = tmp_path / "hello.kuro.app"
    binary = tmp_path / "hello.kuro.bin"
    source.write_text('Print "bundle binary".', encoding="utf-8")
    assert cmd_bundle(str(source), str(bundle)) == 0
    capsys.readouterr()
    assert cmd_artifact_pack(str(bundle), str(binary)) == 0
    capsys.readouterr()
    from compiler.artifacts import read_artifact_document
    document = read_artifact_document(binary)
    assert document["format"] == "kuro.app/1"
    assert document["entry"] == "hello.kuro"


def test_native_artifact_produces_python_free_standalone_executable(tmp_path, capsys):
    source = tmp_path / "hello.kuro"
    artifact = tmp_path / "hello.kuro.ir"
    executable = tmp_path / "hello-native"
    source.write_text('Print "standalone artifact".', encoding="utf-8")
    assert cmd_build(str(source), str(artifact)) == 0
    capsys.readouterr()
    assert cmd_native_artifact(str(artifact), str(executable)) == 0
    capsys.readouterr()
    run = subprocess.run([str(executable)], capture_output=True, text=True, check=True)
    assert run.stdout == "standalone artifact\n"
