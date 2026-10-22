"""Characterize current reference result overlays, not desired cross-engine semantics.

These passing compatibility witnesses do not endorse a stale @_ after
Call/Get/Length. A future scoped repair must update the contract explicitly.
"""

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


@pytest.mark.parametrize("initial, expected", [
    ({}, 42), ({"_": 17}, 17), ({"_": None}, None), ({"_": 0}, 0),
])
def test_capture_presence_not_truthiness_controls_result_read_priority(initial, expected):
    output, runtime = run_bounded(
        _ANSWER + 'Action Worker Dummy;\nCall Answer;\nPrint @_.\nReturn @_;\nDone.\n'
        'Call MakeClosure "Worker";\nHandle = @_;\nCall Invoke Handle, 0;\nPrint @_.',
        initial_env=initial,
    )
    assert output == f"{expected}\n{expected}\n"
    assert runtime.env["_"] == expected
    assert ("_" in runtime.env["Handle"].captured) == ("_" in initial)


@pytest.mark.parametrize("statement, written", [
    ('Call Answer;', 42), ('Get Items 0;', 8), ('Length Word;', 2),
])
def test_result_producers_write_global_but_reads_keep_existing_capture(statement, written):
    output, runtime = run_bounded(
        _ANSWER + 'Items = 8, 9;\nWord = "ok";\nObserved = 0;\n'
        'Action Observe;\nUpdate Observed to @_;\nReturn 0;\nDone.\n'
        'Action Worker Dummy;\n' + statement + '\nCall Observe;\nPrint @_.\nDone.\n'
        'Call MakeClosure "Worker";\nHandle = @_;\nCall Invoke Handle, 0;\nPrint @_.',
        initial_env={"_": 17},
    )
    # The direct helper sees the producer's global write, not Worker's overlay.
    # Outer Call Invoke then stores the no-Return result None into global _.
    assert runtime.env["Observed"] == written
    assert output == '17\nNone\n'
    assert runtime.env["_"] is None
    assert runtime.env["Handle"].captured["_"] == 17


def test_makeclosure_snapshots_previous_result_before_call_stores_new_handle():
    _, runtime = run_bounded(
        'Action Read Dummy;\nReturn @_;\nDone.\nCall MakeClosure "Read";\nHandle = @_;',
        initial_env={"_": 17},
    )
    handle = runtime.env["Handle"]
    assert isinstance(handle, ClosureValue)
    assert handle.captured["_"] == 17
    assert runtime.env["_"] is handle


def test_repeated_invocations_reuse_snapshot_instead_of_refreshing_result():
    output, runtime = run_bounded(
        _ANSWER + 'Action Worker Dummy;\nCall Answer;\nReturn @_;\nDone.\n'
        'Call MakeClosure "Worker";\nHandle = @_;\n'
        'Call Invoke Handle, 0;\nPrint @_.\nCall Answer;\nPrint @_.\n'
        'Call Invoke Handle, 0;\nPrint @_.', initial_env={"_": 17},
    )
    assert output == '17\n42\n17\n'
    assert runtime.env["Handle"].captured["_"] == 17


def test_direct_callee_does_not_inherit_callers_capture_overlay():
    output, runtime = run_bounded(
        _ANSWER + 'Observed = 0;\n'
        'Action Read;\nUpdate Observed to @_;\nReturn @_;\nDone.\n'
        'Action Worker Dummy;\nCall Answer;\nCall Read;\nPrint @_.\nReturn @_;\nDone.\n'
        'Call MakeClosure "Worker";\nHandle = @_;\nCall Invoke Handle, 0;\nPrint @_.',
        initial_env={"_": 17},
    )
    # Only the active frame has read priority; this is not dynamic frame lookup.
    assert runtime.env["Observed"] == 42
    assert output == '17\n17\n'


def test_nested_snapshot_reintroduces_outer_result_even_after_direct_call_write():
    output, runtime = run_bounded(
        _ANSWER + 'Inner = 0;\nAction Leaf Dummy;\nReturn @_;\nDone.\n'
        'Action Factory Dummy;\nCall Answer;\nCall MakeClosure "Leaf";\n'
        # A direct helper can publish the global handle; Factory's @_ is stale.
        'Call Publish;\nReturn 0;\nDone.\n'
        'Action Publish;\nUpdate Inner to @_;\nReturn 0;\nDone.\n'
        'Call MakeClosure "Factory";\nOuter = @_;\nCall Invoke Outer, 0;\n'
        'Call Invoke Inner, 0;\nPrint @_.', initial_env={"_": 17},
    )
    assert output == '17\n'
    assert isinstance(runtime.env["Inner"], ClosureValue)
    assert runtime.env["Inner"].captured["_"] == 17


def test_spawn_await_keeps_creation_snapshot_not_await_time_result():
    output, runtime = run_bounded(
        _ANSWER + 'Action Worker Dummy;\nCall Answer;\nReturn @_;\nDone.\n'
        'Call MakeClosure "Worker";\nHandle = @_;\n'
        'Call Spawn Handle, 0;\nTask = @_;\nCall Answer;\n'
        'Call Await Task;\nPrint @_.', initial_env={"_": 17},
    )
    assert output == '17\n'
    assert runtime.runtime_stats()["task_states"] == {"done": 1}


def test_source_seeded_result_is_captured_without_host_environment_injection():
    output, runtime = run_bounded(
        _ANSWER + 'Action Seed;\nReturn 17;\nDone.\n'
        'Action Worker Dummy;\nCall Answer;\nReturn @_;\nDone.\n'
        'Call Seed;\nCall MakeClosure "Worker";\nHandle = @_;\n'
        'Call Invoke Handle, 0;\nPrint @_.',
    )
    assert output == '17\n'
    assert runtime.env["Handle"].captured["_"] == 17


def test_unset_result_read_is_none_without_creating_a_binding():
    output, runtime = run_bounded('Print @_.')
    assert output == 'None\n'
    assert "_" not in runtime.env
