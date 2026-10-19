"""Transition-level audit of a test-only normalized closure-fact representation.

The order-sensitive returned-target witness below is intentional: the analyzer's
returned set and all-known flag are sticky accumulators, so alternative worklist
orders can expose different triples even when emitter output is unchanged.
"""
from __future__ import annotations

import json

import compiler.native as native
from compiler.ir import IRFunction, IRProgram, Instr
from scripts.audit_normalized_closures import (
    AuditTrace,
    audit_program,
    compare_production_legacy,
    compare_traces,
    audit_corpus,
    make_emitter,
    multibackedge_workload,
    recursive_return_workload,
    validate_trace,
)
from scripts.profile_sparse_closures import (
    closure_edge_workloads,
    generated_graph_workload,
    negative_workload,
    sparse_workload,
)


def _i(op, *args, dest=None):
    return Instr(op, tuple(args), dest)


def _fn(name, *body):
    return IRFunction(name, [], list(body))


def _outcome(emitter, program):
    try:
        return {"kind": "assembly", "assembly": emitter(program)}
    except native.NativeBackendError as error:
        return {"kind": "native-error", "type": f"{type(error).__module__}.{type(error).__qualname__}", "text": str(error)}


def _run_trace(mode, program, **schedule):
    emitter, trace = make_emitter(native, mode=mode, trace=True, **schedule)
    outcome = _outcome(emitter, program)
    return outcome, trace


def test_normalized_plain_dict_clone_and_legacy_match_complete_emitter_outcomes():
    cases = {
        "small_seeded_cfg": sparse_workload(size=12, random_cases=1, seed=8821),
        "known_generated": generated_graph_workload(0, "known"),
        "missing_generated": generated_graph_workload(1, "missing"),
        "mixed_return_error": negative_workload(),
        "multi_backedge_0": multibackedge_workload(0),
        "multi_backedge_1": multibackedge_workload(1),
    }
    cases.update(closure_edge_workloads())
    prod, _ = make_emitter(native, mode="production")
    legacy, _ = make_emitter(native, mode="legacy")
    normalized, _ = make_emitter(native, mode="normalized")
    for label, program in cases.items():
        expected = _outcome(prod, program)
        assert expected == _outcome(legacy, program), f"legacy complete result mismatch: {label}"
        assert expected == _outcome(normalized, program), f"normalized complete result mismatch: {label}"
        assert expected["kind"] == "assembly" and expected["assembly"] or expected["kind"] == "native-error"
        if expected["kind"] == "native-error":
            assert expected["type"] == f"{native.NativeBackendError.__module__}.{native.NativeBackendError.__qualname__}"
            assert expected["text"] == "x86_64-linux Invoke requires closures with statically known targets"


def test_trace_records_exact_calls_transitions_and_shared_legacy_invariants():
    program = sparse_workload(size=10, random_cases=1, seed=127)
    production_outcome, production = _run_trace("production", program)
    legacy_outcome, legacy = _run_trace("legacy", program)
    candidate_outcome, candidate = _run_trace("normalized", program)
    assert production_outcome == legacy_outcome == candidate_outcome
    legacy_check = compare_production_legacy(production, legacy)
    assert legacy_check["shared_summaries_equal"], json.dumps(legacy_check, default=str)
    assert legacy_check["extras_cannot_install"]
    assert legacy_check["legacy_extra_invocations"], "legacy reference should exercise seedless analyzer calls"
    assert all(not extra["can_install_summary"] for extra in legacy_check["legacy_extra_invocations"])

    # Recursive functions are reanalyzed with changing known_returns inputs.
    for function in ("RecursiveA", "RecursiveB"):
        inputs = {record["known_returns"] for record in production.invocations if record["function"] == function}
        assert len(inputs) > 1, f"{function} did not exercise changing recursive summary inputs"
    assert production.outer_transitions, "outer updated_returns transitions must be traced"
    assert production.visits and production.merges and production.queues
    assert any(event["event"] == "pop" for event in production.queues)
    assert any(event["event"] == "append" for event in production.queues)
    assert compare_traces(production, candidate)["equivalent_invocation_summaries"]


def test_missing_name_joins_and_multibackedge_cfgs_are_reachable_and_traced():
    for seed in range(3):
        program = multibackedge_workload(seed)
        _, trace = _run_trace("production", program)
        records = [rec for rec in trace.invocations if rec["function"] == f"MultiBackedge{seed}"]
        assert records and records[0]["result"] == (("GraphTargetA", "GraphTargetB"), True, True)
        visits = [visit for visit in trace.visits if visit["invocation"] == records[0]["id"]]
        assert len(visits) >= 20
        missing_index = next(i for i, visit in enumerate(visits) if visit["op"] == "LOADVAR" and visit["outgoing"] and any(name == f"unknown_{seed}" for name, _ in visit["outgoing"]))
        assert visits[missing_index]["outgoing"]


def test_deterministic_sticky_return_accumulator_counterexample_is_preserved():
    """Reversing successor order changes returned targets despite all_known=False."""
    program = generated_graph_workload(1, "missing")
    normal_outcome, normal = _run_trace("production", program)
    reverse_outcome, reverse = _run_trace("production", program, reverse_successors=True)
    assert normal_outcome == reverse_outcome
    comparison = compare_traces(normal, reverse)
    assert comparison["summary_differences"], "expected the known sticky-accumulator scheduling counterexample"
    witness = next(item for item in comparison["summary_differences"] if item["key"][0] == "GeneratedGraph")
    assert witness["key"] == ("GeneratedGraph", ()) and witness["ordinal"] == 0
    assert witness["production"] == ((), False, True)
    assert witness["candidate"] == (("GraphTargetA",), False, True)
    assert comparison["first_queue_difference"] is not None
    # A normalized map does not itself fix this: schedule order remains observable.
    normalized_reverse_outcome, normalized_reverse = _run_trace("normalized", program, reverse_successors=True)
    assert normalized_reverse_outcome == normal_outcome
    normalized_compare = compare_traces(normal, normalized_reverse)
    normalized_witness = next(item for item in normalized_compare["summary_differences"] if item["key"][0] == "GeneratedGraph")
    assert normalized_witness["production"] == ((), False, True)
    assert normalized_witness["candidate"] == (("GraphTargetA",), False, True)


def test_fifo_lifo_and_successor_orders_are_audited_without_claiming_order_invariance():
    program = multibackedge_workload(2)
    traces = {}
    for label, schedule in {
        "lifo": {},
        "fifo": {"fifo": True},
        "reverse_successors": {"reverse_successors": True},
        "fifo_reverse": {"fifo": True, "reverse_successors": True},
    }.items():
        for mode in ("production", "legacy", "normalized"):
            outcome, trace = _run_trace(mode, program, **schedule)
            assert outcome["kind"] == "assembly"
            traces[(label, mode)] = trace
    for label in ("lifo", "fifo", "reverse_successors", "fifo_reverse"):
        reference = traces[(label, "production")]
        assert compare_production_legacy(reference, traces[(label, "legacy")])["shared_full_trace_equal"]
        normalized = compare_traces(reference, traces[(label, "normalized")])
        assert normalized["production_validation"]["valid"] and normalized["candidate_validation"]["valid"]
        assert normalized["independent_schedule_differences_reported"]


def test_recursive_summaries_change_through_returned_call_results():
    _, trace = _run_trace("production", recursive_return_workload())
    a = [record for record in trace.invocations if record["function"] == "RecursiveA"]
    b = [record for record in trace.invocations if record["function"] == "RecursiveB"]
    assert len({record["known_returns"] for record in a}) > 1
    assert len({record["known_returns"] for record in b}) > 1
    assert ((), False, True) in {record["result"] for record in a}
    assert (("RecursiveSeedTarget",), True, True) in {record["result"] for record in a}
    assert any(record["result"] and record["result"][0] == ("RecursiveSeedTarget",) for record in a + b)


def test_bounded_corpus_all_modes_all_orders_strict_traces_and_transition_checks():
    report = audit_corpus(native)
    assert report["case_count"] >= 12 and report["order_count"] == 4
    assert report["comparison_count"] == report["case_count"] * 4
    assert report["all_outcomes_equal"], json.dumps(report, default=str)
    assert report["all_shared_legacy_traces_equal"], json.dumps(report, default=str)
    assert report["all_outer_transitions_equal"], json.dumps(report, default=str)
    assert report["all_exact_invocation_summaries_equal"], json.dumps(report, default=str)
    assert report["all_trace_validations_pass"], json.dumps(report, default=str)
    assert all(item["production_vs_normalized"]["return_summary_event_sequence_difference_count"] == len(item["production_vs_normalized"]["return_summary_event_sequence_differences"]) for item in report["cases"])
    assert report["aggregate_counts"]["production_representation_only_updates"] >= 0
    assert all(item["production_vs_normalized"]["production_validation"]["visits_checked"] > 0 for item in report["cases"])


def test_independent_validator_rejects_transfer_merge_and_return_corruption():
    from copy import deepcopy
    _, trace = _run_trace("production", multibackedge_workload())
    assert validate_trace(trace)["valid"]
    corrupted = deepcopy(trace)
    corrupted.visits[0]["outgoing"] = (("fake", (("FakeTarget",), True)),)
    corrupted.visits[0]["return_state"] = (("FakeTarget",), True, True)
    corrupted.merges[0]["merged"] = (("fake", (("FakeTarget",), True)),)
    result = validate_trace(corrupted)
    assert not result["valid"]
    assert {error["kind"] for error in result["errors"]} >= {"transfer", "merge", "return-summary"}


def test_trace_comparator_detects_a_changed_returned_set_even_when_all_known_is_false():
    base = AuditTrace()
    changed = AuditTrace()
    base.invocations.append({"id": 0, "function": "F", "known_returns": (), "result": ((), False, True)})
    changed.invocations.append({"id": 0, "function": "F", "known_returns": (), "result": (("Target",), False, True)})
    comparison = compare_traces(base, changed)
    assert not comparison["equivalent_invocation_summaries"]
    witness = comparison["summary_differences"][0]
    assert witness["key"] == ("F", ()) and witness["ordinal"] == 0
    assert witness["production"] == ((), False, True)
    assert witness["candidate"] == (("Target",), False, True)


def test_public_audit_api_returns_json_ready_complete_outcomes_and_traces():
    report = audit_program(multibackedge_workload(4), native)
    serialized = json.dumps(report)
    assert '"production_vs_legacy"' in serialized
    assert '"outer_transitions"' in serialized
    assert report["outcomes"]["production"] == report["outcomes"]["legacy"] == report["outcomes"]["normalized"]
    assert report["production_vs_legacy"]["shared_summaries_equal"]
