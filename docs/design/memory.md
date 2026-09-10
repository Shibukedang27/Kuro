# Memory Management (spec section 12)

## Status: deferred, not yet decided for a native backend — documented honestly rather than guessed

This document exists because spec section 12 requires the decision to be
recorded here once made. As of this session, **no native memory model has
been designed or built**, because there is no native backend yet (Stage 9;
see `docs/architecture/current-state.md` section 9 for the honest inventory
of what doesn't exist). Writing a memory-management design in the abstract,
before a backend exists to constrain it, would be exactly the kind of
speculative architecture spec section 66 warns against ("do not create
architecture purely inside your head").

## What actually governs memory today

Stage 4's runtime (`compiler/interpreter.py`) is a tree-walking interpreter
hosted in CPython. Every Kuro value (`int`, `float`, `str`, `list`) is a
native Python object; Kuro's `self.env` dict and call-frame dicts are
ordinary Python dicts. Memory is entirely managed by CPython's own
reference-counting + cyclic garbage collector. This gives Kuro programs
running under Stage 4 the same memory *safety* properties CPython has
(no use-after-free, no manual allocation), but none of it is a Kuro-language
design decision — it's simply "whatever hosting the interpreter in Python
gets you for free," and it disappears the moment there is a native backend
with its own value representation.

## The real decision, deferred to Stage 9 planning

When a native backend (LLVM, spec section 25) is built, this document must
be updated with an actual choice among:

- **Tracing GC** (e.g. a simple mark-sweep or generational collector) —
  simplest for the compiler to target, most forgiving for programmers,
  but adds runtime pause behavior that needs to be documented for
  latency-sensitive use.
- **Reference counting** — more predictable, no separate collector thread,
  but classic cycle-leak risk unless paired with a cycle collector (which
  starts to resemble tracing GC anyway) and has real overhead on every
  assignment.
- **Ownership/borrowing** (Rust-style) — best raw performance and the
  strongest static safety guarantees, but a large increase in compiler and
  language complexity (borrow checking, lifetime inference) that spec
  section 12 explicitly warns against adopting "merely because it is
  fashionable."

The evaluation criteria spec section 12 lists (simplicity, safety, runtime
cost, compiler complexity, developer ergonomics, concurrency,
native interop) all need to be weighed against an actual backend's
constraints, not decided in a vacuum. Given Kuro's stated design priority
order (spec section 1: correctness, simplicity, safety, determinism,
maintainability *before* performance), a tracing GC is the most likely
outcome of that evaluation — but this is a lean, not yet a decision, and
this file will be rewritten with a real ADR once Stage 9 work begins.
