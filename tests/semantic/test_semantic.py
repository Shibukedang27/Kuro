from compiler.pipeline import compile_source


def codes(src):
    r = compile_source(src)
    return [d.code for d in r.diags.diagnostics]


def test_valid_program_has_no_errors():
    r = compile_source('Name = "Kuro";\nPrint Name.')
    assert r.ok


def test_undefined_variable():
    assert "E4001" in codes("Print Missing.")


def test_undefined_variable_in_expression():
    assert "E4001" in codes("N = 1 + Missing;")


def test_duplicate_declaration():
    assert "E4002" in codes("Age is Integers;\nAge is Integers;")


def test_duplicate_action():
    assert "E4002" in codes("Action A X;\nReturn X;\nDone.\nAction A X;\nReturn X;\nDone.")


def test_unknown_action_call():
    assert "E4003" in codes("Call Missing 1;")


def test_wrong_arg_count():
    assert "E4004" in codes("Action A X;\nReturn X;\nDone.\nCall A;")


def test_return_outside_action():
    assert "E4005" in codes("Return 1;")


def test_action_locals_do_not_leak():
    # 'Local' is only bound inside the Action; using it at top level is an error.
    assert "E4001" in codes(
        "Action A Local;\nReturn Local;\nDone.\nPrint Local."
    )


def test_ordinary_variable_assigned_inside_action_is_visible_after_it():
    # The interpreter's storage is flat (compiler/interpreter.py): a
    # non-parameter name assigned inside an Action body really is visible
    # afterward, matching the bootstrap engine and matching what already
    # holds for Repeat (see resolver.py's ActionDecl handling and its
    # comment). Unlike a parameter, an ordinary Assign is not scoped to
    # the call at all.
    r = compile_source("Action A;\nX = 1;\nReturn X;\nDone.\nCall A;\nPrint X.")
    assert r.ok, r.diags.render_all()


def test_variable_assigned_in_one_action_visible_in_another():
    r = compile_source(
        "Action First;\nShared = 5;\nReturn Shared;\nDone.\n"
        "Action Second;\nReturn Shared;\nDone.\n"
        "Call First;\nCall Second;\nPrint @_."
    )
    assert r.ok, r.diags.render_all()


def test_index_only_defined_inside_repeat():
    assert "E4001" in codes("Print Index.")
    assert compile_source("Repeat 3;\nPrint Index.\nDone.").ok


def test_variable_first_assigned_inside_repeat_is_visible_after_it():
    # The interpreter's storage is flat (compiler/interpreter.py): a name
    # assigned inside a Repeat body really does exist afterward, matching
    # the bootstrap engine. The resolver must not falsely reject this.
    r = compile_source("Repeat 3;\nX = Index;\nDone.\nPrint X.")
    assert r.ok, r.diags.render_all()


def test_index_does_not_leak_past_its_own_repeat():
    assert "E4001" in codes("Repeat 3;\nPrint Index.\nDone.\nPrint Index.")


def test_nested_repeat_inner_index_does_not_shadow_outer_after_it_ends():
    src = (
        "Repeat 2;\n"
        "Repeat 3;\n"
        "Y = Index;\n"
        "Done.\n"
        "Print Index.\n"  # still the outer Repeat's Index — must resolve
        "Done."
    )
    assert compile_source(src).ok


def test_input_variable_must_be_declared():
    assert "E4001" in codes("Take user Age;")
    r = compile_source("Age is Integers;\nTake user Age;")
    assert r.ok


# --- type checking --------------------------------------------------

def test_unknown_type():
    assert "E3003" in codes("Age is Number;")


def test_type_mismatch_on_assign():
    assert "E3001" in codes('Age is Integers;\nAge = "twenty";')


def test_integer_to_decimal_widening_is_allowed():
    r = compile_source("Age is Decimals;\nAge = 25;")
    assert r.ok


def test_add_target_must_be_numeric():
    assert "E3002" in codes('Name is Text;\nName = "hi";\nAdd 1 to Name;')


def test_add_target_numeric_ok():
    r = compile_source("Score is Integers;\nScore = 0;\nAdd 1 to Score;")
    assert r.ok


def test_set_text_requires_single_character():
    r = compile_source('Name is Text;\nName = "abc";\nSet Name 0 to "z";')
    assert r.ok


# --- multiple diagnostics in one pass --------------------------------

def test_while_condition_checks_undefined_variable():
    assert "E4001" in codes("While Missing is equal to 1;\nPrint Missing.\nDone.")


def test_while_body_variable_visible_after_it():
    r = compile_source("N is Integers;\nN = 0;\nWhile N is less than 3;\nX = N;\nAdd 1 to N;\nDone.\nPrint X.")
    assert r.ok, r.diags.render_all()


def test_while_condition_is_type_consistent_with_if():
    # Conditions aren't statically type-checked for either If or While
    # today (see compiler/typecheck.py) — this just documents that While
    # doesn't regress relative to If's existing (lack of) behavior here.
    r = compile_source('N is Text;\nN = "x";\nWhile N is greater than 0;\nPrint N.\nDone.')
    assert r.ok


def test_several_semantic_errors_reported_together():
    src = "Print Missing1.\nPrint Missing2."
    cs = codes(src)
    assert cs.count("E4001") == 2
