"""Execution profiler for Kuro programs."""
from __future__ import annotations

import io
import json
import time
from collections import Counter
from dataclasses import dataclass, field

from .interpreter import Interpreter
from .pipeline import compile_source


@dataclass
class ProfileReport:
    elapsed_seconds: float
    instruction_counts: Counter[str]
    max_call_depth: int
    program_output: str
    runtime_stats: dict[str, object] = field(default_factory=dict)

    def to_dict(self) -> dict[str, object]:
        return {
            "elapsed_seconds": self.elapsed_seconds,
            "instruction_counts": dict(sorted(self.instruction_counts.items())),
            "max_call_depth": self.max_call_depth,
            "program_output": self.program_output,
            "runtime_stats": self.runtime_stats,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True, indent=2) + "\n"


def profile_source(source: str, filename: str = "<source>") -> ProfileReport:
    result = compile_source(source, filename)
    if not result.ok:
        raise ValueError(result.diags.render_all())
    counts: Counter[str] = Counter()
    max_depth = 0

    def trace(instr, _env, depth, _pc):
        nonlocal max_depth
        counts[instr.op] += 1
        max_depth = max(max_depth, depth)

    output = io.StringIO()
    started = time.perf_counter()
    interpreter = Interpreter(result.ir, output=output, trace=trace)
    interpreter.run()
    elapsed = time.perf_counter() - started
    return ProfileReport(elapsed, counts, max_depth, output.getvalue(), interpreter.runtime_stats())
