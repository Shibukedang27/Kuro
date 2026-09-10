"""Canonical semantic result for Stage 7 differential testing.

Mirrors `compiler/ast_canon.py`'s role for Stage 6: a deterministic,
implementation-independent summary of what `resolve()` + `typecheck()`
produced, so it can be compared against the self-hosted resolver +
typechecker's own output without comparing Python object identity or
internal pass structure.

Deliberately order-independent (both the symbol list and the diagnostic
list are sorted before comparison) because ADR-0014 combines what Python
does as two separate passes (resolve, then typecheck) into one combined
self-hosted pass — the two implementations can legitimately visit/report
things in a different order while agreeing on every individual result.
Per ADR-0011's diagnostic compatibility policy (carried forward here):
code and source location are compared; message text is not.
"""
from __future__ import annotations

from .diagnostics import DiagnosticEngine
from .resolver import SymbolTable


def canon_semantic(symbols: SymbolTable, diags: DiagnosticEngine) -> dict:
    return {
        "symbols": sorted(symbols.types.items()),
        "actions": sorted((name, sig.arity) for name, sig in symbols.actions.items()),
        "diagnostics": sorted(
            (d.code, d.span.line, d.span.col) for d in diags.diagnostics
        ),
    }
