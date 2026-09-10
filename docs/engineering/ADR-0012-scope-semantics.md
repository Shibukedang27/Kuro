# ADR-0012: Formal scope semantics for Stage 7, and the Golden Rule for porting them

## Problem

Stage 7 moves name resolution into Kuro itself. Before writing any Kuro
code, the actual scope model needed to be nailed down precisely and in
writing — not re-derived by guessing from the Python implementation, and
not "improved" while porting. Two real bugs already happened from getting
this wrong once each for `Repeat` and `Action` (see
`docs/architecture/self-hosted-semantics.md` §2); a third occurrence in
brand-new self-hosted code is the specific failure mode this ADR exists to
prevent.

## Decision: the model is one flat scope, plus two narrow temporary exceptions

There is exactly **one** persistent symbol scope for an entire program.
Two constructs modify it *temporarily* while resolving their own body,
then undo exactly that modification afterward:

- **`Repeat`**: adds `Index` to the scope if not already present; removes
  it again afterward only if it wasn't already present (so a `Repeat`
  nested inside another `Repeat` doesn't hide the outer loop's `Index`
  once the inner one's body is done).
- **`Action`**: adds each parameter name to the scope if not already
  present; removes each again afterward under the same "only if it wasn't
  already there" rule.

Every other statement that defines a name — `Assign`, `CompareStmt`'s
result variable, a top-level `Decl` — defines it in that same single
scope, permanently, regardless of what block it's nested inside. This is
not a simplification of "real" lexical scoping adopted for convenience;
it is what actually matches the interpreter's runtime storage (one flat
global environment, `docs/architecture/current-state.md` section 7), and
matching it exactly is the entire point.

## Why not a general nested-scope tree

A prior design (both for `Repeat` and, independently, for `Action`) used
a full child `Scope` object for an entire body. It looked more
"correctly lexical" and was wrong in a way that only showed up once real
self-hosted code exercised the pattern it broke: a variable assigned
inside a loop or a function body and read afterward (or, for `Action`, in
a *different* function) is something the runtime already does correctly,
so making the resolver reject it was a bug, not a stricter rule. A
general scope tree is *harder* to get right here than the flat model,
not easier — it invites re-adding exactly this bug for the next construct
that introduces a per-invocation binding (there is no third one in the
current language, but if one is ever added, this ADR is where to look
before designing its resolver handling).

## Nested `Decl`/`Action`: replicate, don't fix

Auditing the actual (not assumed) behavior found two real gaps: a `Decl`
nested inside any block is semantically inert (parses, but never defines
the name or records its type — `docs/architecture/self-hosted-semantics.md`
§3a), and an `Action` declared inside any block is resolved but never
registered as callable (§3b). Both are real, and arguably worth fixing
one day. Per the Golden Rule (below), Stage 7 does **not** fix them: it
replicates the exact current behavior in the self-hosted resolver, and
records both here as named bootstrap limitations rather than either
silently reproducing a bug nobody could point to, or silently fixing
something without going through the change process a real semantic
change requires.

## The Golden Rule, applied

Spec-adjacent guidance for this session set the actual rule: *the
self-hosted implementation must reproduce the Python compiler's actual
semantics unless the language specification explicitly changes*, with a
required process for any deliberate change (identify → determine if it's
a language change → ADR → update spec → update the Python oracle →
update the self-hosted implementation → regression tests). This ADR is
that documentation step for scope semantics: nothing about scoping
changes in Stage 7. Where the audit found the current behavior surprising
(§3a/§3b above), the choice made was explicitly "replicate, document,
defer" — not silent replication of an unexamined bug, and not a silent
fix either.

## Symbol representation for the self-hosted resolver

Kuro has no records/structs (ADR-0010's Decision 2 already established
this constraint for the AST; it applies identically here). The symbol
table is therefore parallel arrays, the same technique
`self_host/lexer.kuro`'s `TokenKinds`/`TokenValues` and
`self_host/parser.kuro`'s `AstOut` already established:
`SymNames`/`SymKinds`/`SymTypes` — one slot per known symbol, `SymKinds`
distinguishing `"Variable"`/`"Parameter"`/`"Action"` (and `"Builtin"` for
the registry — ADR-0014). Lookup is linear scan (`Repeat`/`While` over the
array checking `SymNames[i] is equal to Name`), which is the same
complexity trade-off `self_host/lexer.kuro`/`parser.kuro` already
accepted (ADR-0008: "correct, not fast; performance work is out of scope
for a self-hosting milestone") — a Kuro program's actual symbol count is
small enough that this is not a practical concern, and precedent already
exists for choosing this trade-off deliberately rather than by accident.

`Index`/parameter scoping (the two temporary exceptions above) is
implemented the same way the resolver-level bugfixes fixed them in
Python: add the name(s) before resolving the body, track whether each was
already present, remove afterward only if it wasn't.

## Compatibility impact

None on the language. This ADR documents existing behavior and commits to
preserving it; no previously-valid program's meaning changes.

## Testing strategy

`tests/self_host/test_resolver_cross.py`'s corpus specifically includes
the two "verified findings" cases (nested `Decl`, nested `Action`) as
differential tests asserting the self-hosted resolver produces the *same*
diagnostics as the Python one for them — proving replication, not just
asserting it in prose.
