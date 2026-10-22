"""Current result entry/publication behavior, not a scoped-result implementation.

No Repeat or Index cases: the JSON VM does not admit Repeat save/restore.
The two engines are checked against explicit expectations, not just each other.
"""

import io
import json

import pytest

from compiler.bytecode import BytecodeProgram, BytecodeVM, encode_ir
from compiler.interpreter import Interpreter, KuroRuntimeException
from compiler.pipeline import compile_source


class _BudgetedInstructions(tuple):
    def __new__(cls, instructions, tick):
        result = super().__new__(cls, instructions)
        result.tick = tick
        return result

    def __getitem__(self, index):
        self.tick()
        return super().__getitem__(index)


class _BudgetedVM(BytecodeVM):
    def _execute(self, instructions):
        # VM instruction dispatch fetches instructions[pc]; share one budget
        # across all calls. Label enumeration is finite and does not dispatch.
        return super()._execute(_BudgetedInstructions(instructions, self.tick))


@pytest.fixture(params=["ir", "json-vm"])
def engine(request):
    return request.param


def prepare(source, engine, initial=None):
    compiled = compile_source(source)
    assert compiled.ok, compiled.diags.render_all()
    steps = 0

    def tick(*_args):
        nonlocal steps
        steps += 1
        assert steps <= 10_000, "result publication instruction budget exhausted"

    output = io.StringIO()
    if engine == "ir":
        runtime = Interpreter(compiled.ir, output=output, trace=tick)
    else:
        # Exercise the serialized representation, not only encode_ir objects.
        program = BytecodeProgram.from_data(json.loads(json.dumps(encode_ir(compiled.ir).to_data())))
        runtime = _BudgetedVM(program, output=output)
        runtime.tick = tick
    runtime.env.update(initial or {})
    return runtime, output


def run(source, engine, initial=None):
    runtime, output = prepare(source, engine, initial)
    runtime.run()
    assert runtime.frames == []
    assert not any(name.endswith("$") for name in runtime.env)
    return runtime, output.getvalue()


ANSWER = "Action Answer; Return 42; Done.\n"
SEED = "Action Seed; Return 17; Done.\n"


@pytest.mark.parametrize("initial, expected", [
    ({}, None), ({"_": None}, None), ({"_": 0}, 0), ({"_": 17}, 17),
])
def test_direct_entry_reads_live_global_without_initializing_a_slot(engine, initial, expected):
    runtime, output = run(
        "Action Read; Print @_. Return @_; Done. Call Read; Print @_.",
        engine, initial,
    )
    assert output == f"{expected}\n{expected}\n"
    # Even when the entry read was absent, the caller's store publishes None.
    assert "_" in runtime.env
    assert runtime.env["_"] == expected


@pytest.mark.parametrize("initial, expected", [
    ({}, 42), ({"_": None}, None), ({"_": 0}, 0), ({"_": 17}, 17),
])
def test_invoke_entry_uses_capture_presence_not_callers_live_result(engine, initial, expected):
    runtime, output = run(
        ANSWER + "Action Read Dummy; Return @_; Done.\n"
        'Call MakeClosure "Read"; Handle = @_; Call Answer; '
        "Call Invoke Handle, 0; Print @_.",
        engine, initial,
    )
    assert output == f"{expected}\n"
    assert ("_" in runtime.env["Handle"].captured) == ("_" in initial)
    assert runtime.env["_"] == expected


@pytest.mark.parametrize("invocation", ["Call Outer 17;", "Call Invoke Handle, 17;"])
def test_parameter_named_result_hides_successful_caller_publication(engine, invocation):
    runtime, output = run(
        ANSWER + "Action Outer _; Call Answer; Print @_. Return @_; Done.\n"
        'Call MakeClosure "Outer"; Handle = @_; ' + invocation + " Print @_.",
        engine,
    )
    assert output == "17\n17\n"
    assert runtime.env["_"] == 17


def test_nested_direct_entry_does_not_inherit_effective_caller_result(engine):
    runtime, output = run(
        ANSWER + "Observed = 0;\n"
        "Action Read; Update Observed to @_; Return @_; Done.\n"
        "Action Outer _; Call Answer; Call Read; Print @_. Return @_; Done.\n"
        "Call Outer 17; Print @_.",
        engine,
    )
    assert runtime.env["Observed"] == 42
    assert output == "17\n17\n"


@pytest.mark.parametrize("tail, expected", [("", None), ("Return @_;", 42), ("Return 9;", 9)])
def test_implicit_return_publishes_none_not_callees_last_result(engine, tail, expected):
    runtime, output = run(
        ANSWER + "Action Outer; Call Answer; " + tail + " Done.\n"
        "Call Outer; Print @_.",
        engine,
    )
    assert output == f"{expected}\n"
    assert runtime.env["_"] == expected


@pytest.mark.parametrize("failure, code", [
    ("Get Items 9;", "E6001"),
    ("Length Value;", "E3005"),
    ("Call Fail;", "E6003"),
])
def test_failed_producer_skips_publication_but_does_not_rollback_inner_success(engine, failure, code):
    runtime, output = prepare(
        ANSWER + "Items = 8, 9;\n"
        "Action Fail; Return 1 / 0; Done.\n"
        "Action Outer Value; Call Answer; " + failure + " Print 999. Done.\n"
        "Call Outer 5; Print 998.", engine, {"_": 17},
    )
    with pytest.raises(KuroRuntimeException) as caught:
        runtime.run()
    assert caught.value.code == code
    assert output.getvalue() == ""
    assert runtime.frames == []
    # Outer never completes, but its successful nested Call already wrote 42.
    assert runtime.env["_"] == 42
    assert not any(name.endswith("$") for name in runtime.env)


@pytest.mark.parametrize("body, expected", [("Return 42;", 42), ("", None)])
def test_host_call_returns_value_without_source_level_publication(engine, body, expected):
    runtime, _output = prepare("Action Pick; " + body + " Done.", engine, {"_": 17})
    runtime.run()
    call = runtime.call if engine == "ir" else runtime._call
    assert call("Pick", []) == expected
    assert runtime.env["_"] == 17
    assert runtime.frames == []


def test_source_seeded_captured_caller_rejects_nested_return_publication(engine):
    runtime, output = run(
        SEED + ANSWER + "Action Outer Dummy; Call Answer; Return @_; Done.\n"
        'Call Seed; Call MakeClosure "Outer"; Handle = @_; '
        "Call Invoke Handle, 0; Print @_.", engine,
    )
    assert output == "17\n"
    assert runtime.env["Handle"].captured["_"] == 17


@pytest.mark.parametrize("statement, opcode", [
    ("Call Answer;", "CALL"), ("Get Items 0;", "GET"), ("Length Word;", "LENGTH"),
])
def test_lowering_separates_successful_producer_from_result_publication(statement, opcode):
    compiled = compile_source(ANSWER + 'Items = 8, 9; Word = "ok"; ' + statement)
    assert compiled.ok, compiled.diags.render_all()
    producer, publication = compiled.ir.main[-2:]
    assert producer.op == opcode
    assert publication.op == "STORE_LIST"
    assert publication.args == ("_", (producer.dest,))
