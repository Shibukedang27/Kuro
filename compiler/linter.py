"""Static lint checks for Kuro source."""
from __future__ import annotations

from dataclasses import fields, is_dataclass

from .diagnostics import DiagnosticEngine, Span
from .pipeline import compile_source


def lint_source(source: str, filename: str = "<source>") -> DiagnosticEngine:
    result = compile_source(source, filename)
    diags = result.diags
    if not result.ok or result.program is None:
        return diags

    declared: dict[str, Span] = {}
    used: set[str] = set()

    def walk(node, read_context: bool = False):
        if node is None or isinstance(node, (str, int, float, bool)):
            return
        if isinstance(node, list):
            for item in node:
                walk(item, read_context)
            return
        if not is_dataclass(node):
            return
        name = getattr(node, "name", None)
        if node.__class__.__name__ == "Decl" and name:
            declared[name] = node.span
        elif node.__class__.__name__ == "VarRef" and name:
            used.add(name)
        for field in fields(node):
            if field.name != "span":
                walk(getattr(node, field.name), read_context)

    walk(result.program)
    for name, span in sorted(declared.items()):
        if name not in used:
            diags.warning("W7001", f"declared variable {name!r} is never read", span)
    for number, line in enumerate(source.splitlines(), 1):
        if "\t" in line:
            diags.warning("W7002", "tab indentation; use four spaces", Span(number, line.index("\t") + 1))
        if line.rstrip() != line:
            diags.warning("W7003", "trailing whitespace", Span(number, len(line.rstrip()) + 1))
    return diags
