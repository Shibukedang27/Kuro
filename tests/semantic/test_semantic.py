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
    # ADR-0013 (Stage 7) added E3006, comparison operand type checking,
    # applied uniformly to If/While/Compare's conditions via the same
    # _check_condition helper — this test now documents that While
    # doesn't regress *relative to If's own new behavior* (both reject
    # Text compared with `greater than` against a number the same way),
    # not that neither is checked (that was the pre-Stage-7 behavior this
    # test used to document).
    r = compile_source('N is Text;\nN = "x";\nWhile N is greater than 0;\nPrint N.\nDone.')
    assert not r.ok
    assert "E3006" in [d.code for d in r.diags.diagnostics]

    r_if = compile_source('N is Text;\nN = "x";\nIf N is greater than 0;\nPrint N.\nDone.')
    assert not r_if.ok
    assert "E3006" in [d.code for d in r_if.diags.diagnostics]


def test_several_semantic_errors_reported_together():
    src = "Print Missing1.\nPrint Missing2."
    cs = codes(src)
    assert cs.count("E4001") == 2


# --- ADR-0013 (Stage 7): six new type checks -----------------------------

def test_e3006_comparison_text_vs_integer_rejected():
    assert "E3006" in codes('N is Text;\nN = "x";\nIf N is greater than 5;\nPrint N.\nDone.')


def test_e3006_comparison_integer_vs_decimal_allowed():
    r = compile_source(
        "A is Integers;\nA = 5;\nB is Decimals;\nB = 2.5;\n"
        "If A is greater than B;\nPrint A.\nDone."
    )
    assert r.ok, r.diags.render_all()


def test_e3006_comparison_text_vs_text_allowed():
    r = compile_source('A is Text;\nA = "a";\nB is Text;\nB = "b";\nIf A is greater than B;\nPrint A.\nDone.')
    assert r.ok, r.diags.render_all()


def test_e3006_equality_across_types_is_not_restricted():
    # eq/ne are deliberately NOT restricted (ADR-0013) - equality across
    # differing types is well-defined even though always false.
    r = compile_source('N is Text;\nN = "x";\nIf N is equal to 5;\nPrint N.\nDone.')
    assert r.ok, r.diags.render_all()


def test_e3006_applies_to_compare_statement_too():
    assert "E3006" in codes('N is Text;\nN = "x";\nCompare R N greater than 5;')


def test_e3007_call_argument_type_mismatch():
    assert "E3007" in codes('Action Add A: Integers, B: Integers;\nReturn A + B;\nDone.\nCall Add "x", "y";')


def test_e3007_call_argument_type_match_ok():
    r = compile_source("Action Add A: Integers, B: Integers;\nReturn A + B;\nDone.\nCall Add 1, 2;")
    assert r.ok, r.diags.render_all()


def test_e3007_untyped_parameter_imposes_no_constraint():
    r = compile_source('Action Echo A;\nReturn A;\nDone.\nCall Echo "anything";')
    assert r.ok, r.diags.render_all()


def test_e3008_repeat_count_must_be_integers():
    assert "E3008" in codes('Repeat "three";\nPrint Index.\nDone.')


def test_e3008_repeat_count_integer_ok():
    r = compile_source("Repeat 3;\nPrint Index.\nDone.")
    assert r.ok, r.diags.render_all()


def test_e3009_length_target_must_be_text():
    assert "E3009" in codes("N is Integers;\nN = 5;\nLength N;")


def test_e3009_length_target_text_ok():
    r = compile_source('N is Text;\nN = "hello";\nLength N;')
    assert r.ok, r.diags.render_all()


def test_e3010_get_index_must_be_integers():
    assert "E3010" in codes('Names = "A", "B";\nGet Names "x";')


def test_e3010_set_index_must_be_integers():
    assert "E3010" in codes('Name is Text;\nName = "Kuro";\nSet Name "x" to "k";')


def test_e3010_index_integer_ok():
    r = compile_source('Names = "A", "B";\nGet Names 0;')
    assert r.ok, r.diags.render_all()


def test_e3011_text_concatenation_now_recognized():
    # Closes the real gap documented in the audit: _infer previously
    # didn't know Text + Text was valid, silently treating it as
    # "unknown" rather than Text, so a declared-Text target's E3001
    # check never actually ran against a concatenation result.
    r = compile_source('N is Text;\nN = "a" + "b";')
    assert r.ok, r.diags.render_all()
    assert "E3011" not in codes('N is Text;\nN = "a" + "b";')


def test_e3011_text_plus_integer_rejected():
    assert "E3011" in codes('N = "a" + 5;')


def test_e3011_text_minus_text_rejected():
    # '+' is the only operator Text supports (concatenation); '-'/'*'/'/'
    # between two Text values is not valid arithmetic.
    assert "E3011" in codes('N = "a" - "b";')


def test_e3011_now_catches_assign_of_bad_concatenation_result():
    # Before ADR-0013, this silently passed E3001 because _infer returned
    # None (unknown) for "a" + 5 instead of erroring - now E3011 catches
    # the bad arithmetic itself, at the point it happens.
    assert "E3011" in codes('N is Text;\nN = "a" + 5;')


def test_e3011_numeric_arithmetic_still_works():
    r = compile_source("N is Decimals;\nN = 1 + 2.5;")
    assert r.ok, r.diags.render_all()


# --- ADR-0013's deliberate non-changes (documented, tested) ---------------

def test_isclass_on_non_text_operand_still_compiles():
    # Deliberately not restricted (ADR-0013): the runtime already
    # degrades gracefully (always false) rather than erroring.
    r = compile_source("N = 5;\nIf N is digit;\nPrint N.\nDone.")
    assert r.ok, r.diags.render_all()


def test_append_still_has_no_homogeneity_check():
    # Unchanged from ADR-0005's original stance - not in scope for
    # ADR-0013 either.
    r = compile_source('Tokens = "a";\nAppend 5 to Tokens;')
    assert r.ok, r.diags.render_all()
