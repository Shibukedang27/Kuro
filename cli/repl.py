"""Interactive Kuro session built on the compiler/runtime pipeline."""
from __future__ import annotations

import sys

from compiler.pipeline import run_source


def repl_main(input_fn=input, output=None) -> int:
    output = output or sys.stdout
    source_lines: list[str] = []
    emitted = ""
    while True:
        try:
            line = input_fn("kuro> ")
        except (EOFError, KeyboardInterrupt):
            output.write("\n")
            return 0
        command = line.strip()
        if command in (".exit", ".quit"):
            return 0
        if command == ".clear":
            source_lines.clear()
            emitted = ""
            continue
        if command == ".check":
            result = run_source("\n".join(source_lines)) if source_lines else None
            output.write("ok\n" if result is None or result.compile.ok else result.compile.diags.render_all() + "\n")
            continue
        if not line.strip():
            continue
        source_lines.append(line)
        result = run_source("\n".join(source_lines), filename="<repl>")
        if not result.compile.ok:
            output.write(result.compile.diags.render_all() + "\n")
            source_lines.pop()
            continue
        current = result.stdout or ""
        output.write(current[len(emitted):] if current.startswith(emitted) else current)
        emitted = current
