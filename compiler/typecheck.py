"""Type checking (spec section 21), separate from name resolution.

Kuro's base types (unchanged from the bootstrap implementation — see
docs/architecture/current-state.md section 5): Integers, Decimals, Text,
Symbols. `Integers -> Decimals` is the only implicit widening; everything
else must match exactly. Collections are typed by their element type
(untyped/empty collections are simply not checked further, same as before).

This pass assumes `resolver.resolve()` already ran on the same
DiagnosticEngine and reports type errors as E30xx diagnostics.

Stage 7 (ADR-0013) added six checks beyond the original three
(Assign/AddStmt/SetStmt): comparison operand compatibility (E3006), call
argument types against typed parameters (E3007), Repeat's count (E3008),
Length's target (E3009), Get/Set's index (E3010), and closing a real gap
where `_infer` didn't know Text + Text (string concatenation) was valid,
while also reporting genuinely incompatible arithmetic operands instead of
silently treating them as "unknown" (E3011). ADR-0013 documents exactly
what was — and was deliberately not — added, and why.
"""
from __future__ import annotations

from .ast_nodes import (
    AddStmt, Assign, BinaryExpr, BoolAnd, BoolOr, CallStmt, Comparison,
    CompareStmt, Condition, Expr, GetStmt, IfStmt, IsClass, LengthStmt,
    Literal, Program, RepeatStmt, SetStmt, Stmt, VarRef, WhileStmt,
)
from .diagnostics import DiagnosticEngine
from .resolver import SymbolTable

BASE_TYPES = {"Integers", "Decimals", "Text", "Symbols"}
_NUMERIC = {"Integers", "Decimals"}


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
            # _infer always runs, regardless of whether the target has a
            # declared type: it's also what surfaces E3011 (invalid
            # arithmetic) for a value's own internal consistency. The
            # E3001 compatibility check is the part that's conditional on
            # `declared` being known.
            for v in st.values:
                t = self._infer(v)
                if declared is not None and t is not None and not compatible(declared, t):
                    self.diags.error(
                        "E3001",
                        f"cannot assign {t} to {declared} variable {st.name!r}",
                        v.span,
                        notes=(f"found: {t}", f"expected: {declared}"),
                    )
        elif isinstance(st, AddStmt):
            declared = self.symbols.types.get(st.target)
            if declared is not None and declared not in _NUMERIC:
                self.diags.error("E3002", "Add target must be numeric", st.span, notes=(f"found: {declared}",))
        elif isinstance(st, SetStmt):
            declared = self.symbols.types.get(st.target)
            if declared == "Text":
                vt = self._infer(st.value)
                if vt is not None and vt != "Text":
                    self.diags.error("E3004", "Set on Text requires a single character", st.span)
            self._check_index(st.index)
        elif isinstance(st, GetStmt):
            if st.index is not None:
                self._check_index(st.index)
        elif isinstance(st, LengthStmt):
            declared = self.symbols.types.get(st.target)
            if declared is not None and declared != "Text":
                self.diags.error(
                    "E3009",
                    f"Length target must be Text, found {declared}",
                    st.span,
                    notes=(f"found: {declared}",),
                )
        elif isinstance(st, RepeatStmt):
            ct = self._infer(st.count)
            if ct is not None and ct != "Integers":
                self.diags.error(
                    "E3008",
                    f"Repeat count must be Integers, found {ct}",
                    st.count.span,
                    notes=(f"found: {ct}",),
                )
        elif isinstance(st, CompareStmt):
            self._check_condition(st.condition)
        elif isinstance(st, IfStmt):
            self._check_condition(st.condition)
        elif isinstance(st, WhileStmt):
            self._check_condition(st.condition)
        elif isinstance(st, CallStmt):
            sig = self.symbols.actions.get(st.name)
            if sig is not None:
                for arg, param in zip(st.args, sig.decl.params):
                    if param.typ is None:
                        continue
                    at = self._infer(arg)
                    if at is not None and not compatible(param.typ, at):
                        self.diags.error(
                            "E3007",
                            f"cannot pass {at} as {param.typ} argument {param.name!r} to action {st.name!r}",
                            arg.span,
                            notes=(f"found: {at}", f"expected: {param.typ}"),
                        )
        # nested bodies (If/Repeat/While/Action) are walked generically below
        for child in _child_blocks(st):
            self._check_block(child)

    def _check_index(self, index_expr: Expr):
        it = self._infer(index_expr)
        if it is not None and it != "Integers":
            self.diags.error(
                "E3010",
                f"index must be Integers, found {it}",
                index_expr.span,
                notes=(f"found: {it}",),
            )

    def _check_condition(self, c: Condition):
        if isinstance(c, Comparison):
            lt = self._infer(c.left)
            rt = self._infer(c.right)
            if lt is not None and rt is not None and c.op in ("gt", "lt", "ge", "le"):
                both_numeric = lt in _NUMERIC and rt in _NUMERIC
                both_text = lt == "Text" and rt == "Text"
                if not (both_numeric or both_text):
                    self.diags.error(
                        "E3006",
                        f"cannot compare {lt} and {rt} with {c.op!r}",
                        c.span,
                        notes=(f"left: {lt}", f"right: {rt}"),
                    )
            return
        if isinstance(c, (BoolAnd, BoolOr)):
            self._check_condition(c.left)
            self._check_condition(c.right)
            return
        if isinstance(c, IsClass):
            # No check by design (ADR-0013): a non-Text operand already
            # degrades gracefully at runtime (Interpreter._isclass returns
            # false rather than erroring) — rejecting it here would
            # restrict a currently-valid program for no benefit.
            return

    def _infer(self, e: Expr) -> str | None:
        if isinstance(e, Literal):
            return type_of_literal(e.value)
        if isinstance(e, VarRef):
            return self.symbols.types.get(e.name)
        if isinstance(e, BinaryExpr):
            lt, rt = self._infer(e.left), self._infer(e.right)
            if lt is None or rt is None:
                return None
            if e.op == "+" and lt == "Text" and rt == "Text":
                return "Text"
            if lt in _NUMERIC and rt in _NUMERIC:
                return "Decimals" if (lt == "Decimals" or rt == "Decimals") else "Integers"
            self.diags.error(
                "E3011",
                f"invalid operand types for {e.op!r}: {lt} and {rt}",
                e.span,
                notes=(f"left: {lt}", f"right: {rt}"),
            )
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
