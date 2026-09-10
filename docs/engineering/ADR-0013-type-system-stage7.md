# ADR-0013: Type system stabilization and a bounded expansion for Stage 7

## Problem

`compiler/typecheck.py`'s actual current behavior (audited and verified —
`docs/architecture/self-hosted-semantics.md` §4) only type-checks three
statement kinds: `Assign`, `AddStmt`, `SetStmt`. Comparisons, `and`/`or`,
`Repeat`'s count, `Call` arguments, `Return` values, and most builtins are
not type-checked at all. Stage 7's task explicitly asks for a self-hosted
typechecker that checks comparisons, logical expressions, builtins, calls,
returns, and conditions — "do not simply mark all builtins as `Unknown`;
that would make the typechecker decorative." This is, unavoidably, a real
semantic *expansion*, not a port of existing behavior. The Golden Rule
(ADR-0012) requires exactly this to go through a real change process
instead of happening quietly while writing Kuro code: identify it,
decide if it's a language change, write an ADR (this one), update the
spec, update the Python oracle *first*, then the self-hosted
implementation, then regression tests. This document is that process.

## Decision: six new, narrow, independently-justified checks

Each closes a specific, concrete gap the audit found — not a general
"make the typechecker stricter" pass. `E3006` through `E3011` (the next
free codes in the existing E3xxx family — no second taxonomy).

1. **`E3006` — comparison operand compatibility.** `gt`/`lt`/`ge`/`le`
   require both operands to be in the same comparable family: both
   numeric (`Integers`/`Decimals`, mixing is fine — same widening rule as
   `Assign`) or both `Text` (lexicographic). `Symbols` has no natural
   order, so it's never valid on either side of an ordering comparison.
   `eq`/`ne` are **not** restricted — equality across differing types is
   well-defined (it's just always false), and restricting it would reject
   a currently-legal, harmless pattern (e.g. comparing a possibly-`Symbols`
   `Compare` result against a literal) for no real benefit.
2. **`E3007` — call argument type mismatch.** A parameter with an
   explicit type annotation (`Action Add A: Integers, B: Integers;` —
   ADR-0004) currently has that annotation checked precisely nowhere; a
   `Call Add "x", "y";` compiles today. Checked the same way `Assign`
   already is (`compatible(declared, inferred)`), only for parameters
   that actually have an annotation — untyped parameters impose no
   constraint, matching how untyped `Assign` targets already work.
3. **`E3008` — `Repeat`'s count must be `Integers`.** The interpreter
   already runtime-checks non-negativity (`CHECK_NONNEG`, ADR-0009's
   companion fix) but nothing today statically rejects
   `Repeat "hello";`, which would only be caught in a confusing way at
   runtime once arithmetic on it is attempted.
4. **`E3009` — `Length`'s target must be `Text`.** The only base type
   with a coherent length concept today, given collections have no
   distinct type from their element type (§ "What this ADR does not do"
   below) — `Integers`/`Decimals`/`Symbols` targets are rejected.
5. **`E3010` — `Get`/`Set`'s index must be `Integers`.** Both already
   fail at runtime (`E6001`/type errors) for a non-numeric index; this
   makes the same mistake catchable before running the program, matching
   the spirit of every other statically-checkable case already covered.
6. **`E3011` — arithmetic operand compatibility, and closing the
   `Text + Text` gap.** `_infer`'s `BinaryExpr` handling never recognized
   string concatenation (which the interpreter genuinely supports —
   `compiler/interpreter.py::_binop`), silently treating `"a" + "b"`'s
   type as unknown rather than `Text`. Fixed by teaching `_infer` about
   it, and, now that arithmetic type inference is a real, deliberate
   piece of logic rather than an incidental byproduct, also reporting an
   error for operand combinations that are neither valid numeric
   arithmetic nor `Text + Text` (e.g. `5 + "hello"`, `"a" - "b"`,
   anything involving `Symbols`) instead of silently returning "unknown"
   for them, which is what let `E3001` skip checking their use in an
   `Assign` before.

## What this ADR does not do

- **No `Boolean` type.** `Symbols` already serves that role
  (`CompareStmt` always types its result as `Symbols`); spec section 15's
  "only include `Boolean` if it already exists semantically" is
  respected by not introducing a second name for the same concept.
- **No `List<T>`/collection type.** Collections are still typed by their
  element type, exactly as today (§5 of the audit). Distinguishing "a
  `Text` scalar" from "a list of `Text`" would need a real representation
  change this ADR deliberately does not make — out of Stage 7's scope
  (spec section 15: "keep Stage 7 focused... future types... are NOT
  Stage 7 requirements unless existing code already depends on them").
  `Append`'s lack of a homogeneity check (already documented in
  ADR-0005) is therefore also left exactly as-is.
- **No condition-truthiness rule.** The task prompt raises `If "hello";`
  as an example to check "the language's actual truthiness rules" —
  but that form isn't valid Kuro grammar at all: `If`'s condition is
  always a `Comparison`/`BoolAnd`/`BoolOr`/`IsClass` node, never a bare
  expression (`compiler/parser.py`'s condition grammar has no path that
  accepts one). There is no truthiness concept to extract or preserve
  because the grammar never allows the ambiguous case to arise. `and`/
  `or`'s operands are, for the identical structural reason, always
  well-formed `Condition` nodes — recursively checking each `Comparison`
  leaf via `E3006` is what makes a logical expression well-typed; no
  separate check is needed for the combinator itself.
- **No `Return`-type checking.** There is no syntax to declare an
  Action's return type, so "wrong return type" (raised as a task example)
  cannot be checked without inventing new syntax — explicitly out of
  scope (documented as a real, current language limitation in the audit
  §9 item 7, not silently dropped).
- **No new check for `IsClass`/`Append`.** `IsClass` on a non-`Text`
  operand already degrades gracefully at runtime (`Interpreter._isclass`
  returns `false` rather than erroring) — making it a compile error would
  *restrict* a currently-valid, harmless program, which the Golden Rule's
  "do not silently improve" cuts against just as much as under-checking
  does. `Append` is covered by the existing ADR-0005 stance.

## Process followed

Per the Golden Rule: all six checks are implemented in
`compiler/typecheck.py` (the Python oracle) first, with new tests proving
(a) no previously-passing program now fails and (b) each new invalid
program is now caught — before any self-hosted equivalent is written.
`self_host/typecheck.kuro` then implements the identical rules, verified
by differential testing against the same oracle.

## Compatibility impact

Six previously-silent gaps become compile-time diagnostics. Every program
in the existing 294-test baseline was re-run after this change (Phase 4
below) to confirm none of them exercised one of these gaps — if any had,
that would itself be worth stopping and investigating, since a passing
test hitting one of these would suggest a "valid" program that has
actually always been running with untyped/inconsistent data live.

## Testing strategy

New Python-side tests in `tests/semantic/test_semantic.py` for each of the
six codes (both a triggering and a non-triggering case). Self-hosted
differential coverage in `tests/self_host/test_typecheck_cross.py`, with
dedicated fixtures per code plus realistic combinations (an `Action` call
whose argument type is wrong, a comparison inside a `While` condition,
etc.), mirroring the structure Stage 6's differential suite already
established.
