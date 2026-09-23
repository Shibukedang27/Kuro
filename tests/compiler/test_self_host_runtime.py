from compiler.self_host import run_with_kuro_runtime


def test_kuro_authored_runtime_executes_program():
    env = run_with_kuro_runtime('Print "kuro runtime".')
    assert env["RuntimeExitCode"] == 0
    assert env["RuntimeFailed"] == 0
    assert env["VMOutput"] == ["kuro runtime"]


def test_kuro_authored_runtime_executes_loop_and_recursion():
    env = run_with_kuro_runtime(
        "N = 0;\nWhile N is less than 3;\nAdd 1 to N;\nDone.\n"
        "Action Fact A;\nIf A is less than or equal to 1;\nReturn 1;\nElse;\n"
        "Call Fact A - 1;\nReturn A * @_;\nDone.\nDone.\n"
        "Call Fact 5;\nPrint @_."
    )
    assert env["RuntimeExitCode"] == 0
    assert env["VMOutput"] == [120]
