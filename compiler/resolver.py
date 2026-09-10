"""Name resolution (spec section 20).

Kept separate from type checking (section 21) and from the parser: this pass
only answers "is this name defined here, and is it used consistently
(no duplicate declarations, no calls to unknown actions, no Return outside
an Action)". It builds the symbol tables that typecheck.py and lower.py
both read afterwards, so a caller runs resolve() once and reuses its result.

Scoping model: a flat global scope (matches the bootstrap engine's
single `env`/`types` dict — see docs/architecture/current-state.md section 6)
plus one extra binding layer per Action call, holding that Action's
parameters and, inside a Repeat body, the loop variable `Index`. This is a
conscious, documented choice to keep runtime scoping behavior identical to
the bootstrap implementation (Action bodies can still read/write globals)
while giving name resolution a real, reusable Scope object instead of
threading raw sets through every recursive call by hand.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .ast_nodes import (
    ActionDecl, AddStmt, Assign, BinaryExpr, BoolAnd, BoolOr, CallStmt,
    Comparison, CompareStmt, Condition, Decl, Expr, GetStmt, IfStmt, Input,
    IsClass, Literal, LengthStmt, AppendStmt, PrintStmt, Program, RepeatStmt,
    ReturnStmt, SetStmt, Stmt, UpdateStmt, VarRef,
)
from .diagnostics import DiagnosticEngine


@dataclass
class Scope:
    names: set[str] = field(default_factory=set)
    parent: "Scope | None" = None

    def defined(self, name: str) -> bool:
        return name in self.names or (self.parent is not None and self.parent.defined(name))

    def define(self, name: str) -> None:
        self.names.add(name)

    def child(self) -> "Scope":
        return Scope(set(), self)


@dataclass
class ActionSig:
    decl: ActionDecl

    @property
    def name(self) -> str:
        return self.decl.name

    @property
    def arity(self) -> int:
        return len(self.decl.params)


class SymbolTable:
    """Result of resolution: what typecheck.py / lower.py consume."""

    def __init__(self):
        self.types: dict[str, str] = {}       # inferred/declared type per global name
        self.actions: dict[str, ActionSig] = {}


class Resolver:
    def __init__(self, program: Program, diags: DiagnosticEngine):
        self.program = program
        self.diags = diags
        self.symbols = SymbolTable()

    def run(self) -> SymbolTable:
        self._collect_globals()
        root = Scope()
        for name in self.symbols.types:
            root.define(name)
        self._resolve_block(self.program.statements, root, in_action=False)
        return self.symbols

    # --- pass 1: top-level declarations & action signatures ---------
    def _collect_globals(self):
        for st in self.program.statements:
            if isinstance(st, Decl):
                from .typecheck import BASE_TYPES  # local import: avoid cycle

                if st.typ not in BASE_TYPES:
                    self.diags.error("E3003", f"unknown type {st.typ!r}", st.span)
                    continue
                if st.name in self.symbols.types:
                    self.diags.error("E4002", f"duplicate declaration {st.name!r}", st.span)
                    continue
                self.symbols.types[st.name] = st.typ
            elif isinstance(st, Assign) and st.name not in self.symbols.types:
                if st.typ is not None:
                    self.symbols.types[st.name] = st.typ
                else:
                    inferred = self._infer_literal_list_type(st.values)
                    if inferred:
                        self.symbols.types[st.name] = inferred
            elif isinstance(st, ActionDecl):
                if st.name in self.symbols.actions:
                    self.diags.error("E4002", f"duplicate action {st.name!r}", st.span)
                    continue
                seen = set()
                for p in st.params:
                    if p.name in seen:
                        self.diags.error("E2005", f"duplicate action parameter {p.name!r}", p.span)
                    seen.add(p.name)
                self.symbols.actions[st.name] = ActionSig(st)

    @staticmethod
    def _infer_literal_list_type(values: list[Expr]) -> str | None:
        from .typecheck import type_of_literal

        kinds = []
        for v in values:
            if isinstance(v, Literal):
                kinds.append(type_of_literal(v.value))
            else:
                return None
        if kinds and all(k == kinds[0] for k in kinds):
            return kinds[0]
        return None

    # --- pass 2: usage checking --------------------------------------
    def _resolve_block(self, body: list[Stmt], scope: Scope, in_action: bool):
        for st in body:
            self._resolve_stmt(st, scope, in_action)

    def _resolve_stmt(self, st: Stmt, scope: Scope, in_action: bool):
        if isinstance(st, Decl):
            return
        if isinstance(st, Assign):
            scope.define(st.name)
            for v in st.values:
                self._resolve_expr(v, scope)
            return
        if isinstance(st, Input):
            for n in st.names:
                if not scope.defined(n):
                    self.diags.error("E4001", f"input variable {n!r} must be declared first", st.span)
            return
        if isinstance(st, AddStmt):
            if not scope.defined(st.target):
                self.diags.error("E4001", f"undefined variable {st.target!r}", st.span)
            self._resolve_expr(st.value, scope)
            return
        if isinstance(st, UpdateStmt):
            if not scope.defined(st.name):
                self.diags.error("E4001", f"undefined variable {st.name!r}", st.span)
            self._resolve_expr(st.value, scope)
            return
        if isinstance(st, AppendStmt):
            if not scope.defined(st.target):
                self.diags.error("E4001", f"undefined variable {st.target!r}", st.span)
            self._resolve_expr(st.value, scope)
            return
        if isinstance(st, PrintStmt):
            self._resolve_expr(st.value, scope)
            return
        if isinstance(st, GetStmt):
            if not scope.defined(st.target):
                self.diags.error("E4001", f"undefined target {st.target!r}", st.span)
            if st.index is not None:
                self._resolve_expr(st.index, scope)
            return
        if isinstance(st, LengthStmt):
            if not scope.defined(st.target):
                self.diags.error("E4001", f"undefined target {st.target!r}", st.span)
            return
        if isinstance(st, SetStmt):
            if not scope.defined(st.target):
                self.diags.error("E4001", f"undefined target {st.target!r}", st.span)
            self._resolve_expr(st.index, scope)
            self._resolve_expr(st.value, scope)
            return
        if isinstance(st, CompareStmt):
            self._resolve_condition(st.condition, scope)
            scope.define(st.name)
            self.symbols.types.setdefault(st.name, "Symbols")
            return
        if isinstance(st, IfStmt):
            self._resolve_condition(st.condition, scope)
            self._resolve_block(st.then_body, scope, in_action)
            self._resolve_block(st.else_body, scope, in_action)
            return
        if isinstance(st, RepeatStmt):
            self._resolve_expr(st.count, scope)
            # Only `Index` is scoped to this Repeat (mirroring the
            # interpreter's SAVEVAR/RESTOREVAR around Index — see
            # lower.py::_lower_repeat). Every other name assigned inside
            # the body must land in the SAME (enclosing) scope, not a
            # child, because the interpreter's storage is flat: `X = 1;`
            # inside a Repeat really does define X for code after the loop
            # too (matches the bootstrap engine — see
            # docs/architecture/current-state.md section 7). An earlier
            # version of this pass used a child scope for the whole body,
            # which made that a false "undefined variable" at resolve time
            # even though it would run fine — caught while writing the
            # Stage 5 self-hosted lexer, which relies on exactly this
            # pattern (scan buffers assigned inside nested Repeats).
            had_index = "Index" in scope.names
            scope.define("Index")
            self._resolve_block(st.body, scope, in_action)
            if not had_index:
                scope.names.discard("Index")
            return
        if isinstance(st, ActionDecl):
            inner = scope.child()
            for p in st.params:
                inner.define(p.name)
            self._resolve_block(st.body, inner, True)
            return
        if isinstance(st, ReturnStmt):
            if not in_action:
                self.diags.error("E4005", "Return is only valid inside an Action", st.span)
            self._resolve_expr(st.value, scope)
            return
        if isinstance(st, CallStmt):
            sig = self.symbols.actions.get(st.name)
            if sig is None:
                self.diags.error("E4003", f"unknown action {st.name!r}", st.span)
            elif len(st.args) != sig.arity:
                self.diags.error(
                    "E4004",
                    f"action {st.name!r} expects {sig.arity} argument(s), got {len(st.args)}",
                    st.span,
                )
            for a in st.args:
                self._resolve_expr(a, scope)
            return
        raise AssertionError(f"unhandled statement node {st!r}")

    def _resolve_expr(self, e: Expr, scope: Scope):
        if isinstance(e, Literal):
            return
        if isinstance(e, VarRef):
            if e.name == "_":
                return
            if not scope.defined(e.name):
                self.diags.error("E4001", f"undefined value {e.name!r}", e.span)
            return
        if isinstance(e, BinaryExpr):
            self._resolve_expr(e.left, scope)
            self._resolve_expr(e.right, scope)
            return
        raise AssertionError(f"unhandled expr node {e!r}")

    def _resolve_condition(self, c: Condition, scope: Scope):
        if isinstance(c, Comparison):
            self._resolve_expr(c.left, scope)
            self._resolve_expr(c.right, scope)
            return
        if isinstance(c, (BoolAnd, BoolOr)):
            self._resolve_condition(c.left, scope)
            self._resolve_condition(c.right, scope)
            return
        if isinstance(c, IsClass):
            self._resolve_expr(c.operand, scope)
            return
        raise AssertionError(f"unhandled condition node {c!r}")


def resolve(program: Program, diags: DiagnosticEngine) -> SymbolTable:
    return Resolver(program, diags).run()
