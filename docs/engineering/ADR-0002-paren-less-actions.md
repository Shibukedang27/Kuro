# ADR-0002: Paren-less `Action`/`Call` is canonical; parentheses remain accepted

## Problem

The informal Kuro spec's own examples write `Action AddNumbers A, B;` and
`Call AddNumbers 10, 20;` with no parentheses. The only implementation found
(`kuro.py`) requires them: `Action AddNumbers(A, B);` /
`Call AddNumbers(10, 20);`. Session user confirmed (2026-09-10) which form
should be canonical going forward.

## Decision

Paren-less is canonical. The parenthesized form is still accepted by the
parser (`Parser._param_list` / `Parser._arg_list` in `compiler/parser.py`
both branch on whether the next token is `(`), so nothing that ran under
`kuro.py` stops parsing.

## Reasoning

Spec section 52 ("Compatibility Policy") requires exactly this shape for a
breaking change to informal-spec-vs-implementation mismatches: detect both
forms, document the canonical one, don't remove the old one outright.
Paren-less also reads closer to the rest of Kuro's word-based, low-punctuation
statement grammar (`Add v to N;`, `Print v.`) than a C-style parenthesized
parameter list would.

## Consequences

- `docs/spec/` (when written) must show paren-less in every canonical
  example, with a compatibility note about the parenthesized form.
- A future formatter (spec section 31) should normalize parenthesized
  `Action`/`Call` to paren-less on `kuro fmt`, once the formatter exists —
  not built this session (spec section 55: don't fake it).
