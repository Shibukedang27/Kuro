"""Tests for the Kuro-authored compiler driver composition."""
import re
from pathlib import Path

from compiler.pipeline import run_source
from compiler.self_host import native_compiler_source

ROOT = Path(__file__).resolve().parents[2]
LEXER = ROOT / "self_host" / "lexer.kuro"
PARSER = ROOT / "self_host" / "parser.kuro"
LOWER = ROOT / "self_host" / "lower.kuro"
ENCODER = ROOT / "self_host" / "bytecode.kuro"
DRIVER = ROOT / "self_host" / "compiler.kuro"
SOURCE_RE = re.compile(r'^Source = ".*";$', re.MULTILINE)
TOKENS_RE = re.compile(r"^# --- BEGIN_STANDALONE_TOKENS.*?^# --- END_STANDALONE_TOKENS.*?$\n?", re.MULTILINE | re.DOTALL)
AST_RE = re.compile(r"^# --- BEGIN_STANDALONE_AST.*?^# --- END_STANDALONE_AST.*?$\n?", re.MULTILINE | re.DOTALL)
IR_RE = re.compile(r"^# --- BEGIN_STANDALONE_IR.*?^# --- END_STANDALONE_IR.*?$\n?", re.MULTILINE | re.DOTALL)


def escape(source: str) -> str:
    return source.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


def compile_with_driver(source: str):
    replacement = f'Source = "{escape(source)}";'
    lexer = SOURCE_RE.sub(lambda _: replacement, LEXER.read_text(), count=1)
    parser = TOKENS_RE.sub("", PARSER.read_text(), count=1)
    lower = AST_RE.sub("", LOWER.read_text(), count=1)
    encoder = IR_RE.sub("", ENCODER.read_text(), count=1)
    result = run_source("\n".join((lexer, parser, lower, encoder, DRIVER.read_text())))
    assert result.ok, result.compile.diags.render_all() if not result.compile.ok else result.runtime_error
    return result.interpreter.env


def test_driver_publishes_final_bytecode_artifact():
    env = compile_with_driver('Name = "Kuro";\nPrint Name.')
    assert env["CompilerFailed"] == 0
    assert env["CompilerInstructionCount"] == len(env["CompilerOutput"])
    assert env["CompilerOutput"] == [
        "BC_CONST", "Kuro", "BC_STORE_LIST", "Name",
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
