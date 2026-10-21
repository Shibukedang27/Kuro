"""Small test oracle for loop-flow facts; deliberately not production-ready.

This is a bounded CFG/dataflow model for hand-written raw bytecode fixtures, not a
compiler implementation or general semantic proof. It decodes CONST, LOADVAR,
STORE_LIST, PRINT, BINOP +, and structured IF/Repeat/While delimiters. Literal
validity and stack checks run only at abstractly reachable nodes; this is not a
whole-stream bytecode validator. Reachable CONST operands must be numeric.
All joins are solved to a worklist fixed point; emission order is never a proxy for
fixed-point state. Unknown/uninitialized slots use '?'; numeric kinds are I/D.
"""
from collections import deque
import re

KINDS = frozenset(("?", "I", "D"))
DELIMITERS = {"BC_IF_BEGIN", "BC_ELSE_BEGIN", "BC_IF_END", "BC_REPEAT_BEGIN",
              "BC_REPEAT_END", "BC_WHILE_BEGIN", "BC_WHILE_TEST", "BC_WHILE_END"}
ARITY = {"BC_CONST": 1, "BC_LOADVAR": 1, "BC_STORE_LIST": 1,
         "BC_PRINT": 0, "BC_BINOP": 1, **{op: 0 for op in DELIMITERS}}


def _literal_kind(text):
    if re.fullmatch(r"-?(?:0|[1-9][0-9]*)", text):
        return frozenset(("I",))
    if re.fullmatch(r"-?(?:[0-9]+\.[0-9]+)", text):
        return frozenset(("D",))
    raise ValueError(f"unsupported CONST literal: {text!r}")


def _count_kind(instructions, begin):
    """Classify only an adjacent canonical integer literal; do not evaluate code."""
    previous = next((ins for ins in instructions if ins["next"] == begin["pc"]), None)
    if not previous or previous["op"] != "BC_CONST":
        return "unknown"
    value = previous["arg"]
    if value == "0":
        return "zero"
    if value == "1":
        return "one"
    return "positive" if re.fullmatch(r"[2-9]", value) else "unknown"


def _parse(tokens):
    """Decode explicit arities and parse strictly nested structured delimiters."""
    instructions, i = [], 0
    while i < len(tokens):
        op = tokens[i]
        if op not in ARITY:
            raise ValueError(f"unsupported opcode at token {i}: {op}")
        arity = ARITY[op]
        if i + arity >= len(tokens):
            raise ValueError(f"truncated {op} at token {i}")
        arg = tokens[i + 1] if arity else None
        if op == "BC_BINOP" and arg != "+":
            raise ValueError(f"unsupported BINOP at token {i}: {arg}")
        instructions.append({"pc": i, "next": i + 1 + arity, "op": op, "arg": arg})
        i += 1 + arity

    by_pc = {x["pc"]: x for x in instructions}
    cursor = 0

    def seq(stops):
        nonlocal cursor
        result = []
        while cursor < len(instructions) and instructions[cursor]["op"] not in stops:
            ins = instructions[cursor]
            cursor += 1
            op = ins["op"]
            if op == "BC_IF_BEGIN":
                yes = seq({"BC_ELSE_BEGIN", "BC_IF_END"})
                has_else = cursor < len(instructions) and instructions[cursor]["op"] == "BC_ELSE_BEGIN"
                no = []
                if has_else:
                    cursor += 1
                    no = seq({"BC_IF_END"})
                if cursor >= len(instructions) or instructions[cursor]["op"] != "BC_IF_END":
                    raise ValueError("IF missing IF_END")
                end = instructions[cursor]; cursor += 1
                result.append(("if", ins, yes, no, has_else, end))
            elif op == "BC_REPEAT_BEGIN":
                body = seq({"BC_REPEAT_END"})
                if cursor >= len(instructions) or instructions[cursor]["op"] != "BC_REPEAT_END":
                    raise ValueError("Repeat missing REPEAT_END")
                end = instructions[cursor]; cursor += 1
                result.append(("repeat", ins, body, end))
            elif op == "BC_WHILE_BEGIN":
                condition = seq({"BC_WHILE_TEST"})
                if cursor >= len(instructions) or instructions[cursor]["op"] != "BC_WHILE_TEST":
                    raise ValueError("While missing WHILE_TEST")
                test = instructions[cursor]; cursor += 1
                body = seq({"BC_WHILE_END"})
                if cursor >= len(instructions) or instructions[cursor]["op"] != "BC_WHILE_END":
                    raise ValueError("While missing WHILE_END")
                end = instructions[cursor]; cursor += 1
                result.append(("while", ins, condition, test, body, end))
            elif op in DELIMITERS:
                raise ValueError(f"unexpected/crossed delimiter {op} at token {ins['pc']}")
            else:
                result.append(("op", ins))
        return result

    tree = seq(set())
    if cursor != len(instructions):
        bad = instructions[cursor]
        raise ValueError(f"unexpected/crossed delimiter {bad['op']} at token {bad['pc']}")
    return tree, instructions, by_pc


def analyze(tokens, *, worklist="fifo", successors="forward"):
    """Return fixed-point facts plus loop-local uses from entry/backedge seeds.

    ``worklist`` selects FIFO or LIFO processing; ``successors`` selects sorted
    ascending (forward) or descending (reverse) successor order. These options
    vary traversal only, not the dataflow result.
    """
    if worklist not in ("fifo", "lifo"):
        raise ValueError(f"unsupported worklist order: {worklist}")
    if successors not in ("forward", "reverse"):
        raise ValueError(f"unsupported successor order: {successors}")
    tree, instructions, by_pc = _parse(list(tokens))
    slots = {ins["arg"] for ins in instructions if ins["op"] in ("BC_LOADVAR", "BC_STORE_LIST")}
    sink = len(tokens) + 1
    edges = {sink: set()}
    loop_specs = []

    def edge(source, target):
        edges.setdefault(source, set()).add(target)
        edges.setdefault(target, set())

    def compile_seq(items, following):
        current = following
        for item in reversed(items):
            tag = item[0]
            if tag == "op":
                ins = item[1]
                edge(ins["pc"], current)
                current = ins["pc"]
            elif tag == "if":
                _, begin, yes, no, has_else, end = item
                edge(end["pc"], current)
                then_entry = compile_seq(yes, end["pc"])
                else_entry = compile_seq(no, end["pc"]) if has_else else end["pc"]
                edge(begin["pc"], then_entry); edge(begin["pc"], else_entry)
                current = begin["pc"]
            elif tag == "repeat":
                _, begin, body, end = item
                count = _count_kind(instructions, begin)
                body_entry = compile_seq(body, end["pc"])
                edge(end["pc"], body_entry)
                edge(end["pc"], current)
                edge(begin["pc"], body_entry)
                if count in ("zero", "unknown"):
                    edge(begin["pc"], current)
                loop_specs.append({"kind": "Repeat", "count": count, "begin": begin["pc"],
                                   "end": end["pc"],
                                   "entry_edge": (begin["pc"], body_entry),
                                   "backedge": (end["pc"], body_entry) if count in ("positive", "unknown") else None,
                                   "exit_edges": ([(begin["pc"], current)] if count in ("zero", "unknown") else []) + [(end["pc"], current)]})
                if count == "zero":
                    edges[begin["pc"]].discard(body_entry)
                if count == "one":
                    edges[end["pc"]].discard(body_entry)
                current = begin["pc"]
            else:
                _, begin, condition, test, body, end = item
                cond_entry = compile_seq(condition, test["pc"])
                body_entry = compile_seq(body, end["pc"])
                edge(begin["pc"], cond_entry)
                edge(test["pc"], body_entry); edge(test["pc"], current)
                edge(end["pc"], cond_entry)
                loop_specs.append({"kind": "While", "count": "runtime", "begin": begin["pc"],
                                   "end": end["pc"],
                                   "entry_edge": (begin["pc"], cond_entry),
                                   "body_entry": body_entry, "test": test["pc"],
                                   "backedge": (end["pc"], cond_entry),
                                   "exit_edges": [(test["pc"], current)]})
                current = begin["pc"]
        return current

    first = compile_seq(tree, sink)
    for pc in by_pc:
        edges.setdefault(pc, set())
    initial = {name: frozenset(("?",)) for name in slots}
    def transfer(pc, state):
        if pc == sink:
            return state
        old_slots, old_stack = state
        values, stack = dict(old_slots), list(old_stack)
        op, arg = by_pc[pc]["op"], by_pc[pc]["arg"]
        def pop():
            if not stack:
                raise ValueError(f"abstract stack underflow at {op} token {pc}")
            return stack.pop()
        if op == "BC_CONST": stack.append(_literal_kind(arg))
        elif op == "BC_LOADVAR": stack.append(values[arg])
        elif op == "BC_STORE_LIST": values[arg] = pop()
        elif op == "BC_PRINT": pop()
        elif op == "BC_BINOP":
            right, left = pop(), pop()
            result = set()
            for a in left:
                for b in right:
                    result.add("?" if "?" in (a, b) else "D" if "D" in (a, b) else "I")
            stack.append(frozenset(result))
        elif op in ("BC_IF_BEGIN", "BC_REPEAT_BEGIN", "BC_WHILE_TEST"): pop()
        return values, tuple(stack)

    def solve(seeds, blocked_edges=frozenset()):
        """Solve from boundary states, optionally cutting selected graph edges."""
        incoming = dict(seeds)
        pending = deque(seeds)
        while pending:
            pc = pending.pop() if worklist == "lifo" else pending.popleft()
            out = transfer(pc, incoming[pc])
            targets = sorted(edges[pc], reverse=successors == "reverse")
            for target in targets:
                if (pc, target) in blocked_edges:
                    continue
                if target not in incoming:
                    incoming[target] = out
                    pending.append(target)
                    continue
                old_values, old_stack = incoming[target]
                new_values = {name: old_values[name] | out[0][name] for name in slots}
                if len(old_stack) != len(out[1]):
                    raise ValueError(f"incompatible stack heights joining at token {target}")
                new_stack = tuple(a | b for a, b in zip(old_stack, out[1]))
                merged = (new_values, new_stack)
                if merged != incoming[target]:
                    incoming[target] = merged
                    pending.append(target)
        return incoming

    incoming = solve({first: (initial, ())})

    edge_facts = {}
    edge_states = {}
    for source, targets in edges.items():
        if source not in incoming:
            continue
        out = transfer(source, incoming[source])
        for target in targets:
            edge_facts[(source, target)] = _freeze(out)
            edge_states[(source, target)] = out
    loads = [{"pc": ins["pc"], "name": ins["arg"],
              "kinds": incoming[ins["pc"]][0][ins["arg"]]}
             for ins in instructions if ins["op"] == "BC_LOADVAR" and ins["pc"] in incoming]
    loops = []
    for spec in loop_specs:
        item = dict(spec)
        item["entry_facts"] = edge_facts.get(spec["entry_edge"])
        item["backedge_facts"] = edge_facts.get(spec["backedge"]) if spec["backedge"] else None
        exits = [edge_facts[e]["slots"] for e in spec["exit_edges"] if e in edge_facts]
        item["exit_edge_facts"] = exits
        item["exit_facts"] = ({name: frozenset().union(*(state[name] for state in exits))
                               for name in slots} if exits else {})
        # These are boundary-labelled local traversals, not iteration-number
        # proofs: their seed states come from the globally converged solution.
        cuts = set(spec["exit_edges"])
        if spec["backedge"]:
            cuts.add(spec["backedge"])
        local = {}
        for label, boundary in (("entry", spec["entry_edge"]),
                                ("backedge", spec["backedge"])):
            seed = edge_states.get(boundary) if boundary else None
            local[label] = solve({boundary[1]: seed} if seed is not None else {}, cuts)
        uses = []
        for ins in instructions:
            if ins["op"] != "BC_LOADVAR" or not spec["begin"] < ins["pc"] < spec["end"]:
                continue
            use = {"pc": ins["pc"], "name": ins["arg"]}
            for label in ("entry", "backedge"):
                state = local[label].get(ins["pc"])
                use[f"{label}_kinds"] = state[0][ins["arg"]] if state else None
            reachable = [use[key] for key in ("entry_kinds", "backedge_kinds")
                         if use[key] is not None]
            # Partitioning before a nonrelational BINOP can be more precise
            # than the global merged state; do not promise equality to loads.
            use["kinds"] = frozenset().union(*reachable) if reachable else frozenset()
            uses.append(use)
        item["uses"] = uses
        loops.append(item)
    return {"nodes": {pc: _freeze(state) for pc, state in incoming.items()},
            "edges": edge_facts, "loads": loads, "loops": loops, "entry": first, "exit": sink}


def _freeze(state):
    return {"slots": _plain(state[0]), "stack": tuple(tuple(sorted(x)) for x in state[1])}


def _plain(values):
    return {name: frozenset(kinds) for name, kinds in values.items()}
