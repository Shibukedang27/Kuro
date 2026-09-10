from compiler.ir import validate
from compiler.pipeline import compile_source


def build_ir(src):
    r = compile_source(src)
    assert r.ok, r.diags.render_all()
    return r.ir


def test_simple_program_lowers_to_valid_ir():
    ir = build_ir('Name = "Kuro";\nPrint Name.')
    assert validate(ir) == []
    ops = [i.op for i in ir.main]
    assert "STORE_LIST" in ops and "PRINT" in ops


def test_action_becomes_its_own_function():
    ir = build_ir("Action Add A, B;\nResult = A + B;\nReturn Result;\nDone.")
    assert "Add" in ir.functions
    fn = ir.functions["Add"]
    assert fn.params == ["A", "B"]
    assert any(i.op == "RETURN" for i in fn.body)


def test_if_lowers_to_labels_and_jumps():
    ir = build_ir(
        'Age is Integers;\nAge = 25;\nIf Age is greater than 20;\nPrint "Old".\nElse;\nPrint "Young".\nDone.'
    )
    ops = [i.op for i in ir.main]
    assert "JUMPF" in ops
    assert ops.count("LABEL") == 2
    assert validate(ir) == []


def test_repeat_saves_and_restores_index():
    ir = build_ir("Repeat 3;\nPrint Index.\nDone.")
    ops = [i.op for i in ir.main]
    assert "SAVEVAR" in ops and "RESTOREVAR" in ops
    assert validate(ir) == []


def test_nested_repeat_uses_distinct_counters():
    ir = build_ir("Repeat 2;\nRepeat 3;\nPrint Index.\nDone.\nDone.")
    stores = [i for i in ir.main if i.op == "STORE_LIST" and i.args[0].startswith("__repeat_i")]
    names = {i.args[0] for i in stores}
    assert len(names) == 2  # outer and inner loop got separate counters


def test_while_lowers_to_labels_jump_and_loop_guard():
    ir = build_ir("N is Integers;\nN = 0;\nWhile N is less than 3;\nAdd 1 to N;\nDone.")
    ops = [i.op for i in ir.main]
    assert ops.count("LABEL") == 2  # while_start, while_end
    assert "JUMPF" in ops
    assert "JUMP" in ops
    assert "LOOP_GUARD" in ops
    assert validate(ir) == []


def test_while_has_no_savevar_restorevar_unlike_repeat():
    ir = build_ir("N is Integers;\nN = 0;\nWhile N is less than 3;\nAdd 1 to N;\nDone.")
    ops = [i.op for i in ir.main]
    assert "SAVEVAR" not in ops and "RESTOREVAR" not in ops


def test_nested_while_uses_distinct_loop_guards():
    ir = build_ir(
        "A is Integers;\nA = 0;\nB is Integers;\n"
        "While A is less than 2;\nB = 0;\nWhile B is less than 2;\nAdd 1 to B;\nDone.\nAdd 1 to A;\nDone."
    )
    # Both While loops lower inline into ir.main's flat instruction list.
    guard_ids = [i.args[0] for i in ir.main if i.op == "LOOP_GUARD"]
    assert len(guard_ids) == 2
    assert len(set(guard_ids)) == 2


def test_repeat_still_checks_nonneg_count():
    ir = build_ir("Repeat 3;\nPrint Index.\nDone.")
    assert any(i.op == "CHECK_NONNEG" for i in ir.main)


def test_ir_printer_does_not_crash():
    ir = build_ir("Action Echo A;\nReturn A;\nDone.\nCall Echo 1;")
    text = str(ir)
    assert "func Echo" in text
    assert "main:" in text


def test_validate_catches_bad_jump_target():
    from compiler.ir import Instr, IRProgram

    prog = IRProgram(main=[Instr("JUMP", ("nowhere",))])
    problems = validate(prog)
    assert problems and "nowhere" in problems[0]
