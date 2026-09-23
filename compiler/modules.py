"""Kuro's bootstrap module loader.

Modules are source units joined before semantic compilation. The syntax is
deliberately narrow and deterministic for the first implementation:
`Import "relative/path.kuro";`. Resolution is relative to the importing file,
and cycles/missing files are diagnosed instead of delegated to the host.
"""
from __future__ import annotations

import re
from pathlib import Path

from .diagnostics import DiagnosticEngine, Span

_IMPORT = re.compile(r'^\s*Import\s+"([^"\n]+)"\s*;\s*(?:#.*)?$', re.MULTILINE)


def load_modules(source: str, filename: str, diags: DiagnosticEngine) -> str:
    if filename.startswith("<"):
        return source
    root = Path(filename).resolve()
    project_root = root.parent
    visiting: list[Path] = []
    loaded: set[Path] = set()

    def visit(text: str, path: Path) -> str:
        if path in visiting:
            chain = " -> ".join(str(p) for p in (*visiting, path))
            diags.error("E5002", f"module import cycle: {chain}", Span(1, 1))
            return ""
        if path in loaded:
            return ""
        visiting.append(path)
        chunks: list[str] = []
        cursor = 0
        for match in _IMPORT.finditer(text):
            chunks.append(text[cursor:match.start()])
            child = (path.parent / match.group(1)).resolve()
            try:
                child.relative_to(project_root)
                inside_project = True
            except ValueError:
                inside_project = False
            if not inside_project:
                line = text.count("\n", 0, match.start()) + 1
                diags.error("E5003", f"module import escapes project root: {match.group(1)}", Span(line, 1))
            elif not child.is_file():
                line = text.count("\n", 0, match.start()) + 1
                diags.error("E5001", f"module not found: {match.group(1)}", Span(line, 1))
            else:
                chunks.append(visit(child.read_text(encoding="utf-8"), child))
            cursor = match.end()
        chunks.append(text[cursor:])
        visiting.pop()
        loaded.add(path)
        return "\n".join(chunks)

    return visit(source, root)
