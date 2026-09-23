"""AST node definitions for Kuro.

Kept deliberately separate from the parser (spec section 19): nothing here
knows how to parse; nothing downstream (resolver, typecheck, lowering) is
allowed to import parser internals, only these node types. Every node
carries a `Span` so every later diagnostic can point at real source.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .diagnostics import Span


class Node:
    span: Span


# --- Expressions ----------------------------------------------------------
# Bootstrap Kuro had no expression grammar at all (only literal / @var / bare
# word). ADR-0004 adds arithmetic (+ - * /) with standard precedence and
# parenthesized grouping, because the spec's own examples (`Return A + B;`)
# require it and Stage 5's self-hosted lexer needs integer arithmetic on
# character codes. Nothing about the old single-value grammar stops parsing:
# a bare literal/var is still a valid (trivial) expression.


class Expr(Node):
    pass


@dataclass
class Literal(Expr):
    value: object  # int | float | str
    span: Span


@dataclass
class VarRef(Expr):
    """`@Name` (explicit) or a bare `Name` used as a value."""

    name: str
    explicit_at: bool
    span: Span


@dataclass
class BinaryExpr(Expr):
    op: str  # '+', '-', '*', '/'
    left: Expr
    right: Expr
    span: Span


# --- Conditions -------------------------------------------------------------
# ADR-0004 also adds `and`/`or` combinators over comparisons (needed for
# range checks like "digit between '0' and '9'" in the Stage 5 lexer). A
# single Comparison is still a complete, valid Condition on its own.


class Condition(Node):
    pass


@dataclass
class Comparison(Condition):
    left: Expr
    op: str  # 'gt' | 'lt' | 'eq' | 'ne' | 'ge' | 'le'
    right: Expr
    span: Span


@dataclass
class IsClass(Condition):
    """`X is digit` / `X is alpha` / ... — ADR-0006. A unary character-class
    predicate, added so the Stage 5 self-hosted lexer can classify a
    character without needing raw character-code arithmetic (Kuro has no
    ord()/chr() and ADR-0004 deliberately did not add one — see
    docs/engineering/ADR-0006-char-classification.md)."""

    operand: Expr
    cls: str  # 'digit' | 'alpha' | 'space' | 'alnum' | 'quote'
    span: Span


@dataclass
class BoolAnd(Condition):
    left: Condition
    right: Condition
    span: Span


@dataclass
class BoolOr(Condition):
    left: Condition
    right: Condition
    span: Span


# --- Statements -------------------------------------------------------------


class Stmt(Node):
    pass


@dataclass
class Decl(Stmt):
    name: str
    typ: str
    span: Span


@dataclass
class RecordDecl(Stmt):
    name: str
    fields: list[Param]
    span: Span


@dataclass
class EnumDecl(Stmt):
    name: str
    variants: list[str]
    span: Span


@dataclass
class Assign(Stmt):
    name: str
    values: list[Expr]
    typ: str | None  # set when written as `Name : Type = ...;` (spec section 8)
    span: Span


@dataclass
class Input(Stmt):
    names: list[str]
    span: Span


@dataclass
class AddStmt(Stmt):
    value: Expr
    target: str
    span: Span


@dataclass
class UpdateStmt(Stmt):
    name: str
    value: Expr
    span: Span


@dataclass
class PrintStmt(Stmt):
    value: Expr
    span: Span


@dataclass
class GetStmt(Stmt):
    target: str
    index: Expr | None
    span: Span


@dataclass
class LengthStmt(Stmt):
    target: str
    span: Span


@dataclass
class SetStmt(Stmt):
    target: str
    index: Expr
    value: Expr
    span: Span


@dataclass
class AppendStmt(Stmt):
    """`Append value to List;` — ADR-0005, needed to build growable
    collections (the Stage 5 lexer accumulates a token list one token at a
    time). Bootstrap Kuro had no way to grow a collection at all."""

    value: Expr
    target: str
    span: Span


@dataclass
class CompareStmt(Stmt):
    name: str
    condition: Condition
    span: Span


@dataclass
class IfStmt(Stmt):
    condition: Condition
    then_body: list[Stmt]
    else_body: list[Stmt]
    span: Span


@dataclass
class RepeatStmt(Stmt):
    count: Expr
    body: list[Stmt]
    span: Span


@dataclass
class WhileStmt(Stmt):
    """ADR-0009: a condition-bounded loop, added so a scan doesn't need to
    be padded to a precomputed upper bound (as self_host/lexer.kuro's
    Repeat-plus-flag workaround had to be) to avoid an unbounded loop."""

    condition: Condition
    body: list[Stmt]
    span: Span


@dataclass
class Param:
    name: str
    typ: str | None
    span: Span


@dataclass
class ActionDecl(Stmt):
    name: str
    params: list[Param]
    body: list[Stmt]
    return_type: str | None
    span: Span
    generic_params: list[str] = field(default_factory=list)


@dataclass
class ReturnStmt(Stmt):
    value: Expr
    span: Span


@dataclass
class CallStmt(Stmt):
    name: str
    args: list[Expr]
    span: Span


@dataclass
class Program:
    statements: list[Stmt] = field(default_factory=list)
