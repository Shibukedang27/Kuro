# ADR-0005: Add `Append value to Target;` for growable collections

## Problem

`kuro.py` had no way to grow a collection: `Set` only replaces an element at
an existing index; a collection's size was fixed at the point of its
`Assign`. The Stage 5 self-hosted lexer (spec section 61) needs to build up
a token list one token at a time while scanning — the only prior workaround
would be pre-allocating a fixed-size list and tracking a separate write
cursor, which is exactly the kind of unsafe manual indexing the language is
supposed to avoid by design (spec section 9, "safety").

## Decision

New statement `Append value to Target;` (`AppendStmt` in
`compiler/ast_nodes.py`). At runtime (`compiler/interpreter.py`): if
`Target` doesn't exist yet or holds a scalar, `Append` starts/extends a
list; if it already holds a list, the value is appended in place.

## Reasoning

This is additive syntax — no existing statement's grammar or meaning
changes, so every previously valid program is still valid and behaves
identically (verified: all 16 bootstrap regression fixtures still pass,
`tests/regression/test_regression.py`). The alternative (special-casing
`Set` with an out-of-range index to mean "grow the list") was rejected as
implicit and surprising: it would make an off-by-one bug in ordinary `Set`
usage silently succeed by growing the collection instead of raising the
out-of-range error a programmer would want.

## Consequences

- `Length` after an `Append` reflects the new size, matching what a
  programmer would expect (no special-casing needed there).
- A real `List<T>` type (spec section 7) will eventually need to decide
  whether `Append` can change a list's element type; today collections stay
  dynamically/loosely typed (see `docs/architecture/current-state.md`
  section 5), so this is not yet enforced — tracked as future work, not
  silently ignored.
