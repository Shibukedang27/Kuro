# ADR-0009: Add `While`; do not add `Break`/`Continue`

## Problem

`Repeat N;` only takes a fixed iteration count decided before the loop
starts, with no early exit. The Stage 5 self-hosted lexer
(`self_host/lexer.kuro`, ADR-0008) worked around this by bounding every scan
loop at `SourceLen` and guarding each iteration with an integer flag —
correct, but O(n²)-ish, because a loop that has already "logically"
finished still burns its remaining bounded iterations doing nothing. A
recursive-descent parser (Stage 6) does far more of this kind of
"scan/consume until a condition holds" work than a lexer does — statement
lists, parameter lists, argument lists, and precedence-climbing expression
parsing are all indeterminate-length by nature — so the padding cost would
compound badly, and, separately, the boilerplate cost (a flag variable at
every call site) would make an already-nontrivial parser harder to write
correctly.

## Evaluation

**1. Does Kuro need `While`?** Yes. A loop bound only by a runtime
condition — `While <condition>; ... Done.` — is what "scan until a
condition holds" actually is; it removes the padding (the loop stops the
iteration it becomes false, not `SourceLen` iterations later) and the flag
becomes the loop's own condition instead of a separate guard checked inside
a fixed-count loop. This is not a compiler-specific need: any Kuro program
that reads input until a sentinel, retries until success, or processes a
collection until it's empty needs exactly this, and currently cannot
express it without the same padding trick the lexer used. It satisfies the
evaluation question directly — this measurably improves ordinary Kuro
programs, not only compiler internals.

**2. Does Kuro need `Break`?** No, not now. Once `While` exists, every
"stop early" case the lexer needed can be expressed by folding the stop
condition directly into the loop's own condition (`While Flag is equal to
1 and Pos is less than SourceLen;`) instead of a separate mid-body jump —
this is the same idiom already proven working in `self_host/lexer.kuro`,
just attached to a real conditional loop instead of a padded one, so the
asymptotic problem is already solved by `While` alone. The remaining
argument for `Break` is pure readability/boilerplate reduction, not a
capability gap. Separately: a recursive-descent parser's natural unit of
"stop everything and unwind" is a grammar rule's own function returning
(`Action`/`Return`/`Call` already exist and already provide this), so the
one case where `Break` earns its keep in other languages — unwinding out of
a deeply nested loop at once — is already covered by structuring the parser
as one loop per grammar rule and letting `Return` do the unwinding, which
Stage 6's architecture does anyway (spec section 6: "avoid adding syntax
merely because another language has it").

**3. Does Kuro need `Continue`?** No, for the same reason as `Break`:
"skip the rest of this iteration" is already expressible by wrapping the
remainder of the loop body in an `If`, which is the same shape of code a
`Continue`-based version would need for its non-skipped path anyway.

**4. Can `Repeat` remain as-is?** Yes, unchanged. `Repeat` reads clearly for
its actual common case — "do this exactly N times," with `Index` available
— and nothing here proposes touching it. `While` is additive, not a
replacement.

**5. Can the parser be implemented cleanly without these features?**
Technically (the lexer proves the padded-loop pattern works), but not
*cleanly* — a parser has enough indeterminate-length loops, several of them
nested, that paying the padding-plus-flag tax at every one of them would
make the parser markedly harder to write correctly and to review than the
lexer was. This is the actual argument for doing this work now, before
Stage 6, rather than deferring it again.

**6. Does this improve normal Kuro programming, not just compiler
internals?** Yes — see (1). This is the deciding factor that separates
`While` (general-purpose, justified on its own) from `Break`/`Continue`
(narrowly about loop-writing convenience, and not clearly justified even
there once `While` exists).

## Decision

Add one new statement, `While`. Do not add `Break` or `Continue` at this
time. This is a deliberate, principled "no," not an oversight — Kuro's
design priority order (spec section 1: correctness, simplicity, safety,
determinism, maintainability *before* performance/convenience) favors the
smaller sufficient grammar over the larger convenient one, and section 55
says not to build ahead of a real, current need. If Stage 6 implementation
work turns up a concrete case `While` genuinely cannot express cleanly,
that becomes its own ADR grounded in that specific case — not speculation
here.

## Syntax

```
While <condition>;
    <statements>
Done.
```

Exactly `If`'s block shape (`condition; ... Done.`), and reuses the *same*
condition grammar `If`/`Compare` already have — `Comparison`, `IsClass`,
and `BoolAnd`/`BoolOr` combinators (ADR-0004/0006) — so nothing new is
added to expression or condition parsing, only a new statement that wraps
one.

## Semantics

The condition is evaluated before every iteration, including the first;
`While` executes its body zero or more times. This exactly matches the
"C/Python-style pretest loop" most programmers already expect, and it is
the same evaluation-order relationship `If`'s condition already has to its
then-branch — no new conceptual model, just a new statement shape around
the existing one.

## Scope behavior

Ordinary variables assigned inside a `While` body share the *enclosing*
scope — there is no per-iteration or per-loop scope, matching `Repeat`
(post ADR-fix, see the "Fix resolver" commit between Stage 5 and this ADR)
and matching the interpreter's flat storage model
(`docs/architecture/current-state.md` section 7). Unlike `Repeat`, `While`
introduces no loop variable of its own (nothing analogous to `Index`), so
its resolver handling needs no `SAVEVAR`/`RESTOREVAR`-style special case at
all — it is, if anything, *simpler* to resolve correctly than `Repeat` was.

## Nested-loop behavior

Nested `While` (or `While` inside `Repeat`, or vice versa) needs no special
handling: each loop lowers to its own pair of labels
(`while_start_N`/`while_end_N`, uniquely numbered by the IR builder,
exactly like `If`'s `else_N`/`endif_N` labels already are) and its own loop
guard (see "Error behavior" below), so nesting is structurally identical to
nesting `If` inside `If` — no shared mutable state between loop levels
beyond whatever ordinary Kuro variables the program itself uses.

## Error behavior

`While` is the first Kuro construct that can, by construction, fail to
terminate — every existing loop (`Repeat`, and recursion depth via
`Action`/`Call`) was already bounded and already had a structured error for
exceeding that bound (`E6005` for recursion). `While` needs the equivalent:
a new IR instruction, `LOOP_GUARD`, is emitted once at the top of every
lowered `While` body (`compiler/lower.py`) and increments a per-loop
counter each time it executes; if a single `While` loop's body runs more
than a configurable cap (`Interpreter(..., max_while_iterations=...)`,
default 10,000,000) without its condition going false, the interpreter
raises a new structured runtime error, `E6006` ("While loop exceeded
maximum iteration count"), instead of hanging the process indefinitely —
this is the same "no meaningless crashes, no indefinite hangs" principle
(spec sections 11 and 33) that already motivated `E6005`, now extended to
cover the one new way a Kuro program can misbehave. This required no new
parser- or resolver-level diagnostics beyond the usual "expected `;`" /
"expected a comparison operator" family `If` already gets for free by
reusing its condition grammar.

## Why this design fits Kuro

It is the smallest addition that actually removes the measured problem
(the lexer's O(n²) padding), it reuses 100% of the existing condition
grammar and block-parsing shape (`If`'s), it needed zero new IR
*value*-producing instructions (only a bookkeeping one, `LOOP_GUARD`, for
safety) because the existing `JUMP`/`JUMPF`/`LABEL` primitives already do
everything a loop needs, and it does not import a second, unrelated
control-flow vocabulary (`Break`/`Continue`) that the language's other
constructs (`Action`/`Return`) already make mostly redundant.

## Compatibility impact

None. `While` is new syntax; no previously valid Kuro program's grammar or
meaning changes. `While` is a reserved-by-position word exactly like every
other Kuro keyword (not a reserved token — see `compiler/tokens.py`'s
comment on this), so a program that happened to use `While` as an ordinary
identifier before this change would now have that identifier shadowed in
statement-starting position; this is the same category of risk every prior
positionally-recognized keyword already carried (`If`, `Repeat`, `Action`,
...), not a new one introduced by this ADR.

## Testing strategy

Every layer gets both positive and negative coverage, plus regression
coverage that nothing else moved:
- **Parser** (`tests/parser/`): a basic `While`, nested `While`, `While`
  combined with `and`/`or` conditions, and the standard negative cases
  (missing `Done`, missing `;`, malformed condition) that `If` already has
  equivalents of.
- **Semantic** (`tests/semantic/`): a variable first assigned inside a
  `While` body is visible after it (the same property just fixed for
  `Repeat`); an undefined variable in a `While` condition is caught.
- **IR** (`tests/ir/`): a `While` lowers to exactly one loop-start label,
  one loop-end label, a `JUMPF`, a backward `JUMP`, and a `LOOP_GUARD`;
  `compiler/ir.py::validate()` still accepts it.
- **Runtime** (`tests/runtime/`): a `While` that actually loops and
  terminates via its condition; a `While` that never terminates raises
  `E6006` (tested with a small `max_while_iterations` so the test itself
  stays fast); nested `While` loops don't share loop-guard state
  incorrectly.
- **Full regression** (Phase 4): the entire pre-existing 150-test suite
  must still pass unmodified after this change, with the numbers reported
  exactly, not approximated.
