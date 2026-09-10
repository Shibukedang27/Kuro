"""Canonical AST serialization for Stage 6 differential testing.

Neither side of the differential test (the Python parser's real AST object
graph vs. the self-hosted Kuro parser, which has no structs/records to build
a tree out of — see docs/engineering/ADR-0010-stage6-parser.md) can be
compared directly. Both instead produce a flat, ordered list of strings
using the *same* encoding defined here, and the test just compares those
two lists for equality — exactly the technique
`tests/self_host/test_lexer_cross.py` already used for tokens, extended
from a flat token stream to a flat *tree* stream.

Encoding rules (fixed across both implementations — the Kuro parser,
self_host/parser.kuro, must match this exactly). Two revisions happened
while designing this against what an append-only, single-pass Kuro parser
can actually produce (both are load-bearing, not style choices):

  1. Most nodes are PREFIX-encoded (their own tag first, then children):
     every statement (`ASSIGN`, `IF`, `WHILE`, `ACTION`, ...) and every leaf
     expression (`LIT_INT`, `VAR`, ...) — safe because Kuro's grammar is
     keyword-driven at the start of each statement, so the tag is always
     known before its children are parsed.

     `BinaryExpr` (`BIN`) and every `Condition` node (`CMP`, `AND`, `OR`,
     `ISCLASS`) are POSTFIX instead (children first, own tag last). A
     left-associative precedence-climbing parser only discovers it's
     building one of these *after* it has already parsed (and, on the Kuro
     side, already irrevocably appended) the left operand — there is no
     way to retroactively insert a prefix tag before already-emitted
     tokens, so these emit their children first and their own tag last,
     matching the order the information actually becomes available while
     parsing left to right.

  2. Every *variable*-length list (a block's statement list, a multi-value
     assignment's right-hand side, an action's parameter list, a call's
     argument list) is terminated by an explicit END marker
     (`END_BLOCK`/`END_VALUES`/`END_PARAMS`/`END_ARGS`) *after* its items,
     not a leading count. The same append-only constraint as (1) forces
     this: a block parser doesn't know how many statements it contains
     until it has finished parsing all of them (it stops on seeing a
     terminator token like `Done`), so a leading count isn't available
     when the list starts — only an end marker, emitted once the list is
     actually over, can be produced honestly by a single left-to-right
     pass.

  - `Assign.typ` and `Param.typ`, which are optional, are encoded as the
    literal token "NONE" when absent — safe because "NONE" can never be a
    real Kuro type name (the four base types are Integers/Decimals/Text/
    Symbols).

  - `AddStmt`/`AppendStmt` (`Add v to N;` / `Append v to N;`) encode as
    `ADD <value> <target>` / `APPEND <value> <target>` — target *last* —
    for the same append-only reason as (1): the grammar parses the value
    expression before the target name is even read (`to N` comes after
    `v`), so the target isn't available to emit until after the value's
    tokens are already on the stream. Every other statement either has
    only one child, or reads all its plain-token fields (names, types)
    before parsing any recursive sub-expression, so this reordering is
    specific to these two.
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
        canon_expr(e.left, out)
        canon_expr(e.right, out)
        out.append("BIN")
        out.append(e.op)
        return
    raise AssertionError(f"unhandled expr {e!r}")


def canon_condition(c: Condition, out: list[str]) -> None:
    if isinstance(c, Comparison):
        canon_expr(c.left, out)
        canon_expr(c.right, out)
        out.append("CMP")
        out.append(c.op)
        return
    if isinstance(c, BoolAnd):
        canon_condition(c.left, out)
        canon_condition(c.right, out)
        out.append("AND")
        return
    if isinstance(c, BoolOr):
        canon_condition(c.left, out)
        canon_condition(c.right, out)
        out.append("OR")
        return
    if isinstance(c, IsClass):
        canon_expr(c.operand, out)
        out.append("ISCLASS")
        out.append(c.cls)
        return
    raise AssertionError(f"unhandled condition {c!r}")


def _canon_block(body: list[Stmt], out: list[str]) -> None:
    for s in body:
        canon_stmt(s, out)
    out.append("END_BLOCK")


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
        for v in s.values:
            canon_expr(v, out)
        out.append("END_VALUES")
        return
    if isinstance(s, Input):
        out.append("INPUT")
        out.extend(s.names)
        out.append("END_NAMES")
        return
    if isinstance(s, AddStmt):
        out.append("ADD")
        canon_expr(s.value, out)
        out.append(s.target)
        return
    if isinstance(s, UpdateStmt):
        # UPDATE reads its target name *before* parsing the value
        # (`Update N to v;`), so — unlike ADD/APPEND — target-then-value
        # matches real parse order and stays prefix.
        out.append("UPDATE")
        out.append(s.name)
        canon_expr(s.value, out)
        return
    if isinstance(s, AppendStmt):
        out.append("APPEND")
        canon_expr(s.value, out)
        out.append(s.target)
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
        for p in s.params:
            out.append(p.name)
            out.append(p.typ if p.typ is not None else "NONE")
        out.append("END_PARAMS")
        _canon_block(s.body, out)
        return
    if isinstance(s, ReturnStmt):
        out.append("RETURN")
        canon_expr(s.value, out)
        return
    if isinstance(s, CallStmt):
        out.append("CALL")
        out.append(s.name)
        for a in s.args:
            canon_expr(a, out)
        out.append("END_ARGS")
        return
    raise AssertionError(f"unhandled statement {s!r}")


def canon_program(program: Program) -> list[str]:
    out: list[str] = ["PROGRAM"]
    _canon_block(program.statements, out)
    return out
