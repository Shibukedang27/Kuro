#!/usr/bin/env python3
"""Test-only experiment: sparse fact storage with dense key presence.

The cloned analyzer keeps every mapping key visible to iteration, ``keys``,
``get``, equality, joins, and tracing, while storing only facts other than the
default ``(set(), False)``. The compiler source and inherited audit scripts are
never changed. Run with ``.venv/bin/python scripts/audit_presence_closures.py
--output /tmp/presence-closures.json``; ``--full-output`` additionally saves
complete outcomes and raw timelines.
"""
from __future__ import annotations

import argparse
from collections import Counter
from collections.abc import ItemsView, KeysView, Mapping, ValuesView
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.audit_normalized_closures import _outcome, _outcome_digest
from scripts.replay_closure_queue import Timeline, corpus, replay, traced_emitter


class PresenceFacts(dict):
    """A dict-compatible logical map with a separate dense presence index.

    The inherited dict payload contains only non-default fact tuples; ``_present``
    retains all logically present names, including those whose fact is default.
    Stored target sets remain shallow/read-only aliases, as in production's map
    copies. The analyzer's merge uses fresh set unions and does not mutate them.
    """

    def __init__(self, metrics=None):
        dict.__init__(self)
        self._present = set()
        self._metrics = metrics
        if metrics is not None:
            metrics["maps_created"] += 1

    def __iter__(self):
        return iter(self._present)

    def __len__(self):
        return len(self._present)

    def __contains__(self, key):
        return key in self._present

    def __getitem__(self, key):
        if key not in self._present:
            raise KeyError(key)
        try:
            return dict.__getitem__(self, key)
        except KeyError:
            return (set(), False)

    def get(self, key, default=None):
        if key not in self._present:
            return default
        try:
            return dict.__getitem__(self, key)
        except KeyError:
            return (set(), False)

    def __setitem__(self, key, value):
        targets, known = value
        self._present.add(key)
        if self._metrics is not None:
            self._metrics["logical_writes"] += 1
        if not targets and not known:
            dict.pop(self, key, None)
            if self._metrics is not None:
                self._metrics["elided_default_writes"] += 1
            return
        dict.__setitem__(self, key, (targets, known))
        if self._metrics is not None:
            self._metrics["stored_nondefault_writes"] += 1

    def __delitem__(self, key):
        if key not in self._present:
            raise KeyError(key)
        self._present.remove(key)
        dict.pop(self, key, None)

    def keys(self):
        return KeysView(self)

    def items(self):
        return ItemsView(self)

    def values(self):
        return ValuesView(self)

    def copy(self):
        result = type(self)(self._metrics)
        result._present = self._present.copy()
        for key, fact in dict.items(self):
            dict.__setitem__(result, key, fact)  # same read-only target-set alias as dict.copy()
        if self._metrics is not None:
            self._metrics["copy_calls"] += 1
            self._metrics["copy_presence_keys"] += len(self._present)
            self._metrics["copy_stored_facts"] += dict.__len__(self)
            self._metrics["copy_elided_presence_keys"] += len(self._present) - dict.__len__(self)
        return result

    def __eq__(self, other):
        if not isinstance(other, Mapping):
            return NotImplemented
        if len(self) != len(other) or set(self) != set(other.keys()):
            return False
        return all(self[key] == other[key] for key in self)

    def __ne__(self, other):
        equal = self.__eq__(other)
        return NotImplemented if equal is NotImplemented else not equal

    def setdefault(self, key, default=None):
        if key in self._present:
            return self[key]
        self[key] = default
        return self[key]

    def update(self, *args, **kwargs):
        if len(args) > 1:
            raise TypeError(f"update expected at most 1 argument, got {len(args)}")
        if args:
            source = args[0]
            pairs = source.items() if hasattr(source, "items") else source
            for key, value in pairs:
                self[key] = value
        for key, value in kwargs.items():
            self[key] = value

    def clear(self):
        self._present.clear()
        dict.clear(self)

    def pop(self, key, *default):
        if len(default) > 1:
            raise TypeError(f"pop expected at most 2 arguments, got {len(default) + 1}")
        if key not in self._present:
            if default:
                return default[0]
            raise KeyError(key)
        value = self[key]
        self._present.remove(key)
        dict.pop(self, key, None)
        return value

    def popitem(self):
        if not self._present:
            raise KeyError("popitem(): mapping is empty")
        key = next(iter(self._present))
        return key, self.pop(key)


def _storage_metrics():
    return Counter({
        "maps_created": 0, "logical_writes": 0, "elided_default_writes": 0,
        "stored_nondefault_writes": 0, "copy_calls": 0,
        "copy_presence_keys": 0, "copy_stored_facts": 0,
        "copy_elided_presence_keys": 0, "final_state_maps": 0,
        "final_presence_keys": 0, "final_stored_facts": 0,
        "final_elided_presence_keys": 0,
    })


def _clone_presence_emitter(native, *, fifo=False, reverse_successors=False):
    """Clone via the inherited fail-closed trace transform, then alter two maps."""
    from scripts.audit_normalized_closures import _clone_tree
    import ast

    metrics = _storage_metrics()
    tree = _clone_tree(native, mode="production", trace=True, fifo=fifo,
                       reverse_successors=reverse_successors)
    hits = Counter()

    class SparseMaps(ast.NodeTransformer):
        inside = False

        def visit_FunctionDef(self, node):
            if node.name != "analyze_action_closure_returns":
                return self.generic_visit(node)
            hits["analyzer"] += 1
            old = self.inside
            self.inside = True
            node = self.generic_visit(node)
            self.inside = old
            return node

        def visit_Assign(self, node):
            if self.inside and len(node.targets) == 1 and ast.unparse(node.targets[0]) == "states[0]":
                assert isinstance(node.value, ast.Dict) and not node.value.keys, "initial state ceased to be an empty dict"
                hits["initial_state"] += 1
                node.value = ast.Call(func=ast.Name(id="_PresenceFacts", ctx=ast.Load()), args=[], keywords=[])
            return self.generic_visit(node)

        def visit_AnnAssign(self, node):
            if self.inside and ast.unparse(node.target) == "merged":
                assert isinstance(node.value, ast.Dict) and not node.value.keys, "merge map ceased to be an empty dict"
                hits["merged_map"] += 1
                node.value = ast.Call(func=ast.Name(id="_PresenceFacts", ctx=ast.Load()), args=[], keywords=[])
            return self.generic_visit(node)

    tree = SparseMaps().visit(tree)
    assert hits == Counter({"analyzer": 1, "initial_state": 1, "merged_map": 1}), f"presence-map AST sites changed: {dict(hits)}"
    ast.fix_missing_locations(tree)
    trace = Timeline()
    namespace = vars(native).copy()
    namespace.update(
        _PresenceFacts=lambda: PresenceFacts(metrics),
        _closure_audit_trace=trace,
        _closure_audit_queue=lambda ident, pending, successor: _record_queue(trace, ident, pending, successor),
        _closure_audit_round=lambda target, previous, updated: _record_round(trace, previous, updated),
    )
    exec(compile(tree, "<presence-aware-closure-audit>", "exec"), namespace)
    return namespace["emit_x86_64_linux"], trace, metrics


def _record_queue(trace, ident, pending, successor):
    pending.append(successor)
    trace.queued(ident, successor, pending)


def _record_round(trace, previous, updated):
    trace.round(previous, updated)
    return False


def _dense_presence_size(frozen):
    return len(frozen)


def _nondefault_size(frozen):
    return sum(1 for _name, (targets, known) in frozen if targets or known)


def _copy_expectations(trace, production_replay):
    """Expected mapping-copy workload reconstructed from dense observed traces."""
    # Replay supplies the first-reach count; reconstruct corresponding outgoing
    # states independently from the observed visits and CFG edges.
    first_reach_total = production_replay["counts"].get("first_reach_appends", 0)
    visits = trace.visits
    dense_slots = sum(_dense_presence_size(v["incoming"]) for v in visits)
    sparse_slots = sum(_nondefault_size(v["incoming"]) for v in visits)
    reach_by_invocation = Counter()
    # Every first-reach state copy clones the outgoing state of its predecessor.
    from scripts.replay_closure_queue import edges
    bodies = {}
    for event_kind, event in trace.events:
        if event_kind == "begin":
            bodies[event["id"]] = trace.bodies[event["id"]]
    first_reach_visits = []
    for ident, body in bodies.items():
        reached = {0} if body else set()
        for event_kind, event in trace.events:
            if event_kind != "visit" or event["invocation"] != ident:
                continue
            for successor in edges(body, event["index"], reverse=False):
                if successor not in reached:
                    reached.add(successor)
                    first_reach_visits.append(event)
                    reach_by_invocation[ident] += 1
    # Successor iteration order only affects ordering, not total copied slots.
    dense_slots += sum(_dense_presence_size(v["outgoing"]) for v in first_reach_visits)
    sparse_slots += sum(_nondefault_size(v["outgoing"]) for v in first_reach_visits)
    return {"expected_copy_calls": len(visits) + first_reach_total,
            "dense_copy_presence_slots": dense_slots,
            "candidate_expected_stored_fact_slots": sparse_slots,
            "first_reach_copy_count": first_reach_total,
            "first_reach_by_invocation": dict(reach_by_invocation)}


def audit(*, include_full=False):
    """Run all inherited 29 corpus cases under four exact schedule orders."""
    import compiler.native as native

    schedules = {
        "lifo_forward": {}, "fifo_forward": {"fifo": True},
        "lifo_reverse": {"reverse_successors": True},
        "fifo_reverse": {"fifo": True, "reverse_successors": True},
    }
    reports = []
    aggregates = Counter()
    programs = corpus()
    for case_name, program in programs.items():
        for order, schedule in schedules.items():
            production_emitter, production_trace = traced_emitter(native, mode="production", **schedule)
            presence_emitter, presence_trace, storage = _clone_presence_emitter(native, **schedule)
            production_outcome = _outcome(production_emitter, program, native)
            presence_outcome = _outcome(presence_emitter, program, native)
            production_replay = replay(production_trace, **schedule)
            presence_replay = replay(presence_trace, **schedule)
            exact_trace_equal = production_trace.to_dict() == presence_trace.to_dict()
            exact_timeline_equal = production_trace.events == presence_trace.events
            exact_summaries_equal = production_trace.invocations == presence_trace.invocations
            copy_expectations = _copy_expectations(production_trace, production_replay)
            # Candidate maps count actual copied storage. Final-state storage is
            # computed directly from each recorded dense final-state snapshot.
            final_dense = sum(
                len(state) for invocation in presence_trace.invocations
                for state in (invocation["final_states"] or ()) if state is not None
            )
            final_sparse = sum(
                _nondefault_size(state) for invocation in presence_trace.invocations
                for state in (invocation["final_states"] or ()) if state is not None
            )
            copy_counts = {
                **copy_expectations,
                "actual_copy_calls": storage["copy_calls"],
                "actual_copy_presence_slots": storage["copy_presence_keys"],
                "actual_copy_nondefault_fact_slots": storage["copy_stored_facts"],
                "actual_copy_elided_presence_slots": storage["copy_elided_presence_keys"],
                "final_state_maps": sum(len(x["final_states"] or ()) for x in presence_trace.invocations),
                "final_dense_presence_slots": final_dense,
                "final_nondefault_fact_slots": final_sparse,
                "final_elided_presence_slots": final_dense - final_sparse,
                "elided_default_write_count": storage["elided_default_writes"],
            }
            copy_accounting_valid = (
                copy_counts["actual_copy_calls"] == copy_counts["expected_copy_calls"]
                and copy_counts["actual_copy_presence_slots"] == copy_counts["dense_copy_presence_slots"]
                and copy_counts["actual_copy_nondefault_fact_slots"] == copy_counts["candidate_expected_stored_fact_slots"]
                and copy_counts["actual_copy_elided_presence_slots"] == (
                    copy_counts["dense_copy_presence_slots"] - copy_counts["candidate_expected_stored_fact_slots"]
                )
            )
            item = {
                "case": case_name, "order": order,
                "outcomes_equal": production_outcome == presence_outcome,
                "outcomes": {"production": _outcome_digest(production_outcome),
                             "presence": _outcome_digest(presence_outcome)},
                "exact_invocation_summaries_equal": exact_summaries_equal,
                "raw_dense_states_equal": exact_trace_equal,
                "queue_and_return_timeline_equal": exact_timeline_equal,
                "complete_trace_equal": exact_trace_equal and exact_timeline_equal,
                "production_replay_valid": production_replay["valid"],
                "presence_replay_valid": presence_replay["valid"],
                "copy_accounting_valid": copy_accounting_valid,
                "storage_copy_counts": copy_counts,
            }
            if include_full:
                item["complete_outcomes"] = {"production": production_outcome, "presence": presence_outcome}
                item["timelines"] = {"production": production_trace.events, "presence": presence_trace.events}
                item["traces"] = {"production": production_trace.to_dict(), "presence": presence_trace.to_dict()}
                item["replay_errors"] = {"production": production_replay["errors"], "presence": presence_replay["errors"]}
            reports.append(item)
            aggregates["comparisons"] += 1
            aggregates["copy_calls"] += copy_counts["actual_copy_calls"]
            aggregates["dense_copy_presence_slots"] += copy_counts["dense_copy_presence_slots"]
            aggregates["presence_copy_nondefault_fact_slots"] += copy_counts["actual_copy_nondefault_fact_slots"]
            aggregates["presence_copy_elided_slots"] += copy_counts["actual_copy_elided_presence_slots"]
            aggregates["final_dense_presence_slots"] += final_dense
            aggregates["final_nondefault_fact_slots"] += final_sparse
            aggregates["final_elided_presence_slots"] += final_dense - final_sparse
            aggregates["cases_with_default_elisions"] += copy_counts["actual_copy_elided_presence_slots"] > 0
    return {
        "case_count": len(programs), "order_count": len(schedules),
        "comparison_count": len(reports), "orders": list(schedules),
        "all_outcomes_equal": all(item["outcomes_equal"] for item in reports),
        "all_exact_invocation_summaries_equal": all(item["exact_invocation_summaries_equal"] for item in reports),
        "all_raw_dense_states_equal": all(item["raw_dense_states_equal"] for item in reports),
        "all_queue_and_return_timelines_equal": all(item["queue_and_return_timeline_equal"] for item in reports),
        "all_production_replays_valid": all(item["production_replay_valid"] for item in reports),
        "all_presence_replays_valid": all(item["presence_replay_valid"] for item in reports),
        "all_copy_accounting_valid": all(item["copy_accounting_valid"] for item in reports),
        "scheduling_equivalence_proven": False,
        "production_promotion_allowed": False,
        "aggregate_storage_copy_counts": dict(aggregates),
        "cases": reports,
    }


def compact(result):
    """Return the compact JSON report; outcome hashes represent full comparisons."""
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path, help="compact JSON report path")
    parser.add_argument("--full-output", type=Path, help="optional complete outcomes/raw timelines JSON path")
    args = parser.parse_args()
    result = audit(include_full=bool(args.full_output))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(compact(result), indent=2) + "\n", encoding="utf-8")
    if args.full_output:
        args.full_output.parent.mkdir(parents=True, exist_ok=True)
        # The full report is identical to the compact metadata plus full records.
        args.full_output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    summary = {key: value for key, value in result.items() if key != "cases"}
    print(json.dumps(summary, indent=2))
    assert result["comparison_count"] == 116, f"inherited corpus/order size changed: {result['comparison_count']}"
    assert result["all_outcomes_equal"] and result["all_exact_invocation_summaries_equal"]
    assert result["all_raw_dense_states_equal"] and result["all_queue_and_return_timelines_equal"]
    assert result["all_production_replays_valid"] and result["all_presence_replays_valid"]
    assert result["all_copy_accounting_valid"]


if __name__ == "__main__":
    main()
