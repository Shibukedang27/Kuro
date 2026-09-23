"""Trace debugger for Kuro programs."""
from __future__ import annotations

import sys
import json
import io
from pathlib import Path

from compiler.pipeline import compile_source
from compiler.interpreter import Interpreter, KuroRuntimeException


class DebugStop(Exception):
    """Normal debugger stop (breakpoint or step budget), not a program error."""


def debug_main(path: str, output=None, breakpoints: set[int] | None = None, max_steps: int | None = None, json_output: bool = False, watches: set[str] | None = None) -> int:
    output = output or sys.stdout
    result = compile_source(Path(path).read_text(encoding="utf-8"), filename=path)
    if not result.ok:
        print(result.diags.render_all(), file=sys.stderr)
        return 1

    steps = 0
    breakpoints = breakpoints or set()
    watches = watches or set()

    def trace(instr, env, depth, pc):
        nonlocal steps
        steps += 1
        if max_steps is not None and steps > max_steps:
            raise DebugStop(f"step limit reached ({max_steps})")
        if instr.span is not None and instr.span.line in breakpoints:
            raise DebugStop(f"breakpoint reached at {path}:{instr.span.line}:{instr.span.col}")
        if json_output:
            output.write(json.dumps({
                "event": "instruction",
                "path": path,
                "pc": pc,
                "depth": depth,
                "op": instr.op,
                "args": list(instr.args),
                "line": instr.span.line if instr.span is not None else None,
                "column": instr.span.col if instr.span is not None else None,
                "environment": env,
                "watches": {name: env.get(name, "<undefined>") for name in sorted(watches)},
            }, default=repr, sort_keys=True) + "\n")
            return
        values = ", ".join(f"{key}={value!r}" for key, value in sorted(env.items()))
        location = f" @{instr.span.line}:{instr.span.col}" if instr.span is not None else ""
        output.write(f"[{depth}:{pc:04d}{location}] {instr.op} {instr.args}")
        if values:
            output.write(f"  {{{values}}}")
        output.write("\n")

    runtime_output = output if not json_output else io.StringIO()
    try:
        Interpreter(result.ir, output=runtime_output, trace=trace).run()
        if json_output and runtime_output.getvalue():
            output.write(json.dumps({"event": "program-output", "data": runtime_output.getvalue()}) + "\n")
    except DebugStop as stop:
        if json_output:
            output.write(json.dumps({"event": "stop", "reason": str(stop)}, sort_keys=True) + "\n")
        else:
            output.write(f"[debug] {stop}\n")
        return 0
    except KuroRuntimeException as error:
        print(f"error[{error.code}]: {error.message}", file=sys.stderr)
        return 1
    return 0
