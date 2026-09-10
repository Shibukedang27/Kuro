"""Canonical AST serialization for Stage 6 differential testing.

Neither side of the differential test (the Python parser's real AST object
graph vs. the self-hosted Kuro parser, which has no structs/records to build
a tree out of — see docs/engineering/ADR-0010-stage6-parser.md) can be
compared directly. Both instead produce a flat, ordered list of strings
using the *same* prefix (node-tag-first) encoding defined here, and the
test just compares those two lists for equality — exactly the technique
`tests/self_host/test_lexer_cross.py` already used for tokens, extended
from a flat token stream to a flat *tree* stream.

Encoding rules (fixed across both implementations — the Kuro parser,
self_host/parser.kuro, must match this exactly):
  - Every node contributes its own tag word first (e.g. "LIT_INT").
  - A node with a *fixed* number of children just lists them in order,
    each child itself starting with its own tag (this is what makes the
    stream self-delimiting for fixed-arity nodes — no count needed).
  - A node with a *variable*-length list of children (a block's statement
    list, a call's argument list, an action's parameter list, a
    multi-value assignment's right-hand side) is prefixed with an explicit
    integer count, as its own token, before that many children.
  - `Assign.typ` and `Param.typ`, which are optional, are encoded as the
    literal token "NONE" when absent — safe because "NONE" can never be a
    real Kuro type name (the four base types are Integers/Decimals/Text/
    Symbols).
See docs/engineering/ADR-0010-stage6-parser.md for the full grammar table.
"""
from __future__ import annotations

from .ast_nodes import (
    ActionDecl, AddStmt, Assign, BinaryExpr, BoolAnd, BoolOr, CallStmt,
    Comparison, CompareStmt, Condition, Decl, Expr, GetStmt, IfStmt, Input,
    IsClass, Literal, LengthStmt, AppendStmt, Program, RepeatStmt,
    ReturnStmt, SetStmt, Stmt, UpdateStmt, VarRef, WhileStmt, PrintStmt,
)


def _lit_text(value) -> str:
    # Literal.value is a real Python int/float/str; the canonical form is
    # always its *text spelling*, matching how the Kuro parser has no
    # choice but to carry token text around (it has no int()/float()
    # conversion either — ADR-0004's consequences).
    return str(value)


def canon_expr(e: Expr, out: list[str]) -> None:
    if isinstance(e, Literal):
        if isinstance(e.value, str):
            out.append("LIT_STR")
        elif isinstance(e.value, float):
            out.append("LIT_DEC")
        else:
            out.append("LIT_INT")
        out.append(_lit_text(e.value))
        return
    if isinstance(e, VarRef):
        out.append("VAR")
        out.append("1" if e.explicit_at else "0")
        out.append(e.name)
        return
    if isinstance(e, BinaryExpr):
        out.append("BIN")
        out.append(e.op)
        canon_expr(e.left, out)
        canon_expr(e.right, out)
        return
    raise AssertionError(f"unhandled expr {e!r}")


def canon_condition(c: Condition, out: list[str]) -> None:
    if isinstance(c, Comparison):
        out.append("CMP")
        out.append(c.op)
        canon_expr(c.left, out)
        canon_expr(c.right, out)
        return
    if isinstance(c, BoolAnd):
        out.append("AND")
        canon_condition(c.left, out)
        canon_condition(c.right, out)
        return
    if isinstance(c, BoolOr):
        out.append("OR")
        canon_condition(c.left, out)
        canon_condition(c.right, out)
        return
    if isinstance(c, IsClass):
        out.append("ISCLASS")
        out.append(c.cls)
        canon_expr(c.operand, out)
        return
    raise AssertionError(f"unhandled condition {c!r}")


def _canon_block(body: list[Stmt], out: list[str]) -> None:
    out.append(str(len(body)))
    for s in body:
        canon_stmt(s, out)


def canon_stmt(s: Stmt, out: list[str]) -> None:
    if isinstance(s, Decl):
        out.append("DECL")
        out.append(s.name)
        out.append(s.typ)
        return
    if isinstance(s, Assign):
        out.append("ASSIGN")
        out.append(s.name)
        out.append(s.typ if s.typ is not None else "NONE")
        out.append(str(len(s.values)))
        for v in s.values:
            canon_expr(v, out)
        return
    if isinstance(s, Input):
        out.append("INPUT")
        out.append(str(len(s.names)))
        out.extend(s.names)
        return
    if isinstance(s, AddStmt):
        out.append("ADD")
        out.append(s.target)
        canon_expr(s.value, out)
        return
    if isinstance(s, UpdateStmt):
        out.append("UPDATE")
        out.append(s.name)
        canon_expr(s.value, out)
        return
    if isinstance(s, AppendStmt):
        out.append("APPEND")
        out.append(s.target)
        canon_expr(s.value, out)
        return
    if isinstance(s, PrintStmt):
        out.append("PRINT")
        canon_expr(s.value, out)
        return
    if isinstance(s, GetStmt):
        out.append("GET")
        out.append(s.target)
        out.append("1" if s.index is not None else "0")
        if s.index is not None:
            canon_expr(s.index, out)
        return
    if isinstance(s, LengthStmt):
        out.append("LENGTH")
        out.append(s.target)
        return
    if isinstance(s, SetStmt):
        out.append("SET")
        out.append(s.target)
        canon_expr(s.index, out)
        canon_expr(s.value, out)
        return
    if isinstance(s, CompareStmt):
        out.append("COMPARE")
        out.append(s.name)
        canon_condition(s.condition, out)
        return
    if isinstance(s, IfStmt):
        out.append("IF")
        canon_condition(s.condition, out)
        _canon_block(s.then_body, out)
        _canon_block(s.else_body, out)
        return
    if isinstance(s, RepeatStmt):
        out.append("REPEAT")
        canon_expr(s.count, out)
        _canon_block(s.body, out)
        return
    if isinstance(s, WhileStmt):
        out.append("WHILE")
        canon_condition(s.condition, out)
        _canon_block(s.body, out)
        return
    if isinstance(s, ActionDecl):
        out.append("ACTION")
        out.append(s.name)
        out.append(str(len(s.params)))
        for p in s.params:
            out.append(p.name)
            out.append(p.typ if p.typ is not None else "NONE")
        _canon_block(s.body, out)
        return
    if isinstance(s, ReturnStmt):
        out.append("RETURN")
        canon_expr(s.value, out)
        return
    if isinstance(s, CallStmt):
        out.append("CALL")
        out.append(s.name)
        out.append(str(len(s.args)))
        for a in s.args:
            canon_expr(a, out)
        return
    raise AssertionError(f"unhandled statement {s!r}")


def canon_program(program: Program) -> list[str]:
    out: list[str] = ["PROGRAM"]
    _canon_block(program.statements, out)
    return out
