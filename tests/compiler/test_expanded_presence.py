"""Bounded correctness and fail-closed controls for expanded presence auditing."""
from __future__ import annotations

from copy import deepcopy

import compiler.native as native
from scripts.audit_expanded_presence import SCHEDULES, audit, outcomes_equal
from scripts.audit_presence_closures import _clone_presence_emitter
from scripts.closure_queue_cases import bounded_adversarial_cases
from scripts.replay_closure_queue import corpus, replay
from scripts.search_closure_schedules import minimal_final_summary_counterexample
from scripts.simulate_closure_history import validate_invocations


def test_four_seed_expanded_audit_compares_every_stream_and_observes_claimed_coverage():
    result = audit(seed_count=4)

    assert result["case_count"] == len(corpus()) + len(bounded_adversarial_cases()) + 3 + 2 + 16
    assert result["comparison_count"] == result["case_count"] * 4
    assert result["orders"] == list(SCHEDULES)
    assert result["all_comparisons_passed"]
    assert result["all_outcomes_equal"]
    assert result["all_raw_dense_states_equal"]
    assert result["all_invocation_summaries_equal"]
    assert result["all_chronological_events_equal"]
    assert result["all_production_replays_valid"] and result["all_presence_replays_valid"]
    assert result["all_production_invocation_validations_valid"]
    assert result["all_presence_invocation_validations_valid"]
    assert result["all_presence_storage_accounting_valid"]
    assert all(row["checks"]["no_unexpected_audit_exceptions"] for row in result["cases"])
    assert result["all_required_coverage_observed"]
    assert all(result["coverage_requirements_observed"].values())
    coverage = result["observed_coverage"]
    assert coverage["recursive_installed_summary_changes"] > 0
    assert coverage["alias_operations"] > 0 and coverage["alias_fact_preservations"] > 0
    assert coverage["missing_name_loads"] > 0
    assert coverage["unknown_return_events"] > 0
    assert coverage["unknown_all_path_summaries"] > 0
    assert coverage["static_backedges"] > 0 and coverage["observed_backedge_merges"] > 0

    names = {row["case"] for row in result["cases"]}
    for seed in range(4):
        for mode in ("known", "missing", "scalar"):
            assert f"generated_graph_seed_{seed}_{mode}" in names
        assert f"adversarial_graph_seed_{seed}" in names
    assert all(len(digest) == 64 for row in result["cases"]
               for digest in row["evidence_sha256"].values())
    assert result["aggregate_storage_counts"]["actual_copy_elided_presence_slots"] > 0
    assert result["aggregate_storage_counts"]["final_elided_presence_slots"] > 0
    assert set(result["frontend_source_fixtures"]) == {
        "frontend_ir_returned_closure_capture", "frontend_ir_returned_closure_branch"
    }
    assert all(len(details["source_sha256"]) == 64 and len(details["ir_sha256"]) == 64
               for details in result["frontend_source_fixtures"].values())
    frontend_rows = [row for row in result["cases"] if row["case"] in result["frontend_source_fixtures"]]
    assert len(frontend_rows) == 2 * len(SCHEDULES)
    assert all(row["checks"]["frontend_source_fixture_analyzed"]
               and row["checks"]["frontend_source_fixture_successful_complete_assembly"]
               for row in frontend_rows)
    assert all(row["actual_trace_counts"]["combined"]["invocations"] > 0
               and row["actual_trace_counts"]["combined"]["visits"] > 0
               for row in frontend_rows)
    assert result["aggregate_outcome_kind_counts"]["by_classification"]["successful_assembly"]["assembly"] > 0
    assert result["aggregate_trace_counts"]["returns"] > 0
    assert result["failure_count"] == 0


def test_seed_count_is_configurable_but_fail_closed_above_one_hundred():
    import pytest

    with pytest.raises(ValueError, match="0 through 100"):
        audit(seed_count=101)
    with pytest.raises(ValueError, match="nonnegative"):
        audit(seed_count=0, start_seed=-1)


def test_outcome_comparator_requires_exact_assembly_or_error_type_and_text():
    assembly = {"kind": "assembly", "assembly": "mov %rax, %rbx\n"}
    assert outcomes_equal(assembly, dict(assembly))
    assert not outcomes_equal(assembly, {"kind": "assembly", "assembly": "mov %rax, %rcx\n"})
    error = {"kind": "native-error", "type": "compiler.native.NativeBackendError", "text": "unsupported"}
    assert outcomes_equal(error, dict(error))
    assert not outcomes_equal(error, {**error, "text": "different"})
    assert not outcomes_equal(error, {**error, "type": "OtherError"})
    unexpected = {"kind": "audit-exception", "type": "RuntimeError", "text": "broken"}
    assert not outcomes_equal(unexpected, dict(unexpected)), "even equal unexpected exceptions must fail"


def test_independent_replayers_reject_corrupt_presence_state_queue_and_summary():
    program = minimal_final_summary_counterexample()
    emitter, trace, _storage = _clone_presence_emitter(native)
    try:
        emitter(program)
    except native.NativeBackendError:
        # The witness reaches this expected unsupported-Invoke outcome only
        # after the analyzer has emitted its complete history.
        pass
    assert trace.invocations, "fixture did not produce an analyzer history"

    corruptions = {}

    # Removing a logically present entry from a raw dense incoming state models
    # losing dense key presence even when its payload is the default fact.
    corrupt = deepcopy(trace)
    visit = next(event for kind, event in corrupt.events if kind == "visit"
                 and any(fact == ((), False) for _name, fact in event["incoming"]))
    state = list(visit["incoming"])
    default_index = next(index for index, (_name, fact) in enumerate(state)
                         if fact == ((), False))
    state.pop(default_index)
    visit["incoming"] = tuple(state)
    corruptions["presence"] = corrupt

    corrupt = deepcopy(trace)
    visit = next(event for kind, event in corrupt.events if kind == "visit")
    visit["outgoing"] = (("forged_state", (("ForgedTarget",), True)),)
    corruptions["state"] = corrupt

    corrupt = deepcopy(trace)
    queue = next(event for kind, event in corrupt.events if kind == "queue")
    queue["queue"] = (999,)
    corruptions["queue"] = corrupt

    corrupt = deepcopy(trace)
    invocation = corrupt.invocations[0]
    forged_summary = (("ForgedTarget",), False, True)
    invocation["result"] = forged_summary
    finish = next(event for kind, event in corrupt.events
                  if kind == "finish" and event["id"] == invocation["id"])
    finish["result"] = forged_summary
    corruptions["summary"] = corrupt

    for label, damaged in corruptions.items():
        replay_result = replay(damaged)
        validation_result = validate_invocations(damaged, program)
        assert not replay_result["valid"], label
        assert not validation_result["valid"], label
