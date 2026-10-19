#!/usr/bin/env python3
"""Measure hosted generator emission, not source compilation or host linking.

Examples (from the repository root):
  python scripts/profile_hosted_emitter.py --output /tmp/kuro-emitter
  python scripts/profile_hosted_emitter.py --output /tmp/kuro-profile --profile
  python scripts/profile_hosted_emitter.py --root ../Kuro-baseline --output /tmp/before

The output prefix receives .s and .json files, plus .prof with --profile.
Use the same interpreter/host and compare .s bytes before interpreting timings.
Profiling adds overhead; sampled profiles can instead wrap this command in py-spy.
No assembler, linker, generated image, or persistent build cache is involved.
"""
from __future__ import annotations

import argparse
import cProfile
import faulthandler
import hashlib
import json
from pathlib import Path
import platform
import pstats
import subprocess
import sys
import time


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, required=True, help="output file prefix")
    parser.add_argument("--output-target", default="x86_64-linux", choices=(
        "x86_64-linux", "x86_64-macos", "aarch64-macos",
    ), help="ABI emitted by the generator being compiled (host image stays x86 Linux)")
    parser.add_argument("--profile", action="store_true", help="enable deterministic cProfile")
    args = parser.parse_args()
    root = args.root.resolve()
    sys.path.insert(0, str(root))
    from compiler.native import NATIVE_CODEGEN_TEXT_HEAP_CAPACITY, emit_x86_64_linux
    from compiler.pipeline import compile_source
    from compiler.self_host import native_codegen_source

    metadata = {
        "python": sys.version,
        "platform": platform.platform(),
        "root": str(root),
        "output_target": args.output_target,
        "host_image_target": "x86_64-linux",
        "profile_enabled": args.profile,
        "head": subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip(),
        "tracked_dirty": bool(subprocess.check_output(
            ["git", "-C", str(root), "diff", "HEAD", "--", "compiler", "self_host"], text=True,
        )),
    }
    started = time.perf_counter()
    result = compile_source(native_codegen_source(args.output_target))
    if not result.ok:
        raise RuntimeError(result.diags.render_all())
    metadata["compile_seconds"] = time.perf_counter() - started
    metadata["functions"] = len(result.ir.functions)
    metadata["function_instructions"] = sum(len(f.body) for f in result.ir.functions.values())
    print(json.dumps({"stage": "compiled", **metadata}), flush=True)
    profiler = cProfile.Profile() if args.profile else None
    faulthandler.dump_traceback_later(300, repeat=True)
    started = time.perf_counter()
    try:
        if profiler is not None:
            profiler.enable()
        assembly = emit_x86_64_linux(result.ir, text_heap_capacity=NATIVE_CODEGEN_TEXT_HEAP_CAPACITY)
    finally:
        if profiler is not None:
            profiler.disable()
        faulthandler.cancel_dump_traceback_later()
    metadata["emit_seconds"] = time.perf_counter() - started
    encoded = assembly.encode("utf-8")
    metadata["assembly_bytes"] = len(encoded)
    metadata["assembly_sha256"] = hashlib.sha256(encoded).hexdigest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    Path(f"{args.output}.s").write_bytes(encoded)
    if profiler is not None:
        profiler.dump_stats(f"{args.output}.prof")
        stats = pstats.Stats(profiler)
        metadata["closure_return_analysis_calls"] = sum(
            values[1] for key, values in stats.stats.items()
            if key[2] == "analyze_action_closure_returns"
        )
        stats.sort_stats("cumulative").print_stats(20)
    Path(f"{args.output}.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"stage": "emitted", **metadata}), flush=True)


if __name__ == "__main__":
    main()
