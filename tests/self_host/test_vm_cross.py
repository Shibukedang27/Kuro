"""Tests for executing Kuro bytecode with a Kuro-authored VM."""
import re
from pathlib import Path

from compiler.pipeline import run_source

ROOT = Path(__file__).resolve().parents[2]
LEXER = ROOT / "self_host" / "lexer.kuro"
PARSER = ROOT / "self_host" / "parser.kuro"
LOWER = ROOT / "self_host" / "lower.kuro"
ENCODER = ROOT / "self_host" / "bytecode.kuro"
VM = ROOT / "self_host" / "vm.kuro"
SOURCE_RE = re.compile(r'^Source = ".*";$', re.MULTILINE)
TOKENS_RE = re.compile(r"^# --- BEGIN_STANDALONE_TOKENS.*?^# --- END_STANDALONE_TOKENS.*?$\n?", re.MULTILINE | re.DOTALL)
AST_RE = re.compile(r"^# --- BEGIN_STANDALONE_AST.*?^# --- END_STANDALONE_AST.*?$\n?", re.MULTILINE | re.DOTALL)
IR_RE = re.compile(r"^# --- BEGIN_STANDALONE_IR.*?^# --- END_STANDALONE_IR.*?$\n?", re.MULTILINE | re.DOTALL)
BYTECODE_RE = re.compile(r"^# --- BEGIN_STANDALONE_BYTECODE.*?^# --- END_STANDALONE_BYTECODE.*?$\n?", re.MULTILINE | re.DOTALL)


def escape(source: str) -> str:
    return source.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


def run_kuro_vm(source: str):
    replacement = f'Source = "{escape(source)}";'
    lexer = SOURCE_RE.sub(lambda _: replacement, LEXER.read_text(), count=1)
    parser = TOKENS_RE.sub("", PARSER.read_text(), count=1)
    lower = AST_RE.sub("", LOWER.read_text(), count=1)
    encoder = IR_RE.sub("", ENCODER.read_text(), count=1)
    vm = BYTECODE_RE.sub("", VM.read_text(), count=1)
    result = run_source("\n".join((lexer, parser, lower, encoder, vm)))
    assert result.ok, result.compile.diags.render_all() if not result.compile.ok else result.runtime_error
    return result.interpreter.env.get("VMOutput"), result.interpreter.env.get("VMFailed")


def test_kuro_vm_executes_constants_and_variables():
    output, failed = run_kuro_vm('Name = "Kuro";\nPrint Name.')
    assert failed in (None, 0)
    assert output == ["Kuro"]


def test_kuro_vm_executes_arithmetic_and_updates():
    output, failed = run_kuro_vm("N = 1;\nUpdate N to N + 2;\nPrint N.")
    assert failed in (None, 0)
    assert output == [3]


def test_kuro_vm_keeps_non_numeric_constants_as_text():
    output, failed = run_kuro_vm('Print "Kuro".')
    assert failed in (None, 0)
    assert output == ["Kuro"]


def test_kuro_vm_executes_comparisons():
    output, failed = run_kuro_vm("Compare Answer 4 is less than 9;\nPrint Answer.")
    assert failed in (None, 0)
    assert output == [1]


def test_kuro_vm_executes_boolean_combinations():
    output, failed = run_kuro_vm(
        "Compare Answer 4 is less than 9 and 2 is equal to 2;\nPrint Answer."
    )
    assert failed in (None, 0)
    assert output == [1]


def test_kuro_vm_executes_true_and_false_if_branches():
    output, failed = run_kuro_vm(
        'If 1 is equal to 1;\nPrint "yes".\nElse;\nPrint "no".\nDone.'
    )
    assert failed in (None, 0)
    assert output == ["yes"]

    output, failed = run_kuro_vm(
        'If 1 is equal to 2;\nPrint "yes".\nElse;\nPrint "no".\nDone.'
    )
    assert failed in (None, 0)
    assert output == ["no"]


def test_kuro_vm_executes_repeat_blocks():
    output, failed = run_kuro_vm('Repeat 3;\nPrint "x".\nDone.')
    assert failed in (None, 0)
    assert output == ["x", "x", "x"]

    output, failed = run_kuro_vm('Repeat 2;\nPrint "x".\nDone.\nPrint "after".')
    assert failed in (None, 0)
    assert output == ["x", "x", "after"]


def test_kuro_vm_executes_action_call_and_return():
    output, failed = run_kuro_vm(
        "Action Add A, B;\nReturn A + B;\nDone.\n"
        "Call Add 3, 4;\nPrint @_."
    )
    assert failed in (None, 0)
    assert output == [7]

    output, failed = run_kuro_vm(
        "Action Remember Value;\nSaved = Value;\nDone.\n"
        "Call Remember 9;\nPrint Saved."
    )
    assert failed in (None, 0)
    assert output == [9]


def test_kuro_vm_keeps_recursive_call_frames_isolated():
    output, failed = run_kuro_vm(
        "Action Fact N;\n"
        "If N is less than or equal to 1;\nReturn 1;\nElse;\n"
        "Call Fact N - 1;\nReturn N * @_;\nDone.\nDone.\n"
        "Call Fact 5;\nPrint @_."
    )
    assert failed in (None, 0)
    assert output == [120]

    output, failed = run_kuro_vm(
        "Action Sum N;\n"
        "If N is less than or equal to 0;\nReturn 0;\nElse;\n"
        "Call Sum N - 1;\nPrevious = @_;\nReturn N + Previous;\nDone.\nDone.\n"
        "Call Sum 4;\nPrint @_."
    )
    assert failed in (None, 0)
    assert output == [10]


def test_kuro_vm_re_evaluates_while_conditions():
    output, failed = run_kuro_vm(
        "N = 0;\nWhile N is less than 3;\nPrint N.\nAdd 1 to N;\nDone."
    )
    assert failed in (None, 0)
    assert output == [0, 1, 2]


def test_kuro_vm_supports_indexing_and_length():
    output, failed = run_kuro_vm('Name = "Kuro";\nGet Name 1;\nPrint @_.')
    assert failed in (None, 0)
    assert output == ["u"]

    output, failed = run_kuro_vm('Name = "Kuro";\nLength Name;\nPrint @_.')
    assert failed in (None, 0)
    assert output == [4]


def test_kuro_vm_supports_append_mutation():
    output, failed = run_kuro_vm('Name = "Ku";\nAppend "ro" to Name;\nPrint Name.')
    assert failed in (None, 0)
    assert output == ["Kuro"]

    output, failed = run_kuro_vm(
        'Items is Text;\nAppend "a" to Items;\nAppend "b" to Items;\n'
        'Get Items 1;\nPrint @_.\nLength Items;\nPrint @_. '
    )
    assert failed in (None, 0)
    assert output == ["b", 2]

    output, failed = run_kuro_vm(
        'Items is Text;\nAppend "a" to Items;\nAppend "b" to Items;\n'
        'Copy = Items;\nGet Copy 0;\nPrint @_.\nPrint Copy.'
    )
    assert failed in (None, 0)
    assert output == ["a", "a", "b"]


def test_kuro_vm_decodes_multi_digit_and_decimal_constants():
    output, failed = run_kuro_vm("Print 42.")
    assert failed in (None, 0)
    assert output == [42]

    output, failed = run_kuro_vm("Print 3.25.")
    assert failed in (None, 0)
    assert output == [3.25]

    output, failed = run_kuro_vm("Print 12 + 30.")
    assert failed in (None, 0)
    assert output == [42]
