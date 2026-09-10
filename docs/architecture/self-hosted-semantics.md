# Self-Hosted Semantics Audit (Stage 7)

Date: this session, before any Stage 7 implementation. Method: read
`compiler/resolver.py` and `compiler/typecheck.py` in full, then verified
every non-obvious claim below by actually compiling small programs through
`compiler/pipeline.py` rather than trusting the source reading alone (see
"Verified findings" — three of these contradicted my first reading of the
code). This document is the oracle Stage 7's self-hosted resolver and
typechecker must match, per the Golden Rule (ADR-0012).

## 1. Current resolver behavior (`compiler/resolver.py`)

Two passes over the same `DiagnosticEngine`:

**Pass 1 (`_collect_globals`)**: scans **only the top-level statement
list** (`self.program.statements`, not recursively into any block) for:
`Decl` (registers `name -> type`, `E3003` if type unknown, `E4002` if
already declared), `Assign` with no existing type (infers a type only if
every value is a `Literal` and they all share one type — a mixed-literal
list is left untyped, not an error), and `ActionDecl` (registers the
signature, `E4002` if the name is already an action; also duplicate-checks
parameters here, see §6).

**Pass 2 (`_resolve_block`/`_resolve_stmt`/`_resolve_expr`/
`_resolve_condition`)**: walks the whole tree checking that every name
used is `scope.defined()`. `Scope` is a set of names plus a parent
pointer; `defined()` walks the parent chain.

## 2. Scope semantics — the actual model, not an assumption

There is **one persistent scope for the whole program** (`root`, built
once in `run()`), used for essentially everything. Nothing in the
resolver creates a *lasting* child scope. Two constructs create a
**temporary** scope-like effect and then undo it:

- `RepeatStmt`: adds `Index` to the current scope's own `names` set
  (not a child!), resolves the body against that same scope, then
  removes `Index` again **only if it wasn't already there** (so a nested
  `Repeat` inside another `Repeat` doesn't clobber the outer `Index`'s
  visibility once the inner one finishes).
- `ActionDecl`: same pattern, for each parameter name.

**Everything else assigned inside an `If`/`Repeat`/`While`/`Action` body —
via `Assign`, `CompareStmt`, etc. — registers in that same single
persistent scope and is visible afterward, and visible to sibling
constructs (a different `Action`, code after a loop), for the rest of the
program.** This is not an approximation of lexical scoping; it is the
actual, current, correct-relative-to-the-interpreter model, arrived at
via two real bugs (documented in `ed26e66` and the "Stage 6 completion
(part 2)" commit) where an earlier version used a *child* scope for an
entire body and produced false "undefined variable" errors for code that
ran fine, because the interpreter's storage is flat
(`docs/architecture/current-state.md` section 7 — every STORE-shaped
instruction targets one global `env` dict, with Action parameters as the
only real per-call overlay, via `Interpreter.frames`).

**Conclusion for Stage 7**: the self-hosted resolver's scope model should
be exactly this — one flat symbol table, plus two *narrow, temporary*
exceptions (`Index` during a `Repeat` body, each parameter during its
`Action`'s body) that are added before resolving the body and removed
after, only if not already present. This is materially simpler than a
general nested-scope-tree, and matching it exactly is what avoids a third
occurrence of the same bug class (ADR-0012 §"Decision").

## 3. Verified findings (confirmed by compiling, not just reading)

**3a. A `Decl` nested inside any block is semantically inert.** Pass 1
only scans top-level statements, and pass 2's handling of `Decl` is
`return` — a no-op. A nested `Age is Integers;` inside an `If` body
neither defines `Age` in scope nor records its type; the name only
becomes usable if something else (typically an `Assign`) defines it too.
Verified:
```kuro
If 1 is equal to 1;
Age is Integers;
Take user Age;      # error[E4001]: input variable 'Age' must be declared first
Print Age.           # error[E4001]: undefined value 'Age'
Done.
```
And its declared type is never enforced either — `Score is Integers;
Score = "oops";` nested inside an `If` compiles without a type error,
because `Score` was never added to `symbols.types`.

**3b. An `Action` declared inside any block is parsed and its body is
resolved, but the action itself is never callable.** Pass 1's action-
signature collection is also top-level-only; pass 2 still walks into a
nested `ActionDecl`'s body (checking it for undefined variables etc.),
but nothing ever adds it to `symbols.actions`. Verified:
```kuro
If 1 is equal to 1;
Action Nested A;
Return A;
Done.
Done.
Call Nested 5;   # error[E4003]: unknown action 'Nested'
```

**Addendum, found later in Stage 7 while differentially testing
`self_host/resolver.kuro`**: a nested `Action` with no `Call` site (just
the `If Action Nested ...; Done. Done.` part, no attempt to call it) used
to **crash the Python compiler entirely** — `compiler/lower.py`'s
`Lowering._lower_stmt` had no case for a nested `ActionDecl` (only
top-level ones are filtered out of `main` and lowered separately) and hit
its final `raise AssertionError(f"unhandled statement {st!r}")`. Fixed:
a nested `ActionDecl` now lowers to nothing (matching that it's already
established as inert/uncallable — there's nothing to execute or to make
callable). This was a real, previously-undiscovered "must not crash"
violation on syntactically valid, resolvable input, not a semantic change
— the program still can't call the nested action, it just no longer
crashes the whole compiler while failing to.

**3c. The resolver's own duplicate-parameter check (`E2005` in
`_collect_globals`) is dead code in practice.** `compiler/parser.py`'s
`_param_list` already calls `_check_duplicate_params` unconditionally for
every `Action`, regardless of nesting, at parse time — and
`compiler/pipeline.py::compile_source` returns immediately after parsing
if `diags.has_errors()`, before `resolve()` ever runs. Since it is
structurally impossible to produce an `ActionDecl` AST node with
duplicate parameters without going through parsing (which always flags
it first), the resolver's copy of this check can never fire through the
normal pipeline. Verified by checking a top-level duplicate-parameter
program reports exactly one `E2005`, not two.

**Decision for all three**: replicate exactly (§"Golden Rule" — these are
existing behaviors, not superseded by a spec change), and record them as
named, intentional bootstrap limitations rather than silently "fixing"
them while porting. See ADR-0012.

## 4. Current typechecker behavior (`compiler/typecheck.py`)

Only **three** statement kinds get an actual type check:
`Assign` (`E3001` if an inferred value type is present and incompatible
with a declared type), `AddStmt` (`E3002` if the declared target type
isn't numeric), `SetStmt` (`E3004` if the declared target is `Text` and
the value being set isn't `Text`). Every other statement — `Compare`,
`If`/`While` conditions, `Repeat`'s count, `Call` arguments, `Return`
values, `Get`/`Length`/`Append` — is **not type-checked at all**; the
generic `_child_blocks` walk only recurses into nested bodies, it does
not add any check.

`_infer(expr)` returns a type name or `None` ("unknown, don't check
further" — Python's `None`, not a Kuro value): `Literal` → its type;
`VarRef` → `symbols.types.get(name)` (which is `None` for anything only
ever assigned inside a nested block, per §3a's consequence — nested-only
variables are simply never type-checked, gracefully, not an error);
`BinaryExpr` → numeric-only (`Integers`/`Decimals`, with `Decimals`
"infectious" when mixed with `Integers`) — **`Text + Text` (string
concatenation, which the interpreter genuinely supports —
`compiler/interpreter.py::_binop`) is not recognized here at all** and
silently falls through to `None`, meaning `Name = "a" + "b";` on an
already-`Text`-declared `Name` is never actually checked against that
declaration. This is a real, narrow gap worth closing (ADR-0013), not
because the current typechecker is "wrong" exactly, but because it's
recognizably incomplete relative to what the interpreter actually
executes, in a way that's easy to fix without changing anything else.

`compatible(declared, actual)`: exact match, or the one documented
widening, `Integers -> Decimals`.

## 5. Base types (current, not future roadmap)

Four: `Integers`, `Decimals`, `Text`, `Symbols`. No `Boolean` exists as
a separate name — `Symbols` already serves that role (`CompareStmt`
always types its result variable as `Symbols`; `type_of_literal` maps
Python `bool` to `"Symbols"` too). Collections have **no distinct type
representation** — a list is typed by its element type, the exact same
name a scalar of that type would use (`Names = "A","B","C";` and
`Name = "A";` are both recorded as declared type `Text`). This means
"is this variable a collection or a scalar" is **not answerable from the
type system alone** — a real, current representational limit worth
naming explicitly (§9) rather than working around by inventing a
`List<T>` wrapper type, which would be exactly the kind of premature
generics/collection-type work spec section 15/31's "keep Stage 7
focused" rules out.

## 6. Duplicate definitions — full picture

- Duplicate top-level `Decl`: `E4002`, resolver pass 1.
- Duplicate top-level `Action` name: `E4002`, resolver pass 1.
- Duplicate `Action` parameter: `E2005`, **parser** (`compiler/parser.py`
  `_check_duplicate_params`), for every `Action` regardless of nesting —
  this is the actually-reachable check; see §3c for why the resolver's
  own copy never fires.
- Re-`Assign`ing an existing name is **not** an error at any level — this
  is how ordinary reassignment works, not a bug.

## 7. Undefined symbols

Every use-site check reports `E4001` with a description naming the kind of
use (`"undefined value"`, `"undefined variable"`, `"undefined target"`,
`"input variable ... must be declared first"`) — same code, different
wording depending on statement context. `@_`/bare `_` is always treated
as defined (§8) and never reported undefined.

Critically: **there is no silent bare-word fallback** in `compiler/`
(unlike the bootstrap `kuro.py`, see `docs/architecture/current-state.md`
section 6, deliberately not carried forward per ADR — ground already
covered, restated here because section 12 of this session's task
explicitly calls it out as something not to reintroduce). An undefined
name is always a diagnostic, never silently treated as a literal.

## 8. Builtins and pseudo-variables (current, informal — no registry exists)

There is currently no centralized builtin/keyword registry in
`compiler/`; statement keywords are recognized positionally by the parser
(`compiler/parser.py`'s `isw("Print")` etc. — see `compiler/tokens.py`'s
comment: keywords are not reserved tokens). The resolver has two
hardcoded special names:

- `Index`: only defined while resolving a `Repeat` body (§2); referencing
  it outside one is `E4001`.
- `_` (written `@_`): always treated as defined, everywhere, never
  reported undefined, regardless of whether anything has actually run yet
  to populate it (a purely static allowance — see `_resolve_expr`'s
  explicit `if e.name == "_": return`). At runtime, reading it before
  anything sets it resolves to `None` (`Interpreter._read`'s `_` special
  case), which is not itself a Kuro value any expression could legally
  hold otherwise — a latent inconsistency between "statically always
  valid" and "may not have a meaningful runtime value yet," documented
  here rather than hidden (ADR-0012 §"Known limitations").

Stage 7 should build the builtin/pseudo-variable registry the task asks
for (§13) as new, explicit infrastructure — it doesn't exist to "port,"
it needs to be designed fresh, informed by this list.

## 9. Known bootstrap/current limitations (full list, for Stage 7 to either replicate or explicitly not fix)

1. Nested `Decl` is inert (§3a).
2. Nested `Action` is uncallable (§3b).
3. The resolver's own `E2005` check never fires in practice (§3c) — only
   the parser's copy is reachable.
4. `Text + Text` is invisible to `_infer` (§4) — **this one is being
   closed in Stage 7**, via the Golden Rule's change process (ADR-0013),
   not silently.
5. No type distinguishes a collection from a scalar of the same element
   type (§5).
6. Comparisons, logical `and`/`or`, `Repeat`'s count, `Call` arguments,
   `Return` values, and most builtins have no static type checking at all
   today (§4) — Stage 7 adds a bounded, explicitly-scoped set of new
   checks here (ADR-0013), not exhaustive coverage of every conceivable
   combination.
7. `Return` has no declared-return-type concept — Actions aren't
   statically typed for what they return, because there is no syntax to
   declare it. "Wrong return type" checking (raised as a test case in the
   task prompt) is not implementable without inventing new syntax, which
   is out of scope for Stage 7 (spec section 15's "keep Stage 7 focused";
   no future-type work is required here). Documented, not silently
   dropped.
8. `@_` is always statically valid but may hold a meaningless runtime
   `None` before anything has run (§8).
