"""Result-owner entry, publication, and closure-snapshot regressions for IR."""

import io

import pytest

from compiler.interpreter import Interpreter
from compiler.pipeline import compile_source
from compiler.values import ClosureValue


def run_bounded(source, *, initial_env=None):
    compiled = compile_source(source)
    assert compiled.ok, compiled.diags.render_all()
    steps = 0

    def trace(_instruction, _environment, _depth, _pc):
        nonlocal steps
        steps += 1
        assert steps <= 10_000, "result ownership instruction budget exhausted"

    output = io.StringIO()
    runtime = Interpreter(compiled.ir, output=output, trace=trace)
    runtime.env.update(initial_env or {})
    before = {k: v for k, v in runtime.env.items() if k.endswith("$")}
    runtime.run()
    assert runtime.frames == []
    assert {k: v for k, v in runtime.env.items() if k.endswith("$")} == before
    return output.getvalue(), runtime


_ANSWER = 'Action Answer;\nReturn 42;\nDone.\n'


@pytest.mark.parametrize("initial", [{}, {"_": 17}, {"_": None}, {"_": 0}])
def test_closure_call_producer_replaces_its_result_owner(initial):
    output, runtime = run_bounded(
        _ANSWER + 'Action Worker Dummy;\nCall Answer;\nPrint @_.\nReturn @_;\nDone.\n'
        'Call MakeClosure "Worker";\nHandle = @_;\nCall Invoke Handle, 0;\nPrint @_.',
        initial_env=initial,
    )
    assert output == "42\n42\n"
    assert runtime.env["_"] == 42
    handle = runtime.env["Handle"]
    assert isinstance(handle, ClosureValue)
    assert ("_" in handle.captured) is ("_" in initial)


@pytest.mark.parametrize("statement, written", [
    ('Call Answer;', 42), ('Get Items 0;', 8), ('Length Word;', 2),
])
def test_successful_producers_replace_only_the_active_owner(statement, written):
    output, runtime = run_bounded(
        _ANSWER + 'Items = 8, 9;\nWord = "ok";\nObserved = 0;\n'
        'Action Observe;\nUpdate Observed to @_;\nReturn 0;\nDone.\n'
        'Action Worker Dummy;\n' + statement + '\nCall Observe;\nPrint @_.\nReturn @_;\nDone.\n'
        'Call MakeClosure "Worker";\nHandle = @_;\nCall Invoke Handle, 0;\nPrint @_.',
        initial_env={"_": 17},
    )
    # Worker owns the producer result and passes it to Observe. Observe's
    # explicit Return publishes into Worker, then Invoke publishes to main.
    assert runtime.env["Observed"] == written
    assert output == "0\n0\n"
    assert runtime.env["_"] == 0
    assert runtime.env["Handle"].captured["_"] == 17


def test_makeclosure_snapshots_the_effective_owner_before_call_publication():
    _, runtime = run_bounded(
        'Action Read Dummy;\nReturn @_;\nDone.\nCall MakeClosure "Read";\nHandle = @_;',
        initial_env={"_": 17},
    )
    handle = runtime.env["Handle"]
    assert isinstance(handle, ClosureValue)
    assert handle.captured["_"] == 17
    assert runtime.env["_"] is handle


@pytest.mark.parametrize("initial, expected", [({}, None), ({"_": None}, None), ({"_": 0}, 0), ({"_": 17}, 17)])
def test_closure_without_producer_keeps_creation_snapshot_across_repeated_and_deferred_calls(initial, expected):
    output, runtime = run_bounded(
        _ANSWER + 'Action Worker Dummy;\nReturn @_;\nDone.\n'
        'Call MakeClosure "Worker";\nHandle = @_;\n'
        'Call Invoke Handle, 0;\nPrint @_.\nCall Answer;\n'
        'Call Invoke Handle, 0;\nPrint @_.\n'
        'Call Spawn Handle, 0;\nTask = @_;\nCall Answer;\nCall Await Task;\nPrint @_.',
        initial_env=initial,
    )
    assert output == f"{expected}\n" * 3
    assert ("_" in runtime.env["Handle"].captured) is ("_" in initial)
    if "_" in initial:
        assert runtime.env["Handle"].captured["_"] == initial["_"]
    assert runtime.runtime_stats()["task_states"] == {"done": 1}


def test_absent_closure_snapshot_does_not_fall_back_to_later_main_result():
    output, runtime = run_bounded(
        _ANSWER + 'Action Read Dummy;\nReturn @_;\nDone.\n'
        'Call MakeClosure "Read";\nHandle = @_;\nCall Answer;\n'
        'Call Invoke Handle, 0;\nPrint @_.',
    )
    assert output == "None\n"
    assert "_" not in runtime.env["Handle"].captured
    assert "_" in runtime.env and runtime.env["_"] is None


def test_nested_direct_action_copies_callers_effective_result():
    output, runtime = run_bounded(
        _ANSWER + 'Observed = 0;\n'
        'Action Read;\nUpdate Observed to @_;\nReturn @_;\nDone.\n'
        'Action Worker Dummy;\nCall Answer;\nCall Read;\nPrint @_.\nReturn @_;\nDone.\n'
        'Call MakeClosure "Worker";\nHandle = @_;\nCall Invoke Handle, 0;\nPrint @_.',
        initial_env={"_": 17},
    )
    assert runtime.env["Observed"] == 42
    assert output == "42\n42\n"


def test_failed_action_discards_its_result_but_keeps_global_side_effects():
    from compiler.interpreter import KuroRuntimeException

    compiled = compile_source(
        _ANSWER + 'Action Fail;\nGlobal = 9;\nReturn 1 / 0;\nDone.\n'
        'Action Outer;\nCall Answer;\nCall Fail;\nDone.\nCall Outer;'
    )
    assert compiled.ok, compiled.diags.render_all()
    runtime = Interpreter(compiled.ir, output=io.StringIO())
    runtime.env["_"] = 17
    with pytest.raises(KuroRuntimeException):
        runtime.run()
    assert runtime.env["_"] == 17
    assert runtime.env["Global"] == 9
    assert runtime.frames == []


def test_unset_main_result_read_is_none_without_creating_a_binding():
    output, runtime = run_bounded('Print @_.')
    assert output == 'None\n'
    assert "_" not in runtime.env
