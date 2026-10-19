#!/usr/bin/env python3
"""Opt-in fresh-process resource comparison for production and presence maps.

This is a test-only experiment: it compiles an AST clone of the production
native emitter, changes only its two analyzer map initializations, and compares
it with the unmodified production emitter. No Timeline, trace hooks, metrics, or
callbacks run in either measured emitter. Clone/preparation and workload
construction are excluded from emit timing and tracemalloc; process RSS is a
coarse whole-process high-water mark and therefore includes that setup.

Example (from the checkout root)::

  python scripts/profile_presence_closures.py --output /tmp/kuro-presence-resource
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import platform
import resource
import subprocess
import sys
import time
import tracemalloc

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
MODES = ("production", "presence")
_ANALYZER_MAPS = {"incoming", "state", "current", "merged"}


def _validate_analyzer_map_contract(analyzer):
    """Fail closed if analyzer operations on its logical maps have changed.

    The contract currently depends on ``get`` with the default fact, shallow
    ``copy``, dense iteration via ``set(map)``, dict-style item assignment, and
    equality comparison for merge convergence. An added map API use needs an
    explicit review before being benchmarked against this test-only adapter.
    """
    from collections import Counter

    method_calls = Counter()
    subscript_contexts = Counter()
    set_iteration = Counter()
    merge_comparisons = Counter()
    for node in ast.walk(analyzer):
        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and node.value.id in _ANALYZER_MAPS:
            # All attribute access through these logical maps must be a direct,
            # allowlisted method call; this rejects e.g. map.setdefault or map.keys.
            parent_call = None
            for parent in ast.walk(analyzer):
                if isinstance(parent, ast.Call) and parent.func is node:
                    parent_call = parent
                    break
            assert parent_call is not None, f"unsupported analyzer map attribute: {ast.unparse(node)}"
            method_calls[(node.value.id, node.attr, len(parent_call.args), len(parent_call.keywords))] += 1
        elif isinstance(node, ast.Subscript) and isinstance(node.value, ast.Name) and node.value.id in _ANALYZER_MAPS:
            subscript_contexts[(node.value.id, type(node.ctx).__name__)] += 1
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "set" and len(node.args) == 1:
            argument = node.args[0]
            if isinstance(argument, ast.Name) and argument.id in _ANALYZER_MAPS:
                set_iteration[argument.id] += 1
        elif isinstance(node, ast.Compare) and isinstance(node.left, ast.Name):
            if node.left.id == "merged" and len(node.ops) == 1 and isinstance(node.ops[0], ast.NotEq):
                if len(node.comparators) == 1 and isinstance(node.comparators[0], ast.Name) and node.comparators[0].id == "current":
                    merge_comparisons[("merged", "!=", "current")] += 1

    # Logical maps may not escape through aliases or foreign functions. In
    # particular, dict.clear(state)/dict.copy(state) bypass overridden methods
    # on the candidate map and would make this benchmark invalid.
    for node in ast.walk(analyzer):
        if isinstance(node, ast.Call):
            map_arguments = [
                child for argument in [*node.args, *(kw.value for kw in node.keywords)]
                for child in ast.walk(argument)
                if isinstance(child, ast.Name) and child.id in _ANALYZER_MAPS
            ]
            is_allowed_set_iteration = (
                isinstance(node.func, ast.Name) and node.func.id == "set"
                and len(node.args) == 1 and not node.keywords
                and isinstance(node.args[0], ast.Name)
                and node.args[0].id in {"current", "state"}
            )
            if map_arguments and not is_allowed_set_iteration:
                raise AssertionError(
                    f"unsupported analyzer map passed to function: {ast.unparse(node)}"
                )
            if isinstance(node.func, ast.Name) and node.func.id in _ANALYZER_MAPS:
                raise AssertionError(f"unsupported analyzer map call: {ast.unparse(node)}")
        elif isinstance(node, (ast.Assign, ast.AnnAssign, ast.NamedExpr)):
            value = node.value
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            if (isinstance(value, ast.Name) and value.id in _ANALYZER_MAPS
                    and any(isinstance(target, ast.Name) for target in targets)):
                raise AssertionError(f"unsupported analyzer map alias assignment: {ast.unparse(node)}")

    expected_methods = Counter({
        ("incoming", "copy", 0, 0): 1,
        ("state", "copy", 0, 0): 1,
        ("state", "get", 2, 0): 5,
        ("current", "get", 2, 0): 1,
    })
    expected_subscripts = Counter({("state", "Store"): 6, ("merged", "Store"): 1})
    assert method_calls == expected_methods, f"analyzer map method contract changed: {dict(method_calls)}"
    assert subscript_contexts == expected_subscripts, f"analyzer map subscript contract changed: {dict(subscript_contexts)}"
    assert set_iteration == Counter({"current": 1, "state": 1}), f"analyzer map iteration contract changed: {dict(set_iteration)}"
    assert merge_comparisons == Counter({("merged", "!=", "current"): 1}), f"analyzer merge comparison changed: {dict(merge_comparisons)}"


def _make_presence_emitter(native):
    """Clone the original emitter with precisely two dense-presence map sites.

    The inherited clone helper is deliberately invoked with production mode and
    ``trace=False``. PresenceFacts is instantiated with ``metrics=None`` so its
    storage counters are disabled, not merely omitted from the report.
    """
    from scripts.audit_normalized_closures import _clone_tree
    from scripts.audit_presence_closures import PresenceFacts

    tree = _clone_tree(native, mode="production", trace=False)
    analyzers = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)
                 and node.name == "analyze_action_closure_returns"]
    assert len(analyzers) == 1, "nested analyzer shape changed"
    _validate_analyzer_map_contract(analyzers[0])
    hits = {"analyzer": 0, "initial_state": 0, "merged_map": 0}

    class PresenceMapSites(ast.NodeTransformer):
        inside_analyzer = False

        def visit_FunctionDef(self, node):
            if node.name != "analyze_action_closure_returns":
                return self.generic_visit(node)
            hits["analyzer"] += 1
            previous = self.inside_analyzer
            self.inside_analyzer = True
            node = self.generic_visit(node)
            self.inside_analyzer = previous
            return node

        def visit_Assign(self, node):
            if (self.inside_analyzer and len(node.targets) == 1
                    and ast.unparse(node.targets[0]) == "states[0]"):
                assert isinstance(node.value, ast.Dict) and not node.value.keys, (
                    "initial analyzer state ceased to be an empty dict"
                )
                hits["initial_state"] += 1
                node.value = ast.Call(
                    func=ast.Name(id="_PresenceFacts", ctx=ast.Load()),
                    args=[], keywords=[],
                )
            return self.generic_visit(node)

        def visit_AnnAssign(self, node):
            if (self.inside_analyzer and ast.unparse(node.target) == "merged"):
                assert isinstance(node.value, ast.Dict) and not node.value.keys, (
                    "analyzer merge map ceased to be an empty dict"
                )
                hits["merged_map"] += 1
                node.value = ast.Call(
                    func=ast.Name(id="_PresenceFacts", ctx=ast.Load()),
                    args=[], keywords=[],
                )
            return self.generic_visit(node)

    tree = PresenceMapSites().visit(tree)
    assert hits == {"analyzer": 1, "initial_state": 1, "merged_map": 1}, (
        f"presence candidate AST sites changed: {hits}"
    )
    ast.fix_missing_locations(tree)
    namespace = vars(native).copy()
    namespace["_PresenceFacts"] = lambda: PresenceFacts(metrics=None)
    exec(compile(tree, "<presence-resource-candidate>", "exec"), namespace)
    return namespace["emit_x86_64_linux"], tree


def _outcome(emitter, program):
    """Capture a complete successful output or exact error identity and text."""
    try:
        return {"ok": True, "assembly": emitter(program)}
    except Exception as error:
        return {
            "ok": False,
            "error_module": type(error).__module__,
            "error_type": type(error).__qualname__,
            "error_text": str(error),
        }


def _cpu_affinity(requested):
    """Best-effort CPU pinning; return the effective affinity or None."""
    if not hasattr(os, "sched_getaffinity") or not hasattr(os, "sched_setaffinity"):
        return None
    try:
        available = os.sched_getaffinity(0)
        if not available:
            return None
        cpu = min(available) if requested is None else requested
        if cpu not in available:
            raise ValueError(f"requested CPU {cpu} is not in available affinity {sorted(available)}")
        os.sched_setaffinity(0, {cpu})
        return sorted(os.sched_getaffinity(0))
    except OSError:
        # Affinity may be unavailable or disallowed in a container/macOS.
        return None


def _peak_rss():
    try:
        peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    except (AttributeError, OSError):
        return None, None
    # getrusage reports bytes on macOS and KiB on Linux/BSD implementations.
    unit = "bytes" if sys.platform == "darwin" else "kibibytes"
    return peak, unit


def _child(args):
    import compiler.native as native
    from scripts.profile_sparse_closures import sparse_workload

    affinity = _cpu_affinity(args.cpu)
    program = sparse_workload(args.size, args.random_cases, args.workload_seed)
    if args.mode == "production":
        emitter = native.emit_x86_64_linux
    else:
        emitter, _tree = _make_presence_emitter(native)

    if args.allocation:
        tracemalloc.start()
    started = time.perf_counter()
    outcome = _outcome(emitter, program)
    elapsed = time.perf_counter() - started
    traced_current = traced_peak = None
    if args.allocation:
        traced_current, traced_peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

    peak_rss, rss_unit = _peak_rss()
    if outcome["ok"]:
        args.result_path.with_suffix(".assembly").write_bytes(outcome["assembly"].encode("utf-8"))
        outcome = {"ok": True}
    data = {
        "mode": args.mode,
        "size": args.size,
        "allocation_sample": args.allocation,
        "emit_seconds": elapsed,
        "traced_current_bytes": traced_current,
        "traced_peak_bytes": traced_peak,
        "process_peak_rss": peak_rss,
        "process_peak_rss_unit": rss_unit,
        "rss_includes_setup": True,
        "assembly_bytes": len(_outcome_bytes := (args.result_path.with_suffix(".assembly").read_bytes()
                                                   if outcome["ok"] else b"")),
        "outcome": outcome,
        "hash_seed": os.environ.get("PYTHONHASHSEED"),
        "cpu_affinity": affinity,
        "pid": os.getpid(),
    }
    args.result_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def _sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _run_sample(output_dir, *, size, mode, seed, cpu, random_cases,
                workload_seed, allocation, sample_id):
    result_path = output_dir / f"{sample_id}.json"
    command = [
        sys.executable, str(Path(__file__).resolve()), "--_child",
        "--_result-path", str(result_path), "--_size", str(size),
        "--_mode", mode, "--_cpu", "none" if cpu is None else str(cpu),
        "--_random-cases", str(random_cases), "--_workload-seed", str(workload_seed),
    ]
    if allocation:
        command.append("--_allocation")
    env = {**os.environ, "PYTHONHASHSEED": str(seed)}
    subprocess.run(command, cwd=ROOT, env=env, check=True)
    result = json.loads(result_path.read_text(encoding="utf-8"))
    assembly_path = result_path.with_suffix(".assembly")
    result["command"] = command
    result["hash_seed"] = str(seed)
    return result, assembly_path


def _run_pair(output_dir, *, size, seed, cpu, random_cases, workload_seed,
              allocation, order_index, serial):
    order = MODES if order_index % 2 == 0 else tuple(reversed(MODES))
    results = {}
    assembly_paths = {}
    ids = {}
    for mode in order:
        sample_id = f"size{size}-seed{seed}-{'alloc' if allocation else 'time'}-{serial}-{mode}"
        sample, assembly_path = _run_sample(
            output_dir, size=size, mode=mode, seed=seed, cpu=cpu,
            random_cases=random_cases, workload_seed=workload_seed,
            allocation=allocation, sample_id=sample_id,
        )
        results[mode] = sample
        assembly_paths[mode] = assembly_path
        ids[mode] = sample_id

    # Unexpected errors indicate a changed workload/compiler or a broken
    # candidate; matching failures are not equivalent successful samples.
    import compiler.native as native
    for mode in MODES:
        outcome = results[mode]["outcome"]
        if not outcome["ok"] and not (
            outcome.get("error_module") == native.NativeBackendError.__module__
            and outcome.get("error_type") == native.NativeBackendError.__qualname__
        ):
            raise AssertionError(
                f"unexpected {mode} exception at size={size}, seed={seed}: "
                f"{outcome.get('error_module')}.{outcome.get('error_type')}: "
                f"{outcome.get('error_text')}"
            )

    # Compare full output or complete error objects before computing any digest.
    if results["production"]["outcome"] != results["presence"]["outcome"]:
        raise AssertionError(
            f"complete outcome mismatch at size={size}, seed={seed}, allocation={allocation}"
        )
    if results["production"]["outcome"]["ok"]:
        production_bytes = assembly_paths["production"].read_bytes()
        presence_bytes = assembly_paths["presence"].read_bytes()
        if production_bytes != presence_bytes:
            raise AssertionError(
                f"complete assembly mismatch at size={size}, seed={seed}, allocation={allocation}"
            )
        digest = hashlib.sha256(production_bytes).hexdigest()
        byte_count = len(production_bytes)
        for path in assembly_paths.values():
            path.unlink(missing_ok=True)
    else:
        digest = None
        byte_count = 0

    samples = []
    for mode in MODES:
        sample = results[mode]
        sample["complete_outcomes_equal"] = True
        sample["assembly_sha256_after_exact_compare"] = digest
        sample["all_output_bytes"] = byte_count
        sample["repetition_id"] = serial
        sample["comparison_order"] = list(order)
        sample["assembly_file"] = None
        result_path = output_dir / f"{ids[mode]}.json"
        sample.pop("outcome", None)  # complete result was compared; only summary is retained
        sample["sample_kind"] = "allocation" if allocation else "timing"
        result_path.write_text(json.dumps(sample, indent=2) + "\n", encoding="utf-8")
        samples.append(sample)
    return samples


def _report_metadata(args, cpu):
    import compiler.native as native

    source_files = {
        "native_module": Path(native.__file__),
        "profile_presence_closures.py": Path(__file__).resolve(),
        "audit_presence_closures.py": ROOT / "scripts/audit_presence_closures.py",
        "audit_normalized_closures.py": ROOT / "scripts/audit_normalized_closures.py",
        "profile_sparse_closures.py": ROOT / "scripts/profile_sparse_closures.py",
    }
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    return {
        "python": sys.version,
        "platform": platform.platform(),
        "implementation": platform.python_implementation(),
        "head": head,
        "source_sha256": {name: _sha256(path) for name, path in source_files.items()},
        "compiler_worktree_dirty": bool(subprocess.check_output(
            ["git", "status", "--porcelain", "--", "compiler"], cwd=ROOT, text=True
        ).strip()),
        "requested_command": [sys.executable, str(Path(__file__).resolve()), *sys.argv[1:] ],
        "modes": list(MODES),
        "hash_seeds": args.hash_seeds,
        "cpu_requested": cpu,
        "cpu_affinity_available": hasattr(os, "sched_getaffinity") and hasattr(os, "sched_setaffinity"),
        "random_cases": args.random_cases,
        "workload_seed": args.workload_seed,
        "timing_and_tracemalloc_are_separate_samples": True,
        "candidate_metrics": "PresenceFacts(metrics=None); storage counters disabled",
        "trace_callbacks": "none in either measured emitter",
        "preparation_excluded_from_emit_timing_and_tracemalloc": True,
        "rss_limitation": "ru_maxrss process high-water mark includes imports, workload construction, and candidate AST clone/compile; not emitter-only or a per-allocation measurement",
        "allocation_limitation": "tracemalloc observes Python-managed traced allocations, not all native allocations; emitter result and dict/set payloads are included",
        "dict_adapter_limitation": "PresenceFacts is a test-only dict subclass whose dict payload stores non-default facts while a set stores dense key presence; it is not a production abstraction",
        "speedup_assumed": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="directory for report and sample JSON files")
    parser.add_argument("--sizes", type=int, nargs="+", default=[40, 100, 200])
    parser.add_argument("--repeat", type=int, default=5, help="timing pairs per seed and size")
    parser.add_argument("--hash-seeds", type=int, nargs="+", default=[0, 1, 42])
    parser.add_argument("--cpu", type=int, help="optional CPU pin; best-effort where supported")
    parser.add_argument("--random-cases", type=int, default=8)
    parser.add_argument("--workload-seed", type=int, default=7319)
    parser.add_argument("--skip-allocation", action="store_true",
                        help="run timing pairs only; do not repeat allocation samples")
    parser.add_argument("--_child", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--_result-path", type=Path, help=argparse.SUPPRESS)
    parser.add_argument("--_size", type=int, default=40, help=argparse.SUPPRESS)
    parser.add_argument("--_mode", choices=MODES, help=argparse.SUPPRESS)
    parser.add_argument("--_cpu", default="none", help=argparse.SUPPRESS)
    parser.add_argument("--_random-cases", type=int, default=8, help=argparse.SUPPRESS)
    parser.add_argument("--_workload-seed", type=int, default=7319, help=argparse.SUPPRESS)
    parser.add_argument("--_allocation", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args._child:
        if args._result_path is None or args._mode is None:
            parser.error("internal child arguments missing")
        args.cpu = None if args._cpu == "none" else int(args._cpu)
        args.size = args._size
        args.mode = args._mode
        args.result_path = args._result_path
        args.random_cases = args._random_cases
        args.workload_seed = args._workload_seed
        args.allocation = args._allocation
        _child(args)
        return
    if args.output is None:
        parser.error("--output is required")
    if args.repeat < 1 or not args.sizes or any(n < 0 for n in args.sizes):
        parser.error("repeat must be positive and sizes nonnegative")
    if not args.hash_seeds or args.random_cases < 0:
        parser.error("at least one hash seed and nonnegative random-cases are required")
    args.output.mkdir(parents=True, exist_ok=True)
    cpu = args.cpu
    if cpu is None and hasattr(os, "sched_getaffinity"):
        try:
            cpu = min(os.sched_getaffinity(0))
        except (OSError, ValueError):
            cpu = None
    report = {
        "metadata": _report_metadata(args, cpu),
        "configuration": {
            "sizes": args.sizes,
            "timing_repetitions_per_seed": args.repeat,
            "allocation_repetitions_per_seed": 0 if args.skip_allocation else 1,
            "allocation_hash_seeds": [] if args.skip_allocation else args.hash_seeds[:1],
            "skip_allocation": args.skip_allocation,
            "complete": False,
            "fixed_hash_seeds": args.hash_seeds,
        },
        "sizes": {},
    }
    serial = 0
    for size in args.sizes:
        timing_samples = []
        allocation_samples = []
        for repetition in range(args.repeat):
            for seed_index, seed in enumerate(args.hash_seeds):
                order_index = repetition + seed_index
                print(f"size={size} repetition={repetition} seed={seed} kind=timing", flush=True)
                timing_samples.extend(_run_pair(
                    args.output, size=size, seed=seed, cpu=cpu,
                    random_cases=args.random_cases, workload_seed=args.workload_seed,
                    allocation=False, order_index=order_index, serial=serial,
                ))
                serial += 1
        if not args.skip_allocation:
            for seed_index, seed in enumerate(args.hash_seeds[:1]):
                print(f"size={size} seed={seed} kind=allocation", flush=True)
                allocation_samples.extend(_run_pair(
                    args.output, size=size, seed=seed, cpu=cpu,
                    random_cases=args.random_cases, workload_seed=args.workload_seed,
                    allocation=True, order_index=seed_index, serial=serial,
                ))
                serial += 1
        report["sizes"][str(size)] = {
            "full_outcomes_equal_before_hashing": True,
            "timing_samples": timing_samples,
            "allocation_samples": allocation_samples,
            "sample_counts": {"timing": len(timing_samples), "allocation": len(allocation_samples)},
        }
        (args.output / "report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    report["configuration"]["complete"] = True
    report["configuration"]["sample_counts"] = {
        "timing": sum(item["sample_counts"]["timing"] for item in report["sizes"].values()),
        "allocation": sum(item["sample_counts"]["allocation"] for item in report["sizes"].values()),
        "by_size": {size: item["sample_counts"] for size, item in report["sizes"].items()},
    }
    (args.output / "report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(args.output / "report.json", flush=True)


if __name__ == "__main__":
    main()
