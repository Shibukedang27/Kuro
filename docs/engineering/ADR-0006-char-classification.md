# ADR-0006: `X is digit/alpha/space/alnum/quote` instead of ord()/chr()

## Problem

A lexer needs to classify a character (is this a digit? whitespace? a
quote?). The conventional way to do that in most languages is character-code
arithmetic (`ord(c) >= ord('0') and ord(c) <= ord('9')`), but Kuro has no
`ord()`/`chr()` and ADR-0004 deliberately did not add general character-code
conversion — it only added arithmetic on numbers, not a numeric view of
`Text`.

## Options

1. Add `ord`/`chr`-equivalent conversions plus the comparison operators
   needed to build range checks out of them.
2. Add a small set of built-in unary character-class predicates directly to
   the condition grammar.

## Decision

Option 2: `X is digit`, `X is alpha`, `X is space`, `X is alnum`,
`X is quote` (`IsClass` node, `compiler/ast_nodes.py`;
`CLASSIFY_WORDS` in `compiler/parser.py`). Implemented at runtime via
Python's own `str.isdigit()`/`isalpha()`/`isspace()`/`isalnum()` and a
literal `"` comparison (`compiler/interpreter.py::_isclass`).

## Reasoning

Character-code arithmetic is a bigger, more general capability than a lexer
actually needs, and it reopens questions this codebase isn't ready to
answer yet (what is `ord()` of a multi-codepoint grapheme? what integer
width does a code point become?). A named predicate is also more readable —
`If C is digit;` says what it means without the reader doing arithmetic in
their head — which matches spec section 6's "minimal syntax... readable"
principle better than exposing raw character codes would. This keeps the
new grammar surface exactly as large as Stage 5 requires and no larger
(spec section 55: don't build ahead of a real, current need).

## Consequences

- Full `ord`/`chr` conversion is explicitly deferred, not ruled out — if a
  future stdlib module needs genuine character-code math, it gets its own
  ADR then, informed by an actual use case instead of speculation.
- `IsClass` only classifies single-character `Text` values; applying it to
  a multi-character string or a non-Text value returns `false` rather than
  raising, matching how `Compare`'s boolean-producing statements already
  behave on type mismatches elsewhere in this implementation.
