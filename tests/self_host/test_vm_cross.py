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


def run_kuro_vm_environment(source: str):
    replacement = f'Source = "{escape(source)}";'
    lexer = SOURCE_RE.sub(lambda _: replacement, LEXER.read_text(), count=1)
    parser = TOKENS_RE.sub("", PARSER.read_text(), count=1)
    lower = AST_RE.sub("", LOWER.read_text(), count=1)
    encoder = IR_RE.sub("", ENCODER.read_text(), count=1)
    vm = BYTECODE_RE.sub("", VM.read_text(), count=1)
    result = run_source("\n".join((lexer, parser, lower, encoder, vm)))
    assert result.ok, result.compile.diags.render_all() if not result.compile.ok else result.runtime_error
    return result.interpreter.env


def run_kuro_vm(source: str):
    env = run_kuro_vm_environment(source)
    return env.get("VMOutput"), env.get("VMFailed")


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


def test_kuro_vm_passes_mixed_text_and_integer_action_parameters():
    output, failed = run_kuro_vm(
        "Action EchoPair Count: Integers, Word: Text;\n"
        "Print Word.\nReturn Count;\nDone.\n"
        'Call EchoPair 7, "hello";\nPrint @_.\n'
    )

    assert failed in (None, 0)
    assert output == ["hello", 7]


def test_kuro_vm_passes_and_forwards_decimal_action_parameters():
    output, failed = run_kuro_vm(
        "Action Sink Value: Decimals;\nReturn Value;\nDone.\n"
        "Action Forward Value: Decimals;\nCall Sink Value;\nReturn @_;\nDone.\n"
        "Call Forward 3.25;\nPrint @_."
    )

    assert failed in (None, 0)
    assert output == [3.25]


def test_kuro_vm_returns_typed_decimal_action_values():
    output, failed = run_kuro_vm(
        "Action Echo Value: Decimals;\nReturn Value;\nDone.\n"
        "Call Echo 3.25;\nPrint @_."
    )

    assert failed in (None, 0)
    assert output == [3.25]


def test_kuro_vm_matches_host_for_decimal_action_arithmetic_and_comparisons():
    source = (
        "Action Calculate Left: Decimals, Right: Integers;\n"
        "Return (Left + Right) - (Left * Right) / Right;\nDone.\n"
        "Call Calculate 1.5, 2;\n"
        "If @_ is equal to 2.0;\nPrint 1.\nElse;\nPrint 0.\nDone.\n"
        "Compare Lower 1.5 is less than 2.5;\n"
        "If Lower is equal to 1;\nPrint 1.\nElse;\nPrint 0.\nDone.\n"
        "Compare Different 2.5 is not equal to 3.5;\n"
        "If Different is equal to 1;\nPrint 1.\nElse;\nPrint 0.\nDone."
    )
    host = run_source(source)
    assert host.ok, host.compile.diags.render_all() if not host.compile.ok else host.runtime_error
    env = run_kuro_vm_environment(source)

    assert env["VMFailed"] in (None, 0)
    assert env["VMOutput"] == [1, 1, 1]
    assert host.stdout == "1\n1\n1\n"


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


def test_kuro_vm_executes_control_flow_inside_actions():
    source = (
        "Action First;\n"
        "N = 0;\n"
        "If 1 is equal to 1;\nAdd 1 to N;\nDone.\n"
        "Repeat 1;\nAdd 1 to N;\nDone.\n"
        "While N is less than 3;\nAdd 1 to N;\nDone.\n"
        "Return N;\nDone.\n"
        "Action Second;\n"
        "M = 0;\n"
        "If 1 is equal to 1;\nAdd 1 to M;\nDone.\n"
        "Repeat 1;\nAdd 1 to M;\nDone.\n"
        "While M is less than 3;\nAdd 1 to M;\nDone.\n"
        "Return M;\nDone.\n"
        "Action RaiseToThree Value: Integers;\n"
        "While Value is less than 3;\nAdd 1 to Value;\nDone.\n"
        "Return Value;\nDone.\n"
        "T = 0;\nWhile T is less than 1;\nAdd 1 to T;\nDone.\n"
        "Call First;\nPrint @_.\n"
        "Call Second;\nPrint @_.\n"
        "Call RaiseToThree 0;\nPrint @_.\n"
        "Print T.\n"
    )
    output, failed = run_kuro_vm(source)

    assert failed in (None, 0)
    assert output == [3, 3, 3, 1]


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


def test_kuro_vm_preserves_multi_value_assignment_order_and_length():
    output, failed = run_kuro_vm(
        'Items = "a", "b", "c";\n'
        "Print Items.\nLength Items;\nPrint @_.\nGet Items 1;\nPrint @_."
    )
    assert failed in (None, 0)
    assert output == ["a", "b", "c", 3, "b"]


def test_kuro_vm_replaces_multi_value_collections_on_reassignment():
    output, failed = run_kuro_vm(
        'Items = "a", "b";\n'
        'Items = "c", "d", "e";\n'
        "Print Items.\nLength Items;\nPrint @_ .\n"
        'Items = "z";\nLength Items;\nPrint @_ .\nPrint Items.'
    )
    assert failed in (None, 0)
    assert output == ["c", "d", "e", 3, 1, "z"]


def test_kuro_vm_decodes_multi_digit_and_decimal_constants():
    output, failed = run_kuro_vm("Print 42.")
    assert failed in (None, 0)
    assert output == [42]

    output, failed = run_kuro_vm("Print 3.25.")
    assert failed in (None, 0)
    assert output == [3.25]
    env = run_kuro_vm_environment("Print 3.25.")
    assert env["VMOutput"] == [3.25]
    assert env["VMOutputDisplay"] == ["3.25"]

    env = run_kuro_vm_environment("Amount = 3.25; Print Amount.")
    assert env["VMFailed"] in (None, 0)
    assert env["VMOutput"] == [3.25]
    assert env["VMOutputDisplay"] == ["3.25"]

    env = run_kuro_vm_environment("Action Echo Value; Print Value. Done. Call Echo 3.25;")
    assert env["VMFailed"] in (None, 0)
    assert env["VMOutput"] == [3.25]
    assert env["VMOutputDisplay"] == ["3.25"]

    env = run_kuro_vm_environment("Action Echo Value; Return Value; Done. Call Echo 3.25; Print @_.")
    assert env["VMFailed"] in (None, 0)
    assert env["VMOutput"] == [3.25]
    assert env["VMOutputDisplay"] == ["3.25"]

    output, failed = run_kuro_vm("Print 12 + 30.")
    assert failed in (None, 0)
    assert output == [42]


def test_kuro_vm_preserves_decimal_display_in_collection_items():
    cases = [
        ("Amounts = 3.25, 4.5; Print Amounts.", [3.25, 4.5], ["3.25", "4.5"]),
        ("Amounts = 1.0, 2.0; Get Amounts 0; Print @_.", [1.0], ["1.0"]),
        ("Amounts = 1.0, 2.0; Set Amounts 1 to 3.25; Print Amounts.", [1.0, 3.25], ["1.0", "3.25"]),
        ("Amounts = 3.25, 4.5; Copy = Amounts; Print Copy.", [3.25, 4.5], ["3.25", "4.5"]),
        ("Amounts = 1.0, 2.0; Append 3.25 to Amounts; Print Amounts.", [1.0, 2.0, 3.25], ["1.0", "2.0", "3.25"]),
    ]
    for source, values, displays in cases:
        env = run_kuro_vm_environment(source)
        assert env["VMFailed"] in (None, 0), source
        assert env["VMOutput"] == values, source
        assert env["VMOutputDisplay"] == displays, source


def test_kuro_vm_clears_stale_decimal_display_after_integer_overwrite():
    env = run_kuro_vm_environment("Amount = 3.25; Amount = 4; Print Amount.")
    assert env["VMOutput"] == [4]
    assert env["VMOutputDisplay"] == [""]

    env = run_kuro_vm_environment("Amounts = 1.25, 2.5; Set Amounts 0 to 7; Print Amounts.")
    assert env["VMOutput"] == [7, 2.5]
    assert env["VMOutputDisplay"] == ["", "2.5"]


def test_kuro_vm_matches_host_for_named_decimal_storage_and_mutation():
    source = (
        "Balance = 1.25;\nCopy = Balance;\n"
        "Add 2 to Balance;\nAdd 0.5 to Balance;\n"
        "Print Balance.\nPrint Copy.\n"
        "Update Balance to Copy * 2;\nPrint Balance.\n"
        "Balance = Balance + 0.5;\nPrint Balance.\n"
    )
    hosted = run_source(source)
    assert hosted.ok
    output, failed = run_kuro_vm(source)
    assert failed in (None, 0)
    assert output == [3.75, 1.25, 2.5, 3.0]
    assert hosted.stdout == "".join(f"{value}\n" for value in output)


def test_kuro_vm_matches_host_for_decimal_control_flow_globals():
    from test_native_decimal_control_flow import (
        DECIMAL_CONTROL_FLOW_OUTPUT,
        DECIMAL_CONTROL_FLOW_PROGRAM,
    )

    hosted = run_source(DECIMAL_CONTROL_FLOW_PROGRAM)
    assert hosted.ok, hosted.compile.diags.render_all() if not hosted.compile.ok else hosted.runtime_error
    env = run_kuro_vm_environment(DECIMAL_CONTROL_FLOW_PROGRAM)

    assert env["VMFailed"] in (None, 0)
    assert env["VMOutput"] == [2.0, 3.0, 3.5, 5.0, 2.0, 1.75, 2, -0.0]
    assert hosted.stdout == DECIMAL_CONTROL_FLOW_OUTPUT
    assert hosted.stdout == "".join(f"{value}\n" for value in env["VMOutput"])
