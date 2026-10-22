"""Focused acceptance tests for result-owner boundaries in both Python engines."""

import pytest

from compiler.interpreter import KuroRuntimeException
from compiler.values import ClosureValue
from test_result_publication_contract import ANSWER, engine, prepare, run


@pytest.mark.parametrize("initial", [{}, {"_": None}, {"_": 0}, {"_": 17}])
def test_root_presence_is_preserved_by_closure_creation_and_frozen_for_invoke(engine, initial):
    runtime, output = run(
        ANSWER + 'Action Read Dummy; Return @_; Done. '
        'Call MakeClosure "Read"; Handle = @_; Call Answer; '
        "Call Invoke Handle, 0; Print @_.",
        engine,
        initial,
    )
    closure = runtime.env["Handle"]
    assert isinstance(closure, ClosureValue)
    assert ("_" in closure.captured) is ("_" in initial)
    if "_" in initial:
        assert closure.captured["_"] == initial["_"]
        assert output == f"{initial['_']}\n"
        assert runtime.env["_"] == initial["_"]
    else:
        assert output == "None\n"
        assert "_" in runtime.env and runtime.env["_"] is None


def test_direct_nested_entry_copies_callers_current_result_not_root_or_old_capture(engine):
    runtime, output = run(
        ANSWER + "Seen = 0; "
        "Action Read; Update Seen to @_; Return @_; Done. "
        "Action Worker Dummy; Call Answer; Call Read; Return @_; Done. "
        'Call MakeClosure "Worker"; Handle = @_; Call Invoke Handle, 0; Print @_.',
        engine,
        {"_": 17},
    )
    assert runtime.env["Seen"] == 42
    assert output == "42\n"
    assert runtime.env["_"] == 42


@pytest.mark.parametrize("statement, expected", [
    ("_ = 23;", 23),
    ("Update _ to 23;", 23),
    ("Add 6 to _;", 23),
])
def test_explicit_result_writes_replace_parameter_initializer(engine, statement, expected):
    runtime, output = run(
        "Action Write _; " + statement + " Return @_; Done. Call Write 17; Print @_.",
        engine,
    )
    assert output == f"{expected}\n"
    assert runtime.env["_"] == expected


def test_text_set_and_take_writes_are_owner_local(engine):
    runtime, output = run(
        'Action Change _; Set _ 1 to "X"; Return @_; Done. '
        'Action Read; _ = "old"; Take _; Return @_; Done. '
        'Call Change "abc"; Print @_. Call Read; Print @_.',
        engine,
        input_fn=lambda _prompt: "fresh",
    )
    assert output == "aXc\nfresh\n"
    assert runtime.env["_"] == "fresh"


@pytest.mark.parametrize("initial", [{}, {"_": None}, {"_": 0}, {"_": 17}])
def test_no_producer_closure_keeps_snapshot_on_repeated_and_deferred_invocations(engine, initial):
    runtime, output = run(
        ANSWER + "Action Read Dummy; Return @_; Done. "
        'Call MakeClosure "Read"; Handle = @_; Call Answer; '
        "Call Invoke Handle, 0; Print @_. Call Answer; "
        "Call Invoke Handle, 0; Print @_. Call Spawn Handle, 0; Task = @_; "
        "Call Answer; Call Await Task; Print @_.",
        engine,
        initial,
    )
    expected = initial.get("_")
    assert output == f"{expected}\n" * 3
    assert runtime.env["_"] == expected
    assert ("_" in runtime.env["Handle"].captured) == ("_" in initial)
    if "_" in initial:
        assert runtime.env["Handle"].captured["_"] == initial["_"]
    assert next(iter(runtime.scheduler.tasks.values())).state == "done"


def test_failed_source_call_does_not_publish_callee_result_but_keeps_global_effects(engine):
    runtime, _output = prepare(
        ANSWER + "Action Fail; Global = 9; Return 1 / 0; Done. "
        "Action Outer; Call Answer; Call Fail; Done. Call Outer;",
        engine,
        {"_": 17},
    )
    with pytest.raises(KuroRuntimeException):
        runtime.run()
    assert runtime.env["_"] == 17
    assert runtime.env["Global"] == 9
    assert runtime.frames == []


def test_host_return_value_is_not_a_root_publication(engine):
    runtime, _output = prepare(
        "Action Returner; Return 9; Done.", engine, {"_": 17}
    )
    runtime.run()
    host_call = runtime.call if engine == "ir" else runtime._call
    assert host_call("Returner", []) == 9
    assert runtime.env["_"] == 17
    assert runtime.frames == []


@pytest.mark.parametrize("older", [None, 0, 17])
def test_absent_owner_snapshot_never_resurrects_older_present_frames(engine, older):
    runtime, output = run(
        "Inner = 0; Seen = 0; Handle = 0; Value is Integers; "
        "Action Leaf Dummy; Return @_; Done. "
        "Action Worker Dummy; Update Seen to @_; "
        'Call MakeClosure "Leaf"; Update Inner to @_; Return 9; Done. '
        "Action Outer _; Call Invoke Handle, 0; Return 0; Done. "
        'Call MakeClosure "Worker"; Handle = @_; Call Outer Value; '
        "Call Invoke Inner, 0; Print @_.",
        engine, {"Value": older},
    )
    assert "_" not in runtime.env["Handle"].captured
    assert runtime.env["Seen"] is None
    assert "_" not in runtime.env["Inner"].captured
    assert output == "None\n"


def test_direct_reader_without_producer_inherits_parameter_owner_not_main(engine):
    runtime, output = run(
        "Action Read; Return @_; Done. "
        "Action Outer _; Call Read; Return @_; Done. Call Outer 17; Print @_.",
        engine, {"_": 42},
    )
    assert output == "17\n"
    assert runtime.env["_"] == 17


@pytest.mark.parametrize("statement, expected", [("Add 6 to _;", 6), ("Append 3 to _;", [3])])
def test_absent_owner_add_append_do_not_use_present_ambient_result(engine, statement, expected):
    runtime, _output = run(
        ANSWER + "_ is Integers; Action Worker Dummy; " + statement + " Return @_; Done. "
        'Call MakeClosure "Worker"; Handle = @_; Call Answer; Call Invoke Handle, 0;',
        engine,
    )
    assert "_" not in runtime.env["Handle"].captured
    assert runtime.env["_"] == expected


@pytest.mark.parametrize("initial", [{}, {"_": None}, {"_": 0}, {"_": 17}])
@pytest.mark.parametrize("failure", [False, True])
def test_host_nested_producers_preserve_root_presence_on_success_and_failure(engine, initial, failure):
    tail = "Global = 9; Return 1 / 0;" if failure else "Return 9;"
    runtime, _output = prepare(ANSWER + "Action Host; Call Answer; " + tail + " Done.", engine, initial)
    runtime.run()
    call = runtime.call if engine == "ir" else runtime._call
    if failure:
        with pytest.raises(KuroRuntimeException) as caught:
            call("Host", [])
        assert caught.value.code == "E6003"
        assert runtime.env["Global"] == 9
    else:
        assert call("Host", []) == 9
    assert ("_" in runtime.env) == ("_" in initial)
    if "_" in initial:
        assert runtime.env["_"] == initial["_"]
    assert runtime.frames == []
