#!/usr/bin/env python3
"""Opt-in benchmark of sparse empty/unknown closure facts (test-only AST clones).

Examples:
  python scripts/profile_sparse_closures.py --output /tmp/sparse --size 160
  python scripts/profile_sparse_closures.py --output /tmp/sparse --size 600 --repeat 3 --random-cases 8

The production emitter is never edited or instrumented. Uninstrumented emissions
are timed independently from instrumented merge-work accounting. The JSON report
contains complete outcomes (including full assembly or exact error type/text).
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import inspect
import json
import platform
from pathlib import Path
import random
import subprocess
import sys
import time


def _ins(op, *args, dest=None):
    from compiler.ir import Instr
    return Instr(op, tuple(args), dest)


def _fn(name, *body):
    from compiler.ir import IRFunction
    return IRFunction(name, [], list(body))


def sparse_workload(size: int = 160, random_cases: int = 4, seed: int = 7319):
    """Return valid seeded IR: numeric pressure, CFG joins/loops, aliases, recursion."""
    from compiler.ir import IRProgram
    if size < 0 or random_cases < 0:
        raise ValueError("size and random_cases must be nonnegative")
    funcs = {
        "TargetA": _fn("TargetA", _ins("CONST", 17, dest="n"), _ins("RETURN", "n")),
        "TargetB": _fn("TargetB", _ins("CONST", 27, dest="n"), _ins("RETURN", "n")),
        "ChainTop": _fn("ChainTop", _ins("CALL", "ChainMiddle", dest="c"), _ins("RETURN", "c")),
        "ChainMiddle": _fn("ChainMiddle", _ins("CALL", "ChainLeaf", dest="c"), _ins("RETURN", "c")),
        "ChainLeaf": _fn("ChainLeaf", _ins("CONST", "TargetA", dest="t"), _ins("CALL", "MakeClosure", "t", dest="c"), _ins("RETURN", "c")),
        "ScalarReturn": _fn("ScalarReturn", _ins("CONST", 5, dest="n"), _ins("RETURN", "n")),
        # Recursion with independent direct seeds exercises fixed-point propagation.
        "RecursiveA": _fn("RecursiveA", _ins("CALL", "RecursiveB", dest="ignored"), _ins("CONST", "TargetA", dest="t"), _ins("CALL", "MakeClosure", "t", dest="c"), _ins("RETURN", "c")),
        "RecursiveB": _fn("RecursiveB", _ins("CALL", "RecursiveA", dest="ignored"), _ins("CONST", "TargetB", dest="t"), _ins("CALL", "MakeClosure", "t", dest="c"), _ins("RETURN", "c")),
    }
    body = []
    # Many live numeric facts make state mappings meaningfully wide.
    for i in range(size):
        body.extend((_ins("CONST", i, dest=f"num_{i}"), _ins("LOADVAR", f"num_{i}", dest=f"num_alias_{i}")))
    body.extend((_ins("CONST", "TargetA", dest="target_a"), _ins("CALL", "MakeClosure", "target_a", dest="closure_a"),
                 _ins("CONST", "TargetB", dest="target_b"), _ins("CALL", "MakeClosure", "target_b", dest="closure_b")))
    body.extend((_ins("LABEL", dest="loop"), _ins("CONST", 1, dest="loop_cond"),
                 _ins("JUMPF", "loop_exit", "loop_cond"), _ins("LOADVAR", "selected", dest="loop_alias"),
                 _ins("UPDATE", "selected", "loop_alias"), _ins("JUMP", "loop"), _ins("LABEL", dest="loop_exit")))
    # Deterministic branch diamonds repeatedly reconverge distinct closure targets.
    rng = random.Random(seed)
    for layer in range(max(1, min(24, size // 6 + 1))):
        right, join = f"right_{layer}", f"join_{layer}"
        cond_value = rng.randrange(2)
        body.extend((_ins("CONST", cond_value, dest=f"condition_{layer}"), _ins("JUMPF", right, f"condition_{layer}"),
                     _ins("LOADVAR", "closure_a", dest=f"left_alias_{layer}"),
                     _ins("STORE_LIST", f"box_{layer}", [f"left_alias_{layer}"]),
                     _ins("UPDATE", "selected", f"box_{layer}"), _ins("JUMP", join),
                     _ins("LABEL", dest=right), _ins("LOADVAR", "closure_b", dest=f"right_alias_{layer}"),
                     _ins("STORE_LIST", f"box_{layer}", [f"right_alias_{layer}"]),
                     _ins("UPDATE", "selected", f"box_{layer}"), _ins("LABEL", dest=join)))
    # Missing-name join: a value defined only on one arm is unknown at reconvergence.
    body.extend((_ins("CONST", 1, dest="missing_cond"), _ins("JUMPF", "missing_right", "missing_cond"),
                 _ins("CONST", "TargetA", dest="one_arm_only"), _ins("JUMP", "missing_join"),
                 _ins("LABEL", dest="missing_right"), _ins("LABEL", dest="missing_join"),
                 _ins("LOADVAR", "one_arm_only", dest="missing_alias")))
    body.extend((_ins("CONST", 1, dest="sparse_cond"), _ins("JUMPF", "sparse_right", "sparse_cond"),
                 _ins("LOADVAR", "closure_a", dest="nonempty_unknown"), _ins("JUMP", "sparse_join"),
                 _ins("LABEL", dest="sparse_right"), _ins("LABEL", dest="sparse_join")))
    # Unreachable closure return must not contribute to the summary.
    body.extend((_ins("JUMP", "live_return"), _ins("CONST", "TargetB", dest="dead_name"),
                 _ins("CALL", "MakeClosure", "dead_name", dest="dead_closure"), _ins("RETURN", "dead_closure"),
                 _ins("LABEL", dest="live_return"), _ins("RETURN", "selected")))
    funcs["SparseStress"] = _fn("SparseStress", *body)
    main = []
    for name in ("ChainTop", "SparseStress", "RecursiveA"):
        main.extend((_ins("CALL", name, dest=f"closure_{name}"), _ins("CALL", "Invoke", f"closure_{name}", dest=f"value_{name}")))
    main.append(_ins("CALL", "ScalarReturn", dest="scalar_value"))
    for case in range(random_cases):
        # These seeded diamond/loop graphs are reachable and always return a
        # known closure; negative return shapes are separate named cases.
        fn_name = f"RandomGraph{case}"
        generated = generated_graph_workload(seed + 1009 * (case + 1), "known", function_name=fn_name)
        funcs.update({key: value for key, value in generated.functions.items() if key != fn_name})
        funcs[fn_name] = generated.functions[fn_name]
        main.extend((_ins("CALL", fn_name, dest=f"random_closure_{case}"), _ins("CALL", "Invoke", f"random_closure_{case}", dest=f"random_value_{case}")))
    return IRProgram(main=main, functions=funcs)


def negative_workload():
    """A returned known closure mixed with scalar and absent/unknown return paths."""
    from compiler.ir import IRProgram
    funcs = {
        "TargetA": _fn("TargetA", _ins("CONST", 1, dest="n"), _ins("RETURN", "n")),
        "UnknownMixed": _fn("UnknownMixed", _ins("CONST", "TargetA", dest="t"), _ins("CALL", "MakeClosure", "t", dest="c"),
                             _ins("CONST", 1, dest="cond"), _ins("JUMPF", "scalar", "cond"), _ins("RETURN", "c"),
                             _ins("LABEL", dest="scalar"), _ins("CONST", 8, dest="n"), _ins("RETURN", "n")),
    }
    return IRProgram(main=[_ins("CALL", "UnknownMixed", dest="maybe"), _ins("CALL", "Invoke", "maybe", dest="result")], functions=funcs)


def generated_graph_workload(seed: int, return_mode: str | None = None, *, function_name: str = "GeneratedGraph"):
    """Build a small, reachable, seeded CFG with varied closure dataflow."""
    from compiler.ir import IRProgram
    rng = random.Random(seed)
    modes = ("known", "missing", "scalar")
    if return_mode is None:
        return_mode = modes[seed % len(modes)]
    if return_mode not in modes:
        raise ValueError(f"unknown generated return mode: {return_mode}")
    name = function_name
    body = [
        _ins("CONST", "GraphTargetA", dest="target_a"),
        _ins("CALL", "MakeClosure", "target_a", dest="closure_a"),
        _ins("CONST", "GraphTargetB", dest="target_b"),
        _ins("CALL", "MakeClosure", "target_b", dest="closure_b"),
        _ins("LOADVAR", "closure_a", dest="selected"),
    ]
    # Different layer counts yield different reachable CFG topologies. Each
    # layer has two live arms, one arm-local value, aliasing, stores and updates.
    for layer in range(1 + rng.randrange(3)):
        right, join = f"right_{layer}", f"join_{layer}"
        only = f"{name}_only_{layer}"
        cond = f"condition_{layer}"
        body.extend((
            _ins("CONST", rng.randrange(2), dest=cond),
            _ins("JUMPF", right, cond),
            _ins("LOADVAR", "closure_a", dest=f"left_alias_{layer}"),
            _ins("STORE_LIST", f"box_{layer}", [f"left_alias_{layer}"]),
            _ins("UPDATE", "selected", f"box_{layer}"),
            _ins("LOADVAR", "closure_a", dest=only),
            _ins("JUMP", join),
            _ins("LABEL", dest=right),
            _ins("LOADVAR", "closure_b", dest=f"right_alias_{layer}"),
            _ins("STORE_LIST", f"box_{layer}", [f"right_alias_{layer}"]),
            _ins("UPDATE", "selected", f"box_{layer}"),
            _ins("LABEL", dest=join),
            _ins("LOADVAR", only, dest=f"{name}_observed_{layer}"),
        ))
    if rng.randrange(2):
        body.extend((
            _ins("LABEL", dest="loop"),
            _ins("CONST", rng.randrange(2), dest="loop_condition"),
            _ins("JUMPF", "loop_exit", "loop_condition"),
            _ins("LOADVAR", "selected", dest="loop_alias"),
            _ins("STORE_LIST", "loop_box", ["loop_alias"]),
            _ins("UPDATE", "selected", "loop_box"),
            _ins("JUMP", "loop"),
            _ins("LABEL", dest="loop_exit"),
        ))
    if return_mode == "known":
        body.append(_ins("RETURN", "selected"))
    elif return_mode == "scalar":
        body.extend((_ins("CONST", rng.randrange(10), dest="scalar_result"), _ins("RETURN", "scalar_result")))
    else:
        body.extend((
            _ins("CONST", rng.randrange(2), dest="return_condition"),
            _ins("JUMPF", "missing_return", "return_condition"),
            _ins("LOADVAR", "selected", dest="partial_result"),
            _ins("JUMP", "return_join"),
            _ins("LABEL", dest="missing_return"),
            _ins("LABEL", dest="return_join"),
            _ins("RETURN", "partial_result"),
        ))
    functions = {
        "GraphTargetA": _fn("GraphTargetA", _ins("CONST", 17, dest="n"), _ins("RETURN", "n")),
        "GraphTargetB": _fn("GraphTargetB", _ins("CONST", 27, dest="n"), _ins("RETURN", "n")),
        name: _fn(name, *body),
    }
    main = [_ins("CALL", name, dest="graph_closure"), _ins("CALL", "Invoke", "graph_closure", dest="graph_value")]
    return IRProgram(main=main, functions=functions)


def closure_edge_workloads():
    """Explicit known/unreachable, missing, overwritten and loop-zero returns."""
    from compiler.ir import IRProgram
    targets = {
        "TargetA": _fn("TargetA", _ins("CONST", 1, dest="n"), _ins("RETURN", "n")),
    }
    cases = {
        "unreachable_scalar_return": [
            _ins("JUMP", "live"), _ins("CONST", 4, dest="dead_scalar"), _ins("RETURN", "dead_scalar"),
            _ins("LABEL", dest="live"), _ins("CONST", "TargetA", dest="target"),
            _ins("CALL", "MakeClosure", "target", dest="closure"), _ins("RETURN", "closure"),
        ],
        "missing_target_return": [
            _ins("CONST", 1, dest="cond"), _ins("JUMPF", "missing", "cond"),
            _ins("CONST", "TargetA", dest="target"), _ins("CALL", "MakeClosure", "target", dest="closure"),
            _ins("JUMP", "join"), _ins("LABEL", dest="missing"), _ins("LABEL", dest="join"),
            _ins("RETURN", "closure"),
        ],
        "overwritten_closure": [
            _ins("CONST", "TargetA", dest="target"), _ins("CALL", "MakeClosure", "target", dest="closure"),
            _ins("CONST", 9, dest="closure"), _ins("RETURN", "closure"),
        ],
        "loop_zero_path_unknown": [
            _ins("LABEL", dest="loop"), _ins("CONST", 1, dest="cond"), _ins("JUMPF", "done", "cond"),
            _ins("CONST", "TargetA", dest="target"), _ins("CALL", "MakeClosure", "target", dest="closure"),
            _ins("JUMP", "loop"), _ins("LABEL", dest="done"), _ins("RETURN", "closure"),
        ],
    }
    programs = {}
    for case_name, body in cases.items():
        function_name = "EdgeCase"
        programs[case_name] = IRProgram(
            main=[_ins("CALL", function_name, dest="maybe"), _ins("CALL", "Invoke", "maybe", dest="result")],
            functions={**targets, function_name: _fn(function_name, *body)},
        )
    return programs


def _transform_emitter(native, *, sparse=False, legacy=False, instrument=False):
    """Clone emitter AST and apply strictly asserted analyzer-only changes."""
    tree = ast.parse(inspect.getsource(native.emit_x86_64_linux))
    hits = {"analyzer": 0, "initial_state": 0, "merged_map": 0, "get_default": 0,
            "incoming_copy": 0, "successor_copy": 0, "merge_loop": 0, "target_union": 0,
            "body_visit": 0, "return_site": 0}

    def expr(src):
        return ast.parse(src).body[0]

    class Clone(ast.NodeTransformer):
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
            if not self.inside:
                return self.generic_visit(node)
            target = ast.unparse(node.targets[0]) if len(node.targets) == 1 else ""
            value = ast.unparse(node.value)
            before = []
            if target == "states[0]" and value == "{}":
                hits["initial_state"] += 1
                if sparse:
                    node.value = ast.copy_location(ast.Name(id="_SparseFacts", ctx=ast.Load()), node.value)
                    node.value = ast.Call(func=node.value, args=[], keywords=[])
            elif target == "merged" and isinstance(node.value, ast.Dict):
                hits["merged_map"] += 1
                if sparse:
                    node.value = ast.Call(func=ast.Name(id="_SparseFacts", ctx=ast.Load()), args=[], keywords=[])
            if target == "state" and value == "incoming.copy()":
                hits["incoming_copy"] += 1
            if target == "states[successor]" and value == "state.copy()":
                hits["successor_copy"] += 1
            if target == "item" and value == "body[index]":
                hits["body_visit"] += 1
            if instrument and target in {"state", "states[successor]"} and isinstance(node.value, ast.Call) and ast.unparse(node.value).endswith(".copy()"):
                source = ast.unparse(node.value.func.value)
                before += [expr(f'_sparse_metrics["copy_calls"] += 1'), expr(f'_sparse_metrics["copy_entries"] += len({source})')]
            return before + [self.generic_visit(node)]
        def visit_AnnAssign(self, node):
            if not self.inside:
                return self.generic_visit(node)
            if ast.unparse(node.target) == "merged":
                hits["merged_map"] += 1
                if sparse:
                    node.value = ast.Call(func=ast.Name(id="_SparseFacts", ctx=ast.Load()), args=[], keywords=[])
                if instrument:
                    node = self.generic_visit(node)
                    return [expr('_merge_started = time.perf_counter()'), expr('_sparse_metrics["merge_attempts"] += 1'), node]
            return self.generic_visit(node)
        def visit_If(self, node):
            if legacy and any(isinstance(x, ast.Name) and x.id == "closure_return_constructors" for x in ast.walk(node.test)):
                hits["return_site"] += 1
                return None
            return self.generic_visit(node)
        def visit_For(self, node):
            if not self.inside:
                return self.generic_visit(node)
            if ast.unparse(node.target) == "name" and ast.unparse(node.iter) == "set(current) | set(state)":
                hits["merge_loop"] += 1
                if instrument:
                    node.iter = ast.Call(func=ast.Name(id="_sparse_name_union", ctx=ast.Load()), args=[ast.Name(id="current", ctx=ast.Load()), ast.Name(id="state", ctx=ast.Load())], keywords=[])
            return self.generic_visit(node)
        def visit_BinOp(self, node):
            if self.inside and isinstance(node.op, ast.BitOr) and ast.unparse(node) == "set(current_targets) | set(incoming_targets)":
                hits["target_union"] += 1
                if instrument:
                    return ast.copy_location(ast.Call(func=ast.Name(id="_sparse_target_union", ctx=ast.Load()), args=[ast.Name(id="current_targets", ctx=ast.Load()), ast.Name(id="incoming_targets", ctx=ast.Load())], keywords=[]), node)
            return self.generic_visit(node)
        def visit_Call(self, node):
            if self.inside and isinstance(node.func, ast.Attribute) and node.func.attr == "get":
                if len(node.args) == 2 and ast.unparse(node.args[1]) == "(set(), False)":
                    hits["get_default"] += 1
            return self.generic_visit(node)

    clone = Clone()
    tree = clone.visit(tree)
    assert hits["analyzer"] == 1, f"analyzer shape changed: {hits}"
    # Assignment/dict annotation differs across Python versions, but exactly one merge map must exist.
    assert hits["initial_state"] == 1 and hits["merged_map"] == 1 and hits["get_default"] == 6, f"state-map/default sites changed: {hits}"
    if legacy:
        assert hits["return_site"] == 1, f"seedless guard changed: {hits}"
        # Restore two full-state deep copies only at the two expected assignment sites.
        class RestoreCopies(ast.NodeTransformer):
            inside = False
            count = 0
            def visit_FunctionDef(self, node):
                if node.name == "analyze_action_closure_returns":
                    self.inside = True
                    node = self.generic_visit(node)
                    self.inside = False
                    return node
                return self.generic_visit(node)
            def visit_Assign(self, node):
                if self.inside and len(node.targets) == 1 and ast.unparse(node.targets[0]) in {"state", "states[successor]"}:
                    target = ast.unparse(node.targets[0]); expected_source = "incoming" if target == "state" else "state"
                    if ast.unparse(node.value) == expected_source + ".copy()":
                        node.value = ast.parse("{name: (set(targets), is_known) for name, (targets, is_known) in " + expected_source + ".items()}").body[0].value
                        self.count += 1
                return self.generic_visit(node)
        restore = RestoreCopies(); tree = restore.visit(tree)
        assert restore.count == 2, f"legacy clone sites changed: {restore.count}"
    if instrument:
        assert hits["incoming_copy"] == 1 and hits["successor_copy"] == 1 and hits["merge_loop"] == 1 and hits["target_union"] == 1 and hits["body_visit"] > 0, f"instrumentation sites changed: {hits}"
        class AddCounters(ast.NodeTransformer):
            inside = False
            def visit_FunctionDef(self, node):
                if node.name == "analyze_action_closure_returns":
                    self.inside = True; node = self.generic_visit(node); self.inside = False
                    node.body.insert(0, expr('_sparse_metrics["analyzer_calls"] += 1'))
                    return node
                return self.generic_visit(node)
            def visit_Assign(self, node):
                if not self.inside: return self.generic_visit(node)
                if len(node.targets) == 1 and ast.unparse(node.targets[0]) == "item" and ast.unparse(node.value) == "body[index]":
                    return [expr('_sparse_metrics["body_visits"] += 1'), self.generic_visit(node)]
                if len(node.targets) == 1 and ast.unparse(node.targets[0]) == "states[successor]" and ast.unparse(node.value) == "merged":
                    return [expr('_sparse_metrics["merge_updates"] += 1'), self.generic_visit(node)]
                return self.generic_visit(node)
            def visit_Return(self, node):
                if self.inside and ast.unparse(node.value) == "(returned, all_returns_known, saw_return)":
                    node = self.generic_visit(node)
                    return [expr("_sparse_record_states(states)"), node]
                return self.generic_visit(node)
        tree = AddCounters().visit(tree)
        class CountDeepCopies(ast.NodeTransformer):
            inside = False
            def visit_FunctionDef(self, node):
                if node.name == "analyze_action_closure_returns":
                    self.inside = True; node = self.generic_visit(node); self.inside = False
                    return node
                return self.generic_visit(node)
            def visit_Assign(self, node):
                if self.inside and len(node.targets) == 1 and ast.unparse(node.targets[0]) in {"state", "states[successor]"} and isinstance(node.value, ast.DictComp):
                    source = ast.unparse(node.value.generators[0].iter.func.value)
                    return [expr(f'_sparse_metrics["deep_target_copy_entries"] += len({source})'), self.generic_visit(node)]
                return self.generic_visit(node)
        tree = CountDeepCopies().visit(tree)
        # Count the final merge even if it is unchanged, with timing ending immediately before comparison.
        class EndMergeTimer(ast.NodeTransformer):
            inside = False
            def visit_FunctionDef(self, node):
                if node.name == "analyze_action_closure_returns":
                    self.inside = True; node = self.generic_visit(node); self.inside = False
                    return node
                return self.generic_visit(node)
            def visit_If(self, node):
                node = self.generic_visit(node)
                if self.inside and ast.unparse(node.test) == "merged != current":
                    node.test = ast.BoolOp(op=ast.And(), values=[ast.Call(func=ast.Name(id="_sparse_end_merge", ctx=ast.Load()), args=[ast.Name(id="_merge_started", ctx=ast.Load())], keywords=[]), node.test])
                return node
        tree = EndMergeTimer().visit(tree)
    ast.fix_missing_locations(tree)
    return tree


class SparseFacts(dict):
    """Map that elides only (empty targets, False); empty-known remains explicit."""
    def __setitem__(self, key, value):
        targets, known = value
        if not targets and not known:
            self.pop(key, None)
        else:
            super().__setitem__(key, (set(targets), known))
    def copy(self):
        result = type(self)()
        result.update(self)
        return result


def make_emitter(native, *, mode="sparse", instrument=False):
    if mode not in {"production", "legacy", "sparse"}:
        raise ValueError(mode)
    metrics = {"analyzer_calls": 0, "body_visits": 0, "copy_calls": 0, "copy_entries": 0,
               "deep_target_copy_entries": 0, "merge_attempts": 0, "merge_updates": 0,
               "union_candidate_names": 0, "target_set_operand_elements": 0,
               "target_union_result_elements": 0, "merge_seconds": 0.0,
               "map_size_histogram": {}, "max_mapping_size": 0, "mapping_entries": 0,
               "empty_unknown_entries": 0, "empty_known_entries": 0,
               "nonempty_unknown_entries": 0, "one_sided_join_names": 0}
    tree = _transform_emitter(native, sparse=(mode == "sparse"), legacy=(mode == "legacy"), instrument=instrument)
    namespace = vars(native).copy()
    namespace["_SparseFacts"] = SparseFacts
    if instrument:
        namespace["time"] = time
        namespace["_sparse_metrics"] = metrics
        namespace["_sparse_name_union"] = lambda left, right: _name_union(left, right, metrics)
        namespace["_sparse_target_union"] = lambda left, right: _target_union(left, right, metrics)
        namespace["_sparse_record_states"] = lambda states: _record_states(states, metrics)
        namespace["_sparse_end_merge"] = lambda started: _finish_merge(started, metrics)
    exec(compile(tree, f"<{mode}-sparse-closure-emitter>", "exec"), namespace)
    return namespace["emit_x86_64_linux"], metrics


def _name_union(left, right, metrics):
    names = set(left) | set(right)
    metrics["union_candidate_names"] += len(names)
    metrics["one_sided_join_names"] += sum((name in left) != (name in right) for name in names)
    return names


def _target_union(left, right, metrics):
    metrics["target_set_operand_elements"] += len(left) + len(right)
    result = set(left) | set(right)
    metrics["target_union_result_elements"] += len(result)
    return result


def _record_states(states, metrics):
    for mapping in states:
        if mapping is None:
            continue
        size = len(mapping)
        histogram = metrics["map_size_histogram"]
        histogram[str(size)] = histogram.get(str(size), 0) + 1
        metrics["max_mapping_size"] = max(metrics["max_mapping_size"], size)
        metrics["mapping_entries"] += size
        metrics["empty_unknown_entries"] += sum(1 for targets, known in mapping.values() if not targets and not known)
        metrics["empty_known_entries"] += sum(1 for targets, known in mapping.values() if not targets and known)
        metrics["nonempty_unknown_entries"] += sum(1 for targets, known in mapping.values() if targets and not known)


def _finish_merge(started, metrics):
    metrics["merge_seconds"] += time.perf_counter() - started
    return True


def _outcome(emitter, program):
    from compiler.native import NativeBackendError
    try:
        return {"kind": "assembly", "assembly": emitter(program)}
    except NativeBackendError as error:
        return {"kind": "native-error", "type": f"{type(error).__module__}.{type(error).__qualname__}", "text": str(error)}


def _measure(emitter, program, repeat):
    runs = []
    previous = None
    for _ in range(repeat):
        start = time.perf_counter()
        result = _outcome(emitter, program)
        runs.append(time.perf_counter() - start)
        if previous is not None:
            assert result == previous, "emission outcome changed between repetitions"
        previous = result
    return previous, runs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="report filename prefix")
    parser.add_argument("--size", type=int, default=160, help="numeric local pairs in seeded stress function")
    parser.add_argument("--repeat", type=int, default=1)
    parser.add_argument("--random-cases", type=int, default=4)
    parser.add_argument("--seed", type=int, default=7319)
    args = parser.parse_args()
    if args.size < 0 or args.repeat < 1 or args.random_cases < 0:
        parser.error("size/random-cases must be nonnegative and repeat must be positive")
    root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(root))
    import compiler.native as native
    programs = {"large_seeded_cfg": sparse_workload(args.size, args.random_cases, args.seed),
                "intentional_unknown_return_error": negative_workload()}
    programs.update(closure_edge_workloads())
    for case in range(args.random_cases):
        graph_seed = args.seed + case
        programs[f"generated_seed_{graph_seed}"] = generated_graph_workload(graph_seed)
    emitters = {"production": native.emit_x86_64_linux, "legacy_unpruned": make_emitter(native, mode="legacy")[0],
                "sparse": make_emitter(native, mode="sparse")[0]}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    report = {"metadata": {"python": sys.version, "platform": platform.platform(),
                            "head": subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip(),
                            "size": args.size, "random_cases": args.random_cases, "seed": args.seed,
                            "production_file_sha256": hashlib.sha256(Path(native.__file__).read_bytes()).hexdigest(),
                            "compiler_dirty": bool(subprocess.check_output(["git", "-C", str(root), "status", "--porcelain", "--", "compiler"], text=True).strip()),
                            "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                            "instrumented_timing_is_separate": True}, "cases": {}}
    for case_name, program in programs.items():
        outcomes, timings = {}, {}
        for name, emitter in emitters.items():
            outcome, seconds = _measure(emitter, program, args.repeat)
            outcomes[name] = outcome
            timings[name] = seconds
        assert outcomes["production"] == outcomes["legacy_unpruned"] == outcomes["sparse"], f"semantic mismatch: {case_name}"
        if case_name == "large_seeded_cfg":
            assert outcomes["production"]["kind"] == "assembly" and outcomes["production"]["assembly"], "positive workload must emit assembly"
        instrumented_counts = {}
        for name, mode in (("production", "production"), ("legacy_unpruned", "legacy"), ("sparse", "sparse")):
            # Fresh emitter state per case keeps each set of instrumentation
            # counters cumulative only within that case, never across cases.
            emitter, metrics = make_emitter(native, mode=mode, instrument=True)
            outcome = _outcome(emitter, program)
            assert outcome == outcomes[name], f"instrumented outcome mismatch for {case_name}/{name}"
            instrumented_counts[name] = {key: (dict(value) if isinstance(value, dict) else value) for key, value in metrics.items()}
        report["cases"][case_name] = {"outcomes": outcomes, "uninstrumented_emit_seconds": timings,
                                       "instrumented_merge_counters": instrumented_counts}
        if outcomes["production"]["kind"] == "assembly":
            (args.output.parent / f"{args.output.name}.{case_name}.s").write_text(outcomes["production"]["assembly"], encoding="utf-8")
    report["recommendation"] = "Sparse empty/unknown omission is test-only; compare semantic equivalence and mapping/copy/merge evidence before any production proposal. No production change made."
    args.output.with_suffix(".json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"report": str(args.output.with_suffix('.json')), "cases": list(programs),
                      "outcomes_match": True, "sizes": {k: len(v["outcomes"]["production"].get("assembly", "")) for k, v in report["cases"].items()}}, indent=2))


if __name__ == "__main__":
    main()
