#!/usr/bin/env python3
"""Independent, fail-closed causal replay of closure-return worklist histories.

This diagnostic deliberately compares histories; it does not claim scheduling or
semantic equivalence. Transfer/join rules are reimplemented locally (the rules
are also documented in replay_closure_queue.py and audit_normalized_closures.py).
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque
import gzip
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.audit_normalized_closures import _freeze, _elide_unknown
from scripts.replay_closure_queue import traced_emitter, edges as _edges


def _norm(state):
    return {name: fact for name, fact in state.items() if fact != (set(), False)}


def _encode(value):
    return _freeze(value)


def _constructor_facts(body, function_names):
    """Reconstruct immutable MakeClosure call-site facts from the IR body."""
    text, constructors = {}, {}
    for index, ins in enumerate(body):
        op, args, dest = ins.op, ins.args, ins.dest
        if op == "CONST" and dest:
            if args and isinstance(args[0], str):
                text[dest] = args[0]
            else:
                text.pop(dest, None)
        elif op == "LOADVAR" and dest:
            if args[0] in text:
                text[dest] = text[args[0]]
            else:
                text.pop(dest, None)
        elif op == "STORE_LIST":
            name, values = args
            if len(values) == 1 and values[0] in text:
                text[name] = text[values[0]]
            else:
                text.pop(name, None)
        elif op == "UPDATE":
            name, value = args
            if value in text:
                text[name] = text[value]
            else:
                text.pop(name, None)
        elif op == "CALL":
            if (args[0] == "MakeClosure" and len(args) == 2 and args[1] in text
                    and text[args[1]] in function_names):
                constructors[index] = text[args[1]]
            if dest:
                text.pop(dest, None)
        elif op != "LABEL" and dest:
            text.pop(dest, None)
    return constructors


def _fact_map(frozen):
    return {name: (set(targets), known) for name, (targets, known) in frozen}


def _transfer(state, ins, known_returns, constructors, index, normalized):
    out = dict(state)
    op, args, dest = ins.op, ins.args, ins.dest
    absent = (set(), False)
    if op == "LOADVAR" and dest:
        out[dest] = state.get(args[0], absent)
    elif op == "STORE_LIST":
        out[args[0]] = state.get(args[1][0], absent) if len(args[1]) == 1 else absent
    elif op == "UPDATE":
        out[args[0]] = state.get(args[1], absent)
    elif op == "CALL" and dest:
        target = constructors.get(index)
        targets = {target} if target is not None else set(known_returns.get(args[0], ()))
        out[dest] = (targets, bool(targets))
    elif op != "RETURN" and op != "LABEL" and dest:
        out[dest] = absent
    return _norm(out) if normalized else out


def _join(left, right, normalized):
    merged = {}
    for name in left.keys() | right.keys():
        lt, lk = left.get(name, (set(), False))
        rt, rk = right.get(name, (set(), False))
        merged[name] = (lt | rt, lk and rk)
    return _norm(merged) if normalized else merged


def simulate(function, known_returns, all_function_names, *, normalized=False,
             fifo=False, reverse_successors=False):
    """Run an independently reconstructed invocation; queue tokens carry causes."""
    body = function.body
    constructors = _constructor_facts(body, all_function_names)
    labels = {ins.dest: i for i, ins in enumerate(body) if ins.op == "LABEL" and ins.dest}
    outgoing_edges = []
    for i, ins in enumerate(body):
        nxt = [i + 1] if i + 1 < len(body) else []
        if ins.op == "JUMP":
            nxt = [labels[ins.args[0]]] if ins.args[0] in labels else []
        elif ins.op == "JUMPF":
            target = labels.get(ins.args[0])
            nxt = nxt + ([target] if target is not None else [])
        elif ins.op in {"RETURN", "STOP"}:
            nxt = []
        outgoing_edges.append(list(reversed(nxt)) if reverse_successors else nxt)

    events, nodes, suppressed, returns = [], {}, [], []
    node_no = 0
    def node(kind, parents=(), **data):
        nonlocal node_no
        node_no += 1
        ident = node_no
        nodes[ident] = {"id": ident, "kind": kind, "parents": tuple(parents), **data}
        return ident
    def path(token, limit=24):
        result, seen = [], set()
        todo = [token] if token is not None else []
        while todo and len(result) < limit:
            current = todo.pop(0)
            if current in seen or current not in nodes:
                continue
            seen.add(current)
            record = nodes[current]
            result.append({k: v for k, v in record.items() if k != "parents"})
            todo[0:0] = list(record["parents"])
        return result
    pending = []
    states = [None] * len(body)
    summary = (set(), True, False)
    if body:
        states[0] = {}
        seed = node("seed", index=0)
        pending.append((0, seed))
        events.append(("queue", {"event": "seed", "queue": (0,)}))
    while pending:
        idx, queue_token = pending.pop(0 if fifo else -1)
        events.append(("queue", {"event": "pop", "index": idx,
                                  "queue": tuple(item[0] for item in pending)}))
        visit_token = node("visit", (queue_token,), index=idx)
        incoming = states[idx]
        ins = body[idx]
        out = _transfer(incoming, ins, known_returns, constructors, idx, normalized)
        old_summary = summary
        if ins.op == "RETURN" and ins.args:
            targets, known = out.get(ins.args[0], (set(), False))
            if known and targets:
                summary = (summary[0] | targets, summary[1], True)
            else:
                summary = (summary[0], False, True)
        visit_event = {"index": idx, "op": ins.op, "args": _freeze(ins.args), "dest": ins.dest,
                       "incoming": _freeze(incoming), "outgoing": _freeze(out),
                       "return_state": (_freeze(summary[0]), summary[1], summary[2]),
                       "known_returns": _freeze(known_returns),
                       "constructor_target": constructors.get(idx),
                       "queue": tuple(item[0] for item in pending)}
        events.append(("visit", visit_event))
        if ins.op == "RETURN":
            returns.append({"index": idx, "incoming": _freeze(incoming),
                            "outgoing": _freeze(out), "return_state": visit_event["return_state"],
                            "event_ordinal": len(returns), "causal_token": visit_token,
                            "causal_path": path(visit_token)})
        for successor in outgoing_edges[idx]:
            current = states[successor]
            if current is None:
                states[successor] = dict(out)
                update_token = node("first_reach", (visit_token,), source=idx, target=successor,
                                    incoming=_freeze(out), result=_freeze(out))
                pending.append((successor, update_token))
                events.append(("queue", {"event": "append", "successor": successor,
                                          "queue": tuple(item[0] for item in pending)}))
                continue
            merged = _join(current, out, normalized)
            changed = merged != current
            events.append(("merge", {"index": idx, "successor": successor,
                                      "current": _freeze(current), "incoming": _freeze(out),
                                      "merged": _freeze(merged), "changed": changed,
                                      "queue_before": tuple(item[0] for item in pending)}))
            if changed:
                rep_only = _norm(merged) == _norm(current)
                update_token = node("representation_only_update" if rep_only else "semantic_update",
                                    (visit_token,), source=idx, target=successor,
                                    current=_freeze(current), incoming=_freeze(out), result=_freeze(merged))
                if rep_only:
                    suppressed.append({"source": idx, "target": successor,
                                       "event_ordinal": len(suppressed), "token": update_token,
                                       "causal_path": path(update_token),
                                       "current": _freeze(current), "merged": _freeze(merged)})
                states[successor] = merged
                pending.append((successor, update_token))
                events.append(("queue", {"event": "append", "successor": successor,
                                          "queue": tuple(item[0] for item in pending)}))
    return {"valid": True, "events": events, "returns": returns, "suppressed_appends": suppressed,
            "final_summary": (_freeze(summary[0]), summary[1], summary[2]),
            "final_states": tuple(None if s is None else _freeze(s) for s in states),
            "nodes": nodes, "constructor_facts": constructors}


def _events_for_invocation(trace, ident):
    return [(kind, {k: v for k, v in event.items() if k != "invocation"})
            for kind, event in trace.events if event.get("invocation", event.get("id")) == ident
            and kind in {"queue", "visit", "merge"}]


def validate_invocations(trace, program, *, normalized=False, fifo=False, reverse_successors=False,
                         corrupt=None):
    """Compare complete reconstructed invocation streams against actual trace."""
    failures, simulations = [], {}
    by_name = program.functions
    for record in trace.invocations:
        name = record["function"]
        if name not in by_name:
            failures.append({"invocation": record["id"], "kind": "unknown-function", "function": name})
            continue
        known = {k: set(v) for k, v in record["known_returns"]}
        reconstructed = simulate(by_name[name], known, set(by_name), normalized=normalized,
                                 fifo=fifo, reverse_successors=reverse_successors)
        actual = _events_for_invocation(trace, record["id"])
        expected = reconstructed["events"]
        if corrupt == "drop-append" and expected:
            expected = list(expected)
            pos = next((i for i, (kind, event) in enumerate(expected)
                        if kind == "queue" and event.get("event") == "append"), None)
            if pos is not None:
                expected.pop(pos)
        if actual != expected:
            limit = min(len(actual), len(expected))
            offset = next((i for i in range(limit) if actual[i] != expected[i]), limit)
            failures.append({"invocation": record["id"], "function": name, "kind": "event-stream",
                             "first_offset": offset, "actual_count": len(actual), "expected_count": len(expected),
                             "actual": _freeze(actual[offset]) if offset < len(actual) else None,
                             "expected": _freeze(expected[offset]) if offset < len(expected) else None})
        simulations[record["id"]] = reconstructed
        if record.get("result") != reconstructed["final_summary"]:
            failures.append({"invocation": record["id"], "function": name, "kind": "final-summary"})
        if record.get("final_states") != reconstructed["final_states"]:
            failures.append({"invocation": record["id"], "function": name, "kind": "final-states"})
    return {"valid": not failures, "failures": failures, "simulations": simulations}


def _invocation_groups(trace):
    groups, ordinals = {}, Counter()
    for record in trace.invocations:
        key = (record["function"], record["known_returns"])
        ordinal = ordinals[key]
        ordinals[key] += 1
        groups[(key, ordinal)] = record
    return groups


def _return_seq(sim):
    return [r["return_state"] for r in sim["returns"]]


def _reachability(body, start, target):
    from scripts.replay_closure_queue import edges
    pending, seen = [start], set()
    while pending:
        current = pending.pop()
        if current == target:
            return True
        if current in seen or current < 0 or current >= len(body):
            continue
        seen.add(current)
        pending.extend(edges(body, current, False))
    return False


def pair_histories(program, dense_trace, normalized_trace, dense_sims, normalized_sims):
    """Pair ordinal histories without treating matching keys as equivalence."""
    left, right = _invocation_groups(dense_trace), _invocation_groups(normalized_trace)
    pairs, differing, records = [], 0, []
    for key in sorted(set(left) | set(right), key=repr):
        a, b = left.get(key), right.get(key)
        sa = dense_sims.get(a["id"]) if a else None
        sb = normalized_sims.get(b["id"]) if b else None
        ar, br = sa["returns"] if sa else [], sb["returns"] if sb else []
        seq_a, seq_b = _return_seq(sa) if sa else [], _return_seq(sb) if sb else []
        different = seq_a != seq_b
        if different:
            differing += 1
        pair = {"invocation_key": key, "status": "paired" if a and b else "dense_only" if a else "normalized_only",
                "return_sequence_differs": different, "dense_return_count": len(ar), "normalized_return_count": len(br),
                "dense_returns": [], "normalized_returns": []}
        function = program.functions.get(key[0][0])
        # An unqueued normalized RETURN can have no local provenance from the
        # suppressed update; pair each RETURN with bounded dense suppression
        # witnesses whose updated target can reach that RETURN in the CFG.
        suppression = sa["suppressed_appends"] if sa else []
        for side, side_returns in (("dense", ar), ("normalized", br)):
            for ret in side_returns:
                candidate_suppressions = [s for s in suppression if function and
                                          _reachability(function.body, s["target"], ret["index"])]
                witnesses = candidate_suppressions[-4:]
                pair[side + "_returns"].append({
                    "index": ret["index"], "return_state": ret["return_state"],
                    "exact_incoming": ret["incoming"], "exact_outgoing": ret["outgoing"],
                    "return_event_ordinal": ret["event_ordinal"],
                    "direct_queue_causal_path": ret["causal_path"],
                    "representation_suppression_witnesses": [{
                        "source": item["source"], "target": item["target"],
                        "changed_history_path": item["causal_path"],
                        "dense_current": item["current"], "dense_merged": item["merged"],
                        "normalized_change_suppressed": True,
                    } for item in witnesses],
                    "causal_limit": "CFG reachability plus event ancestry is diagnostic provenance, not a proof that this update alone caused the return difference",
                })
        pairs.append(pair)
        if different:
            records.append(pair)
    return {"paired_invocation_count": len(pairs), "return_sequence_difference_count": differing,
            "pairs": pairs, "differing_pairs": records,
            "matching_policy": "(function, installed known-return map, invocation ordinal); pairing identifies histories, not equivalence"}


def audit_corpus(*, schedules=None, corrupt=None):
    import compiler.native as native
    from scripts.replay_closure_queue import corpus
    schedules = schedules or {"lifo_forward": {}, "fifo_forward": {"fifo": True},
                              "lifo_reverse": {"reverse_successors": True},
                              "fifo_reverse": {"fifo": True, "reverse_successors": True}}
    report = {"cases": [], "counts": Counter(), "valid": True,
              "scope": "bounded inherited closure queue corpus; no equivalence claim"}
    for case_name, program in corpus().items():
        for order, options in schedules.items():
            modes = {}
            for mode, normalized in (("dense", False), ("normalized", True)):
                from scripts.audit_normalized_closures import _outcome
                emitter, trace = traced_emitter(native, "normalized" if normalized else "production", **options)
                _outcome(emitter, program, native)
                validation = validate_invocations(trace, program, normalized=normalized,
                                                  fifo=options.get("fifo", False),
                                                  reverse_successors=options.get("reverse_successors", False),
                                                  corrupt=corrupt if mode == "dense" else None)
                modes[mode] = (trace, validation)
            dense_trace, dense_validation = modes["dense"]
            norm_trace, norm_validation = modes["normalized"]
            dsims, nsims = dense_validation["simulations"], norm_validation["simulations"]
            paired = pair_histories(program, dense_trace, norm_trace, dsims, nsims)
            from scripts.replay_closure_queue import replay
            from scripts.replay_closure_queue import correspondence
            from scripts.audit_normalized_closures import compare_traces
            links = correspondence(dense_trace, norm_trace)
            reference = compare_traces(dense_trace, norm_trace)
            production_only_returns = sum(
                item["status"] == "production_only"
                and item["key"][1] == "visit"
                and item["production"] is not None
                and item["production"][1].get("op") == "RETURN"
                for item in links["all_unmatched_events"])
            paired_return_differences = sum(
                item["status"] == "matched" and not item["same_state_and_accumulator"]
                for item in links["all_return_correspondences"])
            paired_return_observations = sum(
                item["status"] == "matched" for item in links["all_return_correspondences"])
            dense_replay = replay(dense_trace, fifo=options.get("fifo", False),
                                  reverse_successors=options.get("reverse_successors", False))
            norm_replay = replay(norm_trace, normalized=True, fifo=options.get("fifo", False),
                                 reverse_successors=options.get("reverse_successors", False))
            exact_count_match = paired["return_sequence_difference_count"] == reference["return_summary_event_sequence_difference_count"]
            valid = (dense_validation["valid"] and norm_validation["valid"] and dense_replay["valid"]
                     and norm_replay["valid"] and exact_count_match)
            report["valid"] &= valid
            report["counts"]["case_schedule_pairs"] += 1
            report["counts"]["return_sequence_differences"] += paired["return_sequence_difference_count"]
            report["counts"]["paired_differing_invocations"] += sum(
                x["status"] == "paired" and x["return_sequence_differs"] for x in paired["pairs"])
            report["counts"]["production_only_return_observations"] += production_only_returns
            report["counts"]["paired_differing_return_observations"] += paired_return_differences
            report["counts"]["paired_return_observations"] += paired_return_observations
            report["counts"]["paired_invocations"] += paired["paired_invocation_count"]
            report["counts"]["representation_only_dense_appends"] += sum(
                len(sim["suppressed_appends"]) for sim in dsims.values())
            report["counts"]["independent_dense_events_valid"] += dense_validation["valid"]
            report["counts"]["independent_normalized_events_valid"] += norm_validation["valid"]
            report["counts"]["production_replay_valid"] += dense_replay["valid"]
            report["counts"]["autonomous_replay_valid"] += norm_replay["valid"]
            report["cases"].append({"case": case_name, "schedule": order, "valid": valid,
                                    "reference_difference_count": reference["return_summary_event_sequence_difference_count"],
                                    "independent_difference_count": paired["return_sequence_difference_count"],
                                    "paired_differing_invocations": sum(
                                        x["status"] == "paired" and x["return_sequence_differs"] for x in paired["pairs"]),
                                    "paired_differing_return_observations": paired_return_differences,
                                    "paired_return_observations": paired_return_observations,
                                    "production_only_return_observations": production_only_returns,
                                    "dense_failures": dense_validation["failures"],
                                    "normalized_failures": norm_validation["failures"],
                                    "paired": paired})
    report["counts"] = dict(report["counts"])
    report["all_histories_valid"] = report["valid"]
    report["equivalence_proven"] = False
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True,
                        help="write compact JSON counts and per-comparison digests")
    parser.add_argument("--evidence-output", type=Path,
                        help="optional gzip JSON containing detailed return provenance")
    parser.add_argument("--corrupt", choices=("drop-append",), help="test fail-closed validation control")
    args = parser.parse_args()
    result = audit_corpus(corrupt=args.corrupt)
    if args.evidence_output:
        args.evidence_output.write_bytes(gzip.compress(
            (json.dumps(result, separators=(",", ":")) + "\n").encode(), mtime=0))
    compact_cases = [{k: v for k, v in case.items() if k not in {"paired", "dense_failures", "normalized_failures"}}
                     | {"paired_detail_sha256": hashlib.sha256(
                         json.dumps(case["paired"], sort_keys=True).encode()).hexdigest(),
                        "differing_invocation_keys": [x["invocation_key"]
                                                      for x in case["paired"]["differing_pairs"]]}
                     for case in result["cases"]]
    compact = {k: v for k, v in result.items() if k != "cases"}
    compact["cases"] = compact_cases
    args.output.write_text(json.dumps(compact, indent=2) + "\n")
    print(json.dumps({k: v for k, v in compact.items() if k != "cases"}
                     | {"case_records": len(compact_cases)}, indent=2))
    if not result["valid"] and not args.corrupt:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
