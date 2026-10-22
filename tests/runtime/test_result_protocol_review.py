"""Cross-path protocol regressions for result ownership and publication."""

import pytest

from compiler.interpreter import KuroRuntimeException
from compiler.pipeline import compile_source
from compiler.values import ClosureValue
from test_result_publication_contract import ANSWER, engine, prepare, run


@pytest.mark.parametrize("statement, expected", [
    ("_ = 23;", 23),
    ("Update _ to 23;", 23),
    ("Add 6 to _;", 23),
])
@pytest.mark.parametrize("invocation", ["Call Outer 17;", "Call Invoke Handle, 17;"])
def test_explicit_scalar_result_writes_target_current_owner(engine, statement, expected, invocation):
    runtime, output = run(
        "Action Outer _; " + statement + " Return @_; Done. "
        'Call MakeClosure "Outer"; Handle = @_; ' + invocation + " Print @_.",
        engine,
    )
    assert output == f"{expected}\n"
    assert runtime.env["_"] == expected


def test_input_to_result_register_targets_action_owner(engine):
    runtime, output = run(
        'Action Read; _ = "before"; Take _; Return @_; Done. Call Read; Print @_.' ,
        engine,
        input_fn=lambda _prompt: "captured input",
    )
    assert output == "captured input\n"
    assert runtime.env["_"] == "captured input"


def test_append_and_text_set_to_result_register_mutate_owner(engine):
    runtime, _output = run(
        'Action AppendResult _; Append 3 to _; Return @_; Done. '
        "Items = 1, 2; Call AppendResult Items; "
        'Action SetText _; Set _ 1 to "X"; Return @_; Done. '
        'Call SetText "abc";',
        engine,
    )
    # The second action's return replaces the main owner after AppendResult.
    assert runtime.env["_"] == "aXc"
    assert runtime.env["Items"] == [1, 2, 3]


def test_append_mutates_list_owned_by_result_slot(engine):
    runtime, _output = run(
        "Action AppendResult _; Append 3 to _; Return @_; Done. "
        "Items = 1, 2; Call AppendResult Items;",
        engine,
    )
    assert runtime.env["_"] == [1, 2, 3]
    assert runtime.env["Items"] == [1, 2, 3]


@pytest.mark.parametrize("initial", [{}, {"_": None}, {"_": 0}, {"_": 17}])
def test_makeclosure_preserves_presence_and_value_snapshot(engine, initial):
    runtime, _output = run(
        ANSWER + 'Action Read Dummy; Return @_; Done. Call MakeClosure "Read"; Handle = @_; '
        "Call Answer; Call Invoke Handle, 0;",
        engine,
        initial,
    )
    closure = runtime.env["Handle"]
    assert isinstance(closure, ClosureValue)
    assert ("_" in closure.captured) is ("_" in initial)
    if "_" in initial:
        assert closure.captured["_"] == initial["_"]
    # Read has no producer: its saved snapshot, not the later main 42, returns.
    assert runtime.env["_"] == (initial["_"] if "_" in initial else None)


def test_host_call_does_not_publish_return_or_nested_producer_to_main(engine):
    runtime, _output = prepare(
        ANSWER + "Action HostTarget; Call Answer; Return 9; Done.",
        engine,
        {"_": 17},
    )
    runtime.run()
    call = runtime.call if engine == "ir" else runtime._call
    assert call("HostTarget", []) == 9
    # Call Answer changed HostTarget's owner; neither its own producer nor the
    # host-returned value is published into the root owner.
    assert runtime.env["_"] == 17
    assert runtime.frames == []


def test_host_call_failure_discards_action_owner_and_preserves_global_effects(engine):
    runtime, _output = prepare(
        "Action HostTarget; Global = 9; Return 1 / 0; Done.",
        engine,
        {"_": 17},
    )
    runtime.run()
    call = runtime.call if engine == "ir" else runtime._call
    with pytest.raises(KuroRuntimeException):
        call("HostTarget", [])
    assert runtime.env["_"] == 17
    assert runtime.env["Global"] == 9
    assert runtime.frames == []


def test_ordinary_closure_capture_stays_shallow_while_result_snapshot_is_local(engine):
    runtime, output = run(
        ANSWER + "Items = 8, 9; "
        'Action Worker Dummy; Set Items 0 to 23; Call Answer; Return @_; Done. '
        'Call MakeClosure "Worker"; Handle = @_; Call Invoke Handle, 0; Print @_.',
        engine,
        {"_": 17},
    )
    handle = runtime.env["Handle"]
    assert isinstance(handle, ClosureValue)
    assert handle.captured["Items"] is runtime.env["Items"]
    assert runtime.env["Items"] == [23, 9]
    assert handle.captured["_"] == 17
    assert output == "42\n"


def test_successful_lowered_producer_still_has_distinct_publication_store():
    for statement, opcode in [("Call Answer;", "CALL"), ("Get Items 0;", "GET"), ("Length Word;", "LENGTH")]:
        compiled = compile_source(ANSWER + 'Items = 8, 9; Word = "ok"; ' + statement)
        assert compiled.ok, compiled.diags.render_all()
        producer, publication = compiled.ir.main[-2:]
        assert producer.op == opcode
        assert publication.op == "STORE_LIST"
        assert publication.args == ("_", (producer.dest,))
