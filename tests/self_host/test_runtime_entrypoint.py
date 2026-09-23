import re
from pathlib import Path

from compiler.pipeline import run_source

ROOT = Path(__file__).resolve().parents[2]
LEXER = ROOT / "self_host" / "lexer.kuro"
PARSER = ROOT / "self_host" / "parser.kuro"
LOWER = ROOT / "self_host" / "lower.kuro"
ENCODER = ROOT / "self_host" / "bytecode.kuro"
VM = ROOT / "self_host" / "vm.kuro"
RUNTIME = ROOT / "self_host" / "runtime.kuro"
SOURCE_RE = re.compile(r'^Source = ".*";$', re.MULTILINE)
TOKENS_RE = re.compile(r"^# --- BEGIN_STANDALONE_TOKENS.*?^# --- END_STANDALONE_TOKENS.*?$\n?", re.MULTILINE | re.DOTALL)
AST_RE = re.compile(r"^# --- BEGIN_STANDALONE_AST.*?^# --- END_STANDALONE_AST.*?$\n?", re.MULTILINE | re.DOTALL)
IR_RE = re.compile(r"^# --- BEGIN_STANDALONE_IR.*?^# --- END_STANDALONE_IR.*?$\n?", re.MULTILINE | re.DOTALL)
BYTECODE_RE = re.compile(r"^# --- BEGIN_STANDALONE_BYTECODE.*?^# --- END_STANDALONE_BYTECODE.*?$\n?", re.MULTILINE | re.DOTALL)


def run_runtime(source: str):
    escaped = source.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
    lexer = SOURCE_RE.sub(lambda _: f'Source = "{escaped}";', LEXER.read_text(), count=1)
    parser = TOKENS_RE.sub("", PARSER.read_text(), count=1)
    lower = AST_RE.sub("", LOWER.read_text(), count=1)
    encoder = IR_RE.sub("", ENCODER.read_text(), count=1)
    vm = BYTECODE_RE.sub("", VM.read_text(), count=1)
    return run_source("\n".join((lexer, parser, lower, encoder, vm, RUNTIME.read_text())))


def test_kuro_runtime_entrypoint_reports_success_and_output():
    result = run_runtime('Print "runtime".')
    assert result.ok
    assert result.interpreter.env["RuntimeExitCode"] == 0
    assert result.interpreter.env["RuntimeFailed"] == 0
    assert result.interpreter.env["RuntimeOutput"] == ["runtime"]
