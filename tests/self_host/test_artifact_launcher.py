import platform
import re
import subprocess
import pytest
from pathlib import Path

from compiler.pipeline import run_source


ROOT = Path(__file__).resolve().parents[2]
LOADER = ROOT / "self_host" / "artifact_loader.kuro"
VM = ROOT / "self_host" / "vm.kuro"
RUNTIME = ROOT / "self_host" / "runtime.kuro"
BYTECODE_RE = re.compile(
    r"^# --- BEGIN_STANDALONE_BYTECODE.*?^# --- END_STANDALONE_BYTECODE.*?$\n?",
    re.MULTILINE | re.DOTALL,
)
VM_INPUT_DEFAULT_RE = re.compile(
    r"^# --- BEGIN_VM_INPUT_DEFAULT.*?^# --- END_VM_INPUT_DEFAULT.*?$\n?",
    re.MULTILINE | re.DOTALL,
)


def run_artifact(payload: str):
    vm = BYTECODE_RE.sub("", VM.read_text(encoding="utf-8"), count=1)
    vm = VM_INPUT_DEFAULT_RE.sub("", vm, count=1)
    source = "\n".join(
        (LOADER.read_text(encoding="utf-8"), vm, RUNTIME.read_text(encoding="utf-8"))
    )
    result = run_source(source, input_fn=lambda _prompt: payload)
    assert result.compile.ok, result.compile.diags.render_all()
    assert result.runtime_error is None, result.runtime_error
    return result.interpreter.env, result.stdout


def test_kuro_artifact_launcher_executes_framed_bytecode():
    env, output = run_artifact("kuro.bytecode/1\nBC_CONST\n5\nBC_PRINT\n")

    assert env["ArtifactFailed"] == 0
    assert env["RuntimeExitCode"] == 0
    assert output == "5\n"


def test_kuro_artifact_launcher_accepts_balanced_control_flow():
    env, output = run_artifact(
        "kuro.bytecode/1\n"
        "BC_CONST\n1\nBC_IF_BEGIN\n"
        "BC_CONST\nyes\nBC_PRINT\n"
        "BC_ELSE_BEGIN\nBC_CONST\nno\nBC_PRINT\nBC_IF_END\n"
    )

    assert env["ArtifactFailed"] == 0
    assert env["RuntimeExitCode"] == 0
    assert output == "yes\n"


def test_kuro_artifact_launcher_executes_multi_value_assignment():
    env, output = run_artifact(
        "kuro.bytecode/1\n"
        "BC_MULTI_BEGIN\n"
        "BC_CONST\na\nBC_CONST\nb\nBC_CONST\nc\n"
        "BC_STORE_MULTI\nItems\n"
        "BC_LOADVAR\nItems\nBC_PRINT\n"
        "BC_LENGTH\nItems\nBC_PRINT\n"
    )

    assert env["ArtifactFailed"] == 0
    assert env["RuntimeExitCode"] == 0
    assert output == "a\nb\nc\n3\n"


@pytest.mark.skipif(platform.system() not in {"Darwin", "Linux"}, reason="requires a supported native backend")
def test_native_artifact_launcher_executes_multi_value_reassignment(tmp_path):
    from compiler.self_host import build_native_artifact_launcher

    executable = tmp_path / "kuro-bytecode"
    build_native_artifact_launcher(executable)
    payload = (
        "kuro.bytecode/1\n"
        "BC_MULTI_BEGIN\nBC_CONST\nold1\nBC_CONST\nold2\nBC_STORE_MULTI\nItems\n"
        "BC_MULTI_BEGIN\nBC_CONST\na\nBC_CONST\nb\nBC_CONST\nc\nBC_STORE_MULTI\nItems\n"
        "BC_LOADVAR\nItems\nBC_PRINT\nBC_LENGTH\nItems\nBC_PRINT\n"
    )
    result = subprocess.run(
        [str(executable)], input=payload, capture_output=True, text=True, timeout=20
    )

    assert result.returncode == 0, result.stderr
    assert result.stdout == "a\nb\nc\n3\n"


def test_kuro_artifact_launcher_executes_private_suffix_opcode():
    env, output = run_artifact(
        "kuro.bytecode/1\n"
        "BC_CONST\nKuro-native\nBC_CONST\n5\n"
        "BC_ARTIFACT_SUFFIX\nBC_PRINT\n"
    )

    assert env["ArtifactFailed"] == 0
    assert env["RuntimeExitCode"] == 0
    assert output == "native\n"


def test_kuro_artifact_launcher_preserves_numeric_looking_text_constants():
    env, output = run_artifact(
        "kuro.bytecode/1\n"
        "BC_CONST_TEXT\n1\nBC_STORE_LIST\nTextValue\n"
        "BC_LENGTH\nTextValue\nBC_PRINT\n"
    )

    assert env["ArtifactFailed"] == 0
    assert env["RuntimeExitCode"] == 0
    assert output == "1\n"


def test_kuro_artifact_launcher_preserves_large_framed_input_exactly():
    payload = "Q" * 70000 + "tail-END"
    env, output = run_artifact(
        "kuro.bytecode/1\n"
        "BC_INPUT\nFirst\nBC_LENGTH\nFirst\nBC_PRINT\n"
        "BC_LOADVAR\nFirst\nBC_CONST\n70000\nBC_ARTIFACT_SUFFIX\nBC_PRINT\n"
        "BC_INPUT\nLater\nBC_LOADVAR\nLater\nBC_PRINT\n"
        "kuro.input/1\n" + payload
    )

    assert env["ArtifactFailed"] == 0
    assert env["RuntimeExitCode"] == 0
    assert env["VMInput"] == payload
    assert output == f"{len(payload)}\ntail-END\n\n"


@pytest.mark.skipif(platform.system() not in {"Darwin", "Linux"}, reason="requires a supported native backend")
def test_native_artifact_launcher_preserves_large_input_and_runs_suffix_opcode(tmp_path):
    from compiler.self_host import build_native_artifact_launcher

    executable = tmp_path / "kuro-bytecode"
    build_native_artifact_launcher(executable)

    small = subprocess.run(
        [str(executable)],
        input=(
            "kuro.bytecode/1\nBC_CONST\nKuro-native\nBC_CONST\n5\n"
            "BC_ARTIFACT_SUFFIX\nBC_PRINT\n"
        ),
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert small.returncode == 0, small.stderr
    assert small.stdout == "native\n"

    typed_text = subprocess.run(
        [str(executable)],
        input=(
            "kuro.bytecode/1\nBC_CONST_TEXT\n1\nBC_STORE_LIST\nTextValue\n"
            "BC_LENGTH\nTextValue\nBC_PRINT\n"
        ),
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert typed_text.returncode == 0, typed_text.stderr
    assert typed_text.stdout == "1\n"

    payload = "Q" * 70000 + "tail-END"
    loader_only_input = (
        "kuro.bytecode/1\n"
        "BC_INPUT\nFirst\nBC_LENGTH\nFirst\nBC_PRINT\n"
        "kuro.input/1\n" + payload
    )
    loader_only = subprocess.run(
        [str(executable)], input=loader_only_input, capture_output=True,
        text=True, timeout=60,
    )
    assert loader_only.returncode == 0, f"large loader extraction: {loader_only.stderr}"
    assert loader_only.stdout == f"{len(payload)}\n"

    framed = (
        "kuro.bytecode/1\n"
        "BC_INPUT\nFirst\nBC_LENGTH\nFirst\nBC_PRINT\n"
        "BC_LOADVAR\nFirst\nBC_CONST\n70000\nBC_ARTIFACT_SUFFIX\nBC_PRINT\n"
        "BC_INPUT\nLater\nBC_LOADVAR\nLater\nBC_PRINT\n"
        "kuro.input/1\n" + payload
    )
    large = subprocess.run(
        [str(executable)], input=framed, capture_output=True, text=True, timeout=60
    )
    assert large.returncode == 0, large.stderr
    assert large.stdout == f"{len(payload)}\ntail-END\n\n"


def test_kuro_artifact_launcher_rejects_wrong_magic():
    env, output = run_artifact("not-kuro\nBC_CONST\n5\nBC_PRINT\n")

    assert env["ArtifactFailed"] == 1
    assert env["RuntimeExitCode"] == 1
    assert output == ""


def test_kuro_artifact_launcher_rejects_empty_tokens():
    env, output = run_artifact("kuro.bytecode/1\nBC_CONST\n\nBC_PRINT\n")

    assert env["ArtifactFailed"] == 1
    assert env["RuntimeExitCode"] == 1
    assert output == ""


@pytest.mark.parametrize(
    ("encoded", "expected"),
    [
        (r"\e", "\n"),
        (r"line\nnext", "line\nnext\n"),
        (r"tab\tvalue", "tab\tvalue\n"),
        (r"left\\right", "left\\right\n"),
        (r"\i", "kuro.input/1\n"),
    ],
)
def test_kuro_artifact_launcher_decodes_escaped_values(encoded, expected):
    env, output = run_artifact(
        "kuro.bytecode/1\nBC_CONST\n" + encoded + "\nBC_PRINT\n"
    )

    assert env["ArtifactFailed"] == 0
    assert env["RuntimeExitCode"] == 0
    assert output == expected


def test_native_compiler_entry_encodes_marker_literal_as_standalone_escape():
    entry = (ROOT / "self_host" / "native_compiler_entry.kuro").read_text(encoding="utf-8")
    source = (
        'CompilerFailed = 0;\n'
        'BytecodeOut = "BC_CONST_TEXT", "kuro.input/1";\n'
        + entry
    )
    result = run_source(source)

    assert result.ok, result.compile.diags.render_all() if not result.compile.ok else result.runtime_error
    assert result.stdout == "kuro.bytecode/1\nBC_CONST_TEXT\n\\i\n"


def test_kuro_artifact_launcher_rejects_unknown_escape():
    env, output = run_artifact("kuro.bytecode/1\nBC_CONST\n\\q\nBC_PRINT\n")

    assert env["ArtifactFailed"] == 1
    assert env["RuntimeExitCode"] == 1
    assert output == ""


def test_kuro_artifact_launcher_passes_framed_input_to_vm():
    env, output = run_artifact(
        "kuro.bytecode/1\n"
        "BC_INPUT\nSource\nBC_LOADVAR\nSource\nBC_PRINT\n"
        "kuro.input/1\nPrint 42.\n"
    )

    assert env["ArtifactFailed"] == 0
    assert env["RuntimeExitCode"] == 0
    assert env["VMInput"] == "Print 42.\n"
    assert output == "Print 42.\n\n"


def test_kuro_artifact_launcher_executes_type_declarations():
    env, output = run_artifact(
        "kuro.bytecode/1\nBC_DECLTYPE\nSource\nText\n"
        "BC_CONST\nok\nBC_PRINT\n"
    )

    assert env["RuntimeExitCode"] == 0
    assert output == "ok\n"


def test_kuro_artifact_launcher_gives_later_inputs_empty_text():
    env, output = run_artifact(
        "kuro.bytecode/1\n"
        "BC_INPUT\nFirst\nBC_INPUT\nSecond\n"
        "BC_LOADVAR\nFirst\nBC_PRINT\nBC_LOADVAR\nSecond\nBC_PRINT\n"
        "kuro.input/1\nvalue"
    )

    assert env["RuntimeExitCode"] == 0
    assert output == "value\n\n"


@pytest.mark.parametrize("body", ["BC_CONST\n", "BC_GET\nName\n", "BC_UNKNOWN\n"])
def test_loader_rejects_invalid_instructions_before_execution(body):
    env, output = run_artifact("kuro.bytecode/1\n" + body)
    assert env["ArtifactFailed"] == 1
    assert env["RuntimeExitCode"] == 1
    assert output == ""


def test_loader_rejects_truncated_typed_text_constant():
    env, output = run_artifact("kuro.bytecode/1\nBC_CONST_TEXT\n")
    assert env["ArtifactFailed"] == 1
    assert env["RuntimeExitCode"] == 1
    assert output == ""


def test_loader_accepts_more_than_256_instructions_before_vm_execution():
    env, output = run_artifact("kuro.bytecode/1\n" + "BC_PRINT\n" * 257)

    assert env["ArtifactFailed"] == 0
    assert env["RuntimeExitCode"] == 1
    assert output == ""


@pytest.mark.parametrize(
    "body",
    [
        "BC_IF_END\n",
        "BC_IF_BEGIN\n",
        "BC_ELSE_BEGIN\n",
        "BC_REPEAT_END\n",
        "BC_WHILE_TEST\n",
        "BC_WHILE_BEGIN\n",
        "BC_FUNC_END\n",
        "BC_PARAM\nName\nText\n",
        "BC_RETURN\n",
        "BC_CALL_END\n",
        "BC_CALL_BEGIN\nMissingEnd\n",
    ],
)
def test_loader_rejects_unbalanced_structures(body):
    env, output = run_artifact("kuro.bytecode/1\n" + body)
    assert env["ArtifactFailed"] == 1
    assert env["RuntimeExitCode"] == 1
    assert output == ""


@pytest.mark.parametrize(
    "body",
    [
        "BC_PRINT\n",
        "BC_CALL_BEGIN\nMissing\nBC_CALL_END\n",
        "BC_MULTI_BEGIN\nBC_CONST\na\nBC_STORE_MULTI\nItems\n",
    ],
)
def test_vm_preserves_runtime_failures(body):
    env, output = run_artifact("kuro.bytecode/1\n" + body)
    assert env["ArtifactFailed"] == 0
    assert env["RuntimeExitCode"] == 1
    assert output == ""


def test_native_artifact_launcher_returns_runtime_status(tmp_path):
    from compiler.self_host import build_native_artifact_launcher

    executable = tmp_path / "kuro-bytecode"
    build_native_artifact_launcher(executable)

    valid = subprocess.run(
        [str(executable)], input="kuro.bytecode/1\nBC_CONST\n5\nBC_PRINT\n",
        capture_output=True, text=True, check=False,
    )
    invalid = subprocess.run(
        [str(executable)], input="wrong\nBC_PRINT\n",
        capture_output=True, text=True, check=False,
    )

    assert valid.returncode == 0
    assert valid.stdout == "5\n"
    assert invalid.returncode == 1
    assert invalid.stdout == ""

    with_input = subprocess.run(
        [str(executable)],
        input=(
            "kuro.bytecode/1\nBC_INPUT\nSource\nBC_LOADVAR\nSource\nBC_PRINT\n"
            "kuro.input/1\nnative input"
        ),
        capture_output=True,
        text=True,
        check=False,
    )
    assert with_input.returncode == 0
    assert with_input.stdout == "native input\n"
    for body in (
        "BC_CONST\n",
        "BC_GET\nName\n",
        "BC_UNKNOWN\n",
        "BC_IF_END\n",
        "BC_CALL_BEGIN\nMissingEnd\n",
        "BC_PRINT\n",
        "BC_CALL_BEGIN\nMissing\nBC_CALL_END\n",
        "BC_PRINT\n" * 257,
    ):
        rejected = subprocess.run(
            [str(executable)], input="kuro.bytecode/1\n" + body,
            capture_output=True, text=True, timeout=5,
        )
        assert rejected.returncode == 1
        assert rejected.stdout == ""


@pytest.mark.skipif(platform.system() not in {"Darwin", "Linux"}, reason="requires a supported native backend")
def test_native_artifact_launcher_decodes_escaped_values(tmp_path):
    from compiler.self_host import build_native_artifact_launcher

    executable = tmp_path / "kuro-bytecode"
    build_native_artifact_launcher(executable)
    result = subprocess.run(
        [str(executable)],
        input="kuro.bytecode/1\nBC_CONST\nline\\nnext\nBC_PRINT\n",
        capture_output=True,
        text=True,
        timeout=20,
    )

    assert result.returncode == 0, result.stderr
    assert result.stdout == "line\nnext\n"
