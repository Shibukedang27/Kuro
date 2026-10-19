"""Bounded same-schedule production-vs-normalized closure search smoke test."""
from __future__ import annotations

import compiler.native as native
from scripts.audit_normalized_closures import make_emitter
from scripts.search_closure_schedules import (
    _outcome,
    _return_value_mismatch_count,
    _summary_signature,
    adversarial_graph_workload,
    minimal_same_order_return_accumulator_witness,
    minimal_final_summary_counterexample,
    search,
)


def _program_signature(program):
    def body_signature(body):
        return tuple((item.op, item.args, item.dest) for item in body)
    return (
        tuple(body_signature(function.body) for function in program.functions.values()),
        body_signature(program.main),
    )


def test_adversarial_cfg_generator_is_seeded_and_contains_loop_backedges():
    first = adversarial_graph_workload(41)
    repeated = adversarial_graph_workload(41)
    assert _program_signature(first) == _program_signature(repeated)
    graph = first.functions["ScheduleGraph41"].body
    assert sum(item.op == "JUMP" and item.args[0].startswith("head_") for item in graph) == 3
    assert any(item.op == "LOADVAR" and str(item.args[0]).startswith("never_defined_") for item in graph)


def test_bounded_search_compares_exact_same_order_results_and_reports_scope():
    report = search(seed_count=2, start_seed=13)
    assert report["scope"] == "bounded empirical search; absence of mismatch is not proof"
    assert report["fixed_case_count"] == 8
    assert report["generated_case_count"] == 8
    assert report["case_count"] == 16
    assert report["schedules"] == ["lifo_forward", "fifo_forward", "lifo_reverse", "fifo_reverse"]
    assert report["totals"]["case_schedule_pairs"] == 64
    assert report["totals"]["summary_compared"] == 64
    assert report["totals"]["return_accumulators_compared"] == 64
    assert report["totals"]["outcomes_compared"] == 64
    assert report["totals"]["production_invocations"] > 0
    assert report["totals"]["return_events"] > 0
    assert len(report["corpus_sha256"]) == 64
    # This bounded search found a real final-summary counterexample as well as
    # different intermediate sticky RETURN accumulator traces; outputs/errors
    # still agree for the exercised pairs.
    assert report["mismatch_counts"]["outcome"] == 0
    assert report["mismatch_counts"]["final_summary"] > 0
    assert report["final_summary_counterexample_found"]
    assert report["mismatch_counts"]["return_accumulator_sequence"] > 0
    assert report["totals"]["return_value_mismatches"] > 0
    assert any(item["case"] == "minimal_final_summary_counterexample"
               for item in report["summary_counterexamples"])


def test_reduced_same_order_return_accumulator_witness_is_stable():
    program = minimal_same_order_return_accumulator_witness()
    production_emitter, production_trace = make_emitter(native, mode="production", trace=True)
    normalized_emitter, normalized_trace = make_emitter(native, mode="normalized", trace=True)
    production_outcome = _outcome(production_emitter, program, native)
    normalized_outcome = _outcome(normalized_emitter, program, native)
    assert production_outcome == normalized_outcome
    assert _summary_signature(production_trace) == _summary_signature(normalized_trace)
    assert _return_value_mismatch_count(production_trace, normalized_trace) > 0


def test_reduced_final_summary_counterexample_is_preserved():
    program = minimal_final_summary_counterexample()
    production_emitter, production_trace = make_emitter(
        native, mode="production", trace=True, reverse_successors=True,
    )
    normalized_emitter, normalized_trace = make_emitter(
        native, mode="normalized", trace=True, reverse_successors=True,
    )
    production_outcome = _outcome(production_emitter, program, native)
    normalized_outcome = _outcome(normalized_emitter, program, native)
    assert production_outcome == normalized_outcome
    assert production_outcome["kind"] == "native-error"
    production, normalized = _summary_signature(production_trace), _summary_signature(normalized_trace)
    assert production != normalized
    assert production[0] == (("SummaryWitness", ()), 0, (("SummaryTarget",), False, True))
    assert normalized[0] == (("SummaryWitness", ()), 0, ((), False, True))


def test_search_resets_closed_over_trace_collectors_between_cases(monkeypatch):
    import scripts.search_closure_schedules as module

    original = module.make_emitter
    calls = []

    def checked_emitter(*args, **kwargs):
        emit, trace = original(*args, **kwargs)

        def checked(program):
            assert not trace.invocations and not trace.visits
            assert not trace.queues and not trace.outer_transitions
            calls.append(1)
            return emit(program)

        return checked, trace

    monkeypatch.setattr(module, "make_emitter", checked_emitter)
    result = module.search(seed_count=0)
    assert len(calls) == result["totals"]["case_schedule_pairs"] * 2
