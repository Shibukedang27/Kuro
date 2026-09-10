from compiler.ast_nodes import (
    ActionDecl, AddStmt, Assign, BinaryExpr, BoolAnd, BoolOr, CallStmt,
    Comparison, CompareStmt, Decl, GetStmt, IfStmt, Input, IsClass,
    LengthStmt, Literal, PrintStmt, RepeatStmt, ReturnStmt, SetStmt,
    UpdateStmt, VarRef, AppendStmt, WhileStmt,
)
from compiler.diagnostics import DiagnosticEngine
from compiler.lexer import tokenize
from compiler.parser import parse


def parse_ok(src):
    toks, diags = tokenize(src)
    program = parse(toks, diags)
    assert not diags.diagnostics, diags.render_all()
    return program.statements


def parse_errors(src):
    toks, diags = tokenize(src)
    parse(toks, diags)
    return diags


def test_declaration():
    [d] = parse_ok("Age is Integers;")
    assert isinstance(d, Decl) and d.name == "Age" and d.typ == "Integers"


def test_plain_assign():
    [a] = parse_ok('Name = "Kuro";')
    assert isinstance(a, Assign)
    assert a.name == "Name" and a.typ is None
    assert isinstance(a.values[0], Literal) and a.values[0].value == "Kuro"


def test_typed_assign():
    [a] = parse_ok("Age : Integers = 25;")
    assert a.typ == "Integers"
    assert a.values[0].value == 25


def test_multi_value_assign():
    [a] = parse_ok('Names = "A", "B", "C";')
    assert len(a.values) == 3


def test_take_input():
    [i] = parse_ok("Take user Name and Age;")
    assert isinstance(i, Input) and i.names == ["Name", "Age"]


def test_print():
    [p] = parse_ok("Print Name.")
    assert isinstance(p, PrintStmt) and isinstance(p.value, VarRef)


def test_print_at_var():
    [p] = parse_ok("Print @_.")
    assert p.value.name == "_" and p.value.explicit_at is True


def test_add():
    [a] = parse_ok("Add 5 to Score;")
    assert isinstance(a, AddStmt) and a.target == "Score"


def test_update():
    [u] = parse_ok("Update Score to 20;")
    assert isinstance(u, UpdateStmt) and u.name == "Score"


def test_get_with_and_without_index():
    [g1] = parse_ok("Get Names 1;")
    assert isinstance(g1, GetStmt) and g1.index is not None
    [g2] = parse_ok("Get Names;")
    assert g2.index is None


def test_length():
    [l] = parse_ok("Length Name;")
    assert isinstance(l, LengthStmt)


def test_set():
    [s] = parse_ok('Set Name 0 to "k";')
    assert isinstance(s, SetStmt) and s.target == "Name"


def test_append():
    [a] = parse_ok('Append "x" to Tokens;')
    assert isinstance(a, AppendStmt) and a.target == "Tokens"


def test_compare_no_is_required():
    [c] = parse_ok("Compare Bigger A greater than 3;")
    assert isinstance(c, CompareStmt)
    assert isinstance(c.condition, Comparison) and c.condition.op == "gt"


def test_compare_is_optional():
    [c] = parse_ok("Compare Bigger A is greater than 3;")
    assert c.condition.op == "gt"


def test_if_requires_is():
    [i] = parse_ok("If Age is greater than 20;\nPrint Name.\nDone.")
    assert isinstance(i, IfStmt)
    assert i.condition.op == "gt"


def test_if_else():
    [i] = parse_ok('If Age is greater than 20;\nPrint "Old".\nElse;\nPrint "Young".\nDone.')
    assert len(i.then_body) == 1 and len(i.else_body) == 1


def test_if_and_or_combinators():
    [i] = parse_ok(
        "If Age is greater than 5 and Age is less than 10;\nPrint Age.\nDone."
    )
    assert isinstance(i.condition, BoolAnd)

    [j] = parse_ok(
        "If Age is less than 5 or Age is greater than 10;\nPrint Age.\nDone."
    )
    assert isinstance(j.condition, BoolOr)


def test_is_class_condition():
    [i] = parse_ok("If C is digit;\nPrint C.\nDone.")
    assert isinstance(i.condition, IsClass) and i.condition.cls == "digit"


def test_ge_le_operators():
    [c1] = parse_ok("Compare R A greater than or equal to 3;")
    assert c1.condition.op == "ge"
    [c2] = parse_ok("Compare R A at least 3;")
    assert c2.condition.op == "ge"
    [c3] = parse_ok("Compare R A at most 3;")
    assert c3.condition.op == "le"


def test_repeat():
    [r] = parse_ok("Repeat 3;\nPrint Index.\nDone.")
    assert isinstance(r, RepeatStmt)


def test_while_basic():
    [w] = parse_ok("While N is greater than 0;\nAdd -1 to N;\nDone.")
    assert isinstance(w, WhileStmt)
    assert isinstance(w.condition, Comparison) and w.condition.op == "gt"
    assert len(w.body) == 1


def test_while_and_or_condition():
    [w] = parse_ok("While N is greater than 0 and N is less than 10;\nAdd 1 to N;\nDone.")
    assert isinstance(w.condition, BoolAnd)


def test_while_nested_inside_repeat():
    [r] = parse_ok(
        "Repeat 3;\nWhile Flag is equal to 1;\nUpdate Flag to 0;\nDone.\nDone."
    )
    assert isinstance(r, RepeatStmt)
    assert isinstance(r.body[0], WhileStmt)


def test_while_nested_inside_while():
    [w] = parse_ok(
        "While A is equal to 1;\nWhile B is equal to 1;\nUpdate B to 0;\nDone.\nDone."
    )
    assert isinstance(w, WhileStmt)
    assert isinstance(w.body[0], WhileStmt)


def test_error_while_missing_done():
    diags = parse_errors("While N is greater than 0;\nAdd -1 to N;\n")
    assert diags.has_errors()


def test_error_while_missing_semicolon_after_condition():
    diags = parse_errors("While N is greater than 0\nAdd -1 to N;\nDone.")
    assert diags.has_errors()


def test_error_while_malformed_condition():
    diags = parse_errors("While N;\nAdd -1 to N;\nDone.")
    assert diags.has_errors()


def test_action_paren_less_canonical():
    [a] = parse_ok("Action Add A, B;\nReturn A;\nDone.")
    assert isinstance(a, ActionDecl)
    assert [p.name for p in a.params] == ["A", "B"]


def test_action_typed_params():
    [a] = parse_ok("Action Add A: Integers, B: Integers;\nReturn A;\nDone.")
    assert [p.typ for p in a.params] == ["Integers", "Integers"]


def test_action_legacy_parens_still_accepted():
    [a] = parse_ok("Action Add(A, B);\nReturn A;\nDone.")
    assert [p.name for p in a.params] == ["A", "B"]


def test_call_paren_less_canonical():
    [_decl, c] = parse_ok("Action Add A, B;\nReturn A;\nDone.\nCall Add 1, 2;")
    assert isinstance(c, CallStmt) and len(c.args) == 2


def test_call_legacy_parens_still_accepted():
    [_decl, c] = parse_ok("Action Add(A, B);\nReturn A;\nDone.\nCall Add(1, 2);")
    assert len(c.args) == 2


def test_return():
    [_decl] = parse_ok("Action Echo A;\nReturn A;\nDone.")


def test_legacy_entered_syntax():
    [i] = parse_ok(
        'Age is Integers;\nAge = 25;\nEntered Age is greater than 20 then Print "Old" otherwise Print "Young";'
    )[-1:]
    assert isinstance(i, IfStmt)


def test_arithmetic_expression():
    [a] = parse_ok("Action Add A, B;\nResult = A + B * 2;\nReturn Result;\nDone.")
    assign = a.body[0]
    assert isinstance(assign.values[0], BinaryExpr) and assign.values[0].op == "+"


def test_parenthesized_expression():
    [a] = parse_ok("Action F A, B;\nResult = (A + B) * 2;\nReturn Result;\nDone.")
    assign = a.body[0]
    top = assign.values[0]
    assert isinstance(top, BinaryExpr) and top.op == "*"


def test_unary_minus():
    [a] = parse_ok("N = -5;")
    assert isinstance(a.values[0], BinaryExpr) and a.values[0].op == "-"


# --- error cases (spec section 54: negative tests) ------------------

def test_error_missing_semicolon():
    diags = parse_errors("Name = 1")
    assert diags.has_errors()


def test_error_unknown_statement():
    diags = parse_errors("Frobnicate Name;")
    assert diags.has_errors()
    assert diags.diagnostics[0].code == "E2001"


def test_error_unclosed_if():
    diags = parse_errors("If Age is greater than 20;\nPrint Age.\n")
    assert diags.has_errors()


def test_error_duplicate_action_param():
    diags = parse_errors("Action Add A, A;\nReturn A;\nDone.")
    assert any(d.code == "E2005" for d in diags.diagnostics)


def test_multiple_syntax_errors_reported_in_one_pass():
    diags = parse_errors("Bogus1 X;\nBogus2 Y;\n")
    codes = [d.code for d in diags.diagnostics]
    assert codes.count("E2001") == 2


def test_orphaned_done_after_recovery_does_not_hang():
    # Regression: a missing ';' inside a While's condition used to make
    # error recovery loop forever once it reached the block's trailing
    # "Done." at the wrong nesting level — _synchronize treated "Done" as
    # a universal stop point instead of only stopping on it when it
    # belonged to the block currently being recovered, so block() kept
    # calling stmt() on the same unconsumed "Done" token. Found while
    # adding Stage 6's While error-recovery tests (ADR-0009). This must
    # terminate, not hang.
    diags = parse_errors("While N is greater than 0\nAdd -1 to N;\nDone.")
    assert diags.has_errors()


def test_orphaned_done_at_top_level_recovers_and_parses_the_rest():
    toks, diags = tokenize('If Age is greater than 20\nPrint "x".\nDone.\nPrint "after".')
    program = parse(toks, diags)
    assert diags.has_errors()
    # recovery should still find the trailing, syntactically valid statement
    kinds = [type(s).__name__ for s in program.statements]
    assert "PrintStmt" in kinds
