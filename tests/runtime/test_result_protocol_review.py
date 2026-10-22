"""Unselected result-owner decisions, exercised on unchanged Python engines.

These are current-behavior witnesses, not acceptance tests for the proposed
protocol. Keep explicit result writes distinct from lowered producer stores.
"""

import pytest

from compiler.pipeline import compile_source
from compiler.values import ClosureValue
from test_result_publication_contract import ANSWER, engine, prepare, run


@pytest.mark.parametrize("statement, written", [
    ("_ = 23;", 23),
    ("Update _ to 23;", 23),
    ("Add 6 to _;", 23),
])
@pytest.mark.parametrize("invocation", ["Call Outer 17;", "Call Invoke Handle, 17;"])
def test_explicit_result_writes_keep_parameter_read_overlay(engine, statement, written, invocation):
    runtime, output = run(
        "Observed = 0; "
        "Action Observe; Update Observed to @_; Return 0; Done. "
        "Action Outer _; " + statement + " Call Observe; Print @_. Return @_; Done. "
        'Call MakeClosure "Outer"; Handle = @_; ' + invocation + " Print @_.",
        engine,
    )
    # Assignment, Update and Add target env, even though reads still see the
    # parameter. Add reads the parameter 17, not the closure-handle global.
    assert runtime.env["Observed"] == written
    assert output == "17\n17\n"
    assert runtime.env["_"] == 17


@pytest.mark.parametrize("older", [None, 0, 17])
def test_absent_top_capture_can_snapshot_older_frame_result_not_effective_read(engine, older):
    runtime, output = run(
        ANSWER + "Inner = 0; Seen = 0; Handle = 0; Value is Integers; "
        "Action Leaf Dummy; Return @_; Done. "
        "Action Worker Dummy; Call Answer; Update Seen to @_; "
        'Call MakeClosure "Leaf"; Update Inner to @_; Return 9; Done. '
        "Action Outer _; Call Invoke Handle, 0; Return 0; Done. "
        # The first snapshot has no result binding at all. The later Outer
        # parameter is invisible to Worker's ordinary top-frame-only lookup,
        # but is visible to MakeClosure's all-frame merge.
        'Call MakeClosure "Worker"; Handle = @_; Call Outer Value; '
        "Call Invoke Inner, 0; Print @_.",
        engine, {"Value": older},
    )
    assert "_" not in runtime.env["Handle"].captured
    assert runtime.env["Seen"] == 42
    assert runtime.env["Inner"].captured["_"] == older
    assert output == f"{older}\n"


@pytest.mark.parametrize("initial", [{}, {"_": 17}])
@pytest.mark.parametrize("body, returned, global_result", [
    ("Return @_;", None, "absent"),
    ("Call Answer; Return 9;", 9, 42),
    ("Call Answer;", None, 42),
])
def test_host_call_entry_and_nested_source_publication_are_separate(engine, initial, body, returned, global_result):
    runtime, _output = prepare(ANSWER + "Action Pick; " + body + " Done.", engine, initial)
    runtime.run()
    assert ("_" in runtime.env) == ("_" in initial)
    call = runtime.call if engine == "ir" else runtime._call
    if global_result == "absent":
        assert call("Pick", []) == initial.get("_")
        assert ("_" in runtime.env) == ("_" in initial)
        if "_" in initial:
            assert runtime.env["_"] == initial["_"]
    else:
        assert call("Pick", []) == returned
        # The host API does not publish Pick's return value, but the source
        # producer in Pick has already changed the shared global result.
        assert runtime.env["_"] == global_result
    assert runtime.frames == []
    assert not any(name.endswith("$") for name in runtime.env)


def test_result_snapshot_remains_shallow_for_ordinary_collection_alias(engine):
    runtime, output = run(
        ANSWER + "Items = 8, 9; "
        "Action Worker Dummy; Set Items 0 to 23; Call Answer; Return @_; Done. "
        'Call MakeClosure "Worker"; Handle = @_; Call Invoke Handle, 0; Print @_.',
        engine, {"_": 17},
    )
    handle = runtime.env["Handle"]
    assert isinstance(handle, ClosureValue)
    assert handle.captured["Items"] is runtime.env["Items"]
    assert runtime.env["Items"] == [23, 9]
    assert handle.captured["_"] == 17
    assert output == "17\n"


def test_direct_reader_without_prior_producer_uses_global_not_callers_capture(engine):
    runtime, output = run(
        ANSWER + "Seen = 0; "
        "Action Read; Update Seen to @_; Return @_; Done. "
        "Action Worker Dummy; Call Read; Return @_; Done. "
        'Call MakeClosure "Worker"; Handle = @_; Call Answer; '
        "Call Invoke Handle, 0; Print @_.",
        engine, {"_": 17},
    )
    assert runtime.env["Seen"] == 42
    assert output == "17\n"


@pytest.mark.parametrize("initial, expected", [
    ({}, 42), ({"_": None}, None), ({"_": 0}, 0), ({"_": 17}, 17),
])
def test_repeated_and_deferred_calls_reuse_result_snapshot_in_both_engines(engine, initial, expected):
    runtime, output = run(
        ANSWER + "Action Worker Dummy; Call Answer; Return @_; Done. "
        'Call MakeClosure "Worker"; Handle = @_; '
        "Call Invoke Handle, 0; Print @_. Call Answer; "
        "Call Invoke Handle, 0; Print @_. "
        "Call Spawn Handle, 0; Task = @_; Call Answer; Call Await Task; Print @_.",
        engine, initial,
    )
    assert output == f"{expected}\n" * 3
    assert ("_" in runtime.env["Handle"].captured) == ("_" in initial)
    if "_" in initial:
        assert runtime.env["Handle"].captured["_"] == initial["_"]
    assert next(iter(runtime.scheduler.tasks.values())).state == "done"


def test_explicit_assignment_and_producer_share_result_store_opcode():
    stores = []
    for statement in ("_ = 23;", "Call Answer;"):
        compiled = compile_source(ANSWER + statement)
        assert compiled.ok, compiled.diags.render_all()
        store = compiled.ir.main[-1]
        assert store.op == "STORE_LIST"
        assert store.args[0] == "_"
        assert len(store.args[1]) == 1
        stores.append(store)
    # A rule keyed only on this opcode/destination changes explicit writes as
    # well as producer publication. The operand temporaries are not policy tags.
    assert stores[0].op == stores[1].op
