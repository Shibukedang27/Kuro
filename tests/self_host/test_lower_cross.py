"""Initial differential test for Kuro-authored lowering.

The self-hosted parser builds AstOut, then self_host/lower.kuro consumes that
same stream and emits IROut. The Python compiler remains only the harness for
executing the Kuro source during this bootstrap phase.
"""
import re
from pathlib import Path

import pytest

from compiler.ast_canon import canon_program
from compiler.lexer import tokenize
from compiler.parser import parse
from compiler.pipeline import run_source

ROOT = Path(__file__).resolve().parents[2]
LEXER = ROOT / "self_host" / "lexer.kuro"
PARSER = ROOT / "self_host" / "parser.kuro"
LOWER = ROOT / "self_host" / "lower.kuro"
SOURCE_RE = re.compile(r'^Source = ".*";$', re.MULTILINE)
STANDALONE_TOKENS_RE = re.compile(
    r"^# --- BEGIN_STANDALONE_TOKENS.*?^# --- END_STANDALONE_TOKENS.*?$\n?",
    re.MULTILINE | re.DOTALL,
)
STANDALONE_AST_RE = re.compile(
    r"^# --- BEGIN_STANDALONE_AST.*?^# --- END_STANDALONE_AST.*?$\n?",
    re.MULTILINE | re.DOTALL,
)


def escape(source: str) -> str:
    return (
        source.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
        .replace("\t", "\\t")
        .replace("\r", "\\r")
    )


def lower_source(source: str):
    replacement = f'Source = "{escape(source)}";'
    lexer = SOURCE_RE.sub(lambda _match: replacement, LEXER.read_text(), count=1)
    parser = STANDALONE_TOKENS_RE.sub("", PARSER.read_text(), count=1)
    lower = STANDALONE_AST_RE.sub("", LOWER.read_text(), count=1)
    result = run_source(lexer + "\n" + parser + "\n" + lower)
    assert result.ok, result.compile.diags.render_all() if not result.compile.ok else result.runtime_error
    return result.interpreter.env.get("IROut"), result.interpreter.env.get("LowerFailed")


@pytest.mark.parametrize(
    "source",
    ['Print "hello".', "Print 42.", 'Name = 7;\nPrint Name.', "Print 2 + 3 * 4."],
)
def test_kuro_lowering_emits_print_ir_for_basic_programs(source):
    ir, failed = lower_source(source)
    assert failed in (None, 0)
    assert ir[-1] == "PRINT"
    assert ir[0] in ("CONST", "LOADVAR")


def test_kuro_lowering_handles_assignment_then_variable_read():
    ir, failed = lower_source('Name = 7;\nPrint Name.')
    assert failed in (None, 0)
    assert ir == ["CONST", "7", "STORE_LIST", "Name", "LOADVAR", "Name", "PRINT"]


def test_kuro_lowering_handles_multi_value_assignment():
    ir, failed = lower_source('Names = "A", "B", "C";')
    assert failed in (None, 0)
    assert ir == [
        "CONST", "A", "CONST", "B", "CONST", "C", "STORE_LIST", "Names"
    ]


def test_kuro_lowering_preserves_postfix_arithmetic_order():
    ir, failed = lower_source("Print 2 + 3 * 4.")
    assert failed in (None, 0)
    assert ir == ["CONST", "2", "CONST", "3", "CONST", "4", "BINOP", "*", "BINOP", "+", "PRINT"]


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ("N = 1;\nUpdate N to N + 2;", ["CONST", "1", "STORE_LIST", "N", "LOADVAR", "N", "CONST", "2", "BINOP", "+", "UPDATE", "N"]),
        ("N = 1;\nAdd 2 to N;", ["CONST", "1", "STORE_LIST", "N", "CONST", "2", "ADD", "N"]),
        ("N = 1;\nAppend 2 to N;", ["CONST", "1", "STORE_LIST", "N", "CONST", "2", "APPEND", "N"]),
    ],
)
def test_kuro_lowering_handles_state_mutation(source, expected):
    ir, failed = lower_source(source)
    assert failed in (None, 0)
    assert ir == expected


def test_kuro_lowering_handles_if_and_comparison():
    ir, failed = lower_source('N = 1;\nIf N is greater than 0;\nPrint N.\nDone.')
    assert failed in (None, 0)
    assert ir == [
        "CONST", "1", "STORE_LIST", "N",
        "LOADVAR", "N", "CONST", "0", "CMP", "gt",
        "IF_BEGIN", "LOADVAR", "N", "PRINT", "ELSE_BEGIN", "IF_END",
    ]


def test_kuro_lowering_continues_boolean_tail_after_character_class():
    ir, failed = lower_source(
        'If Ch is alpha or Ch is equal to "_";\nPrint Ch.\nDone.'
    )
    assert failed in (None, 0)
    assert ir == [
        "LOADVAR", "Ch", "ISCLASS", "alpha",
        "LOADVAR", "Ch", "CONST", "_", "CMP", "eq", "BOOL", "OR",
        "IF_BEGIN", "LOADVAR", "Ch", "PRINT", "ELSE_BEGIN", "IF_END",
    ]


def test_kuro_lowering_handles_repeat_and_while_blocks():
    ir, failed = lower_source("Repeat 2;\nPrint Index.\nDone.")
    assert failed in (None, 0)
    assert ir == ["CONST", "2", "REPEAT_BEGIN", "LOADVAR", "Index", "PRINT", "REPEAT_END"]

    ir, failed = lower_source("N = 0;\nWhile N is less than 2;\nAdd 1 to N;\nDone.")
    assert failed in (None, 0)
    assert ir == [
        "CONST", "0", "STORE_LIST", "N",
        "WHILE_BEGIN", "LOADVAR", "N", "CONST", "2", "CMP", "lt", "WHILE_TEST",
        "CONST", "1", "ADD", "N", "WHILE_END",
    ]


def test_kuro_lowering_handles_action_return_and_call():
    ir, failed = lower_source(
        "Action Add A, B;\nReturn A + B;\nDone.\nCall Add 3, 4;"
    )
    assert failed in (None, 0)
    assert ir == [
        "FUNC_BEGIN", "Add", "PARAM", "A", "NONE", "PARAM", "B", "NONE",
        "LOADVAR", "A", "LOADVAR", "B", "BINOP", "+", "RETURN", "FUNC_END",
        "CALL_BEGIN", "Add", "CONST", "3", "CONST", "4", "CALL_END",
    ]


def test_kuro_lowering_handles_typed_action_parameter():
    ir, failed = lower_source("Action Echo X: Integers;\nReturn X;\nDone.")
    assert failed in (None, 0)
    assert ir == ["FUNC_BEGIN", "Echo", "PARAM", "X", "Integers", "LOADVAR", "X", "RETURN", "FUNC_END"]


def test_kuro_lowering_handles_complex_set_and_call_arguments():
    ir, failed = lower_source(
        'Name = "Kuro";\nSet Name 1 + 1 to "X" + "Y";'
    )
    assert failed in (None, 0)
    assert ir == [
        "CONST", "Kuro", "STORE_LIST", "Name",
        "CONST", "1", "CONST", "1", "BINOP", "+",
        "CONST", "X", "CONST", "Y", "BINOP", "+", "SET", "Name",
    ]

    ir, failed = lower_source(
        "Action Add A, B;\nReturn A + B;\nDone.\nCall Add 1 + 2, 3 * 4;"
    )
    assert failed in (None, 0)
    assert ir[-15:] == [
        "CALL_BEGIN", "Add", "CONST", "1", "CONST", "2", "BINOP", "+",
        "CONST", "3", "CONST", "4", "BINOP", "*", "CALL_END",
    ]


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ("Take user Name;", ["INPUT", "Name"]),
        ("Take user Name and Age;", ["INPUT", "Name", "INPUT", "Age"]),
        ("Name = \"Kuro\";\nGet Name;", ["CONST", "Kuro", "STORE_LIST", "Name", "GET", "Name", "0"]),
        ("Name = \"Kuro\";\nGet Name 0;", ["CONST", "Kuro", "STORE_LIST", "Name", "CONST", "0", "GET", "Name", "1"]),
        ("Name = \"Kuro\";\nLength Name;", ["CONST", "Kuro", "STORE_LIST", "Name", "LENGTH", "Name"]),
        ("Name = \"Kuro\";\nSet Name 0 to \"X\";", ["CONST", "Kuro", "STORE_LIST", "Name", "CONST", "0", "CONST", "X", "SET", "Name"]),
        ("Compare R 1 is equal to 1;", ["CONST", "1", "CONST", "1", "CMP", "eq", "STORE_LIST", "R"]),
    ],
)
def test_kuro_lowering_handles_remaining_basic_statements(source, expected):
    ir, failed = lower_source(source)
    assert failed in (None, 0)
    assert ir == expected


def test_kuro_lowering_matches_parser_ast_contract():
    source = 'Print "hello".'
    tokens, diags = tokenize(source)
    program = parse(tokens, diags)
    assert not diags.has_errors()
    assert canon_program(program) == ["PROGRAM", "PRINT", "LIT_STR", "hello", "END_EXPR", "END_BLOCK"]
    ir, failed = lower_source(source)
    assert failed in (None, 0)
    assert ir == ["CONST", "hello", "PRINT"]
