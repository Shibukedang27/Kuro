"""Tests for the Kuro-authored compiler driver composition."""
import shutil
import subprocess
from pathlib import Path

import pytest

from compiler import self_host
from compiler.pipeline import run_source
from compiler.self_host import native_compiler_source

ROOT = Path(__file__).resolve().parents[2]
DRIVER = ROOT / "self_host" / "compiler.kuro"


def compile_with_driver(source: str):
    result = run_source(native_compiler_source(source))
    assert result.ok, result.compile.diags.render_all() if not result.compile.ok else result.runtime_error
    return result.interpreter.env


def test_driver_publishes_final_bytecode_artifact():
    env = compile_with_driver('Name = "Kuro";\nPrint Name.')
    assert env["CompilerFailed"] == 0
    assert env["CompilerInstructionCount"] == len(env["CompilerOutput"])
    assert env["CompilerOutput"] == [
        "BC_CONST_TEXT", "Kuro", "BC_STORE_LIST", "Name",
        "BC_LOADVAR", "Name", "BC_PRINT",
    ]


def test_driver_propagates_stage_failure():
    env = compile_with_driver("Print 1")
    assert env["CompilerFailed"] == 1


def test_driver_compiles_its_own_kuro_source():
    env = compile_with_driver(DRIVER.read_text(encoding="utf-8"))
    assert env["CompilerFailed"] == 0
    assert env["CompilerInstructionCount"] > 0
    assert "BC_FUNC_BEGIN" in env["CompilerOutput"]


def test_native_compiler_source_is_reproducible_complete_input():
    first = native_compiler_source()
    second = native_compiler_source()

    assert first == second
    assert len(first.encode("utf-8")) > 65536
    assert "Take user Source;" in first
    assert "# --- BEGIN_STANDALONE_TOKENS" not in first
    assert "# --- BEGIN_STANDALONE_AST" not in first
    assert "# --- BEGIN_STANDALONE_IR" not in first
    assert 'Print "kuro.bytecode/1".' in first


def test_shell_native_compiler_source_matches_python_composer():
    completed = subprocess.run(
        [str(ROOT / "bootstrap" / "compose-native-compiler-source.sh")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )

    assert completed.stdout == native_compiler_source()


@pytest.mark.parametrize("entry", ["", "Call LowerBlock;\nCall LowerBlock;\n"])
def test_python_compiler_gate_rejects_missing_or_duplicate_stage_entry(entry):
    with pytest.raises(self_host.SelfHostError, match="exactly one"):
        self_host._gate_compiler_stage(entry, "LowerBlock", "LowerFailed", "Ready is equal to 1")


@pytest.mark.parametrize("drift", ["marker", "missing-entry", "duplicate-entry"])
def test_shell_compiler_composer_fails_on_source_drift(tmp_path, drift):
    shutil.copytree(ROOT / "self_host", tmp_path / "self_host")
    bootstrap = tmp_path / "bootstrap"
    bootstrap.mkdir()
    composer = bootstrap / "compose-native-compiler-source.sh"
    shutil.copy2(ROOT / "bootstrap" / composer.name, composer)
    lower_path = tmp_path / "self_host" / "lower.kuro"
    lower = lower_path.read_text(encoding="utf-8")
    if drift == "marker":
        lower = lower.replace("BEGIN_STANDALONE_AST", "MISSING_AST_MARKER")
    elif drift == "missing-entry":
        lower = lower.replace("\nCall LowerBlock;\n", "\n")
    else:
        lower += "Call LowerBlock;\n"
    lower_path.write_text(lower, encoding="utf-8")
    completed = subprocess.run(["sh", str(composer)], capture_output=True, text=True)
    assert completed.returncode != 0
