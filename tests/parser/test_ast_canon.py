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
    assert canon("") == ["PROGRAM", "END_BLOCK"]


def test_simple_assign_and_print():
    assert canon('Name = "Kuro";\nPrint Name.') == [
        "PROGRAM",
        "ASSIGN", "Name", "NONE", "LIT_STR", "Kuro", "END_VALUES",
        "PRINT", "VAR", "0", "Name",
        "END_BLOCK",
    ]


def test_typed_assign():
    assert canon("Age : Integers = 25;") == [
        "PROGRAM",
        "ASSIGN", "Age", "Integers", "LIT_INT", "25", "END_VALUES",
        "END_BLOCK",
    ]


def test_multi_value_assign_uses_end_marker_not_count():
    assert canon('Names = "A", "B", "C";') == [
        "PROGRAM",
        "ASSIGN", "Names", "NONE",
        "LIT_STR", "A", "LIT_STR", "B", "LIT_STR", "C", "END_VALUES",
        "END_BLOCK",
    ]


def test_arithmetic_precedence_shape():
    # 2 + 3 * 4  ->  postfix: 2 (3 4 BIN *) BIN +
    c = canon("N = 2 + 3 * 4;")
    assert c == [
        "PROGRAM",
        "ASSIGN", "N", "NONE",
        "LIT_INT", "2", "LIT_INT", "3", "LIT_INT", "4", "BIN", "*", "BIN", "+",
        "END_VALUES", "END_BLOCK",
    ]


def test_grouping_changes_shape():
    # (2 + 3) * 4  ->  postfix: (2 3 BIN +) 4 BIN *
    c = canon("N = (2 + 3) * 4;")
    assert c == [
        "PROGRAM",
        "ASSIGN", "N", "NONE",
        "LIT_INT", "2", "LIT_INT", "3", "BIN", "+", "LIT_INT", "4", "BIN", "*",
        "END_VALUES", "END_BLOCK",
    ]


def test_add_encodes_value_before_target():
    # Add v to N; parses v before N is even read (target comes after "to"),
    # so the encoding must put the value first too - see ast_canon.py.
    assert canon("Score is Integers;\nScore = 0;\nAdd 1 to Score;")[-5:] == [
        "ADD", "LIT_INT", "1", "Score", "END_BLOCK",
    ]


def test_update_encodes_target_before_value():
    # Update reads its target name before "to v", so target-then-value
    # matches parse order and stays a prefix encoding (unlike Add).
    assert canon("Score is Integers;\nUpdate Score to 5;")[-5:] == [
        "UPDATE", "Score", "LIT_INT", "5", "END_BLOCK",
    ]


def test_at_var_vs_bare_var_distinguished():
    assert canon("Print @_.") == ["PROGRAM", "PRINT", "VAR", "1", "_", "END_BLOCK"]


def test_if_else_and_or():
    c = canon(
        "If A is greater than 3 and B is less than 10;\nPrint A.\nElse;\nPrint B.\nDone."
    )
    assert c[0] == "PROGRAM"
    assert c[1] == "IF"  # If itself is prefix - the keyword is seen first
    assert c.count("CMP") == 2 and "gt" in c and "lt" in c
    # AND/CMP are postfix (children-before-tag - see ast_canon.py's module
    # docstring), so AND must appear strictly after both CMPs it combines.
    and_idx = c.index("AND")
    assert all(i < and_idx for i, tok in enumerate(c) if tok == "CMP")
    # then-block and else-block each end with their own END_BLOCK, and the
    # whole program's block ends with one more.
    assert c.count("END_BLOCK") == 3


def test_action_and_call_and_return():
    c = canon("Action Add A, B;\nReturn A + B;\nDone.\nCall Add 1, 2;")
    assert c[0] == "PROGRAM"
    assert c[1:5] == ["ACTION", "Add", "A", "NONE"]
    assert "B" in c and "END_PARAMS" in c
    assert "RETURN" in c
    call_idx = c.index("CALL")
    assert c[call_idx : call_idx + 2] == ["CALL", "Add"]
    assert "END_ARGS" in c[call_idx:]


def test_while_shape():
    c = canon("N is Integers;\nN = 0;\nWhile N is less than 3;\nAdd 1 to N;\nDone.")
    assert "WHILE" in c
    while_idx = c.index("WHILE")
    # WHILE itself is prefix (the keyword is seen before its condition);
    # CMP is postfix, so it appears after WHILE but only once its operands
    # (the condition's left/right expressions) have already been emitted.
    assert c[while_idx + 1] == "VAR"
    cmp_idx = c.index("CMP")
    assert cmp_idx > while_idx and c[cmp_idx + 1] == "lt"


def test_encoding_is_deterministic():
    src = 'Name = "Kuro";\nPrint Name.\nRepeat 3;\nPrint Index.\nDone.'
    assert canon(src) == canon(src)


def test_take_encoding():
    assert canon("Name is Text;\nAge is Integers;\nTake user Name and Age;") == [
        "PROGRAM",
        "DECL", "Name", "Text",
        "DECL", "Age", "Integers",
        "INPUT", "Name", "Age", "END_NAMES",
        "END_BLOCK",
    ]


def test_get_direct_vs_indexed():
    assert canon('Name = "Kuro";\nGet Name;') == [
        "PROGRAM",
        "ASSIGN", "Name", "NONE", "LIT_STR", "Kuro", "END_VALUES",
        "GET", "Name", "0",
        "END_BLOCK",
    ]
    assert canon('Name = "Kuro";\nGet Name 0;') == [
        "PROGRAM",
        "ASSIGN", "Name", "NONE", "LIT_STR", "Kuro", "END_VALUES",
        "GET", "Name", "1", "LIT_INT", "0",
        "END_BLOCK",
    ]


def test_length_encoding():
    assert canon('Name = "Kuro";\nLength Name;')[-3:-1] == ["LENGTH", "Name"]


def test_set_encoding_explicit():
    # target is read before either expression is parsed (Set N idx to v;),
    # so target-then-index-then-value matches real parse order and stays
    # a prefix encoding, unlike Add/Append.
    assert canon('Name = "Kuro";\nSet Name 0 to "k";') == [
        "PROGRAM",
        "ASSIGN", "Name", "NONE", "LIT_STR", "Kuro", "END_VALUES",
        "SET", "Name", "LIT_INT", "0", "LIT_STR", "k",
        "END_BLOCK",
    ]


def test_compare_statement_encoding():
    c = canon("A = 5;\nCompare Bigger A greater than 3;")
    assert c[:5] == ["PROGRAM", "ASSIGN", "A", "NONE", "LIT_INT"]
    compare_idx = c.index("COMPARE")
    assert c[compare_idx : compare_idx + 2] == ["COMPARE", "Bigger"]
    assert "CMP" in c[compare_idx:] and "gt" in c[compare_idx:]


def test_entered_legacy_desugars_to_if_encoding():
    legacy = canon(
        'Age is Integers;\nAge = 25;\n'
        'Entered Age is greater than 20 then Print "Old" otherwise Print "Young";'
    )
    equivalent = canon(
        'Age is Integers;\nAge = 25;\n'
        'If Age is greater than 20;\nPrint "Old".\nElse;\nPrint "Young".\nDone.'
    )
    assert legacy == equivalent


def test_block_end_markers_nest_correctly():
    # A Repeat inside an If's then-body: four blocks total (Repeat's own
    # body, the If's then-body containing it, the If's empty else-body,
    # and the outer program body), each closed by its own END_BLOCK in
    # the order they actually finish — innermost (Repeat's body) first,
    # outermost (the program) last.
    c = canon(
        "If Age is greater than 0;\nRepeat 2;\nPrint Index.\nDone.\nDone."
    )
    assert c[0] == "PROGRAM"
    assert c[1] == "IF"
    repeat_idx = c.index("REPEAT")
    end_positions = [i for i, tok in enumerate(c) if tok == "END_BLOCK"]
    assert len(end_positions) == 4
    assert repeat_idx < end_positions[0] < end_positions[1] < end_positions[2] < end_positions[3]
