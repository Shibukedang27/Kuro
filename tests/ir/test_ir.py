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
