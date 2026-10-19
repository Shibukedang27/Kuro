"""Compact schedule witnesses and bounded adversarial closure-queue fixtures."""
from __future__ import annotations

import compiler.native as native
from scripts.audit_normalized_closures import make_emitter, validate_trace
from scripts.closure_queue_cases import (
    bounded_adversarial_cases,
    layout_swapped_predecessor_program,
    minimal_sticky_return_program,
    traced_outcome,
)


def _first_function_record(trace, name):
    return next(record for record in trace.invocations if record["function"] == name)


def _return_states(trace, invocation):
    return [
        visit["return_state"]
        for visit in trace.visits
        if visit["invocation"] == invocation and visit["op"] == "RETURN"
    ]


def test_compact_production_vs_reversed_successors_exposes_sticky_return_accumulator():
    program = minimal_sticky_return_program()
    body = program.functions["QueueWitness"].body
    assert len(body) == 9  # Compact concrete witness; no global minimality claim.

    normal_outcome, normal = traced_outcome(program)
    reverse_outcome, reverse = traced_outcome(program, reverse_successors=True)
    assert normal_outcome == reverse_outcome

    normal_record = _first_function_record(normal, "QueueWitness")
    reverse_record = _first_function_record(reverse, "QueueWitness")
    # Production LIFO visits the unknown predecessor first. Reversing the
    # JUMPF successors reaches the known closure first, then revisits RETURN
    # after the unknown join. The target union is sticky, all_known is not.
    assert normal_record["result"] == ((), False, True)
    assert reverse_record["result"] == (("QueueTarget",), False, True)
    assert _return_states(normal, normal_record["id"]) == [
        ((), False, True), ((), False, True),
    ]
    assert _return_states(reverse, reverse_record["id"]) == [
        (("QueueTarget",), True, True),
        (("QueueTarget",), False, True),
    ]
    assert validate_trace(normal)["valid"] and validate_trace(reverse)["valid"]


def test_physical_layout_swaps_predecessor_arrival_without_schedule_perturbation():
    program = layout_swapped_predecessor_program()
    outcome, trace = traced_outcome(program)
    record = _first_function_record(trace, "LayoutWitness")

    # With unknown on fallthrough and known on the label edge, production's
    # LIFO successor processing arrives at the known predecessor first.
    assert outcome["kind"] == "assembly"
    assert record["result"] == (("QueueTarget",), False, True)
    assert _return_states(trace, record["id"]) == [
        (("QueueTarget",), True, True),
        (("QueueTarget",), False, True),
    ]
    assert validate_trace(trace)["valid"]


def test_bounded_adversarial_backedge_missing_join_and_return_fixtures():
    cases = bounded_adversarial_cases()
    assert set(cases) == {
        "multiple_backedges_and_missing_name_join",
        "generated_missing_name_return_join",
        "missing_target_return_path",
        "loop_zero_path_return",
        "unreachable_return_path",
    }

    for name, program in cases.items():
        for reverse in (False, True):
            results = {}
            traces = {}
            for mode in ("production", "legacy", "normalized"):
                results[mode], traces[mode] = traced_outcome(
                    program, mode=mode, reverse_successors=reverse, native=native,
                )
            assert results["production"] == results["legacy"] == results["normalized"], name
            for trace in traces.values():
                assert validate_trace(trace)["valid"], name

    # The reused multibackedge builder combines three backedges, a one-sided
    # definition/missing-name join, and a reachable closure return.
    _, trace = traced_outcome(cases["multiple_backedges_and_missing_name_join"])
    record = _first_function_record(trace, "MultiBackedge0")
    assert record["result"] == (("GraphTargetA", "GraphTargetB"), True, True)
    visits = [visit for visit in trace.visits if visit["invocation"] == record["id"]]
    assert sum(visit["op"] == "JUMP" for visit in visits) >= 3
    assert any(
        visit["op"] == "LOADVAR"
        and any(name == "unknown_0" and not fact[1] for name, fact in visit["outgoing"])
        for visit in visits
    )
