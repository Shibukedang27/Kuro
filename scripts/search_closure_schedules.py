#!/usr/bin/env python3
"""Bounded deterministic search for same-schedule closure-summary divergence.

This is an empirical corpus search, not a proof of equivalence. It compares the
production emitter with the test-only normalized AST clone under FIFO/LIFO and
forward/reversed successor orders. No production source is patched.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.audit_normalized_closures import make_emitter
from scripts.audit_normalized_closures import recursive_return_workload
from scripts.closure_queue_cases import bounded_adversarial_cases
from scripts.profile_sparse_closures import generated_graph_workload


def _ins(op, *args, dest=None):
    from compiler.ir import Instr
    return Instr(op, tuple(args), dest)


def _fn(name, *body):
    from compiler.ir import IRFunction
    return IRFunction(name, [], list(body))


def minimal_same_order_return_accumulator_witness():
    """Reduced forward-branch witness: RETURN steps differ, final result does not.

    One branch writes an absent local over a known closure. The sticky
    accumulator's intermediate transition depends on which incoming facts have
    reached the RETURN instruction; this does not change the final function
    summary or native error.
    """
    from compiler.ir import IRProgram

    target = _fn("AccumulatorWitnessTarget", _ins("CONST", 1, dest="n"), _ins("RETURN", "n"))
    body = [
        _ins("CONST", "AccumulatorWitnessTarget", dest="target"),
        _ins("CALL", "MakeClosure", "target", dest="known"),
        _ins("LOADVAR", "known", dest="selected"),
        _ins("CONST", 1, dest="condition"),
        _ins("JUMPF", "exit", "condition"),
        _ins("CONST", 1, dest="branch"),
        _ins("JUMPF", "missing_arm", "branch"),
        _ins("LOADVAR", "absent", dest="selected"),
        _ins("LABEL", dest="missing_arm"),
        _ins("LABEL", dest="exit"),
        _ins("RETURN", "selected"),
    ]
    function = _fn("AccumulatorWitness", *body)
    main = [_ins("CALL", "AccumulatorWitness", dest="c"), _ins("CALL", "Invoke", "c", dest="r")]
    return IRProgram(main=main, functions={target.name: target, function.name: function})


def minimal_final_summary_counterexample():
    """Reduced CFG from seed 13: normalized and production summaries diverge.

    Under LIFO with reversed successors the graph function returns a different
    sticky target set in the first analyzer invocation. The complete native
    emitter outcome remains the same native error in both modes.
    """
    from compiler.ir import IRProgram

    target_name, graph_name = "SummaryTarget", "SummaryWitness"
    rec_a, rec_b = "SummaryRecA", "SummaryRecB"
    target = _fn(target_name, _ins("CONST", 16, dest="n"), _ins("RETURN", "n"))
    graph = _fn(graph_name,
        _ins("CONST", target_name, dest="target_a"),
        _ins("CALL", "MakeClosure", "target_a", dest="closure_a"),
        _ins("LOADVAR", "closure_a", dest="selected"),
        _ins("LABEL", dest="head"),
        _ins("JUMPF", "loop_exit", "loop_condition"),
        _ins("CONST", 0, dest="pick_a"),
        _ins("JUMPF", "arm_b", "pick_a"),
        _ins("JUMP", "head"),
        _ins("LABEL", dest="arm_b"),
        _ins("LOADVAR", "missing_loop", dest="selected"),
        _ins("LABEL", dest="loop_exit"),
        _ins("LOADVAR", "selected", dest="result"),
        _ins("RETURN", "result"),
    )
    functions = {
        target_name: target,
        graph_name: graph,
        rec_a: _fn(rec_a, _ins("CALL", rec_b, dest="from_b"), _ins("RETURN", "from_b")),
        rec_b: _fn(rec_b, _ins("CALL", rec_a, dest="recursive_call"),
                   _ins("CONST", target_name, dest="seed_target"),
                   _ins("CALL", "MakeClosure", "seed_target", dest="seed_closure"),
                   _ins("RETURN", "seed_closure")),
    }
    main = [_ins("CALL", graph_name, dest="graph_closure"),
            _ins("CALL", "Invoke", "graph_closure", dest="graph_value"),
            _ins("CALL", rec_a, dest="recursive_closure")]
    return IRProgram(main=main, functions=functions)


def adversarial_graph_workload(seed: int):
    """Generate a small valid IR program with joins, missing facts and 3 backedges."""
    from compiler.ir import IRProgram

    rng = random.Random(seed)
    suffix = str(seed)
    name = f"ScheduleGraph{suffix}"
    ta, tb = f"ScheduleTargetA{suffix}", f"ScheduleTargetB{suffix}"
    a, b = f"closure_a_{suffix}", f"closure_b_{suffix}"
    selected, result = f"selected_{suffix}", f"result_{suffix}"
    body = [
        _ins("CONST", ta, dest="target_a"), _ins("CALL", "MakeClosure", "target_a", dest=a),
        _ins("CONST", tb, dest="target_b"), _ins("CALL", "MakeClosure", "target_b", dest=b),
    ]
    # Small randomized pressure on aliases, overwrites, and missing-name facts.
    for layer in range(1 + seed % 4):
        right, join = f"right_{suffix}_{layer}", f"join_{suffix}_{layer}"
        condition = f"condition_{suffix}_{layer}"
        body.extend((_ins("CONST", rng.randrange(2), dest=condition),
                     _ins("JUMPF", right, condition)))
        left_source = rng.choice((a, b, f"absent_left_{layer}"))
        body.extend((_ins("LOADVAR", left_source, dest=selected),
                     _ins("JUMP", join), _ins("LABEL", dest=right)))
        right_source = rng.choice((a, b, f"absent_right_{layer}"))
        if rng.randrange(2):
            body.append(_ins("LOADVAR", right_source, dest=f"alias_{layer}"))
            body.append(_ins("UPDATE", selected, f"alias_{layer}"))
        else:
            body.append(_ins("LOADVAR", right_source, dest=selected))
        body.append(_ins("LABEL", dest=join))
        if rng.randrange(2):
            body.append(_ins("LOADVAR", f"never_defined_{layer}", dest=f"missing_{layer}"))

    # Three independent backedges rejoin at head; analyzer explores both sides
    # of constant branches. Aliasing and overwrite paths are intentionally mixed.
    head, arm_b, arm_c, loop_exit = (f"head_{suffix}", f"arm_b_{suffix}",
                                      f"arm_c_{suffix}", f"loop_exit_{suffix}")
    body.extend((
        _ins("LABEL", dest=head), _ins("CONST", 1, dest=f"loop_cond_{suffix}"),
        _ins("JUMPF", loop_exit, f"loop_cond_{suffix}"),
        _ins("CONST", rng.randrange(2), dest=f"pick_a_{suffix}"),
        _ins("JUMPF", arm_b, f"pick_a_{suffix}"), _ins("LOADVAR", a, dest=selected),
        _ins("JUMP", head), _ins("LABEL", dest=arm_b),
        _ins("CONST", rng.randrange(2), dest=f"pick_b_{suffix}"),
        _ins("JUMPF", arm_c, f"pick_b_{suffix}"), _ins("LOADVAR", b, dest=f"loop_alias_{suffix}"),
        _ins("UPDATE", selected, f"loop_alias_{suffix}"), _ins("JUMP", head),
        _ins("LABEL", dest=arm_c), _ins("LOADVAR", f"missing_loop_{suffix}", dest=selected),
        _ins("JUMP", head), _ins("LABEL", dest=loop_exit),
    ))
    # Distinct RETURN arms exercise the sticky target/all-known accumulator.
    body.extend((
        _ins("CONST", rng.randrange(2), dest=f"return_cond_{suffix}"),
        _ins("JUMPF", f"unknown_return_{suffix}", f"return_cond_{suffix}"),
        _ins("LOADVAR", selected, dest=result), _ins("RETURN", result),
        _ins("LABEL", dest=f"unknown_return_{suffix}"),
    ))
    mode = ("known", "missing", "scalar")[seed % 3]
    if mode == "known":
        body.extend((_ins("LOADVAR", b, dest=result), _ins("RETURN", result)))
    elif mode == "missing":
        body.extend((_ins("LOADVAR", f"absent_return_{suffix}", dest=result), _ins("RETURN", result)))
    else:
        body.extend((_ins("CONST", rng.randrange(20), dest=result), _ins("RETURN", result)))

    functions = {
        ta: _fn(ta, _ins("CONST", seed + 3, dest="n"), _ins("RETURN", "n")),
        tb: _fn(tb, _ins("CONST", seed + 7, dest="n"), _ins("RETURN", "n")),
        name: _fn(name, *body),
    }
    # Mutual recursion whose return summary changes as the direct seed propagates.
    rec_a, rec_b = f"ScheduleRecA{suffix}", f"ScheduleRecB{suffix}"
    functions[rec_a] = _fn(rec_a, _ins("CALL", rec_b, dest="from_b"), _ins("RETURN", "from_b"))
    functions[rec_b] = _fn(rec_b, _ins("CALL", rec_a, dest="recursive_call"),
                           _ins("CONST", ta, dest="seed_target"),
                           _ins("CALL", "MakeClosure", "seed_target", dest="seed_closure"),
                           _ins("RETURN", "seed_closure"))
    main = [_ins("CALL", name, dest="graph_closure"), _ins("CALL", "Invoke", "graph_closure", dest="graph_value"),
            _ins("CALL", rec_a, dest="recursive_closure")]
    return IRProgram(main=main, functions=functions)


def _outcome(emitter, program, native):
    try:
        return {"kind": "assembly", "assembly": emitter(program)}
    except native.NativeBackendError as error:
        return {"kind": "native-error", "type": f"{type(error).__module__}.{type(error).__qualname__}", "text": str(error)}


def _outcome_digest(outcome):
    if outcome["kind"] == "assembly":
        raw = outcome["assembly"].encode("utf-8")
        return {"kind": "assembly", "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}
    return dict(outcome)


def _summary_signature(trace):
    """Exact per-function invocation summaries, with stable invocation ordinals."""
    ordinals, entries = {}, []
    for item in trace.invocations:
        key = (item["function"], item["known_returns"])
        ordinal = ordinals.get(key, 0)
        ordinals[key] = ordinal + 1
        entries.append((key, ordinal, item["result"]))
    return tuple(entries)


def _return_signature(trace):
    """Exact RETURN accumulator sequence, independent of absent-map encoding."""
    ordinals, ids = {}, {}
    for item in trace.invocations:
        key = (item["function"], item["known_returns"])
        ordinal = ordinals.get(key, 0)
        ordinals[key] = ordinal + 1
        ids[item["id"]] = (key, ordinal)
    return tuple((ids[event["invocation"]], event["index"], event["return_state"])
                 for event in trace.visits if event["op"] == "RETURN")


def _return_value_mismatch_count(left, right):
    """Count aligned RETURN-site occurrences with unequal accumulator triples."""
    def grouped(trace):
        ordinals, ids, events = {}, {}, {}
        for item in trace.invocations:
            key = (item["function"], item["known_returns"])
            ordinal = ordinals.get(key, 0)
            ordinals[key] = ordinal + 1
            ids[item["id"]] = (key, ordinal)
        for item in trace.visits:
            if item["op"] != "RETURN":
                continue
            events.setdefault((ids[item["invocation"]], item["index"]), []).append(item["return_state"])
        return events
    a, b = grouped(left), grouped(right)
    return sum(x != y for key in a.keys() & b.keys() for x, y in zip(a[key], b[key]))


def _json_hash(value):
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), default=repr).encode()
    return hashlib.sha256(payload).hexdigest()


def search(seed_count=8, start_seed=0):
    """Run bounded fixed and generated cases under all four worklist schedules."""
    import compiler.native as native
    if seed_count < 0:
        raise ValueError("seed_count must be nonnegative")
    cases = [(label, program) for label, program in bounded_adversarial_cases().items()]
    cases.append(("minimal_same_order_return_accumulator", minimal_same_order_return_accumulator_witness()))
    cases.append(("minimal_final_summary_counterexample", minimal_final_summary_counterexample()))
    cases.append(("recursive_return_calls", recursive_return_workload()))
    # Each seed gets three return shapes, not merely one seed-modulo choice.
    for seed in range(start_seed, start_seed + seed_count):
        for mode in ("known", "missing", "scalar"):
            cases.append((f"generated_{seed}_{mode}", generated_graph_workload(seed, mode,
                                                                                function_name=f"SeedGraph{seed}_{mode}")))
        cases.append((f"adversarial_{seed}", adversarial_graph_workload(seed)))

    schedules = {
        "lifo_forward": {}, "fifo_forward": {"fifo": True},
        "lifo_reverse": {"reverse_successors": True},
        "fifo_reverse": {"fifo": True, "reverse_successors": True},
    }
    runners = {}
    for schedule, options in schedules.items():
        for mode in ("production", "normalized"):
            runners[(schedule, mode)] = make_emitter(native, mode=mode, trace=True, **options)

    mismatches, digest_rows = [], []
    totals = {"case_schedule_pairs": 0, "summary_compared": 0, "return_accumulators_compared": 0,
              "outcomes_compared": 0, "production_invocations": 0, "normalized_invocations": 0,
              "return_events": 0, "return_value_mismatches": 0}
    mismatch_counts = {"outcome": 0, "final_summary": 0, "return_accumulator_sequence": 0}
    summary_counterexamples = []
    for label, program in cases:
        for schedule in schedules:
            totals["case_schedule_pairs"] += 1
            outcomes, traces = {}, {}
            for mode in ("production", "normalized"):
                emitter, trace = runners[(schedule, mode)]
                # The emitter closes over this collector: reset it in place so
                # every case has independent invocation ids and event histories.
                trace.__init__()
                outcomes[mode] = _outcome(emitter, program, native)
                traces[mode] = trace
            prod, norm = traces["production"], traces["normalized"]
            totals["outcomes_compared"] += 1
            totals["summary_compared"] += 1
            totals["return_accumulators_compared"] += 1
            totals["production_invocations"] += len(prod.invocations)
            totals["normalized_invocations"] += len(norm.invocations)
            totals["return_events"] += sum(v["op"] == "RETURN" for v in prod.visits)
            out_equal = outcomes["production"] == outcomes["normalized"]
            summary_equal = _summary_signature(prod) == _summary_signature(norm)
            returns_equal = _return_signature(prod) == _return_signature(norm)
            return_value_mismatches = _return_value_mismatch_count(prod, norm)
            totals["return_value_mismatches"] += return_value_mismatches
            mismatch_counts["outcome"] += not out_equal
            mismatch_counts["final_summary"] += not summary_equal
            mismatch_counts["return_accumulator_sequence"] += not returns_equal
            prod_digest, norm_digest = _outcome_digest(outcomes["production"]), _outcome_digest(outcomes["normalized"])
            digest_rows.append((label, schedule, prod_digest, norm_digest,
                                _json_hash(_summary_signature(prod)), _json_hash(_summary_signature(norm)),
                                _json_hash(_return_signature(prod)), _json_hash(_return_signature(norm))))
            if not (out_equal and summary_equal and returns_equal):
                if not summary_equal and len(summary_counterexamples) < 10:
                    summary_counterexamples.append({"case": label, "schedule": schedule,
                                                    "production_summary_sha256": _json_hash(_summary_signature(prod)),
                                                    "normalized_summary_sha256": _json_hash(_summary_signature(norm))})
                mismatches.append({"case": label, "schedule": schedule,
                                   "outcomes_equal": out_equal, "production_outcome": prod_digest,
                                   "normalized_outcome": norm_digest,
                                   "summaries_equal": summary_equal,
                                   "production_summary_sha256": _json_hash(_summary_signature(prod)),
                                   "normalized_summary_sha256": _json_hash(_summary_signature(norm)),
                                   "return_accumulators_equal": returns_equal,
                                   "aligned_return_value_mismatch_count": return_value_mismatches,
                                   "production_returns_sha256": _json_hash(_return_signature(prod)),
                                   "normalized_returns_sha256": _json_hash(_return_signature(norm))})
    return {
        "scope": "bounded empirical search; absence of mismatch is not proof",
        "seed_start": start_seed, "seed_count": seed_count,
        "fixed_case_count": len(cases) - seed_count * 4,
        "generated_case_count": seed_count * 4,
        "case_count": len(cases), "schedules": list(schedules),
        "totals": totals,
        "mismatch_count": len(mismatches), "mismatch_counts": mismatch_counts,
        "final_summary_counterexample_found": mismatch_counts["final_summary"] > 0,
        "summary_counterexamples": summary_counterexamples,
        "mismatches": mismatches[:10],
        "first_mismatch_truncated": len(mismatches) > 10,
        "corpus_sha256": _json_hash(digest_rows),
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seeds", type=int, default=100, help="number of deterministic seeds (each expands to four graph cases)")
    parser.add_argument("--start-seed", type=int, default=0)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    result = search(args.seeds, args.start_seed)
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
