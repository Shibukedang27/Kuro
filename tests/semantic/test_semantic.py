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


def test_index_only_defined_inside_repeat():
    assert "E4001" in codes("Print Index.")
    assert compile_source("Repeat 3;\nPrint Index.\nDone.").ok


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

def test_several_semantic_errors_reported_together():
    src = "Print Missing1.\nPrint Missing2."
    cs = codes(src)
    assert cs.count("E4001") == 2
