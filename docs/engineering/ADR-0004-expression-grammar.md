# ADR-0004: Add arithmetic expressions and and/or condition combinators

## Problem

`kuro.py` had no expression grammar at all: a "value" was only a literal, an
`@var`, or a bare word. The spec's own example `Return A + B;` (section 10)
does not parse under that grammar. Separately, `If` could only test one
comparison; there was no way to write "digit between '0' and '9'"-style
range checks, which the Stage 5 self-hosted lexer needs.

## Decision

- Arithmetic: `+ - * /` with standard precedence (`*`/`/` bind tighter than
  `+`/`-`) and parenthesized grouping, implemented as `BinaryExpr` nodes
  (`compiler/ast_nodes.py`, `compiler/parser.py::_term/_factor/_atom`).
  Unary minus is sugar for `0 - x`.
- Conditions: `and`/`or` combinators over comparisons (`or` binds loosest),
  as `BoolAnd`/`BoolOr` nodes wrapping `Comparison`.
- A bare literal/`@var`/word is still a complete, valid expression — nothing
  that parsed before stops parsing.

## Reasoning

Both were required, not optional nice-to-haves: without arithmetic, the
spec's own canonical `Action` example is unparseable; without `and`/`or`,
range-style conditions needed by any nontrivial control flow (including the
Stage 5 lexer's character classification) require nesting `If` statements
awkwardly instead of writing the condition directly. Keeping the operator
words (`and`/`or`) rather than introducing symbolic `&&`/`||` matches Kuro's
existing "readable word" style (`is greater than`, not `>`).

## Consequences

- `division by zero` is now a reachable runtime condition (`E6003`); it did
  not exist as a concept before there was a `/` operator.
- Integer division (`10 / 2`) stays an `Integers` result when it divides
  evenly, and produces a `Decimals` (float) result otherwise — a pragmatic
  choice documented in `compiler/interpreter.py::_binop`, not a fully
  flow-sensitive type system (`compiler/typecheck.py`'s static inference for
  `/` can therefore be optimistic about the result type; this is a known,
  narrow limitation, not silently wrong behavior — it never reports a type
  error, only occasionally infers a looser type than the runtime turns out
  to produce).
- Found and fixed a real lexer bug while adding this (see
  `compiler/lexer.py::_scan_number`): `.` is both the decimal point and the
  `Print`-statement terminator, so `Print 10 / 2.` requires the lexer not to
  swallow the trailing `.` into the number `2`.
