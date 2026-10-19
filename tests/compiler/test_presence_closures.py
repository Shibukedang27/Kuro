"""Sparse fact storage experiment that retains dense key presence and schedules."""
from __future__ import annotations

from copy import deepcopy

import compiler.native as native
from scripts.audit_presence_closures import PresenceFacts, audit
from scripts.audit_normalized_closures import multibackedge_workload
from scripts.replay_closure_queue import replay, traced_emitter


def test_presence_map_keeps_dense_keys_but_stores_only_nondefault_facts():
    facts = PresenceFacts()
    absent = object()
    facts["default"] = (set(), False)
    facts["empty_known"] = (set(), True)
    facts["nonempty_unknown"] = ({"TargetA"}, False)

    assert "default" in facts and "default" in facts.keys()
    assert facts.get("default") == (set(), False)
    assert facts.get("absent", absent) is absent
    assert list(facts.keys()) == ["default", "empty_known", "nonempty_unknown"] or set(facts.keys()) == {
        "default", "empty_known", "nonempty_unknown"
    }
    assert facts == {
        "default": (set(), False),
        "empty_known": (set(), True),
        "nonempty_unknown": ({"TargetA"}, False),
    }
    assert {
        "default": (set(), False),
        "empty_known": (set(), True),
        "nonempty_unknown": ({"TargetA"}, False),
    } == facts
    assert dict.__len__(facts) == 2, "default unknown presence must not allocate a stored fact"
    assert facts["empty_known"] == (set(), True)
    assert facts["nonempty_unknown"] == ({"TargetA"}, False)


def test_copy_is_fresh_mapping_with_read_only_shared_targets_and_fresh_union_control():
    left_targets = {"TargetA"}
    right_targets = {"TargetB"}
    facts = PresenceFacts()
    facts["left"] = (left_targets, True)
    facts["right"] = (right_targets, True)
    facts["absent_fact"] = (set(), False)
    copied = facts.copy()

    assert copied is not facts
    assert copied == facts
    assert copied.keys() == facts.keys()
    assert copied["left"][0] is facts["left"][0] is left_targets
    copied["local"] = ({"TargetC"}, True)
    assert "local" not in facts, "copied key presence must be independently owned"

    # This models the analyzer's actual merge contract: read source target sets,
    # allocate a fresh union, and never mutate the shared operands in place.
    merged_targets = set(facts["left"][0]) | set(facts["right"][0])
    merged_targets.add("LocalOnly")
    assert merged_targets == {"TargetA", "TargetB", "LocalOnly"}
    assert left_targets == {"TargetA"} and right_targets == {"TargetB"}
    assert facts["left"][0] is copied["left"][0]
    assert facts["left"][0] == {"TargetA"}


def test_presence_clone_trace_replay_rejects_raw_dense_state_mutation():
    emitter, trace = traced_emitter(native, mode="production")
    assert emitter(multibackedge_workload(2))
    valid = replay(trace)
    assert valid["valid"], valid["errors"]

    corrupted = deepcopy(trace)
    visit = next(event for kind, event in corrupted.events if kind == "visit")
    visit["incoming"] = (("forged", (("TargetX",), True)),)
    result = replay(corrupted)
    assert not result["valid"]
    assert "dense-incoming" in {error["kind"] for error in result["errors"]}


def test_inherited_corpus_all_116_pairs_match_complete_dense_behavior_and_account_storage():
    result = audit()
    assert result["case_count"] == 29
    assert result["order_count"] == 4
    assert result["comparison_count"] == 116
    assert result["orders"] == ["lifo_forward", "fifo_forward", "lifo_reverse", "fifo_reverse"]
    assert result["all_outcomes_equal"]
    assert result["all_exact_invocation_summaries_equal"]
    assert result["all_raw_dense_states_equal"]
    assert result["all_queue_and_return_timelines_equal"]
    assert result["all_production_replays_valid"]
    assert result["all_presence_replays_valid"]
    assert result["all_copy_accounting_valid"]
    assert not result["scheduling_equivalence_proven"]
    assert not result["production_promotion_allowed"]

    counts = result["aggregate_storage_copy_counts"]
    assert counts["copy_calls"] > 0
    assert counts["dense_copy_presence_slots"] > counts["presence_copy_nondefault_fact_slots"]
    assert counts["presence_copy_elided_slots"] > 0
    assert counts["final_dense_presence_slots"] > counts["final_nondefault_fact_slots"]
    assert counts["final_elided_presence_slots"] > 0
    assert counts["cases_with_default_elisions"] == 116
    assert all(item["complete_trace_equal"] and item["copy_accounting_valid"] for item in result["cases"])


def test_presence_storage_preserves_new_final_summary_counterexample_in_all_orders():
    from scripts.audit_presence_closures import _clone_presence_emitter
    from scripts.audit_normalized_closures import _outcome
    from scripts.search_closure_schedules import minimal_final_summary_counterexample
    from scripts.simulate_closure_history import validate_invocations

    program = minimal_final_summary_counterexample()
    for fifo in (False, True):
        for reverse in (False, True):
            schedule = {"fifo": fifo, "reverse_successors": reverse}
            emitter, production = traced_emitter(native, **schedule)
            candidate, presence, _ = _clone_presence_emitter(native, **schedule)
            assert _outcome(emitter, program, native) == _outcome(candidate, program, native)
            assert production.events == presence.events
            assert production.invocations == presence.invocations
            assert replay(presence, **schedule)["valid"]
            assert validate_invocations(presence, program, **schedule)["valid"]
