#!/usr/bin/env python3
"""Test-only production-queue replay; never changes compiler source.

Dense and normalized shadow maps execute independently on the dense schedule.
An autonomous normalized run is compared separately, not assumed equivalent.
"""
from __future__ import annotations

import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.audit_normalized_closures import (
    AuditTrace, _clone_tree, _freeze, _outcome, _outcome_digest,
    _record_queue, _record_round, _elide_unknown, _normalized_final_states,
    multibackedge_workload, recursive_return_workload,
)
from scripts.profile_sparse_closures import generated_graph_workload


class Timeline(AuditTrace):
    """Record callbacks in their actual execution order, not separate buckets."""

    def __init__(self):
        super().__init__()
        self.events = []
        self.bodies = {}

    def begin(self, function, known_returns):
        ident = super().begin(function, known_returns)
        self.bodies[ident] = function.body
        self.events.append(("begin", dict(self.invocations[-1])))
        return ident

    def seeded(self, *args):
        super().seeded(*args)
        self.events.append(("queue", self.queues[-1]))

    def popped(self, *args):
        super().popped(*args)
        self.events.append(("queue", self.queues[-1]))

    def queued(self, *args):
        super().queued(*args)
        self.events.append(("queue", self.queues[-1]))

    def visit(self, *args):
        super().visit(*args)
        self.events.append(("visit", self.visits[-1]))

    def merge(self, *args):
        super().merge(*args)
        self.events.append(("merge", self.merges[-1]))

    def finish(self, *args):
        super().finish(*args)
        self.events.append(("finish", dict(self.invocations[args[0]])))

    def round(self, *args):
        super().round(*args)
        self.events.append(("round", self.outer_transitions[-1]))


def traced_emitter(native, mode="production", **schedule):
    trace = Timeline()
    tree = _clone_tree(native, mode=mode, trace=True, **schedule)
    namespace = vars(native).copy()
    namespace.update(_closure_audit_trace=trace,
                     _closure_audit_queue=lambda ident, pending, successor: _record_queue(trace, ident, pending, successor),
                     _closure_audit_round=lambda target, previous, updated: _record_round(target, previous, updated))
    exec(compile(tree, f"<{mode}-queue-replay>", "exec"), namespace)
    return namespace["emit_x86_64_linux"], trace


def normalize(state):
    return {name: fact for name, fact in state.items() if fact != (set(), False)}


def transfer(state, event, *, normalized=False):
    """Independent transfer model, including the sticky RETURN accumulator input."""
    result = dict(state)
    op, args, dest = event["op"], event["args"], event["dest"]
    default = (set(), False)
    if op == "LOADVAR" and dest:
        result[dest] = state.get(args[0], default)
    elif op == "STORE_LIST":
        result[args[0]] = state.get(args[1][0], default) if len(args[1]) == 1 else default
    elif op == "UPDATE":
        result[args[0]] = state.get(args[1], default)
    elif op == "CALL" and dest:
        target = event["constructor_target"]
        targets = {target} if target is not None else set(dict(event["known_returns"]).get(args[0], ()))
        result[dest] = (targets, bool(targets))
    elif op == "RETURN" and args:
        pass
    elif op != "LABEL" and dest:
        result[dest] = default
    return normalize(result) if normalized else result


def join(left, right, *, normalized=False):
    result = {}
    for name in left.keys() | right.keys():
        lt, lk = left.get(name, (set(), False))
        rt, rk = right.get(name, (set(), False))
        result[name] = (lt | rt, lk and rk)
    return normalize(result) if normalized else result


def accumulate(summary, state, event):
    targets, known, saw = summary
    if event["op"] == "RETURN" and event["args"]:
        rt, rk = state.get(event["args"][0], (set(), False))
        return (targets | rt if rk and rt else targets, known if rk and rt else False, True)
    return targets, known, saw


def edges(body, index, reverse):
    item = body[index]
    labels = {i.dest: n for n, i in enumerate(body) if i.op == "LABEL" and i.dest}
    target = labels.get(item.args[0]) if item.op in {"JUMP", "JUMPF"} else None
    following = [index + 1] if index + 1 < len(body) else []
    if item.op == "JUMP":
        result = [target] if target is not None else []
    elif item.op == "JUMPF":
        result = following + ([target] if target is not None else [])
    elif item.op in {"RETURN", "STOP"}:
        result = []
    else:
        result = following
    return list(reversed(result)) if reverse else result


def replay(trace, *, fifo=False, reverse_successors=False, normalized=False):
    """Reconstruct EVERY event, including all events after autonomous divergence.

    Shadow normalized states never decide the queue. Dense changes do. Any
    unexpected/missing event, wrong predecessor, state, accumulator or install
    fails closed. Empty-body invocations and rounds with no eligible calls work.
    With normalized=True the reference also normalizes writes/joins, validating
    the autonomous candidate queue instead of imposing dense scheduling.
    """
    errors, expected, details = [], [], []
    dense = shadow = None
    pending = []
    ds = ss = (set(), True, False)
    round_installs = {}
    installed = ()
    return_steps = []
    counts = Counter()
    active = None
    active_function = None

    def check(kind, actual, wanted):
        if actual != wanted:
            errors.append({"event": position, "kind": kind, "expected": _freeze(wanted), "observed": _freeze(actual)})

    for position, (kind, event) in enumerate(trace.events):
        counts[kind] += 1
        if kind == "begin":
            check("previous-invocation-finished", active, None)
            active = event["id"]
            active_function = event["function"]
            check("installed-summary-input", event["known_returns"], installed)
            if active not in trace.bodies:
                errors.append({"event": position, "kind": "unknown-invocation-id"})
                return {"valid": False, "errors": errors, "counts": dict(counts),
                        "representation_only_appends": details, "all_return_steps": return_steps}
            body = trace.bodies[active]
            dense = [None] * len(body)
            shadow = [None] * len(body)
            pending = [0] if body else []
            if body:
                dense[0], shadow[0] = {}, {}
            ds = ss = (set(), True, False)
            expected = [("queue", {"invocation": active, "event": "seed", "queue": (0,)})] if body else []
        elif kind == "queue" and event["event"] == "pop":
            check("undrained-successor-events", expected, [])
            if not pending:
                errors.append({"event": position, "kind": "unexpected-pop"})
                continue
            index = pending.pop(0 if fifo else -1)
            check("dequeue", event, {"invocation": active, "event": "pop", "index": index, "queue": tuple(pending)})
            expected = [("visit-index", index)]
        elif kind == "visit":
            check("visit-correspondence", expected, [("visit-index", event["index"])])
            check("visit-invocation", event["invocation"], active)
            check("visit-summary-input", event["known_returns"], installed)
            index = event["index"]
            if not isinstance(index, int) or index < 0 or index >= len(body):
                errors.append({"event": position, "kind": "invalid-visit-index"})
                return {"valid": False, "errors": errors, "counts": dict(counts),
                        "representation_only_appends": details, "all_return_steps": return_steps}
            item = body[index]
            check("instruction", (event["op"], event["args"], event["dest"]), (item.op, _freeze(item.args), item.dest))
            incoming, normalized_incoming = dense[index], shadow[index]
            check("dense-incoming", event["incoming"], _freeze(incoming))
            check("normalized-incoming", normalize(incoming), normalized_incoming)
            outgoing = transfer(incoming, event, normalized=normalized)
            normalized_outgoing = transfer(normalized_incoming, event, normalized=True)
            check("dense-transfer", event["outgoing"], _freeze(outgoing))
            check("shadow-transfer", normalize(outgoing), normalized_outgoing)
            previous = ds
            ds, ss = accumulate(ds, outgoing, event), accumulate(ss, normalized_outgoing, event)
            check("returned-update", event["return_state"], _freeze(ds))
            check("shadow-returned-update", ds, ss)
            check("visit-queue", event["queue"], tuple(pending))
            expected = []
            for successor in edges(body, index, reverse_successors):
                current, normalized_current = dense[successor], shadow[successor]
                if current is None:
                    dense[successor], shadow[successor] = dict(outgoing), dict(normalized_outgoing)
                    pending.append(successor)
                    expected.append(("queue", {"invocation": active, "event": "append", "successor": successor, "queue": tuple(pending)}))
                    counts["first_reach_appends"] += 1
                else:
                    merged = join(current, outgoing, normalized=normalized)
                    normalized_merged = join(normalized_current, normalized_outgoing, normalized=True)
                    check("shadow-merge", normalize(merged), normalized_merged)
                    changed = merged != current
                    expected.append(("merge", {"invocation": active, "index": index, "successor": successor,
                                              "current": _freeze(current), "incoming": _freeze(outgoing), "merged": _freeze(merged),
                                              "changed": changed, "queue_before": tuple(pending)}))
                    if changed:
                        representation_only = normalized_merged == normalized_current
                        counts["representation_only_appends" if representation_only else "semantic_appends"] += 1
                        if representation_only:
                            details.append({"invocation": active, "from": index, "to": successor,
                                            "event": position, "queue_before": tuple(pending),
                                            "dense_before": _freeze(current), "dense_after": _freeze(merged),
                                            "normalized": _freeze(normalized_merged)})
                        dense[successor], shadow[successor] = merged, normalized_merged
                        pending.append(successor)
                        expected.append(("queue", {"invocation": active, "event": "append", "successor": successor, "queue": tuple(pending)}))
            counts["shadow_visits"] += 1
            if event["op"] == "RETURN":
                counts["shadow_returns"] += 1
                return_steps.append({"event": position, "invocation": active, "index": index,
                                     "dense_before": _freeze(previous), "dense_after": _freeze(ds),
                                     "shadow_after": _freeze(ss), "normalized_input": _freeze(normalized_outgoing)})
        elif kind in {"queue", "merge"}:
            if expected:
                check("successor-event", (kind, event), expected.pop(0))
            else:
                errors.append({"event": position, "kind": "unexpected-successor-event", "observed": (kind, event)})
        elif kind == "finish":
            check("invocation-finish", event["id"], active)
            check("invocation-function", event["function"], active_function)
            check("finish-summary-input", event["known_returns"], installed)
            check("complete-successor-events", expected, [])
            check("queue-exhausted", pending, [])
            check("final-summary", event["result"], _freeze(ds))
            check("shadow-summary", ds, ss)
            check("final-dense-states", event["final_states"], _freeze(dense) if body else None)
            check("final-shadow-states", _normalized_final_states(event["final_states"]), _freeze(shadow) if body else None)
            if ds[0] and ds[1] and ds[2]:
                round_installs[active_function] = ds[0]
            active = None
        elif kind == "round":
            check("round-after-finish", active, None)
            check("previous-installed-summary", event["previous"], installed)
            check("summary-installation", event["updated"], _freeze(round_installs))
            if event["previous"] == event["updated"]:
                check("stop-after-convergence", position, len(trace.events) - 1)
            installed = event["updated"]
            round_installs = {}
        else:
            errors.append({"event": position, "kind": "unknown-event", "observed": kind})
    position = len(trace.events)
    check("final-round-present", trace.events[-1][0] if trace.events else None, "round")
    check("complete-timeline", (active, expected, pending, round_installs), (None, [], [], {}))
    return {"valid": not errors, "errors": errors, "counts": dict(counts),
            "representation_only_appends": details, "all_return_steps": return_steps}


def correspondence(production, candidate):
    """Match by invocation ordinal and instruction/edge occurrence, not zip-prefix.

    Extra occurrences remain explicitly unmatched. Matched occurrences may have
    different inputs/accumulators; matching a key is NOT semantic correspondence.
    """
    def index(trace):
        ids, ordinals = {}, Counter()
        for rec in trace.invocations:
            key = (rec["function"], rec["known_returns"])
            ids[rec["id"]] = key + (ordinals[key],)
            ordinals[key] += 1
        indexed, occurrences = {}, Counter()
        for offset, (kind, e) in enumerate(trace.events):
            if kind not in {"queue", "visit", "merge"}:
                continue
            site = (ids[e["invocation"]], kind, e.get("event"), e.get("index"), e.get("successor"))
            key = site + (occurrences[site],)
            occurrences[site] += 1
            indexed[key] = (offset, e)
        return indexed

    left, right = index(production), index(candidate)
    counts, returns, mismatches, transition_differences = Counter(), [], [], []
    for key in sorted(left.keys() | right.keys(), key=repr):
        a, b = left.get(key), right.get(key)
        status = "matched" if a and b else "production_only" if a else "candidate_only"
        counts[status] += 1
        if status != "matched":
            mismatches.append({"key": key, "status": status, "production": a, "candidate": b})
        else:
            def normalized_view(item):
                result = dict(item[1])
                for field in ("incoming", "outgoing", "current", "merged"):
                    if field in result:
                        result[field] = _elide_unknown(result[field])
                return result
            av, bv = normalized_view(a), normalized_view(b)
            if av != bv:
                counts["matched_transition_differences"] += 1
                transition_differences.append({"key": key, "production_event": a[0], "candidate_event": b[0],
                                               "differences": {f: {"production": av.get(f), "candidate": bv.get(f)}
                                                               for f in av.keys() | bv.keys() if av.get(f) != bv.get(f)}})
        if key[1] == "visit" and ((a and a[1]["op"] == "RETURN") or (b and b[1]["op"] == "RETURN")):
            def view(item):
                if item is None:
                    return None
                offset, e = item
                return {"event": offset, "incoming_normalized": _elide_unknown(e["incoming"]), "return_state": e["return_state"], "queue": e["queue"]}
            av, bv = view(a), view(b)
            equal = bool(a and b and av["incoming_normalized"] == bv["incoming_normalized"] and av["return_state"] == bv["return_state"])
            returns.append({"key": key, "status": status, "same_state_and_accumulator": equal, "production": av, "candidate": bv})
            counts["return_matches" if equal else "return_differences"] += 1
    first = None
    for offset in range(max(len(production.events), len(candidate.events))):
        a = production.events[offset] if offset < len(production.events) else None
        b = candidate.events[offset] if offset < len(candidate.events) else None
        # Compare scheduling only here; representation differences aren't divergence.
        def control(item):
            if item is None:
                return None
            kind, event = item
            return kind, event.get("invocation", event.get("id")), event.get("event"), event.get("index"), event.get("successor"), event.get("queue")
        if control(a) != control(b):
            first = {"event": offset, "production": a, "candidate": b}
            break
    return {"counts": dict(counts), "first_control_divergence": first,
            "all_unmatched_events": mismatches, "all_return_correspondences": returns,
            "all_matched_transition_differences": transition_differences,
            "matching_policy": "invocation (function, known_returns, ordinal), event site, occurrence; not a proof of matching histories"}


def corpus():
    from scripts.profile_sparse_closures import closure_edge_workloads, negative_workload, sparse_workload
    from scripts.closure_queue_cases import (
        bounded_adversarial_cases, minimal_sticky_return_program, layout_swapped_predecessor_program,
    )
    cases = {f"generated_{i}_{mode}": generated_graph_workload(311 + i * 17, mode)
             for i, mode in enumerate(("known", "missing", "scalar") * 4)}
    cases.update({f"multibackedge_{i}": multibackedge_workload(i) for i in range(3)})
    cases.update(closure_edge_workloads())
    cases.update(recursive_return_calls=recursive_return_workload(), negative_mixed_return=negative_workload(),
                 small_recursive_join_cfg=sparse_workload(size=8, random_cases=1, seed=442))
    cases.update(bounded_adversarial_cases())
    cases.update(compact_sticky_return=minimal_sticky_return_program(),
                 swapped_predecessor_layout=layout_swapped_predecessor_program())
    return cases


def audit(*, include_timelines=False):
    import compiler.native as native
    schedules = {"lifo_forward": {}, "fifo_forward": {"fifo": True},
                 "lifo_reverse": {"reverse_successors": True}, "fifo_reverse": {"fifo": True, "reverse_successors": True}}
    cases, counts = [], Counter()
    for name, program in corpus().items():
        for order, schedule in schedules.items():
            runs = {}
            outcomes = {}
            for mode in ("production", "normalized"):
                emitter, trace = traced_emitter(native, mode, **schedule)
                outcomes[mode] = _outcome(emitter, program, native)
                runs[mode] = trace
            proof = replay(runs["production"], **schedule)
            autonomous = replay(runs["normalized"], normalized=True, **schedule)
            from scripts.audit_normalized_closures import compare_traces, validate_trace
            compare = compare_traces(runs["production"], runs["normalized"])
            links = correspondence(runs["production"], runs["normalized"])
            item = {"case": name, "order": order, "production_replay": proof,
                    "autonomous_queue_replay": autonomous,
                    "autonomous_validation": validate_trace(runs["normalized"]),
                    "outcomes_equal": outcomes["production"] == outcomes["normalized"],
                    "outcomes": {m: _outcome_digest(o) for m, o in outcomes.items()},
                    "exact_invocation_summaries_equal": compare["equivalent_invocation_summaries"],
                    "summary_differences": compare["summary_differences"],
                    "outer_transitions_equal": compare["outer_transitions_equal"],
                    "return_sequence_difference_count": compare["return_summary_event_sequence_difference_count"],
                    "correspondence": links,
                    "timeline_sha256": {m: hashlib.sha256(json.dumps(t.events, sort_keys=True).encode()).hexdigest() for m, t in runs.items()}}
            if include_timelines:
                item["timelines"] = {m: t.events for m, t in runs.items()}
            cases.append(item)
            counts.update(proof["counts"])
            counts["return_sequence_differences"] += item["return_sequence_difference_count"]
            counts["cases_with_control_divergence"] += links["first_control_divergence"] is not None
            counts["unmatched_events"] += len(links["all_unmatched_events"])
    return {"case_count": len(cases) // len(schedules), "comparison_count": len(cases), "order_count": len(schedules),
            "all_production_replays_valid": all(c["production_replay"]["valid"] for c in cases),
            "all_autonomous_queue_replays_valid": all(c["autonomous_queue_replay"]["valid"] for c in cases),
            "all_autonomous_transfers_valid": all(c["autonomous_validation"]["valid"] for c in cases),
            "all_outcomes_equal": all(c["outcomes_equal"] for c in cases),
            "all_exact_invocation_summaries_equal": all(c["exact_invocation_summaries_equal"] for c in cases),
            "all_outer_transitions_equal": all(c["outer_transitions_equal"] for c in cases),
            "scheduling_equivalence_proven": False, "production_promotion_allowed": False,
            "counts": dict(counts), "cases": cases}


def compact(result):
    """Keep counts and first witnesses; hash complete lists retained in gzip."""
    from copy import deepcopy
    result = deepcopy(result)
    def digest(value):
        return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()
    for case in result["cases"]:
        for name in ("production_replay", "autonomous_queue_replay"):
            proof = case[name]
            for field in ("representation_only_appends", "all_return_steps"):
                records = proof.pop(field)
                proof[field + "_count"] = len(records)
                proof[field + "_sha256"] = digest(records)
                proof[field + "_first"] = records[0] if records else None
        links = case["correspondence"]
        links["first_return_difference"] = next((e for e in links["all_return_correspondences"]
                                                if not e["same_state_and_accumulator"]), None)
        for field in ("all_unmatched_events", "all_return_correspondences", "all_matched_transition_differences"):
            records = links.pop(field)
            links[field + "_count"] = len(records)
            links[field + "_sha256"] = digest(records)
            links[field + "_first"] = records[0] if records else None
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--full-output", type=Path)
    parser.add_argument("--evidence-output", type=Path, help="Complete non-timeline evidence as gzip JSON")
    args = parser.parse_args()
    result = audit(include_timelines=bool(args.full_output))
    if args.full_output:
        args.full_output.write_text(json.dumps(result, indent=2) + "\n")
        for case in result["cases"]:
            case.pop("timelines")
    import compiler.native as native
    result["source_sha256"] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                               for p in (Path(native.__file__), Path(__file__), ROOT / "scripts/audit_normalized_closures.py", ROOT / "scripts/closure_queue_cases.py",
                                         ROOT / "scripts/profile_sparse_closures.py")}
    if args.evidence_output:
        payload = (json.dumps(result, separators=(",", ":")) + "\n").encode()
        args.evidence_output.write_bytes(gzip.compress(payload, mtime=0))
    args.output.write_text(json.dumps(compact(result), indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k not in {"cases", "source_sha256"}}, indent=2), flush=True)
    assert result["all_production_replays_valid"] and result["all_autonomous_queue_replays_valid"] and result["all_autonomous_transfers_valid"]


if __name__ == "__main__":
    main()
