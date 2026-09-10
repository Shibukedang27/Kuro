"""AST -> Kuro IR lowering (spec section 22).

Every expression is flattened into a chain of instructions producing one
named temporary; every statement becomes zero or more instructions,
operating on named variables (STORE/LOADVAR) rather than the AST directly.
Control flow (`If`, `Repeat`) becomes explicit LABEL/JUMP/JUMPF.

`Repeat`'s loop variable `Index` is saved with SAVEVAR before the loop and
restored with RESTOREVAR after, matching the bootstrap engine's behavior of
not leaking `Index` into surrounding code (see resolver.py's scoping note
and docs/architecture/current-state.md section 6) — but implemented as real
IR instructions instead of ad hoc Python dict save/restore, so a native
backend can implement the same save/restore contract.

`While` (ADR-0009) has no loop variable, so it needs no save/restore — just
a loop-start/loop-end label pair around a JUMPF, like `If`, plus one
LOOP_GUARD instruction so an unbounded condition can't hang the runtime
forever (see compiler/interpreter.py).
"""
from __future__ import annotations

from .ast_nodes import (
    ActionDecl, AddStmt, Assign, BinaryExpr, BoolAnd, BoolOr, CallStmt,
    Comparison, CompareStmt, Condition, Decl, Expr, GetStmt, IfStmt, Input,
    IsClass, Literal, LengthStmt, AppendStmt, PrintStmt, Program, RepeatStmt,
    ReturnStmt, SetStmt, Stmt, UpdateStmt, VarRef, WhileStmt,
)
from .ir import IRBuilder, IRFunction, IRProgram
from .resolver import SymbolTable


class Lowering:
    def __init__(self, program: Program, symbols: SymbolTable):
        self.program = program
        self.symbols = symbols
        self.ir = IRProgram()
        self._repeat_depth = 0

    def run(self) -> IRProgram:
        b = IRBuilder()
        top = [st for st in self.program.statements if not isinstance(st, ActionDecl)]
        for st in self.program.statements:
            if isinstance(st, ActionDecl):
                self._lower_action(st)
        self._lower_block(top, b)
        self.ir.main = b.instrs
        return self.ir

    def _lower_action(self, decl: ActionDecl):
        b = IRBuilder()
        fn = IRFunction(decl.name, [p.name for p in decl.params])
        self._lower_block(decl.body, b)
        fn.body = b.instrs
        self.ir.functions[decl.name] = fn

    def _lower_block(self, body: list[Stmt], b: IRBuilder):
        for st in body:
            self._lower_stmt(st, b)

    # --- expressions -----------------------------------------------
    def _lower_expr(self, e: Expr, b: IRBuilder) -> str:
        if isinstance(e, Literal):
            return b.emit_value("CONST", e.value, span=e.span)
        if isinstance(e, VarRef):
            return b.emit_value("LOADVAR", e.name, span=e.span)
        if isinstance(e, BinaryExpr):
            lt = self._lower_expr(e.left, b)
            rt = self._lower_expr(e.right, b)
            return b.emit_value("BINOP", e.op, lt, rt, span=e.span)
        raise AssertionError(f"unhandled expr {e!r}")

    def _lower_condition(self, c: Condition, b: IRBuilder) -> str:
        if isinstance(c, Comparison):
            lt = self._lower_expr(c.left, b)
            rt = self._lower_expr(c.right, b)
            return b.emit_value("CMP", c.op, lt, rt, span=c.span)
        if isinstance(c, BoolAnd):
            lt = self._lower_condition(c.left, b)
            rt = self._lower_condition(c.right, b)
            return b.emit_value("AND", lt, rt, span=c.span)
        if isinstance(c, BoolOr):
            lt = self._lower_condition(c.left, b)
            rt = self._lower_condition(c.right, b)
            return b.emit_value("OR", lt, rt, span=c.span)
        if isinstance(c, IsClass):
            operand = self._lower_expr(c.operand, b)
            return b.emit_value("ISCLASS", operand, c.cls, span=c.span)
        raise AssertionError(f"unhandled condition {c!r}")

    # --- statements --------------------------------------------------
    def _lower_stmt(self, st: Stmt, b: IRBuilder):
        if isinstance(st, Decl):
            b.emit("DECLTYPE", st.name, st.typ, span=st.span)
            return
        if isinstance(st, Assign):
            temps = tuple(self._lower_expr(v, b) for v in st.values)
            b.emit("STORE_LIST", st.name, temps, span=st.span)
            return
        if isinstance(st, Input):
            for n in st.names:
                b.emit("INPUT", n, self.symbols.types.get(n, "Text"), span=st.span)
            return
        if isinstance(st, AddStmt):
            v = self._lower_expr(st.value, b)
            b.emit("ADD", st.target, v, span=st.span)
            return
        if isinstance(st, UpdateStmt):
            v = self._lower_expr(st.value, b)
            b.emit("UPDATE", st.name, v, span=st.span)
            return
        if isinstance(st, AppendStmt):
            v = self._lower_expr(st.value, b)
            b.emit("APPEND", st.target, v, span=st.span)
            return
        if isinstance(st, PrintStmt):
            v = self._lower_expr(st.value, b)
            b.emit("PRINT", v, span=st.span)
            return
        if isinstance(st, GetStmt):
            idx = self._lower_expr(st.index, b) if st.index is not None else None
            dest = b.emit_value("GET", st.target, idx, span=st.span)
            b.emit("STORE_LIST", "_", (dest,), span=st.span)
            return
        if isinstance(st, LengthStmt):
            dest = b.emit_value("LENGTH", st.target, span=st.span)
            b.emit("STORE_LIST", "_", (dest,), span=st.span)
            return
        if isinstance(st, SetStmt):
            idx = self._lower_expr(st.index, b)
            val = self._lower_expr(st.value, b)
            b.emit("SET", st.target, idx, val, span=st.span)
            return
        if isinstance(st, CompareStmt):
            cond = self._lower_condition(st.condition, b)
            b.emit("STORE_LIST", st.name, (cond,), span=st.span)
            return
        if isinstance(st, IfStmt):
            cond = self._lower_condition(st.condition, b)
            else_label = b.fresh_label("else")
            end_label = b.fresh_label("endif")
            b.emit("JUMPF", else_label, cond, span=st.span)
            self._lower_block(st.then_body, b)
            b.emit("JUMP", end_label, span=st.span)
            b.label(else_label)
            self._lower_block(st.else_body, b)
            b.label(end_label)
            return
        if isinstance(st, RepeatStmt):
            self._lower_repeat(st, b)
            return
        if isinstance(st, WhileStmt):
            self._lower_while(st, b)
            return
        if isinstance(st, ReturnStmt):
            v = self._lower_expr(st.value, b)
            b.emit("RETURN", v, span=st.span)
            return
        if isinstance(st, CallStmt):
            args = tuple(self._lower_expr(a, b) for a in st.args)
            dest = b.emit_value("CALL", st.name, *args, span=st.span)
            b.emit("STORE_LIST", "_", (dest,), span=st.span)
            return
        raise AssertionError(f"unhandled statement {st!r}")

    def _lower_repeat(self, st: RepeatStmt, b: IRBuilder):
        self._repeat_depth += 1
        counter = f"__repeat_i{self._repeat_depth}"
        try:
            count = self._lower_expr(st.count, b)
            b.emit("CHECK_NONNEG", count, span=st.span)
            saved_index = b.emit_value("SAVEVAR", "Index", span=st.span)
            zero = b.emit_value("CONST", 0, span=st.span)
            b.emit("STORE_LIST", counter, (zero,), span=st.span)
            start = b.fresh_label("repeat_start")
            end = b.fresh_label("repeat_end")
            b.label(start)
            i = b.emit_value("LOADVAR", counter, span=st.span)
            cond = b.emit_value("CMP", "lt", i, count, span=st.span)
            b.emit("JUMPF", end, cond, span=st.span)
            b.emit("STORE_LIST", "Index", (i,), span=st.span)
            self._lower_block(st.body, b)
            i2 = b.emit_value("LOADVAR", counter, span=st.span)
            one = b.emit_value("CONST", 1, span=st.span)
            inc = b.emit_value("BINOP", "+", i2, one, span=st.span)
            b.emit("STORE_LIST", counter, (inc,), span=st.span)
            b.emit("JUMP", start, span=st.span)
            b.label(end)
            b.emit("RESTOREVAR", "Index", saved_index, span=st.span)
        finally:
            self._repeat_depth -= 1

    def _lower_while(self, st: WhileStmt, b: IRBuilder):
        # ADR-0009: unlike Repeat, While has no loop variable to save/
        # restore — only the LOOP_GUARD safety counter (see
        # compiler/interpreter.py) is loop-specific, keyed by a unique
        # label so nested/sibling While loops never share a counter.
        start = b.fresh_label("while_start")
        end = b.fresh_label("while_end")
        guard_id = b.fresh_label("while_guard")
        b.label(start)
        b.emit("LOOP_GUARD", guard_id, span=st.span)
        cond = self._lower_condition(st.condition, b)
        b.emit("JUMPF", end, cond, span=st.span)
        self._lower_block(st.body, b)
        b.emit("JUMP", start, span=st.span)
        b.label(end)


def lower(program: Program, symbols: SymbolTable) -> IRProgram:
    return Lowering(program, symbols).run()
