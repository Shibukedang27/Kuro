#!/usr/bin/env python3
"""Fresh-process measurements; opt-in, test-only, no production modifications.

Run from the repository root with the installed test interpreter:
  .venv/bin/python scripts/profile_normalized_closures.py --output /tmp/normalized
Each sample owns a fresh Python process, pinned CPU and fixed hash seed. Timing
and tracemalloc are separate samples. Full output equality precedes digesting.
"""
from __future__ import annotations

import argparse
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
MODES = ("production", "legacy", "normalized")


def child(args):
    import compiler.native as native
    from scripts.audit_normalized_closures import make_emitter
    from scripts.profile_sparse_closures import sparse_workload
    os.sched_setaffinity(0, {args.cpu})
    program = sparse_workload(args.size, 8, 7319)
    emitter = native.emit_x86_64_linux if args.mode == "production" else make_emitter(native, mode=args.mode, trace=False)[0]
    if args.allocation:
        tracemalloc.start()
    started = time.perf_counter()
    assembly = emitter(program)
    seconds = time.perf_counter() - started
    traced = tracemalloc.get_traced_memory() if args.allocation else None
    if args.allocation:
        tracemalloc.stop()
    # Capture resource usage before writing output. Linux ru_maxrss is KiB and
    # includes interpreter, IR, AST clone setup and emitter, not just emission.
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    output = args.output.with_suffix(".s")
    output.write_text(assembly, encoding="utf-8")
    data = {"mode": args.mode, "size": args.size, "allocation_sample": args.allocation,
            "emit_seconds": seconds, "traced_current_bytes": traced[0] if traced else None,
            "traced_peak_bytes": traced[1] if traced else None, "process_peak_rss_kib": rss,
            "assembly_bytes": len(assembly.encode()), "assembly_sha256": hashlib.sha256(assembly.encode()).hexdigest(),
            "hash_seed": os.environ.get("PYTHONHASHSEED"), "cpu_affinity": sorted(os.sched_getaffinity(0)),
            "pid": os.getpid()}
    args.output.write_text(json.dumps(data, indent=2) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--sizes", type=int, nargs="+", default=[80, 160])
    parser.add_argument("--repeat", type=int, default=3)
    parser.add_argument("--cpu", type=int, default=min(os.sched_getaffinity(0)))
    parser.add_argument("--child", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--size", type=int, default=80, help=argparse.SUPPRESS)
    parser.add_argument("--mode", choices=MODES, help=argparse.SUPPRESS)
    parser.add_argument("--allocation", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.child:
        child(args)
        return
    if args.repeat < 1 or any(n < 0 for n in args.sizes):
        parser.error("repeat must be positive and sizes nonnegative")
    args.output.mkdir(parents=True, exist_ok=True)
    import compiler.native as native
    scripts = [Path(__file__), ROOT / "scripts/audit_normalized_closures.py", ROOT / "scripts/profile_sparse_closures.py"]
    report = {"metadata": {"python": sys.version, "platform": platform.platform(),
        "head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "production_sha256": hashlib.sha256(Path(native.__file__).read_bytes()).hexdigest(),
        "scripts_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in scripts},
        "compiler_dirty": bool(subprocess.check_output(["git", "status", "--porcelain", "--", "compiler"], cwd=ROOT, text=True).strip()),
        "hash_seed": "0", "cpu": args.cpu, "random_cases": 8, "seed": 7319,
        "timing_allocation_separate": True}, "sizes": {}}
    for size in args.sizes:
        expected = None
        samples = []
        # Cyclic order balances each mode's position across three repetitions.
        for repetition in range(args.repeat + 1):
            allocation = repetition == args.repeat
            order = MODES[repetition % 3:] + MODES[:repetition % 3]
            for mode in order:
                prefix = args.output / f"size{size}-{mode}-{'alloc' if allocation else repetition}"
                command = [sys.executable, str(Path(__file__).resolve()), "--child", "--output", str(prefix.with_suffix('.json')),
                           "--size", str(size), "--mode", mode, "--cpu", str(args.cpu)]
                if allocation:
                    command.append("--allocation")
                print(f"size={size} mode={mode} sample={'allocation' if allocation else repetition}", flush=True)
                subprocess.run(command, cwd=ROOT, env={**os.environ, "PYTHONHASHSEED": "0"}, check=True)
                assembly = prefix.with_suffix('.s').read_bytes()
                if expected is None:
                    expected = assembly
                assert assembly == expected, f"complete assembly mismatch: {prefix}"
                sample = json.loads(prefix.with_suffix('.json').read_text())
                sample["repetition"] = None if allocation else repetition
                samples.append(sample)
        report["sizes"][str(size)] = {"all_full_outputs_equal": True, "samples": samples}
        (args.output / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(args.output / "report.json", flush=True)


if __name__ == "__main__":
    main()
