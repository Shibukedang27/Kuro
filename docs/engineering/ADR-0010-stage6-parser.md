# ADR-0010: Stage 6 self-hosted parser — module system, AST representation, and grammar scope

## Problem

Stage 6 (spec section 61) asks for a Kuro-in-Kuro parser, cross-tested
against `compiler/parser.py`. Three problems have no existing answer in
this codebase and had to be resolved before writing a line of parser code:

1. Kuro has no import/module system (spec section 14 describes one
   aspirationally; nothing implements it). The task's suggested layout
   (`lexer.kuro`, `tokens.kuro`, `parser.kuro`, `ast.kuro`,
   `parser_helpers.kuro` as separate, presumably importing, files) is not
   buildable as literal separate Kuro modules without either faking an
   import statement that doesn't exist, or building a real one.
2. Kuro has no structs/records/tagged unions. A parser's natural output —
   a tree — has no native Kuro value to be represented as.
3. `self_host/lexer.kuro` (Stage 5) only *prints* its tokens; a parser
   needs to *read* them programmatically, which a print stream doesn't
   support.

## Decision 1: no fake modules — one file, organized in labeled sections

**Minimum capability a real module system would need**: the ability for
one file to reference a name (variable or Action) defined in another file,
resolved at compile time. This does not exist, and this ADR does not build
it — building a real module system is its own substantial design problem
(namespacing, visibility, circular-dependency detection — spec section 14
lists all of it) that deserves its own ADR grounded in more than "the
parser file got long," not a corner cut here to make Stage 6 look tidier.

Given that, `self_host/parser.kuro` is one file, like `lexer.kuro` was,
organized with clearly labeled comment-header sections (`# --- token
access helpers ---`, `# --- expression parsing ---`, `# --- statement
parsing ---`, `# --- entry point ---`) mirroring the module boundaries the
task suggested, so the *organization* the task asked for exists in the
source even though the *file* boundaries don't. This is stated as a real,
named limitation, not smoothed over: true multi-file self-hosted Kuro
source is blocked on a real module system, which remains future work.

## Decision 2: canonical flat-list AST encoding, not an in-memory tree

Since Kuro cannot build a tree value, `self_host/parser.kuro` does not
attempt to; it does what `self_host/lexer.kuro` already does for tokens —
append a flat, ordered sequence of strings to a global list
(`AstOut`) as it recognizes each grammar construct, using a prefix
(node-tag-first) encoding with an explicit count prefix wherever a node has
a variable number of children (a block's statement list, a call's argument
list, an action's parameter list, a multi-value assignment). Fixed-arity
nodes (a binary expression always has exactly two children, an `If` always
has exactly one condition, one then-block, one else-block) need no count —
the encoding is self-delimiting because every node consumes a known shape.

The exact same encoding is implemented on the Python side as
`compiler/ast_canon.py::canon_program()`, which walks the *real* parsed AST
from `compiler/parser.py` and produces the identical flat list for the
same source. Stage 6's differential test
(`tests/self_host/test_parser_cross.py`) is then a plain list-equality
check between the two, the same technique
`tests/self_host/test_lexer_cross.py` already validated for token streams
in Stage 5, now applied to trees instead of a flat token sequence. Full
encoding rules are documented in `compiler/ast_canon.py`'s module
docstring, which is the single source of truth both implementations must
match.

## Decision 3: the lexer gains a structured output, additively

`self_host/lexer.kuro` is extended, not rewritten: two new declarations
near the top (`TokenKinds is Text;` / `TokenValues is Text;` — `Decl` with
no initial value, so `Append`'s "target doesn't exist yet" branch cleanly
starts a fresh list on the first token rather than needing an empty-list
literal Kuro doesn't have) and, at each of the existing token-emission
points, one additional pair of `Append <Kind> to TokenKinds;` /
`Append <Value> to TokenValues;` statements alongside the `Print` calls
that were already there. Every existing `Print` call is untouched, in the
same order, with the same values — `tests/self_host/test_lexer_cross.py`
(Stage 5's 23 cross-tests) is re-run unmodified after this change and must
still pass, proving the addition is genuinely additive, not a rewrite.

`self_host/parser.kuro` reads `TokenKinds`/`TokenValues` (two parallel
lists) plus a global cursor variable `TokPos`, using `Get`/`Length` —
exactly the same access pattern the lexer already used to read `Source`.

## Grammar scope for this session (honest, not full)

Implementing every statement form in one pass risked exactly the failure
mode spec section 55 warns about — either it doesn't really work
end-to-end, or "working" quietly means "never actually tested." Given that,
this session's `self_host/parser.kuro` covers, with real differential
tests proving each part:

**Expressions** (full precedence, matching `compiler/parser.py` exactly):
literals (integer/decimal/text), variable references (bare and `@`-form),
`+ - * /` with standard precedence, parenthesized grouping, unary minus.

**Conditions**: comparisons (`gt/lt/eq/ne/ge/le`, including the `or equal
to`/`at least`/`at most` phrasings), `and`/`or` combinators, `is
digit/alpha/space/alnum/quote` classification.

**Statements**: `Decl`, `Assign` (typed and untyped, single- and
multi-value), `Add`, `Update`, `Print`, `Return`, `Call` (with arguments,
paren-less and legacy-parenthesized), `Action` (with typed/untyped
parameters, either form), `If`/`Else`, `Repeat`, `While` (ADR-0009 — the
newest statement, included specifically to prove the self-hosted parser
isn't perpetually one stage behind the language it parses).

**Deferred to a later increment**, named explicitly rather than silently
missing: `Take`, `Get`, `Length`, `Set`, `Append`, `Compare` (the
statement — not to be confused with the condition grammar, which *is*
covered since `If`/`While` need it), and the legacy `Entered ... then
... otherwise ...;` one-line form. None of these are structurally harder
than what's covered — they're mechanically similar to statements already
implemented — so this is a scope decision to ship a real, fully-tested
subset now rather than a wider, less-verified one, not a sign any of them
are especially difficult.

## Error behavior

The self-hosted parser must not crash on malformed input (spec section 33),
but does not yet produce the structured, coded diagnostics
`compiler/diagnostics.py` gives (E2xxx with span/help text) — that parity
is real future work, not built this session. Concretely: on an unexpected
token, the current grammar rule's Action stops consuming and returns
without appending further `AstOut` entries for that construct, and parsing
continues from wherever `TokPos` was left — this bounds the damage to "an
incomplete/wrong parse of the malformed construct," never a hang or a
Python-level crash, but it is not equivalent to `compiler/parser.py`'s
per-error-site `E2001`-`E2005` diagnostics with recovery/synchronization.
Malformed-input test cases in `tests/self_host/test_parser_cross.py`
therefore assert "does not hang and does not crash," not "produces the
same diagnostic as the Python parser."

## Why this design fits Kuro

It reuses every architectural decision Stage 5 already validated (a flat
global-array output, read via the same `Get`/`Length`/`Append` primitives,
run by the same Stage 1-4 interpreter, cross-tested by the same
flat-list-equality technique) rather than inventing a second approach for
trees. It is honest about the two real gaps that made a "clean," literally
multi-file, fully-diagnostic parser impossible this session (no module
system, no structured self-hosted diagnostics) instead of papering over
either with something that only looks like the real thing.

## Compatibility impact

None on the language: no grammar changes. `self_host/lexer.kuro`'s
observable `Print` behavior is unchanged (verified by re-running its
existing cross-tests). This ADR only adds new files/tests and additive
statements to an existing self-hosted program.

## Testing strategy

- `tests/parser/test_ast_canon.py`: the canonical encoding itself, checked
  against known expected token lists, independent of the self-hosted
  parser (so a mismatch is diagnosable without doubting the encoding).
- `tests/self_host/test_lexer_cross.py`: re-run unmodified after extending
  `lexer.kuro`, to prove the extension was additive.
- `tests/self_host/test_parser_cross.py`: differential tests — real Kuro
  source (drawn from this repository's existing fixtures where they fit
  the covered grammar subset, plus hand-written cases for expression
  precedence, `If`/`While`/`Repeat`, and `Action`/`Call`) parsed by both
  `compiler/parser.py` (via `ast_canon.canon_program`) and
  `self_host/parser.kuro` (via its `AstOut` list), asserted equal.
- Malformed-input cases (missing `Done`, missing `;`, an incomplete
  expression, unexpected EOF) asserted not to hang or crash the
  interpreter, per "Error behavior" above.
