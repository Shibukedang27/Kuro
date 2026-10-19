#!/usr/bin/env python3
"""Expanded guarded audit of dense key presence with sparse fact payloads.

The production compiler is never modified.  The candidate is a test-only AST
clone that preserves dense logical key presence while eliding only default
``(set(), False)`` payloads.  The audit compares the inherited corpus, fixed
reduced witnesses, generated known/missing/scalar return shapes, and seeded
adversarial CFGs under four FIFO/LIFO successor schedules.

Example: ``.venv/bin/python scripts/audit_expanded_presence.py --output /tmp/expanded-presence.json``
Use ``--seed-count 100`` for the larger generated evidence run; ``--full-output``
adds complete outcomes, traces, replay failures, and invocation validations.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.audit_normalized_closures import _outcome, _outcome_digest
from scripts.audit_presence_closures import (
    PresenceFacts, _clone_presence_emitter, _copy_expectations,
    _nondefault_size, _storage_metrics,
)
from scripts.closure_queue_cases import bounded_adversarial_cases
from scripts.replay_closure_queue import (
    corpus, edges, replay, traced_emitter,
)
from scripts.search_closure_schedules import (
    adversarial_graph_workload, minimal_final_summary_counterexample,
    minimal_same_order_return_accumulator_witness,
)
from scripts.profile_sparse_closures import generated_graph_workload
from scripts.audit_normalized_closures import recursive_return_workload
from scripts.simulate_closure_history import validate_invocations
from compiler.pipeline import compile_source

SCHEDULES = {
    "lifo_forward": {},
    "fifo_forward": {"fifo": True},
    "lifo_reverse": {"reverse_successors": True},
    "fifo_reverse": {"fifo": True, "reverse_successors": True},
}
RETURN_MODES = ("known", "missing", "scalar")


def _json_hash(value):
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), default=repr).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def outcomes_equal(left, right):
    """Strict outcome comparator: complete assembly or exact native error type/text."""
    if left.get("kind") == "audit-exception" or right.get("kind") == "audit-exception":
        return False
    return left == right


def _reset_trace(trace):
    trace.__init__()


def _reset_storage(storage):
    storage.clear()
    storage.update(_storage_metrics())


def _state_map(frozen):
    return dict(frozen or ())


def _recursive_functions(program):
    """Return functions in call-graph cycles, derived from the actual IR bodies."""
    graph = {name: {ins.args[0] for ins in fn.body
                    if ins.op == "CALL" and ins.args and ins.args[0] in program.functions}
             for name, fn in program.functions.items()}
    # Tarjan SCC keeps this independent of naming conventions in the fixtures.
    serial, stack, on_stack, indexes, lowlinks, cyclic = 0, [], set(), {}, {}, set()

    def visit(node):
        nonlocal serial
        indexes[node] = lowlinks[node] = serial
        serial += 1
        stack.append(node)
        on_stack.add(node)
        for target in graph[node]:
            if target not in indexes:
                visit(target)
                lowlinks[node] = min(lowlinks[node], lowlinks[target])
            elif target in on_stack:
                lowlinks[node] = min(lowlinks[node], indexes[target])
        if lowlinks[node] == indexes[node]:
            component = []
            while True:
                member = stack.pop()
                on_stack.remove(member)
                component.append(member)
                if member == node:
                    break
            if len(component) > 1 or node in graph[node]:
                cyclic.update(component)

    for name in graph:
        if name not in indexes:
            visit(name)
    return cyclic


def _coverage(program, trace):
    """Count observable coverage; these are observations, not labels or promises."""
    aliases, alias_fact_preserved = 0, 0
    missing_loads, unknown_returns, unknown_summaries = 0, 0, 0
    backedges_static, backedges_observed = 0, 0
    for name, function in program.functions.items():
        for index, instruction in enumerate(function.body):
            backedges_static += sum(successor <= index for successor in edges(function.body, index, False))
    for event in trace.visits:
        incoming, outgoing = _state_map(event["incoming"]), _state_map(event["outgoing"])
        op, args, dest = event["op"], event["args"], event["dest"]
        if op == "LOADVAR" and args:
            if args[0] not in incoming:
                missing_loads += 1
            if dest and args[0] in incoming:
                aliases += 1
                alias_fact_preserved += outgoing.get(dest) == incoming[args[0]]
        elif op == "STORE_LIST" and len(args) > 1 and len(args[1]) == 1:
            aliases += 1
            source = incoming.get(args[1][0], ((), False))
            alias_fact_preserved += outgoing.get(args[0], ((), False)) == source
        elif op == "UPDATE" and len(args) > 1:
            aliases += 1
            source = incoming.get(args[1], ((), False))
            alias_fact_preserved += outgoing.get(args[0], ((), False)) == source
        if event["op"] == "RETURN" and not event["return_state"][1]:
            unknown_returns += 1
    for invocation in trace.invocations:
        result = invocation["result"]
        if result is not None and result[2] and not result[1]:
            unknown_summaries += 1
    for merge in trace.merges:
        if merge["successor"] <= merge["index"]:
            backedges_observed += 1
    recursive = _recursive_functions(program)
    recursive_summary_changes = 0
    for transition in trace.outer_transitions:
        previous, updated = _state_map(transition["previous"]), _state_map(transition["updated"])
        recursive_summary_changes += sum(previous.get(name) != updated.get(name) for name in recursive)
    return {
        "recursive_functions_in_call_graph": len(recursive),
        "recursive_functions_with_installed_summary_changes": recursive_summary_changes,
        "alias_operations_observed": aliases,
        "alias_facts_preserved": alias_fact_preserved,
        "missing_name_loads_observed": missing_loads,
        "unknown_return_events_observed": unknown_returns,
        "unknown_all_path_invocation_summaries_observed": unknown_summaries,
        "static_backedges_in_program_bodies": backedges_static,
        "backedge_merge_events_observed": backedges_observed,
    }


def _fixed_cases():
    cases = list(bounded_adversarial_cases().items())
    cases.extend((
        ("reduced_same_order_return_accumulator", minimal_same_order_return_accumulator_witness()),
        ("reduced_final_summary_counterexample", minimal_final_summary_counterexample()),
        ("recursive_return_calls", recursive_return_workload()),
    ))
    return cases


FRONTEND_SOURCE_FIXTURES = {
    "frontend_ir_returned_closure_capture": (
        'Prefix = "Kuro ";\n'
        'Action Greet Name;\n'
        'Return Prefix + Name;\n'
        'Done.\n'
        'Action Factory;\n'
        'Call MakeClosure "Greet";\n'
        'Return @_;\n'
        'Done.\n'
        'Call Factory;\n'
        'Call Invoke @_, "language";\n'
        'Print @_.\n'
    ),
    "frontend_ir_returned_closure_branch": (
        'Action Left Name;\n'
        'Return Name;\n'
        'Done.\n'
        'Action Right Name;\n'
        'Return Name;\n'
        'Done.\n'
        'Action Factory Flag;\n'
        'If Flag is equal to 1;\n'
        'Call MakeClosure "Left";\n'
        'Return @_;\n'
        'Else;\n'
        'Call MakeClosure "Right";\n'
        'Return @_;\n'
        'Done.\n'
        'Done.\n'
        'Call Factory 1;\n'
        'Call Invoke @_, "hello";\n'
        'Print @_.\n'
    ),
}


def _frontend_cases():
    """Compile accepted source fixtures through the real frontend into IR."""
    cases, provenance = [], {}
    for name, source in FRONTEND_SOURCE_FIXTURES.items():
        result = compile_source(source, filename=f"<{name}>")
        if not result.ok or result.ir is None:
            raise AssertionError(f"frontend audit fixture {name} did not compile: {result.diags.render_all()}")
        if not any(instruction.op == "RETURN" for function in result.ir.functions.values()
                   for instruction in function.body):
            raise AssertionError(f"frontend audit fixture {name} did not lower an action RETURN")
        cases.append((name, result.ir))
        provenance[name] = {"source_sha256": hashlib.sha256(source.encode("utf-8")).hexdigest(),
                            "ir_sha256": _json_hash(str(result.ir))}
    return cases, provenance


def _make_cases(seed_count, start_seed):
    cases = list(corpus().items())
    cases.extend(_fixed_cases())
    frontend_cases, _provenance = _frontend_cases()
    cases.extend(frontend_cases)
    for seed in range(start_seed, start_seed + seed_count):
        for mode in RETURN_MODES:
            cases.append((f"generated_graph_seed_{seed}_{mode}",
                          generated_graph_workload(seed, mode, function_name=f"ExpandedGraph{seed}_{mode}")))
        cases.append((f"adversarial_graph_seed_{seed}", adversarial_graph_workload(seed)))
    return cases


def _case_comparison(case_name, schedule_name, program, native, runners, include_full):
    options = SCHEDULES[schedule_name]
    traces, outcomes, storage = {}, {}, None
    for mode in ("production", "presence"):
        emitter, trace, counters = runners[(schedule_name, mode)]
        _reset_trace(trace)
        if counters is not None:
            _reset_storage(counters)
        try:
            outcomes[mode] = _outcome(emitter, program, native)
        except Exception as error:
            # Keep infrastructure/candidate exceptions visible as failures; do
            # not disguise them as compiler outcomes.
            outcomes[mode] = {"kind": "audit-exception", "type": type(error).__qualname__, "text": str(error)}
        traces[mode] = trace
        if mode == "presence":
            storage = counters

    production, presence = traces["production"], traces["presence"]
    replays = {mode: replay(traces[mode], **options) for mode in traces}
    validators = {mode: validate_invocations(traces[mode], program, **options) for mode in traces}
    raw_states_equal = production.to_dict() == presence.to_dict()
    timelines_equal = production.events == presence.events
    summaries_equal = production.invocations == presence.invocations
    outcome_equal = outcomes_equal(outcomes["production"], outcomes["presence"])
    audit_exceptions = {mode: value for mode, value in outcomes.items()
                        if value.get("kind") == "audit-exception"}
    accounting = _copy_expectations(production, replays["production"])
    dense_copy_slots = accounting["dense_copy_presence_slots"]
    sparse_copy_slots = storage["copy_stored_facts"]
    copy_valid = (
        storage["copy_calls"] == accounting["expected_copy_calls"]
        and storage["copy_presence_keys"] == dense_copy_slots
        and sparse_copy_slots == accounting["candidate_expected_stored_fact_slots"]
        and storage["copy_elided_presence_keys"] == dense_copy_slots - sparse_copy_slots
    )
    final_dense = sum(len(state) for record in presence.invocations
                      for state in (record["final_states"] or ()) if state is not None)
    final_sparse = sum(_nondefault_size(state) for record in presence.invocations
                       for state in (record["final_states"] or ()) if state is not None)
    coverage = _coverage(program, production)
    checks = {
        "outcomes_equal": outcome_equal,
        "no_unexpected_audit_exceptions": not audit_exceptions,
        "exact_raw_dense_state_and_trace_equal": raw_states_equal,
        "exact_invocation_summaries_equal": summaries_equal,
        "exact_chronological_queue_merge_return_timeline_equal": timelines_equal,
        "production_replay_valid": replays["production"]["valid"],
        "presence_replay_valid": replays["presence"]["valid"],
        "production_independent_invocation_validation_valid": validators["production"]["valid"],
        "presence_independent_invocation_validation_valid": validators["presence"]["valid"],
        "presence_storage_accounting_valid": copy_valid,
    }
    if case_name in FRONTEND_SOURCE_FIXTURES:
        checks["frontend_source_fixture_analyzed"] = all(trace.invocations for trace in traces.values())
        checks["frontend_source_fixture_successful_complete_assembly"] = all(
            outcomes[mode].get("kind") == "assembly"
            and isinstance(outcomes[mode].get("assembly"), str)
            and bool(outcomes[mode]["assembly"])
            for mode in outcomes
        )
    per_mode_counts = {
        mode: {"invocations": len(trace.invocations),
               "visits": len(trace.visits),
               "returns": sum(event["op"] == "RETURN" for event in trace.visits)}
        for mode, trace in traces.items()
    }
    outcome_kinds = Counter(value.get("kind", "unknown") for value in outcomes.values())
    classifications = {key: Counter() for key in
                       ("successful_assembly", "rejection", "unexpected_exception", "other", "analyzed", "nonanalyzed")}
    for mode, value in outcomes.items():
        kind = value.get("kind", "unknown")
        key = ("successful_assembly" if kind == "assembly" else
               "rejection" if kind == "native-error" else
               "unexpected_exception" if kind == "audit-exception" else "other")
        classifications[key][kind] += 1
        classifications["analyzed" if traces[mode].invocations else "nonanalyzed"][kind] += 1
    item = {
        "case": case_name,
        "schedule": schedule_name,
        "checks": checks,
        "outcomes": {mode: _outcome_digest(value) for mode, value in outcomes.items()},
        "evidence_sha256": {
            "production_outcome": _json_hash(_outcome_digest(outcomes["production"])),
            "presence_outcome": _json_hash(_outcome_digest(outcomes["presence"])),
            "production_trace": _json_hash(production.to_dict()),
            "presence_trace": _json_hash(presence.to_dict()),
            "production_chronological_events": _json_hash(production.events),
            "presence_chronological_events": _json_hash(presence.events),
            "production_invocation_summaries": _json_hash(production.invocations),
            "presence_invocation_summaries": _json_hash(presence.invocations),
        },
        "coverage_observed": coverage,
        "actual_trace_counts": {
            "by_mode": per_mode_counts,
            "combined": {key: sum(counts[key] for counts in per_mode_counts.values())
                         for key in ("invocations", "visits", "returns")},
        },
        "outcome_kind_counts": {
            "by_mode": {mode: {value.get("kind", "unknown"): 1}
                        for mode, value in outcomes.items()},
            "combined": dict(outcome_kinds),
            "by_classification": {key: dict(value) for key, value in classifications.items()},
        },
        "storage_copy_counts": {
            **accounting,
            "actual_copy_calls": storage["copy_calls"],
            "actual_copy_presence_slots": storage["copy_presence_keys"],
            "actual_copy_nondefault_fact_slots": sparse_copy_slots,
            "actual_copy_elided_presence_slots": storage["copy_elided_presence_keys"],
            "final_state_maps": sum(len(record["final_states"] or ()) for record in presence.invocations),
            "final_dense_presence_slots": final_dense,
            "final_nondefault_fact_slots": final_sparse,
            "final_elided_presence_slots": final_dense - final_sparse,
            "elided_default_write_count": storage["elided_default_writes"],
            "accounting_valid": copy_valid,
        },
    }
    failed_checks = [name for name, valid in checks.items() if not valid]
    if failed_checks:
        item["failure_details"] = {
            "failed_checks": failed_checks,
            "replay_errors": {mode: result["errors"][:12] for mode, result in replays.items() if not result["valid"]},
            "invocation_validation_failures": {mode: result["failures"][:12] for mode, result in validators.items() if not result["valid"]},
            "outcome_values": {mode: _outcome_digest(value) for mode, value in outcomes.items()},
            "unexpected_audit_exceptions": {mode: _outcome_digest(value) for mode, value in audit_exceptions.items()},
        }
    if include_full:
        item["complete_outcomes"] = outcomes
        item["complete_traces"] = {mode: trace.to_dict() for mode, trace in traces.items()}
        item["chronological_events"] = {mode: trace.events for mode, trace in traces.items()}
        item["replay_results"] = replays
        item["invocation_validation_results"] = validators
    return item


def audit(*, seed_count=25, start_seed=0, include_full=False, progress=False):
    """Run inherited, fixed, generated, and adversarial cases in four schedules."""
    if not isinstance(seed_count, int) or not 0 <= seed_count <= 100:
        raise ValueError("seed_count must be an integer from 0 through 100")
    if not isinstance(start_seed, int) or start_seed < 0:
        raise ValueError("start_seed must be a nonnegative integer")
    import compiler.native as native

    runners = {}
    for schedule_name, options in SCHEDULES.items():
        emitter, trace = traced_emitter(native, mode="production", **options)
        runners[(schedule_name, "production")] = (emitter, trace, None)
        emitter, trace, storage = _clone_presence_emitter(native, **options)
        runners[(schedule_name, "presence")] = (emitter, trace, storage)

    frontend_provenance = _frontend_cases()[1]
    programs = _make_cases(seed_count, start_seed)
    reports, totals, coverage_totals, storage_totals = [], Counter(), Counter(), Counter()
    aggregate_outcome_kinds = {mode: Counter() for mode in ("production", "presence")}
    aggregate_classifications = {key: Counter() for key in
                                 ("successful_assembly", "rejection", "unexpected_exception", "other", "analyzed", "nonanalyzed")}
    aggregate_trace_counts = Counter()
    for case_index, (case_name, program) in enumerate(programs, 1):
        for schedule_name in SCHEDULES:
            row = _case_comparison(case_name, schedule_name, program, native, runners, include_full)
            reports.append(row)
            totals["comparisons"] += 1
            totals["all_checks_passed"] += all(row["checks"].values())
            totals["cases_with_failures"] += not all(row["checks"].values())
            for key, value in row["coverage_observed"].items():
                coverage_totals[key] += value
            for key, value in row["storage_copy_counts"].items():
                if isinstance(value, int):
                    storage_totals[key] += value
            for mode, kind_counts in row["outcome_kind_counts"]["by_mode"].items():
                aggregate_outcome_kinds[mode].update(kind_counts)
            for key, kind_counts in row["outcome_kind_counts"]["by_classification"].items():
                aggregate_classifications[key].update(kind_counts)
            aggregate_trace_counts.update(row["actual_trace_counts"]["combined"])
        if progress and (case_index % 20 == 0 or case_index == len(programs)):
            print(f"expanded presence audit: {case_index}/{len(programs)} cases",
                  file=sys.stderr, flush=True)
    observed_coverage = {
        "recursive_installed_summary_changes": coverage_totals["recursive_functions_with_installed_summary_changes"],
        "alias_operations": coverage_totals["alias_operations_observed"],
        "alias_fact_preservations": coverage_totals["alias_facts_preserved"],
        "missing_name_loads": coverage_totals["missing_name_loads_observed"],
        "unknown_return_events": coverage_totals["unknown_return_events_observed"],
        "unknown_all_path_summaries": coverage_totals["unknown_all_path_invocation_summaries_observed"],
        "static_backedges": coverage_totals["static_backedges_in_program_bodies"],
        "observed_backedge_merges": coverage_totals["backedge_merge_events_observed"],
    }
    coverage_requirements = {key: value > 0 for key, value in observed_coverage.items()}
    result = {
        "scope": "bounded empirical comparison; not a proof of scheduling equivalence or promotion authorization",
        "start_seed": start_seed,
        "seed_count": seed_count,
        "case_count": len(programs),
        "order_count": len(SCHEDULES),
        "comparison_count": len(reports),
        "orders": list(SCHEDULES),
        "all_comparisons_passed": totals["cases_with_failures"] == 0,
        "all_outcomes_equal": all(row["checks"]["outcomes_equal"] for row in reports),
        "all_raw_dense_states_equal": all(row["checks"]["exact_raw_dense_state_and_trace_equal"] for row in reports),
        "all_invocation_summaries_equal": all(row["checks"]["exact_invocation_summaries_equal"] for row in reports),
        "all_chronological_events_equal": all(row["checks"]["exact_chronological_queue_merge_return_timeline_equal"] for row in reports),
        "all_production_replays_valid": all(row["checks"]["production_replay_valid"] for row in reports),
        "all_presence_replays_valid": all(row["checks"]["presence_replay_valid"] for row in reports),
        "all_production_invocation_validations_valid": all(row["checks"]["production_independent_invocation_validation_valid"] for row in reports),
        "all_presence_invocation_validations_valid": all(row["checks"]["presence_independent_invocation_validation_valid"] for row in reports),
        "all_presence_storage_accounting_valid": all(row["checks"]["presence_storage_accounting_valid"] for row in reports),
        "observed_coverage": observed_coverage,
        "coverage_requirements_observed": coverage_requirements,
        "all_required_coverage_observed": all(coverage_requirements.values()),
        "aggregate_storage_counts": dict(storage_totals),
        "frontend_source_fixtures": frontend_provenance,
        "aggregate_trace_counts": dict(aggregate_trace_counts),
        "aggregate_outcome_kind_counts": {
            "by_mode": {mode: dict(counts) for mode, counts in aggregate_outcome_kinds.items()},
            "combined": dict(sum(aggregate_outcome_kinds.values(), Counter())),
            "by_classification": {key: dict(value) for key, value in aggregate_classifications.items()},
        },
        "failure_count": totals["cases_with_failures"],
        "failures": [{"case": row["case"], "schedule": row["schedule"], **row["failure_details"]}
                     for row in reports if "failure_details" in row],
        "cases": reports,
    }
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path, help="compact JSON evidence path")
    parser.add_argument("--full-output", type=Path, help="optional full traces/outcomes/validation path")
    parser.add_argument("--seed-count", type=int, default=25, help="generated/adversarial seed count, 0..100 (default 25)")
    parser.add_argument("--start-seed", type=int, default=0)
    args = parser.parse_args()
    result = audit(seed_count=args.seed_count, start_seed=args.start_seed,
                   include_full=bool(args.full_output), progress=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    if args.full_output:
        args.full_output.parent.mkdir(parents=True, exist_ok=True)
        args.full_output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in result.items() if key != "cases" and key != "failures"}, indent=2))
    if not result["all_comparisons_passed"] or not result["all_required_coverage_observed"]:
        raise SystemExit("expanded presence audit failed; see emitted report and failure details")


if __name__ == "__main__":
    main()
