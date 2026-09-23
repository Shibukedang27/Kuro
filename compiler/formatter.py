"""Deterministic formatter for Kuro's line-oriented source syntax."""
from __future__ import annotations

import re

_OPEN = re.compile(r"^(If|Repeat|While|Action)\b")
_MID = re.compile(r"^(Else)\s*;")
_END = re.compile(r"^Done\s*\.")


def _clean_line(line: str) -> str:
    text = line.strip()
    if not text:
        return ""
    if text.startswith("#"):
        return text
    # Normalize only outside quoted strings.
    out: list[str] = []
    quoted = False
    escaped = False
    pending_space = False
    for char in text:
        if escaped:
            out.append(char)
            escaped = False
            continue
        if char == "\\" and quoted:
            out.append(char)
            escaped = True
            continue
        if char == '"':
            if pending_space and out:
                out.append(" ")
            pending_space = False
            quoted = not quoted
            out.append(char)
            continue
        if char.isspace() and not quoted:
            pending_space = True
            continue
        if pending_space and out and not quoted and char not in ";.,":
            out.append(" ")
        pending_space = False
        out.append(char)
    return "".join(out).replace(" ;", ";").replace(" .", ".")


def format_source(source: str) -> str:
    depth = 0
    lines: list[str] = []
    for raw in source.splitlines():
        clean = _clean_line(raw)
        if not clean:
            if lines and lines[-1] != "":
                lines.append("")
            continue
        if _END.match(clean) or _MID.match(clean):
            depth = max(0, depth - 1)
        lines.append("    " * depth + clean)
        if _OPEN.match(clean) or _MID.match(clean):
            depth += 1
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines) + ("\n" if lines else "")
