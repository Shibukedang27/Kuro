# ADR-0007: `Get`/`Length` no longer print as a side effect

## Problem

In `kuro.py`, `Get` and `Length` both unconditionally called Python's
`print()` in addition to setting `@_` — e.g. `exec1()`'s `Get` handler does
`self.env["_"]=y; print(y); ...`. No statement in the spec or in any test
file's comments describes this as intended language behavior; it reads as a
debug convenience left over from interactive development
(`docs/architecture/current-state.md` section 7).

## Decision

`Get`/`Length` only set `@_`; they never print on their own
(`compiler/interpreter.py`, `GET`/`LENGTH` ops). Getting the printed
behavior back requires an explicit `Print @_.` afterward.

## Reasoning

An implicit print on a statement whose name suggests "fetch a value" (not
"fetch and display it") is a surprising side effect — exactly the kind of
"dangerous implicit behavior" spec section 6 says to avoid, and the kind of
inherited bug the audit (`docs/architecture/current-state.md` section 10)
flagged as something not to carry forward on autopilot. `@_`/`_` already
exists specifically so a statement's result can be used afterward
(`Print @_.`, or as an argument to another statement); the auto-print made
that mechanism redundant for exactly these two statements while being silent
everywhere else.

## Consequences

- This is a genuine breaking change for any program that relied on the
  auto-print (spec section 52 requires this to be acknowledged, not
  smoothed over). Two of the sixteen bootstrap regression fixtures
  (`get.kuro`, `length.kuro`) exist purely to exercise that auto-print and
  now produce no output; `tests/regression/test_regression.py` documents
  both by name (`KNOWN_DIVERGENCES`) and asserts the new, empty-output
  behavior explicitly rather than silently passing.
- No migration tool was built for this one specific case (spec section 52
  step 4, "provide migration tooling when practical") — the fix for an
  affected program is mechanical (add `Print @_.`), and building tooling
  for a single-statement mechanical fix would be premature relative to
  spec section 55 ("no fake features" / don't build ahead of real need).
