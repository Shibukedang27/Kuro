"""Exact production scheduling evidence is distinct from autonomous equivalence."""
from copy import deepcopy

import pytest
import compiler.native as native
from compiler.ir import IRFunction, IRProgram
from scripts.audit_normalized_closures import multibackedge_workload, recursive_return_workload, _outcome
from scripts.replay_closure_queue import audit, correspondence, replay, traced_emitter


def run(program, mode="production", **schedule):
    emitter, trace = traced_emitter(native, mode, **schedule)
    return _outcome(emitter, program, native), trace


@pytest.mark.parametrize("schedule", [{}, {"fifo": True}, {"reverse_successors": True}, {"fifo": True, "reverse_successors": True}])
def test_every_dense_queue_event_and_normalized_shadow_step_replays(schedule):
    outcome, trace = run(multibackedge_workload(2), **schedule)
    assert outcome["kind"] == "assembly"
    result = replay(trace, **schedule)
    assert result["valid"], result["errors"]
    assert result["counts"]["shadow_visits"] == len(trace.visits)
    assert result["counts"]["shadow_returns"] == len(result["all_return_steps"])
    assert result["representation_only_appends"]
    assert all(e["dense_after"] == e["shadow_after"] for e in result["all_return_steps"])


@pytest.mark.parametrize("schedule", [{}, {"fifo": True}, {"reverse_successors": True}, {"fifo": True, "reverse_successors": True}])
def test_autonomous_normalized_queue_is_independently_reconstructed(schedule):
    _, trace = run(multibackedge_workload(2), "normalized", **schedule)
    result = replay(trace, normalized=True, **schedule)
    assert result["valid"], result["errors"]
    assert not result["representation_only_appends"]


def test_recursive_summary_installation_and_changing_inputs_replay():
    _, trace = run(recursive_return_workload())
    result = replay(trace)
    assert result["valid"], result["errors"]
    a = [r for r in trace.invocations if r["function"] == "RecursiveA"]
    assert len({r["result"] for r in a}) > 1
    assert len({r["known_returns"] for r in a}) > 1


@pytest.mark.parametrize("mutation,expected", [
    ("queue", "successor-event"), ("dequeue", "dequeue"),
    ("state", "dense-incoming"), ("return", "returned-update"),
    ("install", "summary-installation"), ("input", "installed-summary-input"),
    ("remove-merge", "successor-event"), ("final-summary", "final-summary"),
    ("finish-function", "invocation-function"), ("bad-id", "unknown-invocation-id"),
    ("bad-index", "invalid-visit-index"), ("negative-index", "invalid-visit-index"),
    ("remove-final-round", "final-round-present"),
])
def test_replay_rejects_corrupted_or_omitted_events(mutation, expected):
    _, original = run(multibackedge_workload())
    trace = deepcopy(original)
    if mutation == "queue":
        next(e for k, e in trace.events if k == "queue" and e["event"] == "append")["queue"] = (999,)
    elif mutation == "dequeue":
        next(e for k, e in trace.events if k == "queue" and e["event"] == "pop")["queue"] = (999,)
    elif mutation == "state":
        next(e for k, e in trace.events if k == "visit")["incoming"] = (("fake", (("Fake",), True)),)
    elif mutation == "return":
        next(e for k, e in trace.events if k == "visit" and e["op"] == "RETURN")["return_state"] = (("Fake",), False, True)
    elif mutation == "install":
        next(e for k, e in trace.events if k == "round")["updated"] = ()
    elif mutation == "input":
        next(e for k, e in trace.events if k == "begin")["known_returns"] = (("Fake", ("Bad",)),)
    elif mutation == "remove-merge":
        offset = next(i for i, (k, _) in enumerate(trace.events) if k == "merge")
        trace.events.pop(offset)
    elif mutation == "final-summary":
        next(e for k, e in trace.events if k == "finish")["result"] = ((), False, True)
    elif mutation == "finish-function":
        next(e for k, e in trace.events if k == "finish")["function"] = "WrongFunction"
    elif mutation == "bad-id":
        next(e for k, e in trace.events if k == "begin")["id"] = 999
    elif mutation in {"bad-index", "negative-index"}:
        next(e for k, e in trace.events if k == "visit")["index"] = 999 if mutation == "bad-index" else -1
    elif mutation == "remove-final-round":
        trace.events.pop()
    result = replay(trace)
    assert not result["valid"]
    assert expected in {e["kind"] for e in result["errors"]}


def test_correspondence_keeps_unmatched_returns_after_first_divergence():
    p, production = run(multibackedge_workload())
    n, normalized = run(multibackedge_workload(), "normalized")
    assert p == n
    links = correspondence(production, normalized)
    assert links["first_control_divergence"] is not None
    assert links["all_unmatched_events"]
    assert links["counts"]["return_differences"] > 0
    assert any(e["status"] != "matched" for e in links["all_return_correspondences"])
    # Replay still checks the complete production stream, not just its prefix.
    result = replay(production)
    assert result["valid"]
    assert max(e["event"] for e in result["all_return_steps"]) > links["first_control_divergence"]["event"]


def test_empty_and_seedless_program_has_an_explicit_empty_round():
    outcome, trace = run(IRProgram(main=[], functions={"Empty": IRFunction("Empty", [], [])}))
    assert replay(trace)["valid"]
    assert trace.outer_transitions == [{"previous": (), "updated": ()}]


def test_bounded_adversarial_replay_corpus_reports_limits_honestly():
    result = audit()
    assert result["comparison_count"] == result["case_count"] * 4
    assert result["case_count"] > 22
    assert result["all_production_replays_valid"]
    assert result["all_autonomous_queue_replays_valid"]
    assert result["all_autonomous_transfers_valid"]
    # This bounded evidence is not permission to change production scheduling.
    assert not result["scheduling_equivalence_proven"]
    assert not result["production_promotion_allowed"]
    assert result["counts"]["cases_with_control_divergence"] > 0
    assert result["counts"]["return_sequence_differences"] > 0


def test_compact_evidence_preserves_counts_and_hashes_without_mutating_full_records():
    import hashlib
    import json
    from scripts.replay_closure_queue import compact
    _, production = run(multibackedge_workload())
    _, candidate = run(multibackedge_workload(), "normalized")
    links = correspondence(production, candidate)
    proof = replay(production)
    full = {"cases": [{"production_replay": proof,
                       "autonomous_queue_replay": replay(candidate, normalized=True),
                       "correspondence": links}]}
    summary = compact(full)
    actual = summary["cases"][0]["correspondence"]
    assert "all_return_correspondences" in links  # no mutation
    assert actual["all_return_correspondences_count"] == len(links["all_return_correspondences"])
    assert actual["all_return_correspondences_sha256"] == hashlib.sha256(
        json.dumps(links["all_return_correspondences"], sort_keys=True).encode()).hexdigest()
    assert actual["first_return_difference"] is not None
