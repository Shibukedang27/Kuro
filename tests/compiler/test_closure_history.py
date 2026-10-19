"""History-aware closure scheduling diagnostics fail closed and avoid equivalence claims."""
from copy import deepcopy

import compiler.native as native
from scripts.audit_normalized_closures import _outcome, multibackedge_workload
from scripts.replay_closure_queue import traced_emitter
from scripts.simulate_closure_history import (
    pair_histories, simulate, validate_invocations,
)


def traces(program, mode="production", **schedule):
    emitter, trace = traced_emitter(native, mode, **schedule)
    _outcome(emitter, program, native)
    return trace


def test_independent_history_scheduler_reconstructs_both_complete_traces():
    program = multibackedge_workload(2)
    dense = traces(program)
    normalized = traces(program, "normalized")
    dense_result = validate_invocations(dense, program)
    norm_result = validate_invocations(normalized, program, normalized=True)
    assert dense_result["valid"], dense_result["failures"]
    assert norm_result["valid"], norm_result["failures"]
    paired = pair_histories(program, dense, normalized,
                            dense_result["simulations"], norm_result["simulations"])
    assert paired["return_sequence_difference_count"] > 0
    assert paired["matching_policy"].endswith("not equivalence")
    assert any(record["representation_suppression_witnesses"]
               for item in paired["differing_pairs"]
               for side in ("dense_returns", "normalized_returns")
               for record in item[side])


def test_corruption_control_rejects_an_omitted_successor_append():
    program = multibackedge_workload()
    trace = traces(program)
    result = validate_invocations(trace, program, corrupt="drop-append")
    assert not result["valid"]
    assert any(error["kind"] == "event-stream" for error in result["failures"])


def test_constructor_facts_are_reconstructed_from_ir_body():
    program = multibackedge_workload()
    function = next(iter(program.functions.values()))
    facts = simulate(function, {}, set(program.functions))
    expected = {}
    text = {}
    for index, ins in enumerate(function.body):
        if ins.op == "CONST" and ins.dest and isinstance(ins.args[0], str):
            text[ins.dest] = ins.args[0]
        elif ins.op == "CALL" and ins.args[0] == "MakeClosure" and len(ins.args) == 2:
            if text.get(ins.args[1]) in program.functions:
                expected[index] = text[ins.args[1]]
            if ins.dest:
                text.pop(ins.dest, None)
        elif ins.dest:
            text.pop(ins.dest, None)
    assert facts["constructor_facts"] == expected


def test_independent_history_rejects_mutated_states_queues_accumulators_and_summaries():
    program = multibackedge_workload()
    original = traces(program)
    for field, replacement in (
        ("incoming", (("forged", (("TargetX",), True)),)),
        ("queue", (-1,)),
        ("return_state", (("ForgedTarget",), True, True)),
        ("constructor_target", "ForgedTarget"),
    ):
        trace = deepcopy(original)
        event = next(event for kind, event in trace.events if kind == "visit")
        event[field] = replacement
        assert not validate_invocations(trace, program)["valid"], field
    trace = deepcopy(original)
    trace.invocations[0]["result"] = (("ForgedTarget",), True, True)
    assert not validate_invocations(trace, program)["valid"]
