"""Unit tests for the canonical AST encoding (compiler/ast_canon.py) that
Stage 6's differential test (tests/self_host/test_parser_cross.py) relies
on. These test the *encoding itself* against known expected token lists —
independent of the self-hosted parser — so a mismatch there is diagnosable
without also doubting this file.
"""
from compiler.ast_canon import canon_program
from compiler.diagnostics import DiagnosticEngine
from compiler.lexer import tokenize
from compiler.parser import parse


def canon(src: str) -> list[str]:
    toks, diags = tokenize(src)
    program = parse(toks, diags)
    assert not diags.diagnostics, diags.render_all()
    return canon_program(program)


def test_empty_program():
    assert canon("") == ["PROGRAM", "0"]


def test_simple_assign_and_print():
    assert canon('Name = "Kuro";\nPrint Name.') == [
        "PROGRAM", "2",
        "ASSIGN", "Name", "NONE", "1", "LIT_STR", "Kuro",
        "PRINT", "VAR", "0", "Name",
    ]


def test_typed_assign():
    assert canon("Age : Integers = 25;") == [
        "PROGRAM", "1",
        "ASSIGN", "Age", "Integers", "1", "LIT_INT", "25",
    ]


def test_arithmetic_precedence_shape():
    # 2 + 3 * 4  ->  BIN + 2 (BIN * 3 4)
    c = canon("N = 2 + 3 * 4;")
    assert c == [
        "PROGRAM", "1",
        "ASSIGN", "N", "NONE", "1",
        "BIN", "+", "LIT_INT", "2", "BIN", "*", "LIT_INT", "3", "LIT_INT", "4",
    ]


def test_grouping_changes_shape():
    # (2 + 3) * 4  ->  BIN * (BIN + 2 3) 4
    c = canon("N = (2 + 3) * 4;")
    assert c == [
        "PROGRAM", "1",
        "ASSIGN", "N", "NONE", "1",
        "BIN", "*", "BIN", "+", "LIT_INT", "2", "LIT_INT", "3", "LIT_INT", "4",
    ]


def test_at_var_vs_bare_var_distinguished():
    c = canon("Print @_.")
    assert c == ["PROGRAM", "1", "PRINT", "VAR", "1", "_"]


def test_if_else_and_or():
    c = canon(
        "If A is greater than 3 and B is less than 10;\nPrint A.\nElse;\nPrint B.\nDone."
    )
    assert c[:2] == ["PROGRAM", "1"]
    assert c[2] == "IF"
    assert c[3] == "AND"
    assert "CMP" in c and "gt" in c and "lt" in c


def test_action_and_call_and_return():
    c = canon("Action Add A, B;\nReturn A + B;\nDone.\nCall Add 1, 2;")
    assert c[:2] == ["PROGRAM", "2"]
    assert c[2:6] == ["ACTION", "Add", "2", "A"]
    assert "RETURN" in c
    assert "CALL" in c and "Add" in c


def test_while_shape():
    c = canon("N is Integers;\nN = 0;\nWhile N is less than 3;\nAdd 1 to N;\nDone.")
    assert "WHILE" in c
    idx = c.index("WHILE")
    assert c[idx + 1] == "CMP" and c[idx + 2] == "lt"


def test_encoding_is_deterministic():
    src = 'Name = "Kuro";\nPrint Name.\nRepeat 3;\nPrint Index.\nDone.'
    assert canon(src) == canon(src)
