"""Repeat's flat runtime bindings must survive nested and reentrant actions."""

import io

from compiler.interpreter import Interpreter
from compiler.pipeline import compile_source


_TRACE_BUDGET = 50_000


class _TraceBudgetExceeded(RuntimeError):
    pass


def run_bounded(source, *, initial_env=None):
    compiled = compile_source(source)
    assert compiled.ok, compiled.diags.render_all()

    remaining = _TRACE_BUDGET

    def trace(_instr, _env, _depth, _pc):
        nonlocal remaining
        remaining -= 1
        if remaining < 0:
            raise _TraceBudgetExceeded(
                f"execution exceeded the {_TRACE_BUDGET}-instruction trace budget"
            )

    output = io.StringIO()
    interpreter = Interpreter(compiled.ir, output=output, trace=trace)
    if initial_env:
        interpreter.env.update(initial_env)
    initial_hidden_counters = {
        name for name in interpreter.env
        if name.startswith("__repeat_i") and name.endswith("$")
    }
    interpreter.run()
    assert interpreter.frames == [], "action frames must be popped after execution"
    leaked_hidden_counters = {
        name for name in interpreter.env
        if name.startswith("__repeat_i") and name.endswith("$")
    } - initial_hidden_counters
    assert not leaked_hidden_counters, (
        f"hidden Repeat counters leaked into the environment: {leaked_hidden_counters!r}"
    )
    return output.getvalue(), interpreter


def test_completing_callee_repeat_preserves_callers_repeat_index_and_counter():
    source = (
        "Action Callee;\n"
        "Repeat 2;\nPrint Index.\nDone.\n"
        "Return 0;\nDone.\n"
        "Repeat 3;\n"
        "Call Callee;\nPrint Index.\n"
        "Done."
    )
    output, _ = run_bounded(source)
    assert output == "0\n1\n0\n0\n1\n1\n0\n1\n2\n"


def test_early_returning_callee_preserves_outer_index_for_all_iterations():
    source = (
        "Action Stop;\n"
        "Repeat 4;\nReturn Index + 100;\nDone.\n"
        "Return -1;\nDone.\n"
        "Repeat 3;\nCall Stop;\nPrint Index.\nPrint @_.\nDone."
    )
    output, _ = run_bounded(source)
    assert output == "0\n100\n1\n100\n2\n100\n"


def test_recursive_action_repeat_keeps_each_invocations_counter():
    source = (
        "Action Recur N;\n"
        "If N is greater than 0;\n"
        "Repeat 2;\n"
        "Call Recur N - 1;\n"
        "Print Index.\n"
        "Done.\n"
        "Done.\n"
        "Return 0;\nDone.\n"
        "Call Recur 2;"
    )
    output, _ = run_bounded(source)
    assert output == "0\n1\n0\n0\n1\n1\n"


def test_early_return_unwinds_nested_repeat_inside_while_and_if():
    source = (
        "Action Escape;\n"
        "Counter = 0;\n"
        "While Counter is less than 2;\n"
        "If Counter is equal to 1;\n"
        "Repeat 2;\n"
        "Repeat 2;\n"
        "If Index is equal to 1;\n"
        "Return Index;\n"
        "Done.\n"
        "Done.\n"
        "Done.\n"
        "Done.\n"
        "Add 1 to Counter;\n"
        "Done.\n"
        "Return -1;\nDone.\n"
        "Repeat 3;\n"
        "Call Escape;\n"
        "Print Index.\nPrint @_.\n"
        "Done."
    )
    output, _ = run_bounded(source)
    # The Return expression must read the inner Index (1) before either
    # nested Repeat restores it; cleanup must then reinstate the caller's Index.
    assert output == "0\n1\n1\n1\n2\n1\n"


def test_zero_count_repeat_restores_preexisting_index_and_counter():
    output, interpreter = run_bounded(
        "Repeat 0;\nPrint \"unreachable\".\nDone.",
        initial_env={"Index": 41, "__repeat_i1$": 73},
    )
    assert output == ""
    assert interpreter.env["Index"] == 41
    assert interpreter.env["__repeat_i1$"] == 73


def test_repeat_restores_preexisting_index_after_normal_completion():
    _, interpreter = run_bounded(
        "Repeat 2;\nDone.", initial_env={"Index": 41}
    )
    assert interpreter.env["Index"] == 41


def test_repeat_does_not_leave_index_or_hidden_counter_when_unset_before_entry():
    _, interpreter = run_bounded("Repeat 2;\nDone.")
    assert "Index" not in interpreter.env
    assert not any(name.startswith("__repeat_i") for name in interpreter.env)


def test_repeated_invocations_of_same_action_start_with_fresh_repeat_state():
    source = (
        "Action Emit N;\n"
        "Repeat N;\nPrint Index.\nDone.\n"
        "Return N;\nDone.\n"
        "Call Emit 2;\nCall Emit 3;\nPrint @_."
    )
    output, _ = run_bounded(source)
    assert output == "0\n1\n0\n1\n2\n3\n"


def test_repeat_counter_name_cannot_collide_with_global_or_parameter():
    source = (
        "__repeat_i1 = 71;\nShared = 0;\n"
        "Action Probe __repeat_i1;\n"
        "Repeat 2;\nAdd 1 to Shared;\nDone.\n"
        "Return __repeat_i1;\nDone.\n"
        "Call Probe 13;\n"
        "Print @_.\nPrint __repeat_i1.\nPrint Shared."
    )
    output, _ = run_bounded(source)
    assert output == "13\n71\n2\n"


def test_ordinary_global_writes_inside_reentrant_repeat_remain_shared():
    source = (
        "Total = 0;\n"
        "Action AddTwice;\n"
        "Repeat 2;\nAdd 1 to Total;\nDone.\n"
        "Return Total;\nDone.\n"
        "Repeat 2;\nCall AddTwice;\nDone.\n"
        "Print Total."
    )
    output, _ = run_bounded(source)
    assert output == "4\n"
