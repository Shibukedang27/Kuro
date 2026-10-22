"""Compiler-private Repeat counters are invocation state, not closure data.

These reference-only contracts intentionally retain captured Index/user overlay
semantics. Every witness has an external budget, including baseline failures.
"""

import io

import pytest

from compiler.interpreter import Interpreter
from compiler.pipeline import compile_source
from compiler.values import ClosureValue


_BUDGET = 10_000


def run_bounded(source, *, initial_env=None):
    compiled = compile_source(source)
    assert compiled.ok, compiled.diags.render_all()
    steps = 0

    def trace(_instruction, _environment, _depth, _pc):
        nonlocal steps
        steps += 1
        assert steps <= _BUDGET, "closure Repeat instruction budget exhausted"

    output = io.StringIO()
    runtime = Interpreter(compiled.ir, output=output, trace=trace)
    runtime.env.update(initial_env or {})
    before = {k: v for k, v in runtime.env.items() if k.endswith("$")}
    runtime.run()
    assert runtime.frames == []
    assert {k: v for k, v in runtime.env.items() if k.endswith("$")} == before
    return output.getvalue(), runtime


_WORKER = (
    "Action Worker Dummy: Integers;\n"
    "Repeat 2;\nPrint 7.\nDone.\nReturn 0;\nDone.\n"
)


@pytest.mark.parametrize("invocation", [
    'Repeat 1;\nCall MakeClosure "Worker";\nHandle = @_;\n'
    'Call Invoke Handle, 0;\nDone.',
    'Handle = 0;\nRepeat 1;\nCall MakeClosure "Worker";\n'
    'Update Handle to @_;\nDone.\nCall Invoke Handle, 0;',
])
def test_closure_created_in_repeat_completes_inside_or_after_creator_loop(invocation):
    output, runtime = run_bounded(_WORKER + invocation)
    assert output == "7\n7\n"
    handle = runtime.env["Handle"]
    assert isinstance(handle, ClosureValue)
    assert "__repeat_i1$" not in handle.captured
    # Index is source-visible snapshot data and is deliberately not filtered.
    assert handle.captured["Index"] == 0


def test_early_returning_closure_restores_each_callers_live_counter():
    output, runtime = run_bounded(
        'Action Worker Dummy: Integers;\n'
        'Repeat 4;\nPrint 7.\nReturn 11;\nDone.\nReturn -1;\nDone.\n'
        'Handle = 0;\nRepeat 1;\nCall MakeClosure "Worker";\n'
        'Update Handle to @_;\nDone.\n'
        'Repeat 3;\nCall Invoke Handle, 0;\nPrint @_.\nPrint Index.\nDone.'
    )
    assert output == "7\n11\n0\n7\n11\n1\n7\n11\n2\n"
    assert "Index" not in runtime.env


def test_nested_counters_are_not_captured_and_existing_global_state_is_restored():
    output, runtime = run_bounded(
        'Action Worker Dummy: Integers;\n'
        'Repeat 2;\nRepeat 3;\nPrint 7.\nDone.\nDone.\nReturn 0;\nDone.\n'
        'Handle = 0;\nRepeat 1;\nRepeat 1;\nCall MakeClosure "Worker";\n'
        'Update Handle to @_;\nDone.\nDone.\n'
        'Repeat 2;\nCall Invoke Handle, 0;\nDone.',
        initial_env={"Index": 41, "__repeat_i1$": 73, "__repeat_i2$": 89},
    )
    assert output == "7\n" * 12
    assert runtime.env["Index"] == 41
    assert not any(k.endswith("$") for k in runtime.env["Handle"].captured)


def test_closure_can_call_direct_repeat_action_without_sharing_counters():
    output, _ = run_bounded(
        'Action Callee;\nRepeat 2;\nPrint 8.\nDone.\nReturn 0;\nDone.\n'
        'Action Worker Dummy: Integers;\n'
        'Repeat 2;\nCall Callee;\nPrint 7.\nDone.\nReturn 0;\nDone.\n'
        'Repeat 1;\nCall MakeClosure "Worker";\nHandle = @_;\n'
        'Call Invoke Handle, 0;\nDone.'
    )
    assert output == "8\n8\n7\n" * 2


def test_nested_closure_creation_filters_counters_from_all_active_frames():
    output, runtime = run_bounded(
        'Inner = 0;\n'
        'Action Leaf Value;\nRepeat 2;\nPrint Value.\nDone.\nReturn 0;\nDone.\n'
        'Action Factory Value;\nRepeat 1;\nCall MakeClosure "Leaf";\n'
        'Update Inner to @_;\nReturn @_;\nDone.\nReturn 0;\nDone.\n'
        'Repeat 1;\nCall MakeClosure "Factory";\nOuter = @_;\n'
        'Call Invoke Outer, 19;\nDone.\nCall Invoke Inner, 23;'
    )
    assert output == "23\n23\n"
    assert runtime.env["Inner"].captured["Value"] == 19
    assert not any(k.endswith("$") for k in runtime.env["Inner"].captured)


def test_recursive_closure_invocation_preserves_counter_cleanup():
    output, _ = run_bounded(
        'Again is Integers;\n'
        'Action Worker N;\nIf N is greater than 0;\nRepeat 2;\n'
        'Call Invoke Again, N - 1;\nPrint N.\n'
        'Done.\nDone.\nReturn N;\nDone.\n'
        'Repeat 1;\nCall MakeClosure "Worker";\nAgain = @_;\n'
        'Call Invoke Again, 2;\nDone.'
    )
    assert output == "1\n1\n2\n1\n1\n2\n"


def test_spawned_closure_uses_fresh_repeat_state_after_creator_loop_exits():
    output, _ = run_bounded(
        _WORKER + 'Task = 0;\nRepeat 1;\nCall MakeClosure "Worker";\n'
        'Call Spawn @_, 0;\nUpdate Task to @_;\nDone.\nCall Await Task;\nPrint @_.',
    )
    assert output == "7\n7\n0\n"


def test_user_counter_like_names_parameters_and_snapshot_writes_are_unchanged():
    output, runtime = run_bounded(
        '__repeat_i1 = 71;\nShared = 5;\nHandle = 0;\n'
        'Action Worker __repeat_i1;\nRepeat 2;\nPrint __repeat_i1.\n'
        'Add 1 to Shared;\nDone.\nReturn Shared;\nDone.\n'
        'Repeat 1;\nCall MakeClosure "Worker";\nUpdate Handle to @_;\nDone.\n'
        'Update Shared to 90;\nCall Invoke Handle, 13;\nPrint @_.\n'
        'Print Shared.\nPrint __repeat_i1.'
    )
    # Reads retain immutable capture priority even after writes to globals.
    assert output == "13\n13\n5\n6\n71\n"
    assert runtime.env["Handle"].captured["__repeat_i1"] == 71


def test_captured_index_overlay_is_preserved_not_claimed_as_loop_index_parity():
    output, runtime = run_bounded(
        'Action Worker Dummy: Integers;\nRepeat 2;\nReturn Index;\nDone.\n'
        'Return -1;\nDone.\nHandle = 0;\n'
        'Repeat 3;\nCall MakeClosure "Worker";\nUpdate Handle to @_;\nDone.\n'
        'Call Invoke Handle, 0;\nPrint @_.',
        initial_env={"Index": 41},
    )
    assert output == "2\n"
    assert runtime.env["Index"] == 41
    assert runtime.env["Handle"].captured["Index"] == 2


def test_zero_count_closure_repeat_does_not_enter_body_or_leak_bindings():
    output, runtime = run_bounded(
        'Action Worker Dummy: Integers;\nRepeat 0;\nPrint 99.\nDone.\n'
        'Return 3;\nDone.\nRepeat 1;\nCall MakeClosure "Worker";\n'
        'Handle = @_;\nCall Invoke Handle, 0;\nPrint @_.\nDone.'
    )
    assert output == "3\n"
    assert "Index" not in runtime.env


@pytest.mark.parametrize("name, retained", [
    ("__repeat_i1$", False),
    ("__repeat_i12$", False),
    ("__repeat_i0$", True),
    ("__repeat_i01$", True),
    ("__repeat_i1", True),
    ("__repeat_i1$extra", True),
    ("Other$", True),
])
def test_only_exact_lowerer_counter_names_are_excluded(name, retained):
    _, runtime = run_bounded(
        'Action Read;\nReturn 0;\nDone.\n'
        'Call MakeClosure "Read";\nHandle = @_;',
        initial_env={name: 71},
    )
    assert (name in runtime.env["Handle"].captured) is retained
    assert runtime.env[name] == 71
