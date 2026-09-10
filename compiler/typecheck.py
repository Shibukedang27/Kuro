"""Type checking (spec section 21), separate from name resolution.

Kuro's base types (unchanged from the bootstrap implementation — see
docs/architecture/current-state.md section 5): Integers, Decimals, Text,
Symbols. `Integers -> Decimals` is the only implicit widening; everything
else must match exactly. Collections are typed by their element type
(untyped/empty collections are simply not checked further, same as before).

This pass assumes `resolver.resolve()` already ran on the same
DiagnosticEngine and reports type errors as E30xx diagnostics.
"""
from __future__ import annotations

from .ast_nodes import (
    AddStmt, Assign, BinaryExpr, Comparison, Condition, Expr, IsClass,
    Literal, Program, SetStmt, Stmt, UpdateStmt, VarRef,
)
from .diagnostics import DiagnosticEngine
from .resolver import SymbolTable

BASE_TYPES = {"Integers", "Decimals", "Text", "Symbols"}


def type_of_literal(value: object) -> str:
    if isinstance(value, bool):
        return "Symbols"
    if isinstance(value, int):
        return "Integers"
    if isinstance(value, float):
        return "Decimals"
    if isinstance(value, str):
        return "Text"
    raise TypeError(f"no Kuro type for literal {value!r}")


def compatible(declared: str, actual: str) -> bool:
    return declared == actual or (declared == "Decimals" and actual == "Integers")


class TypeChecker:
    def __init__(self, program: Program, symbols: SymbolTable, diags: DiagnosticEngine):
        self.program = program
        self.symbols = symbols
        self.diags = diags

    def run(self):
        self._check_block(self.program.statements)

    def _check_block(self, body: list[Stmt]):
        for st in body:
            self._check_stmt(st)

    def _check_stmt(self, st: Stmt):
        if isinstance(st, Assign):
            declared = self.symbols.types.get(st.name)
            if declared is not None:
                for v in st.values:
                    t = self._infer(v)
                    if t is not None and not compatible(declared, t):
                        self.diags.error(
                            "E3001",
                            f"cannot assign {t} to {declared} variable {st.name!r}",
                            v.span,
                            notes=(f"found: {t}", f"expected: {declared}"),
                        )
        elif isinstance(st, AddStmt):
            declared = self.symbols.types.get(st.target)
            if declared is not None and declared not in ("Integers", "Decimals"):
                self.diags.error("E3002", "Add target must be numeric", st.span, notes=(f"found: {declared}",))
        elif isinstance(st, SetStmt):
            declared = self.symbols.types.get(st.target)
            if declared == "Text":
                vt = self._infer(st.value)
                if vt is not None and vt != "Text":
                    self.diags.error("E3004", "Set on Text requires a single character", st.span)
        # nested bodies (If/Repeat/Action) are walked generically below
        for child in _child_blocks(st):
            self._check_block(child)

    def _infer(self, e: Expr) -> str | None:
        if isinstance(e, Literal):
            return type_of_literal(e.value)
        if isinstance(e, VarRef):
            return self.symbols.types.get(e.name)
        if isinstance(e, BinaryExpr):
            lt, rt = self._infer(e.left), self._infer(e.right)
            if lt is None or rt is None:
                return None
            if lt == "Decimals" or rt == "Decimals":
                return "Decimals" if lt in ("Integers", "Decimals") and rt in ("Integers", "Decimals") else None
            if lt == "Integers" and rt == "Integers":
                return "Integers"
            return None
        return None


def _child_blocks(st: Stmt) -> list[list[Stmt]]:
    out = []
    for attr in ("then_body", "else_body", "body"):
        v = getattr(st, attr, None)
        if isinstance(v, list):
            out.append(v)
    return out


def typecheck(program: Program, symbols: SymbolTable, diags: DiagnosticEngine):
    TypeChecker(program, symbols, diags).run()
