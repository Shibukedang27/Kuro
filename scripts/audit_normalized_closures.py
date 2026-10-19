#!/usr/bin/env python3
"""Test-only trace audit for normalized closure-return fact maps.

No compiler source is changed. ``make_emitter`` builds fail-closed AST clones of
``compiler.native.emit_x86_64_linux``. The normalized candidate uses ordinary
dicts and explicit writes/pops; it does not use a dict subclass.
"""
from __future__ import annotations

import ast
import inspect
from collections import Counter, defaultdict
from dataclasses import dataclass, field


@dataclass
class AuditTrace:
    invocations: list[dict] = field(default_factory=list)
    visits: list[dict] = field(default_factory=list)
    merges: list[dict] = field(default_factory=list)
    queues: list[dict] = field(default_factory=list)
    outer_transitions: list[dict] = field(default_factory=list)
    _next_id: int = 0

    def to_dict(self):
        return {"invocations": self.invocations, "visits": self.visits, "merges": self.merges,
                "queues": self.queues, "outer_transitions": self.outer_transitions}

    def begin(self, function, known_returns):
        ident = self._next_id
        self._next_id += 1
        self.invocations.append({
            "id": ident,
            "function": function.name,
            "known_returns": _freeze(known_returns),
            "result": None,
            "final_states": None,
        })
        return ident

    def seeded(self, ident, pending):
        self.queues.append({"invocation": ident, "event": "seed", "queue": tuple(pending)})

    def popped(self, ident, index, pending):
        self.queues.append({"invocation": ident, "event": "pop", "index": index, "queue": tuple(pending)})

    def visit(self, ident, index, item, incoming, outgoing, returned, all_known, saw_return, pending, known_returns=None, constructor_target=None):
        self.visits.append({
            "invocation": ident, "index": index, "op": item.op,
            "args": _freeze(item.args), "dest": item.dest,
            "incoming": _freeze(incoming), "outgoing": _freeze(outgoing),
            "return_state": (_freeze(returned), all_known, saw_return),
            "known_returns": _freeze(known_returns or {}), "constructor_target": constructor_target,
            "queue": tuple(pending),
        })

    def merge(self, ident, index, successor, current, incoming, merged, pending):
        self.merges.append({
            "invocation": ident, "index": index, "successor": successor,
            "current": _freeze(current), "incoming": _freeze(incoming),
            "merged": _freeze(merged), "changed": merged != current,
            "queue_before": tuple(pending),
        })

    def queued(self, ident, successor, pending):
        self.queues.append({"invocation": ident, "event": "append", "successor": successor, "queue": tuple(pending)})

    def round(self, previous, updated):
        self.outer_transitions.append({"previous": _freeze(previous), "updated": _freeze(updated)})

    def finish(self, ident, result, states):
        self.invocations[ident]["result"] = (_freeze(result[0]), result[1], result[2])
        self.invocations[ident]["final_states"] = None if states is None else _freeze(states)


def _freeze(value):
    """Stable immutable representation of nested closure-state maps/sets."""
    if isinstance(value, dict):
        return tuple(sorted((key, _freeze(item)) for key, item in value.items()))
    if isinstance(value, (set, frozenset)):
        return tuple(sorted(value))
    if isinstance(value, tuple):
        return tuple(_freeze(item) for item in value)
    if isinstance(value, list):
        return tuple(_freeze(item) for item in value)
    return value


def _parse_stmt(source):
    return ast.parse(source).body[0]


def _clone_tree(native, *, mode, trace, fifo=False, reverse_successors=False):
    assert mode in {"production", "legacy", "normalized"}
    tree = ast.parse(inspect.getsource(native.emit_x86_64_linux))
    hit = Counter()
    trace_name = "_closure_audit_trace"
    analyzers = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)
                 and node.name == "analyze_action_closure_returns"]
    assert len(analyzers) == 1, "nested analyzer shape changed"
    assignments = Counter((ast.unparse(node.targets[0]), ast.unparse(node.value))
                          for node in ast.walk(analyzers[0])
                          if isinstance(node, ast.Assign) and len(node.targets) == 1)
    for site in (("states[0]", "{}"), ("state", "incoming.copy()"),
                 ("states[successor]", "state.copy()")):
        assert assignments[site] == 1, f"state initialization/copy site changed: {site}"
    fact_reads = [node for node in ast.walk(analyzers[0])
                  if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                  and node.func.attr == "get" and len(node.args) == 2
                  and ast.unparse(node.args[1]) == "(set(), False)"]
    assert len(fact_reads) == 6, "closure fact default reads changed"

    class Clone(ast.NodeTransformer):
        inside = False
        serial = 0

        def visit_FunctionDef(self, node):
            if node.name != "analyze_action_closure_returns":
                return self.generic_visit(node)
            hit["analyzer"] += 1
            was_inside = self.inside
            self.inside = True
            node = self.generic_visit(node)
            self.inside = was_inside
            if trace:
                node.body.insert(0, _parse_stmt(f"_closure_audit_id = {trace_name}.begin(function, known_returns)"))
            return node

        def visit_Assign(self, node):
            if self.inside and mode == "legacy" and len(node.targets) == 1 and ast.unparse(node.targets[0]) in {"state", "states[successor]"} and isinstance(node.value, ast.Call) and ast.unparse(node.value).endswith(".copy()"):
                source = ast.unparse(node.value.func.value)
                node.value = ast.parse("{name: (set(targets), is_known) for name, (targets, is_known) in " + source + ".items()}", mode="eval").body
                hit["legacy_deepcopy"] += 1
            if self.inside and len(node.targets) == 1 and isinstance(node.targets[0], ast.Subscript):
                target = node.targets[0]
                base = ast.unparse(target.value)
                if base in {"state", "merged"}:
                    hit[f"write_{base}"] += 1
                    if mode == "normalized":
                        self.serial += 1
                        tmp = f"_normalized_fact_{self.serial}"
                        # Evaluate RHS once; only (empty-set, False) is absent.
                        return self._normalized_assignment(node, tmp)
            node = self.generic_visit(node)
            if self.inside and trace and len(node.targets) == 1:
                target, value = ast.unparse(node.targets[0]), ast.unparse(node.value)
                if target == "pending" and value == "[0]":
                    hit["queue_seed"] += 1
                    return [node, _parse_stmt(f"{trace_name}.seeded(_closure_audit_id, pending)")]
                if target == "index" and value in {"pending.pop()", "pending.pop(0)"}:
                    hit["queue_pop"] += 1
                    return [node, _parse_stmt(f"{trace_name}.popped(_closure_audit_id, index, pending)")]
            return node

        def _normalized_assignment(self, node, tmp):
            target = node.targets[0]
            mapping = ast.unparse(target.value)
            key = ast.unparse(target.slice)
            write = ast.Assign(targets=[ast.Subscript(value=ast.Name(id=mapping, ctx=ast.Load()), slice=ast.parse(key, mode="eval").body, ctx=ast.Store())], value=ast.Name(id=tmp, ctx=ast.Load()))
            pop = ast.Expr(value=ast.Call(func=ast.Attribute(value=ast.Name(id=mapping, ctx=ast.Load()), attr="pop", ctx=ast.Load()), args=[ast.parse(key, mode="eval").body, ast.Constant(value=None)], keywords=[]))
            branch = ast.If(test=ast.BoolOp(op=ast.Or(), values=[ast.Subscript(value=ast.Name(id=tmp, ctx=ast.Load()), slice=ast.Constant(value=0), ctx=ast.Load()), ast.Subscript(value=ast.Name(id=tmp, ctx=ast.Load()), slice=ast.Constant(value=1), ctx=ast.Load())]), body=[write], orelse=[pop])
            return [ast.Assign(targets=[ast.Name(id=tmp, ctx=ast.Store())], value=node.value), ast.copy_location(branch, node)]

        def visit_AnnAssign(self, node):
            if self.inside and isinstance(node.target, ast.Name) and node.target.id == "merged":
                hit["merged_map"] += 1
            return self.generic_visit(node)

        def visit_If(self, node):
            if mode == "legacy" and any(isinstance(x, ast.Name) and x.id == "closure_return_constructors" for x in ast.walk(node.test)):
                hit["legacy_guard"] += 1
                return None
            node = self.generic_visit(node)
            if trace and ast.unparse(node.test) == "updated_returns == function_return_closure_targets":
                hit["outer_round"] += 1
                node.test = ast.BoolOp(op=ast.Or(), values=[
                    ast.Call(func=ast.Name(id="_closure_audit_round", ctx=ast.Load()), args=[ast.Name(id=trace_name, ctx=ast.Load()), ast.Name(id="function_return_closure_targets", ctx=ast.Load()), ast.Name(id="updated_returns", ctx=ast.Load())], keywords=[]),
                    node.test,
                ])
            return node

        def visit_Call(self, node):
            node = self.generic_visit(node)
            if self.inside and isinstance(node.func, ast.Attribute) and node.func.attr == "pop" and len(node.args) == 0 and fifo:
                pass
            if self.inside and isinstance(node.func, ast.Attribute) and node.func.attr == "append" and ast.unparse(node.func.value) == "pending" and trace:
                hit["queue_append"] += 1
                return ast.copy_location(ast.Call(func=ast.Name(id="_closure_audit_queue", ctx=ast.Load()), args=[ast.Name(id="_closure_audit_id", ctx=ast.Load()), ast.Name(id="pending", ctx=ast.Load()), node.args[0]], keywords=[]), node)
            return node

        def visit_For(self, node):
            if self.inside and ast.unparse(node.target) == "successor" and ast.unparse(node.iter) == "successors[index]" and reverse_successors:
                hit["successor_order"] += 1
                node.iter = ast.Call(func=ast.Name(id="reversed", ctx=ast.Load()), args=[node.iter], keywords=[])
            return self.generic_visit(node)

        def visit_While(self, node):
            node = self.generic_visit(node)
            if self.inside and ast.unparse(node.test) == "pending":
                hit["workloop"] += 1
                if trace:
                    # The visit hook belongs immediately before the successor loop.
                    for statement in list(node.body):
                        if isinstance(statement, ast.For) and ast.unparse(statement.target) == "successor":
                            node.body.insert(node.body.index(statement), _parse_stmt(f"{trace_name}.visit(_closure_audit_id, index, item, incoming, state, returned, all_returns_known, saw_return, pending, known_returns, function_closure_construction_targets.get((function.name, index)) )"))
                            # Merge hook immediately before the changed test, which lives in the loop body.
                            for child in list(statement.body):
                                if isinstance(child, ast.If) and ast.unparse(child.test) == "merged != current":
                                    statement.body.insert(statement.body.index(child), _parse_stmt(f"{trace_name}.merge(_closure_audit_id, index, successor, current, state, merged, pending)"))
                                    hit["merge_hook"] += 1
                            hit["visit_hook"] += 1
                if fifo:
                    node.body[0].value = ast.Call(func=ast.Attribute(value=ast.Name(id="pending", ctx=ast.Load()), attr="pop", ctx=ast.Load()), args=[ast.Constant(value=0)], keywords=[])
                    hit["fifo"] += 1
            return node

        def visit_Return(self, node):
            node = self.generic_visit(node)
            if self.inside and trace:
                hit["return_hook"] += 1
                states = "None" if ast.unparse(node.value) == "set(), True, False" else "states"
                return [_parse_stmt(f"{trace_name}.finish(_closure_audit_id, {ast.unparse(node.value)}, {states})"), node]
            return node

    clone = Clone()
    tree = clone.visit(tree)
    ast.fix_missing_locations(tree)
    assert hit["analyzer"] == 1, f"expected one nested analyzer; AST shape changed: {dict(hit)}"
    # Fail closed on every dictionary fact write. A new assignment site requires audit review.
    assert hit["write_state"] == 6 and hit["write_merged"] == 1, f"state/merge write sites changed: {dict(hit)}"
    assert hit["merged_map"] == 1, f"merge map declaration changed: {dict(hit)}"
    assert hit["workloop"] == 1, f"worklist shape changed: {dict(hit)}"
    if mode == "legacy":
        assert hit["legacy_guard"] == 1, f"expected exactly one seedless guard: {dict(hit)}"
        assert hit["legacy_deepcopy"] == 2, f"expected two legacy deep-copy sites: {dict(hit)}"
    else:
        assert hit["legacy_guard"] == 0
    if trace:
        assert hit["visit_hook"] == hit["merge_hook"] == 1 and hit["return_hook"] == 2, f"trace insertion sites changed: {dict(hit)}"
        assert hit["queue_append"] == 2, f"queue append sites changed: {dict(hit)}"
        assert hit["queue_seed"] == hit["queue_pop"] == 1, f"queue seed/pop sites changed: {dict(hit)}"
        assert hit["outer_round"] == 1, f"outer fixed-point hook changed: {dict(hit)}"
    if fifo:
        assert hit["fifo"] == 1
    if reverse_successors:
        assert hit["successor_order"] == 1
    return tree


def make_emitter(native, mode="production", trace=False, *, fifo=False, reverse_successors=False):
    """Return (emitter, AuditTrace-or-None); trace=False has no tracing hooks.

    Modes: production (current source clone), legacy (guard removed and legacy
    deep copies restored), normalized (plain dict with explicit write/pop).
    FIFO/reversed-successor controls are test-only scheduling perturbations.
    """
    if mode not in {"production", "legacy", "normalized"}:
        raise ValueError(mode)
    if mode == "production" and not trace and not fifo and not reverse_successors:
        return native.emit_x86_64_linux, None
    audit = AuditTrace() if trace else None
    tree = _clone_tree(native, mode=mode, trace=trace, fifo=fifo, reverse_successors=reverse_successors)
    namespace = vars(native).copy()
    if trace:
        namespace["_closure_audit_trace"] = audit
        namespace["_closure_audit_queue"] = lambda ident, pending, successor: _record_queue(audit, ident, pending, successor)
        namespace["_closure_audit_round"] = lambda target, previous, updated: _record_round(target, previous, updated)
    exec(compile(tree, f"<{mode}-normalized-closure-audit>", "exec"), namespace)
    return namespace["emit_x86_64_linux"], audit


def _record_queue(trace, ident, pending, successor):
    pending.append(successor)
    trace.queued(ident, successor, pending)


def _record_round(trace, previous, updated):
    trace.round(previous, updated)
    return False


def invocation_key(record):
    return record["function"], record["known_returns"]


def _elide_unknown(mapping):
    return tuple((name, fact) for name, fact in mapping if fact != ((), False))


def _first_difference(left, right):
    for index, (a, b) in enumerate(zip(left, right)):
        if a != b:
            return {"index": index, "production": a, "candidate": b}
    if len(left) != len(right):
        return {"index": min(len(left), len(right)), "production": left[len(right)] if len(left) > len(right) else None,
                "candidate": right[len(left)] if len(right) > len(left) else None}
    return None


def _event_groups(trace, field):
    ordinals, ids = Counter(), {}
    for rec in trace.invocations:
        key = invocation_key(rec)
        ids[rec["id"]] = (key, ordinals[key])
        ordinals[key] += 1
    grouped = defaultdict(list)
    for event in getattr(trace, field):
        grouped[ids[event["invocation"]]].append({k: v for k, v in event.items() if k != "invocation"})
    return grouped


def _record_groups(trace):
    groups = defaultdict(list)
    for rec in trace.invocations:
        groups[invocation_key(rec)].append(rec)
    return groups


def _fact_map(frozen):
    return {name: (set(targets), known) for name, (targets, known) in frozen}


def validate_trace(trace: AuditTrace):
    """Independently check each observed transfer, merge, and sticky return step."""
    visits_checked = merges_checked = returns_checked = 0
    errors = []
    return_by_invocation = {}
    for visit in trace.visits:
        incoming = _fact_map(visit["incoming"])
        expected = dict(incoming)
        op, args, dest = visit["op"], visit.get("args", ()), visit.get("dest")
        default = (set(), False)
        if op == "LOADVAR" and dest:
            expected[dest] = tuple(incoming.get(args[0], default))
        elif op == "STORE_LIST":
            name, values = args
            expected[name] = tuple(incoming.get(values[0], default)) if len(values) == 1 else default
        elif op == "UPDATE":
            name, value = args
            expected[name] = tuple(incoming.get(value, default))
        elif op == "CALL" and dest:
            call_name = args[0]
            targets = {visit["constructor_target"]} if visit.get("constructor_target") is not None else set(dict(visit.get("known_returns", ())).get(call_name, ()))
            expected[dest] = (targets, bool(targets))
        elif op == "RETURN" and args:
            pass
        elif op != "LABEL" and dest:
            expected[dest] = default
        expected_frozen = _elide_unknown(_freeze(expected))
        observed = _elide_unknown(visit["outgoing"])
        if expected_frozen != observed:
            errors.append({"kind": "transfer", "index": visit["index"], "op": op, "expected": expected_frozen, "observed": observed})
        visits_checked += 1
        previous = return_by_invocation.setdefault(visit["invocation"], (set(), True, False))
        targets, all_known, saw_return = previous
        if op == "RETURN" and args:
            facts = _fact_map(visit["outgoing"])
            returned_targets, known = facts.get(args[0], default)
            if known and returned_targets:
                targets = targets | returned_targets
            else:
                all_known = False
            saw_return = True
        actual = (tuple(sorted(targets)), all_known, saw_return)
        if actual != visit["return_state"]:
            errors.append({"kind": "return-summary", "index": visit["index"], "expected": actual, "observed": visit["return_state"]})
        return_by_invocation[visit["invocation"]] = (targets, all_known, saw_return)
        returns_checked += 1
    for merge in trace.merges:
        current, incoming = _fact_map(merge["current"]), _fact_map(merge["incoming"])
        expected = {}
        for name in set(current) | set(incoming):
            ct, ck = current.get(name, (set(), False)); it, ik = incoming.get(name, (set(), False))
            expected[name] = (ct | it, ck and ik)
        expected_frozen = _elide_unknown(_freeze(expected))
        observed = _elide_unknown(merge["merged"])
        if expected_frozen != observed:
            errors.append({"kind": "merge", "index": merge["index"], "successor": merge["successor"], "expected": expected_frozen, "observed": observed})
        merges_checked += 1
    return {"valid": not errors, "visits_checked": visits_checked, "merges_checked": merges_checked,
            "return_steps_checked": returns_checked, "errors": errors}


def _first_diff(left, right):
    for index, (a, b) in enumerate(zip(left, right)):
        if a != b: return {"index": index, "left": a, "right": b}
    if len(left) != len(right): return {"index": min(len(left), len(right)), "left": left[len(right)] if len(left)>len(right) else None, "right": right[len(left)] if len(right)>len(left) else None}
    return None


def _normalized_final_states(states):
    if states is None: return None
    return tuple(None if state is None else _elide_unknown(state) for state in states)


def _summary_differences(left, right):
    lg, rg = _record_groups(left), _record_groups(right)
    differences = []
    for key in sorted(set(lg) | set(rg), key=repr):
        for ordinal in range(max(len(lg.get(key, [])), len(rg.get(key, [])))):
            a = lg.get(key, [])[ordinal] if ordinal < len(lg.get(key, [])) else None
            b = rg.get(key, [])[ordinal] if ordinal < len(rg.get(key, [])) else None
            af = _normalized_final_states(a.get("final_states")) if a is not None else None
            bf = _normalized_final_states(b.get("final_states")) if b is not None else None
            if a is None or b is None or a.get("result") != b.get("result") or af != bf:
                differences.append({"key": key, "ordinal": ordinal,
                                   "production": None if a is None else a.get("result"),
                                   "candidate": None if b is None else b.get("result"),
                                   "production_final_normalized": af, "candidate_final_normalized": bf})
    return differences


def _return_sequences(trace):
    grouped = _event_groups(trace, "visits")
    return {key: [visit["return_state"] for visit in visits if visit["op"] == "RETURN"]
            for key, visits in grouped.items()}


def _aligned_transition_audit(production, candidate):
    pv, cv = _event_groups(production, "visits"), _event_groups(candidate, "visits")
    pm, cm = _event_groups(production, "merges"), _event_groups(candidate, "merges")
    output, visit_count, merge_count = [], 0, 0
    for key in sorted(set(pv) | set(cv), key=repr):
        left, right = pv.get(key, []), cv.get(key, [])
        divergence = None
        transition_mismatches = []
        local_visits = local_merges = 0
        ml, mr = pm.get(key, []), cm.get(key, [])
        li = ri = 0
        for i, (a, b) in enumerate(zip(left, right)):
            if (a["index"], a["op"]) != (b["index"], b["op"]):
                divergence = {"kind":"visit-order", "event_index":i, "production":{"index":a["index"],"op":a["op"]}, "candidate":{"index":b["index"],"op":b["op"]}}
                break
            local_visits += 1
            mismatch = {}
            for field in ("incoming", "outgoing"):
                if _elide_unknown(a[field]) != _elide_unknown(b[field]): mismatch[field] = {"production":_elide_unknown(a[field]),"candidate":_elide_unknown(b[field])}
            if a["return_state"] != b["return_state"]: mismatch["return_state"] = {"production":a["return_state"],"candidate":b["return_state"]}
            if mismatch: transition_mismatches.append({"kind":"visit-state","event_index":i,"differences":mismatch})
            while li < len(ml) and ml[li]["index"] == a["index"]:
                if ri >= len(mr) or mr[ri]["index"] != b["index"]:
                    divergence = {"kind":"merge-order","visit_index":i,"production":ml[li],"candidate":mr[ri] if ri < len(mr) else None}
                    li += 1
                    break
                x, y = ml[li], mr[ri]; li += 1; ri += 1; local_merges += 1
                mm = {}
                for field in ("current", "incoming", "merged"):
                    if _elide_unknown(x[field]) != _elide_unknown(y[field]): mm[field] = {"production":_elide_unknown(x[field]),"candidate":_elide_unknown(y[field])}
                if x["successor"] != y["successor"] or x["changed"] != y["changed"]:
                    mm["control"] = {"production":(x["successor"],x["changed"]),"candidate":(y["successor"],y["changed"])}
                    if x["successor"] != y["successor"] and divergence is None:
                        divergence = {"kind":"successor-order","visit_index":i,"production":x["successor"],"candidate":y["successor"]}
                if mm: transition_mismatches.append({"kind":"merge-state","visit_index":i,"differences":mm})
                if divergence: break
            if divergence: break
            if a["queue"] != b["queue"]:
                divergence = {"kind":"pending-queue","visit_index":i,"production":a["queue"],"candidate":b["queue"]}
                break
        if divergence is None and len(left) != len(right):
            divergence = {"kind":"visit-count","event_index":min(len(left),len(right)),"production_count":len(left),"candidate_count":len(right)}
        visit_count += local_visits; merge_count += local_merges
        output.append({"invocation_key":key,"aligned_visits_checked":local_visits,"aligned_merges_checked":local_merges,
                       "transition_mismatches_before_schedule_divergence":transition_mismatches,
                       "first_schedule_divergence":divergence})
    return output, visit_count, merge_count


def compare_traces(production: AuditTrace, candidate: AuditTrace):
    """Compare exact summaries and expose dense aligned-prefix and divergence evidence."""
    summaries = _summary_differences(production, candidate)
    event_diffs = {}
    for field in ("queues", "visits", "merges"):
        left, right = _event_groups(production, field), _event_groups(candidate, field)
        diffs = {}
        for key in sorted(set(left) | set(right), key=repr):
            diff = _first_diff(left.get(key, []), right.get(key, []))
            if diff: diffs[repr(key)] = diff
        event_diffs[field] = diffs
    changed_classification = Counter()
    changed_witnesses = []
    qgroups = _event_groups(production, "queues")
    id_to_key = {}
    for key, records in _record_groups(production).items():
        for ordinal, record in enumerate(records): id_to_key[record["id"]] = (key,ordinal)
    for merge in production.merges:
        if not merge["changed"]: continue
        cls = "representation_only" if _elide_unknown(merge["current"]) == _elide_unknown(merge["merged"]) else "semantic"
        changed_classification[cls] += 1
        invkey = id_to_key[merge["invocation"]]
        evidence = [event for event in qgroups.get(invkey, []) if event.get("event") == "append" and event.get("successor") == merge["successor"]]
        changed_witnesses.append({"invocation_key":invkey,"index":merge["index"],"successor":merge["successor"],"classification":cls,
                                  "current_normalized":_elide_unknown(merge["current"]),"merged_normalized":_elide_unknown(merge["merged"]),
                                  "queue_before":merge["queue_before"],"matching_append_queue_evidence":evidence})
    aligned, visit_count, merge_count = _aligned_transition_audit(production, candidate)
    ret_a, ret_b = _return_sequences(production), _return_sequences(candidate)
    return_differences = []
    for key in sorted(set(ret_a) | set(ret_b), key=repr):
        diff = _first_diff(ret_a.get(key, []), ret_b.get(key, []))
        if diff: return_differences.append({"invocation_key":key,"difference":diff})
    return {"equivalent_invocation_summaries": not summaries, "summary_differences": summaries,
            "return_summary_event_sequence_differences":return_differences,
            "return_summary_event_sequence_difference_count":len(return_differences),
            "queue_differences": event_diffs["queues"], "visit_differences": event_diffs["visits"], "merge_differences": event_diffs["merges"],
            "first_queue_difference": next(iter(event_diffs["queues"].items()), None),
            "first_visit_difference": next(iter(event_diffs["visits"].items()), None),
            "independent_schedule_differences_reported": True, "aligned_visit_prefix_count": visit_count,
            "aligned_merge_prefix_count":merge_count,"aligned_transition_audit":aligned,
            "production_changed_merge_classification": dict(changed_classification),
            "production_changed_merge_witnesses":changed_witnesses,
            "production_validation": validate_trace(production), "candidate_validation": validate_trace(candidate),
            "outer_transitions_equal": production.outer_transitions == candidate.outer_transitions,
            "outer_transition_difference": _first_diff(production.outer_transitions, candidate.outer_transitions)}


def compare_production_legacy(production: AuditTrace, legacy: AuditTrace):
    """Strictly compare shared invocations after removing run-local IDs."""
    pg, lg = _record_groups(production), _record_groups(legacy)
    shared_differences = []
    for key in sorted(pg, key=repr):
        for ordinal, rec in enumerate(pg[key]):
            other = lg.get(key, [])
            match = other[ordinal] if ordinal < len(other) else None
            checks = {}
            if match is not None:
                for field in ("queues", "visits", "merges"):
                    a = _event_groups(production, field).get((key, ordinal), [])
                    b = _event_groups(legacy, field).get((key, ordinal), [])
                    checks[field] = _first_diff(a, b)
                checks["result"] = None if rec["result"] == match["result"] else {"production":rec["result"],"legacy":match["result"]}
                checks["final_states"] = None if rec["final_states"] == match["final_states"] else {"production":rec["final_states"],"legacy":match["final_states"]}
                checks["visit_count"] = None if len(_event_groups(production,"visits").get((key,ordinal),[])) == len(_event_groups(legacy,"visits").get((key,ordinal),[])) else {"production":len(_event_groups(production,"visits").get((key,ordinal),[])),"legacy":len(_event_groups(legacy,"visits").get((key,ordinal),[]))}
            else:
                checks["missing_shared_invocation"] = True
            if match is None or any(checks.get(field) for field in ("queues","visits","merges","result","final_states","visit_count")):
                shared_differences.append({"key":key,"ordinal":ordinal,"differences":checks})
    extras = []
    for key, records in lg.items():
        for rec in records[len(pg.get(key, [])):]:
            result = rec["result"]
            can_install = result is not None and bool(result[0]) and result[1] and result[2]
            extras.append({"key":key,"result":result,"can_install_summary":can_install})
    outer_equal = production.outer_transitions == legacy.outer_transitions
    return {"shared_summaries_equal": not shared_differences, "shared_full_trace_equal": not shared_differences and outer_equal,
            "shared_differences":shared_differences,"outer_transitions_equal":outer_equal,
            "outer_transition_difference":_first_diff(production.outer_transitions, legacy.outer_transitions),
            "legacy_extra_invocations":extras,"extras_cannot_install":all(not item["can_install_summary"] for item in extras)}


def _outcome(emitter, program, native):
    try:
        return {"kind": "assembly", "assembly": emitter(program)}
    except native.NativeBackendError as error:
        return {"kind": "native-error", "type": f"{type(error).__module__}.{type(error).__qualname__}", "text": str(error)}


def audit_program(program, native=None):
    """Return JSON-ready full outcomes and comparisons (including raw traces)."""
    if native is None:
        import compiler.native as native
    emitters = {mode: make_emitter(native, mode, trace=True) for mode in ("production", "legacy", "normalized")}
    outcomes, traces = {}, {}
    for mode, (emitter, trace) in emitters.items():
        outcomes[mode] = _outcome(emitter, program, native)
        traces[mode] = trace
    return {"outcomes": outcomes, "traces": {mode: trace.to_dict() for mode, trace in traces.items()},
            "production_vs_legacy": compare_production_legacy(traces["production"], traces["legacy"]),
            "production_vs_normalized": compare_traces(traces["production"], traces["normalized"])}


def recursive_return_workload():
    """Mutual recursion whose returned closure summaries flow through CALLs."""
    from compiler.ir import IRFunction, IRProgram, Instr
    ins = lambda op, *args, dest=None: Instr(op, tuple(args), dest)
    fn = lambda name, *body: IRFunction(name, [], list(body))
    functions = {
        "RecursiveSeedTarget": fn("RecursiveSeedTarget", ins("CONST", 9, dest="n"), ins("RETURN", "n")),
        # An unused constructor keeps A eligible even before B has a summary;
        # its actual return still depends only on the changing B CALL result.
        "RecursiveA": fn("RecursiveA", ins("CONST", "RecursiveSeedTarget", dest="unused_target"),
                         ins("CALL", "MakeClosure", "unused_target", dest="unused_seed"),
                         ins("CALL", "RecursiveB", dest="from_b"), ins("RETURN", "from_b")),
        # B closes the recursion cycle via a call to A, but returns its direct
        # seed; A's returned summary is obtained only from B's CALL result.
        "RecursiveB": fn("RecursiveB", ins("CALL", "RecursiveA", dest="recursive_call"),
                         ins("CONST", "RecursiveSeedTarget", dest="target"), ins("CALL", "MakeClosure", "target", dest="seed"), ins("RETURN", "seed")),
    }
    return IRProgram(main=[ins("CALL", "RecursiveA", dest="closure"), ins("CALL", "Invoke", "closure", dest="result")], functions=functions)


def multibackedge_workload(seed: int = 0):
    """Three-backedge CFG plus a one-sided definition/missing-name join."""
    from compiler.ir import IRFunction, IRProgram, Instr
    ins = lambda op, *args, dest=None: Instr(op, tuple(args), dest)
    fn = lambda name, *body: IRFunction(name, [], list(body))
    suffix, name = str(seed), f"MultiBackedge{seed}"
    body = [ins("CONST", "GraphTargetA", dest="ta"), ins("CALL", "MakeClosure", "ta", dest="ca"),
            ins("CONST", "GraphTargetB", dest="tb"), ins("CALL", "MakeClosure", "tb", dest="cb"),
            ins("CONST", 1, dest="missing_cond"), ins("JUMPF", f"mr_{suffix}", "missing_cond"),
            ins("CONST", "GraphTargetA", dest=f"one_{suffix}"), ins("JUMP", f"mj_{suffix}"),
            ins("LABEL", dest=f"mr_{suffix}"), ins("LABEL", dest=f"mj_{suffix}"),
            ins("LOADVAR", f"one_{suffix}", dest=f"unknown_{suffix}"), ins("LOADVAR", "ca", dest="selected"),
            ins("LABEL", dest=f"head_{suffix}"), ins("CONST", 1, dest="loop_cond"), ins("JUMPF", f"exit_{suffix}", "loop_cond"),
            ins("CONST", seed % 2, dest="ra"), ins("JUMPF", f"arm_b_{suffix}", "ra"), ins("LOADVAR", "ca", dest="selected"), ins("JUMP", f"head_{suffix}"),
            ins("LABEL", dest=f"arm_b_{suffix}"), ins("CONST", (seed + 1) % 2, dest="rb"), ins("JUMPF", f"arm_c_{suffix}", "rb"),
            ins("LOADVAR", "cb", dest="selected"), ins("JUMP", f"head_{suffix}"), ins("LABEL", dest=f"arm_c_{suffix}"),
            ins("LOADVAR", "ca", dest="selected"), ins("JUMP", f"head_{suffix}"), ins("LABEL", dest=f"exit_{suffix}"), ins("RETURN", "selected")]
    functions = {"GraphTargetA": fn("GraphTargetA", ins("CONST", 11, dest="n"), ins("RETURN", "n")),
                 "GraphTargetB": fn("GraphTargetB", ins("CONST", 21, dest="n"), ins("RETURN", "n")), name: fn(name, *body)}
    return IRProgram(main=[ins("CALL", name, dest="c"), ins("CALL", "Invoke", "c", dest="r")], functions=functions)


def _outcome_digest(outcome):
    import hashlib
    if outcome["kind"] == "assembly":
        data = outcome["assembly"].encode("utf-8")
        return {"kind":"assembly", "sha256":hashlib.sha256(data).hexdigest(), "bytes":len(data)}
    return {"kind":outcome["kind"], "type":outcome.get("type"), "text":outcome.get("text")}


def audit_corpus(native=None, *, include_traces=False):
    """Audit bounded corpus in LIFO/FIFO × forward/reversed successor orders.

    Assemblies are fully compared before compact digests are emitted. Set
    ``include_traces`` to attach raw traces for machine-level inspection.
    """
    if native is None:
        import compiler.native as native
    from scripts.profile_sparse_closures import closure_edge_workloads, generated_graph_workload, negative_workload, sparse_workload
    cases = {f"generated_{i}_{mode}": generated_graph_workload(311 + i * 17, mode)
             for i, mode in enumerate(("known", "missing", "scalar") * 4)}
    cases.update({f"multibackedge_{i}":multibackedge_workload(i) for i in range(3)})
    cases["recursive_return_calls"] = recursive_return_workload()
    cases["negative_mixed_return"] = negative_workload()
    cases["small_recursive_join_cfg"] = sparse_workload(size=8, random_cases=1, seed=442)
    cases.update(closure_edge_workloads())
    schedules = {"lifo_forward":{}, "fifo_forward":{"fifo":True},
                 "lifo_reverse":{"reverse_successors":True}, "fifo_reverse":{"fifo":True,"reverse_successors":True}}
    modes = ("production", "legacy", "normalized")
    reports, counts = [], Counter()
    for case_name, program in cases.items():
        for order, schedule in schedules.items():
            outcomes, traces = {}, {}
            for mode in modes:
                emitter, trace = make_emitter(native, mode, trace=True, **schedule)
                raw = _outcome(emitter, program, native)
                outcomes[mode] = raw
                traces[mode] = trace
            equal = outcomes["production"] == outcomes["legacy"] == outcomes["normalized"]
            pl = compare_production_legacy(traces["production"], traces["legacy"])
            pn = compare_traces(traces["production"], traces["normalized"])
            validators = {m:validate_trace(t) for m,t in traces.items()}
            counts["cases"] += 1
            counts["return_summary_sequence_differences"] += pn["return_summary_event_sequence_difference_count"]
            counts["invocation_summary_differences"] += len(pn["summary_differences"])
            for mode, trace in traces.items():
                counts[f"{mode}_invocations"] += len(trace.invocations)
                counts[f"{mode}_visits"] += len(trace.visits)
                counts[f"{mode}_merges"] += len(trace.merges)
                counts[f"{mode}_representation_only_updates"] += sum(m["changed"] and _elide_unknown(m["current"]) == _elide_unknown(m["merged"]) for m in trace.merges)
                counts[f"{mode}_semantic_updates"] += sum(m["changed"] and _elide_unknown(m["current"]) != _elide_unknown(m["merged"]) for m in trace.merges)
            item = {"case":case_name,"order":order,"outcomes_equal":equal,
                    "outcomes":{m:_outcome_digest(o) for m,o in outcomes.items()},
                    "production_vs_legacy":pl,"production_vs_normalized":pn,
                    "trace_validation":validators}
            if include_traces: item["traces"] = {m:t.to_dict() for m,t in traces.items()}
            reports.append(item)
    return {"case_count":len(cases),"order_count":len(schedules),"comparison_count":len(reports),
            "all_outcomes_equal":all(x["outcomes_equal"] for x in reports),
            "all_shared_legacy_traces_equal":all(x["production_vs_legacy"]["shared_full_trace_equal"] for x in reports),
            "all_outer_transitions_equal":all(x["production_vs_legacy"]["outer_transitions_equal"] and x["production_vs_normalized"]["outer_transitions_equal"] for x in reports),
            "all_exact_invocation_summaries_equal":all(x["production_vs_normalized"]["equivalent_invocation_summaries"] for x in reports),
            "all_trace_validations_pass":all(all(v["valid"] for v in x["trace_validation"].values()) for x in reports),
            "aggregate_counts":dict(counts),"cases":reports}
