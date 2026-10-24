"""Closed integer-offset contracts for the composed native compiler parser."""
from __future__ import annotations

from collections import Counter

from compiler.pipeline import compile_source
from compiler.self_host import native_compiler_source


def test_composed_native_compiler_types_closed_peek_offsets_as_integers():
    source = native_compiler_source()
    assert source.count("Action PeekKind Offset: Integers;") == 1
    assert source.count("Action PeekValue Offset: Integers;") == 1

    result = compile_source(source)
    assert result.ok, result.diags.render_all()
    assert result.ir.functions["PeekKind"].parameter_types == {"Offset": "Integers"}
    assert result.ir.functions["PeekValue"].parameter_types == {"Offset": "Integers"}

    bodies = [("", result.ir.main), *[
        (name, function.body) for name, function in result.ir.functions.items()
    ]]
    all_ops = {instruction.op for _, body in bodies for instruction in body}
    assert not all_ops.intersection({"MAKE_CLOSURE", "INVOKE", "SPAWN", "AWAIT"})

    expected_calls = {
        "PeekKind": Counter({
            ("CurKind", 0): 1,
            ("IsDeclAhead", 1): 1,
            ("ParseStatement", 1): 1,
        }),
        "PeekValue": Counter({
            ("CurValue", 0): 1,
            ("IsDeclAhead", 1): 1,
            ("IsDeclAhead", 2): 1,
        }),
    }
    actual_calls = {name: Counter() for name in expected_calls}
    for scope, body in bodies:
        for index, instruction in enumerate(body):
            if instruction.op != "CALL" or instruction.args[0] not in actual_calls:
                continue
            argument = body[index - 1]
            assert argument.dest == instruction.args[1]
            assert argument.op == "CONST"
            assert type(argument.args[0]) is int
            actual_calls[instruction.args[0]][(scope, argument.args[0])] += 1
    assert actual_calls == expected_calls

    write_ops = {
        "DECLTYPE", "STORE_LIST", "APPEND", "ADD", "UPDATE", "SET",
        "INPUT", "RESTOREVAR",
    }
    for name in expected_calls:
        body = result.ir.functions[name].body
        offset_loads = [
            instruction for instruction in body
            if instruction.op == "LOADVAR" and instruction.args[0] == "Offset"
        ]
        position_additions = [
            instruction for instruction in body
            if instruction.op == "BINOP" and instruction.args[0] == "+"
        ]
        assert len(offset_loads) == 1
        assert len(position_additions) == 1
        assert offset_loads[0].dest in position_additions[0].args[1:]
        assert not any(
            instruction.op in write_ops
            and instruction.args
            and instruction.args[0] == "Offset"
            for instruction in body
        )
