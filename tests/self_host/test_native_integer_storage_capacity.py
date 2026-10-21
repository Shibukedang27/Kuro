"""Regression coverage for expanded fixed native integer collection storage."""
from __future__ import annotations

import hashlib
import json
import platform
import subprocess

import pytest

from compiler.pipeline import run_source
from compiler.self_host import build_native_artifact_launcher, build_native_compiler, compile_with_kuro_driver
from test_native_codegen import run_codegen, x86_linux_codegen
from test_native_integer_storage import execute, generate, requires_linux
from test_vm_cross import BYTECODE_RE, VM


LINUX_X86 = platform.system() == "Linux" and platform.machine().lower() in {"x86_64", "amd64"}


@pytest.fixture(scope="module")
def native_compiler_image(tmp_path_factory):
    """Build one fresh Kuro compiler for accepted and rejected source cases."""
    if not LINUX_X86:
        pytest.skip("fresh native compiler fixture executes Linux x86-64 images")
    image = tmp_path_factory.mktemp("native-integer-capacity-compiler") / "kuro-compiler"
    build_native_compiler(None, image)
    return image


@pytest.fixture(scope="module")
def native_compiler(native_compiler_image):
    """Require complete hosted/native token parity for every capacity witness."""
    image = native_compiler_image
    compiler_sha256 = hashlib.sha256(image.read_bytes()).hexdigest()

    def compile_source_tokens(source: str, artifact_dir):
        completed = subprocess.run(
            [str(image)], input=source, text=True, capture_output=True,
            check=False, timeout=30,
        )
        assert (completed.returncode, completed.stderr) == (0, "")
        framed_output = completed.stdout
        assert framed_output.startswith("kuro.bytecode/1\n")
        assert framed_output.endswith("\n")
        tokens = framed_output.splitlines()[1:]
        assert 0 < len(tokens) < 4096
        hosted = compile_with_kuro_driver(source)
        assert hosted["CompilerFailed"] == 0
        assert hosted["CompilerOutput"] == tokens
        assert hosted["CompilerInstructionCount"] == len(tokens)
        artifact_dir.mkdir(parents=True, exist_ok=True)
        (artifact_dir / "native-compiler-record.json").write_text(
            json.dumps({
                "native_compiler_sha256": compiler_sha256,
                "source": source,
                "framed_token_output": framed_output,
                "hosted_tokens": hosted["CompilerOutput"],
                "tokens": tokens,
            }, indent=2) + "\n",
            encoding="utf-8",
        )
        return tokens

    return compile_source_tokens


@requires_linux
def test_fresh_bytecode_stage_compiler_reproduces_self_and_large_initializer(
    tmp_path, native_compiler_image
):
    # Direct native execution is not enough: the authored VM must execute the
    # compiler too. In particular, do not introduce Return inside its While.
    launcher = tmp_path / "kuro-bytecode"
    build_native_artifact_launcher(launcher, target="x86_64-linux")
    source = native_compiler_image.with_suffix(".source.kuro").read_text(encoding="utf-8")
    stage1 = subprocess.run(
        [str(native_compiler_image)], input=source, text=True, capture_output=True,
        check=False, timeout=30,
    )
    assert (stage1.returncode, stage1.stderr) == (0, "")
    assert stage1.stdout.startswith("kuro.bytecode/1\n")
    (tmp_path / "stage1.kurobc").write_text(stage1.stdout, encoding="utf-8")
    for name, program, expected in [
        ("self", source, stage1.stdout),
        ("initializer", f"Items = {_values(272)};\nGet Items -1; Print @_.\n", None),
    ]:
        if expected is None:
            direct = subprocess.run(
                [str(native_compiler_image)], input=program, text=True, capture_output=True,
                check=False, timeout=30,
            )
            assert (direct.returncode, direct.stderr) == (0, "")
            expected = direct.stdout
        framed_input = stage1.stdout + "kuro.input/1\n" + program
        rebuilt = subprocess.run(
            [str(launcher)], input=framed_input, text=True, capture_output=True,
            check=False, timeout=120,
        )
        (tmp_path / f"{name}-stage-input.kurobc").write_text(framed_input, encoding="utf-8")
        (tmp_path / f"{name}-stage-output.kurobc").write_text(rebuilt.stdout, encoding="utf-8")
        assert (rebuilt.returncode, rebuilt.stdout, rebuilt.stderr) == (0, expected, "")


def _values(count: int, start: int = 0) -> str:
    return ", ".join(str(start + index) for index in range(count))


def _run_authored_vm(tokens):
    bytecode = ", ".join(json.dumps(token) for token in tokens)
    vm_source = BYTECODE_RE.sub("", VM.read_text(encoding="utf-8"), count=1)
    result = run_source(f"BytecodeOut = {bytecode};\n" + vm_source)
    assert result.ok, result.compile.diags.render_all() if not result.compile.ok else result.runtime_error
    return result.interpreter.env


def _assert_source_and_vm(source: str, tokens, expected: str, *, bounds_failure=False) -> None:
    hosted = run_source(source)
    assert hosted.compile.ok, hosted.compile.diags.render_all()
    assert hosted.stdout == expected
    authored = _run_authored_vm(tokens)
    vm_stdout = "".join(
        (display if display else str(value)) + "\n"
        for value, display in zip(authored.get("VMOutput", []), authored.get("VMOutputDisplay", []))
    )
    assert vm_stdout == expected
    if bounds_failure:
        assert hosted.runtime_error is not None
        assert hosted.runtime_error.code == "E6001"
        assert authored["VMFailed"]
    else:
        assert hosted.runtime_error is None
        assert not authored["VMFailed"]


def test_run_codegen_accepts_272_and_rejects_273_cells_portably():
    def compile_initializer(count: int):
        tokens = ["BC_MULTI_BEGIN"]
        for value in range(count):
            tokens.extend(("BC_CONST", str(value)))
        tokens.extend(("BC_STORE_MULTI", "Items", "BC_CONST", "0", "BC_PRINT"))
        bytecode = ", ".join(json.dumps(token) for token in tokens)
        return run_codegen(
            bytecode, target="x86_64-linux", execution_target="x86_64-linux"
        )

    accepted = compile_initializer(272)
    assert accepted["NativeFailed"] == 0
    assert accepted["NativeOut"]

    rejected = compile_initializer(273)
    assert (rejected["NativeFailed"], rejected["NativeOut"]) == (1, "")


@pytest.mark.parametrize("tokens", [
    ["BC_MULTI_BEGIN"],
    ["BC_MULTI_BEGIN", "BC_CONST", "1"],
    ["BC_MULTI_BEGIN", "BC_STORE_MULTI", "Items"],
    ["BC_MULTI_BEGIN", "BC_CONST", "1", "BC_STORE_MULTI", "Items"],
], ids=["unterminated", "missing-owner", "empty", "singleton"])
def test_hosted_generator_rejects_invalid_initializers_before_name_lookup(tokens):
    env = run_codegen(
        ", ".join(json.dumps(token) for token in tokens),
        target="x86_64-linux", execution_target="x86_64-linux",
    )
    assert (env["NativeFailed"], env["NativeOut"]) == (1, "")


@requires_linux
@pytest.mark.parametrize("count", [190, 191, 272])
def test_hosted_and_fresh_native_compiler_initializer_boundary(
    count, tmp_path, x86_linux_codegen, native_compiler
):
    source = f"Items = {_values(count)};\nGet Items -1; Print @_.\n"
    tokens = native_compiler(source, tmp_path)
    expected = f"{count - 1}\n"
    _assert_source_and_vm(source, tokens, expected)
    result = execute(x86_linux_codegen, source, tmp_path, tokens=tokens)
    assert (result.returncode, result.stdout, result.stderr) == (0, expected, "")


@requires_linux
@pytest.mark.parametrize("suffix", [",;", ",", ",, 1;", ", * 1;", ", (1 + );", ""])
def test_fresh_native_compiler_rejects_malformed_long_initializer(
    suffix, tmp_path, native_compiler_image
):
    source = f"Items = {_values(272)}{suffix}"
    completed = subprocess.run(
        [str(native_compiler_image)], input=source, text=True, capture_output=True,
        check=False, timeout=30,
    )
    (tmp_path / "source.kuro").write_text(source, encoding="utf-8")
    (tmp_path / "compiler-output.txt").write_text(completed.stdout, encoding="utf-8")
    assert (completed.returncode, completed.stdout, completed.stderr) == (
        1, "kuro.compile-error/1\n", "",
    )


@requires_linux
def test_actual_generator_272_mask_and_256_snapshot_runtime_index_witness(
    tmp_path, x86_linux_codegen, native_compiler
):
    source = (
        f"Masks = {_values(16, 100)};\n"
        f"Snapshots = {_values(256)};\n"
        "Frame = 0; Slot = 0; Position = Frame * 16 + Slot;\n"
        "Set Snapshots Position to 700;\n"
        "Frame = 15; Slot = 15; Position = Frame * 16 + Slot;\n"
        "Set Snapshots Position to 701;\n"
        "Frame = 7; Slot = 9; Position = Frame * 16 + Slot;\n"
        "Set Snapshots Position to 702;\n"
        "Set Masks 15 to 799;\n"
        "Get Snapshots 0; Print @_.\n"
        "Get Snapshots 255; Print @_.\n"
        "Get Snapshots 121; Print @_.\n"
        "Get Snapshots 1; Print @_.\n"
        "Get Snapshots 254; Print @_.\n"
        "Get Masks 15; Print @_.\n"
        "Get Masks 0; Print @_.\n"
    )
    expected = "700\n701\n702\n1\n254\n799\n100\n"
    tokens = native_compiler(source, tmp_path)
    _assert_source_and_vm(source, tokens, expected)
    result = execute(x86_linux_codegen, source, tmp_path, tokens=tokens)
    assert (result.returncode, result.stdout, result.stderr) == (0, expected, "")


@requires_linux
def test_actual_generator_single_owner_capacity_boundary(tmp_path, x86_linux_codegen, native_compiler):
    accepted_source = f"Items = {_values(272)};\nGet Items -1; Print @_.\n"
    accepted_dir = tmp_path / "accepted"
    accepted_tokens = native_compiler(accepted_source, accepted_dir)
    expected_initializer = ["BC_MULTI_BEGIN"]
    for value in range(272):
        expected_initializer.extend(("BC_CONST", str(value)))
    expected_initializer.extend(("BC_STORE_MULTI", "Items"))
    assert accepted_tokens[:len(expected_initializer)] == expected_initializer
    assert accepted_tokens[-1] == "BC_PRINT"
    _assert_source_and_vm(accepted_source, accepted_tokens, "271\n")
    accepted = execute(x86_linux_codegen, accepted_source, accepted_dir, tokens=accepted_tokens)
    assert (accepted.returncode, accepted.stdout, accepted.stderr) == (0, "271\n", "")

    rejected_source = f"Items = {_values(273)};\nGet Items 272; Print @_.\n"
    rejected_dir = tmp_path / "rejected"
    rejected_tokens = native_compiler(rejected_source, rejected_dir)
    rejected = generate(x86_linux_codegen, rejected_tokens, rejected_dir)
    assert (rejected.returncode, rejected.stdout, rejected.stderr) == (1, "", "")


@requires_linux
def test_actual_generator_aggregate_capacity_boundary_split_across_owners(
    tmp_path, x86_linux_codegen, native_compiler
):
    accepted_source = (
        f"Left = {_values(136)};\nRight = {_values(136, 1000)};\n"
        "Get Right -1; Print @_.\n"
    )
    accepted_dir = tmp_path / "accepted"
    accepted_tokens = native_compiler(accepted_source, accepted_dir)
    _assert_source_and_vm(accepted_source, accepted_tokens, "1135\n")
    accepted = execute(x86_linux_codegen, accepted_source, accepted_dir, tokens=accepted_tokens)
    assert (accepted.returncode, accepted.stdout, accepted.stderr) == (0, "1135\n", "")

    rejected_source = (
        f"Left = {_values(136)};\nRight = {_values(137, 1000)};\n"
        "Get Right -1; Print @_.\n"
    )
    rejected_dir = tmp_path / "rejected"
    rejected_tokens = native_compiler(rejected_source, rejected_dir)
    rejected = generate(x86_linux_codegen, rejected_tokens, rejected_dir)
    assert (rejected.returncode, rejected.stdout, rejected.stderr) == (1, "", "")


@requires_linux
def test_actual_generator_rejects_seventeen_owners_below_cell_capacity(
    tmp_path, x86_linux_codegen, native_compiler
):
    source = "".join(f"Owner{index} = {index}, {index};\n" for index in range(17))
    source += "Get Owner16 0; Print @_.\n"
    owner_tokens = native_compiler(source, tmp_path)
    result = generate(x86_linux_codegen, owner_tokens, tmp_path)
    assert (result.returncode, result.stdout, result.stderr) == (1, "", "")


@requires_linux
def test_actual_generator_sixteen_owners_at_expanded_cell_capacity(
    tmp_path, x86_linux_codegen, native_compiler
):
    source = "".join(
        f"Owner{owner} = {_values(17, owner * 100)};\n"
        for owner in range(16)
    )
    source += (
        "Set Owner15 16 to 999;\n"
        "Get Owner0 16; Print @_.\n"
        "Get Owner15 16; Print @_.\n"
    )
    expected = "16\n999\n"
    tokens = native_compiler(source, tmp_path)
    _assert_source_and_vm(source, tokens, expected)
    result = execute(x86_linux_codegen, source, tmp_path, tokens=tokens)
    assert (result.returncode, result.stdout, result.stderr) == (0, expected, "")


@requires_linux
@pytest.mark.parametrize(
    "operation,index,expected_returncode,expected_stdout",
    [
        ("get", -272, 0, "777\n0\n888\n"),
        ("get", -273, 1, "777\n"),
        ("get", 272, 1, "777\n"),
        ("set", 271, 0, "777\n999\n888\n"),
        ("set", -1, 1, "777\n"),
        ("set", 272, 1, "777\n"),
    ],
    ids=["get-minus-length", "get-before-start", "get-length", "set-last", "set-negative", "set-length"],
)
def test_actual_generator_large_owner_runtime_bounds_stop_output(
    tmp_path, x86_linux_codegen, native_compiler,
    operation, index, expected_returncode, expected_stdout,
):
    access = (
        f"Get Items {index}; Print @_.\n"
        if operation == "get"
        else f"Set Items {index} to 999;\n"
    )
    if operation == "set" and expected_returncode == 0:
        access += f"Get Items {index}; Print @_.\n"
    source = f"Items = {_values(272)};\nPrint 777.\n" + access + "Print 888.\n"
    tokens = native_compiler(source, tmp_path)
    _assert_source_and_vm(
        source, tokens, expected_stdout, bounds_failure=expected_returncode == 1
    )
    result = execute(x86_linux_codegen, source, tmp_path, tokens=tokens)
    assert (result.returncode, result.stdout, result.stderr) == (
        expected_returncode, expected_stdout, "",
    )


@requires_linux
@pytest.mark.parametrize("operation", ["get", "set"])
def test_actual_generator_small_owner_one_past_end_does_not_enter_adjacent_large_owner(
    tmp_path, x86_linux_codegen, native_compiler, operation
):
    access = (
        "Get Small 16; Print @_.\n"
        if operation == "get"
        else "Set Small 16 to 999;\n"
    )
    source = (
        f"Small = {_values(16, 2000)};\n"
        f"Large = {_values(256, 1000)};\n"
        "Print 777.\n" + access + "Print 888.\n"
    )
    tokens = native_compiler(source, tmp_path)
    _assert_source_and_vm(source, tokens, "777\n", bounds_failure=True)
    result = execute(x86_linux_codegen, source, tmp_path, tokens=tokens)
    assert (result.returncode, result.stdout, result.stderr) == (1, "777\n", "")
