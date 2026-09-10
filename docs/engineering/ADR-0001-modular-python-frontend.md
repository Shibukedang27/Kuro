# ADR-0001: Rebuild the frontend as a modular Python package, not a rewrite of kuro.py

## Problem

The only implementation found was `kuro.py`, a single 425-line file combining
lexer, parser, semantic checker, and interpreter in one process, with no
separate IR and no diagnostic recovery (see
`docs/architecture/current-state.md`). The spec calls for a real multi-phase
architecture (lexer / parser / AST / resolver / typecheck / IR / backend as
independent, testable units — spec sections 19-22).

## Options

1. Keep editing `kuro.py` in place, growing it toward the target
   architecture incrementally.
2. Freeze `kuro.py` as-is and build a new `compiler/` package from scratch,
   phase by phase, using it only as a behavioral reference during migration.
3. Start the self-hosting effort immediately and skip a Python rewrite.

## Decision

Option 2. `kuro.py` (and its tests) were copied verbatim into
`bootstrap/python/` and are not modified. A new `compiler/` package
implements each phase as its own module (`lexer.py`, `parser.py`,
`ast_nodes.py`, `resolver.py`, `typecheck.py`, `ir.py`, `lower.py`,
`interpreter.py`, `diagnostics.py`, `pipeline.py`).

## Reasoning

- A single file with everything inlined cannot support spec section 33
  (fuzzing each phase independently), section 21 (semantic analysis as its
  own testable subsystem), or a future non-interpreter backend (section 25)
  without first being split apart — so the split has to happen regardless.
- Editing in place risks silently changing behavior mid-file with no
  reference point to check against. Freezing the original and testing the
  new implementation against its captured golden output
  (`tests/regression/`) makes every behavioral difference a conscious,
  reviewed decision (recorded as its own ADR) instead of an accident.
- Option 3 (skip straight to self-hosting) was rejected: Stage 5
  (spec section 61) requires the Kuro-in-Kuro lexer to be cross-tested
  against a trustworthy reference lexer, and the old `kuro.py` lexer has
  known bugs (silent bare-word fallback, no error recovery) that would make
  it a poor oracle.

## Consequences

- Every behavioral difference from `kuro.py` needs its own ADR (see
  ADR-0002 through ADR-0007) — this is the intended cost of the approach,
  not overhead to be trimmed.
- `bootstrap/python/` must not be deleted until the new implementation is
  proven at least as capable (spec section 56); it remains the Stage
  0-era reference and the regression suite's oracle.
