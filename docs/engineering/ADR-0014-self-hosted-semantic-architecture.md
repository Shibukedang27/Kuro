# ADR-0014: Self-hosted semantic architecture — why the resolver re-scans tokens instead of walking AstOut

## Problem

The target pipeline (this session's task, §1) is `... → Kuro Parser →
Kuro AST → Kuro Resolver → Kuro Typechecker → ...`, suggesting the
resolver should consume the parser's AST output. Stage 6 already produces
exactly one artifact that could serve as "the AST": `AstOut`, the flat
canonical token stream `self_host/parser.kuro` builds (`compiler/
ast_canon.py` defines its encoding). Before writing any resolver code,
whether the resolver can actually *walk `AstOut` back into structure* had
to be checked directly — not assumed just because it worked for Stage 6's
own purpose (byte-for-byte comparison against the Python side).

## Finding: `AstOut` is not walkable for expressions, by construction

Traced concretely, not assumed. Compare the encodings of two different
programs:

- `Names = A, B*C;` (**two** comma-separated values: `A`, and `B*C`) →
  `VAR 0 A` + `VAR 0 B VAR 0 C BIN *` = `VAR 0 A VAR 0 B VAR 0 C BIN *`
- `Names = A+(B*C);` (**one** value: `A+(B*C)`) →
  `VAR 0 A VAR 0 B VAR 0 C BIN *` + `BIN +` = `VAR 0 A VAR 0 B VAR 0 C BIN * BIN +`

The first six tokens are **identical** in both. The only difference is
whether a trailing `BIN +` follows — and a walker positioned right after
those first six tokens cannot tell, from local content or fixed-width
lookahead, whether it has just finished one complete value (case 1) or is
midway through building a longer one that a later reducer tag will still
fold together (case 2). This is not a corner case: postfix (RPN) notation
is only unambiguous to a *producer* that already knows the tree shape
(which is how `compiler/ast_canon.py` — walking real Python objects — and
`self_host/parser.kuro` — walking tokens via real precedence climbing —
both avoid the problem, by construction). A *consumer* trying to
reconstruct structure from the flat stream alone, with no further
information, provably cannot, because the encoding was never designed to
be self-delimiting at the sub-expression level (ADR-0010's Decision 2 only
guarantees this for statement-level constructs, which are prefix-tagged
and count/end-marker delimited — not for the postfix expression/condition
nodes ADR-0010's Decision 4 introduced for entirely different reasons).

Two ways out were considered and rejected:

- **Change the encoding** to be walkable (e.g. an explicit end marker per
  expression). Rejected: it would require touching `compiler/ast_canon.py`
  and `self_host/parser.kuro`, both stable and differentially verified —
  exactly the "do NOT rewrite working lexer/parser code" this session was
  told to avoid, for a problem that has a clean alternative.
- **Guess using heuristics** (lookahead, precedence tables reconstructed
  from tag sequences). Rejected outright: any such heuristic is a second,
  independent definition of Kuro's expression grammar that could silently
  drift from the parser's real one — precisely the "don't let Python and
  Kuro quietly diverge" failure mode this stage exists to prevent, just
  self-inflicted instead of cross-language.

## Decision: the resolver and typechecker re-scan the token stream directly

Neither `self_host/resolver.kuro` nor `self_host/typecheck.kuro` reads
`AstOut`. Both operate on `TokenKinds`/`TokenValues`/`TokenStarts` — the
same arrays the parser already reads — using their own cursor
(`SemPos`), independently re-implementing the relevant parts of the
grammar (expression precedence climbing, statement dispatch, condition
parsing) that `self_host/parser.kuro` already implements once for
building `AstOut`. `AstOut` remains exactly what Stage 6 needed it for —
a byte-for-byte comparable serialization for differential testing against
the Python parser's real AST — and is simply not the resolver's input.

This is real, acknowledged duplication (spec section 31 anticipates
exactly this: "if something is difficult because of ... no proper local
variables ... document the limitation and design around it cleanly").
Kuro has no closures or function values, so there is no way to write one
shared "walk the grammar" routine parameterized by different actions
(emit an AST tag vs. resolve a name vs. check a type) the way a visitor
pattern would in a language with first-class functions. Three consumers
of the same grammar (parser, resolver, typechecker) mean three
independent implementations of recognizing it. This is named here as a
concrete, load-bearing consequence of Kuro's current language, not a
design preference.

## Decision: two Kuro-side passes, not three

Python keeps name resolution and type checking as genuinely separate
passes (`compiler/resolver.py` then `compiler/typecheck.py`), each its
own full tree walk. Given the cost just established — every full grammar
walk is a substantial, independent piece of code — Stage 7 combines what
would be Python's *second* resolver pass (usage checking) and the
typechecker into **one** self-hosted pass, in `self_host/typecheck.kuro`:
as each name-use is encountered, it is checked for definedness (the
resolution question) *and* its type is computed and validated in the same
walk (the type question). `self_host/resolver.kuro` remains the *first*
pass only — top-level collection (§ below) — matching Python's own
`_collect_globals` almost exactly, because that part is cheap and doesn't
need full expression understanding at all.

This changes internal pass structure, not observable behavior: nothing
about *which* diagnostics fire, for *which* programs, changes — only
whether "is X defined" and "what type is X" are answered in the same
walk or two consecutive ones. Differential testing compares final
diagnostics and symbol results, which is unaffected. Documented here per
spec section 30's explicit allowance ("if the implementation must
temporarily use one combined file [or pass], that is acceptable — document
the limitation").

## Resolver pass 1: lightweight, not a second full parser

Python's `_collect_globals` only needs to recognize three shapes at the
top level — `Decl`, `Assign` (inferring a type only when every value is a
literal), `ActionDecl` (name + arity) — and, for everything else, skip
past it without understanding its internals at all (§2 of the semantics
audit already established pass 1 never looks inside nested blocks).
`self_host/resolver.kuro`'s pass 1 exploits this: statement boundaries in
Kuro's grammar are unambiguous even without understanding expressions —
no expression can contain a bare `;` or `.` token (both only ever appear
as statement/block terminators; a decimal literal's `.` is lexed as part
of the `DECIMAL` token, not a separate `DOT`), so a leaf statement can be
skipped by scanning to the next `;`/`.` without knowing anything about
what's between. A block-opening statement (`If`/`Repeat`/`While`/`Action`)
is skipped by recursively applying the same rule until a matching `Done`
`.` is found. This keeps pass 1 genuinely light — no precedence climbing,
no condition grammar — while still being precise about exactly what
Python's pass 1 is precise about.

For a `Call`'s argument *types* to be checkable later without a ragged
per-action parameter-type list (which Kuro's flat-array-only
representation makes awkward — ADR-0012's parallel-array approach doesn't
extend cleanly to "a variable number of typed fields per action"), pass 1
records only each action's name, its parameter *count*, and the **token
position** where its parameter list begins (`ActionParamPos`). When
`self_host/typecheck.kuro` needs a specific parameter's declared type at
a `Call` site, it jumps `SemPos` to that recorded position, re-scans just
that one parameter list (cheap — parameter lists are short and have no
recursive expression structure of their own), and returns to where it
was. This trades a small amount of re-scanning for avoiding a symbol-table
shape Kuro cannot represent cleanly.

## Symbol table representation

Parallel arrays, per ADR-0012: `SymNames`/`SymTypes`/`SymActive` for
variables (`SymActive` is the toggle that implements "temporarily add,
remove afterward only if not already present" for `Index` and Action
parameters — Kuro's `Append`-only lists have no real deletion, so
"removed" is represented as `SymActive[i] = 0` rather than shrinking the
list); `ActionNames`/`ActionArity`/`ActionParamPos` for actions. `Index`'s
scoping specifically uses a simpler mechanism than the general
active-flag one: an integer depth counter (`IndexDepth`, incremented
entering a `Repeat` body, decremented leaving it; `Index` is defined
exactly when `IndexDepth > 0`) — equivalent to Python's set-based
had-before tracking but simpler, because `Index` is a single name with no
per-instance identity to track, unlike parameters.

## Known simplification: parameter/global name collision edge case

Python's resolver precisely tracks, per parameter, whether a
same-named global already existed before the `Action`, restoring exactly
that prior state afterward. `self_host/typecheck.kuro` always marks a
parameter inactive again when its `Action`'s body finishes, without
checking whether a global of the same name existed first. The only
observable difference: a global variable that happens to share its name
with some *other* Action's parameter would, in the self-hosted version
only, be briefly (and incorrectly) reported as undefined immediately
after a call to that unrelated Action, in the rare case examined
specifically for this. Documented rather than silently accepted;
considered low-risk given how unlikely the name collision is in practice,
and not worth the added bookkeeping given everything else this stage
already requires.

## Diagnostic codes

Reused from the existing registry unchanged for name resolution (`E4001`,
`E4002`, `E4003`, `E4004`, `E4005`) and from ADR-0013's new type-checking
family (`E3001`, `E3002`, `E3004`, `E3006`-`E3011`). No new codes are
introduced by this ADR. `E2005` (duplicate Action parameter) is
deliberately **not** re-implemented in the self-hosted resolver, matching
the audit finding that Python's own copy of this check is dead code in
practice (`docs/architecture/self-hosted-semantics.md` §3c) — the
reachable check lives in the parser, and completing that specific gap (it
was already named as missing in ADR-0011) belongs in `self_host/
parser.kuro`, not here.

## Builtin registry

A small, explicit set of reserved statement keywords
(`Print`/`Take`/`Add`/`Update`/`Get`/`Length`/`Set`/`Append`/`Compare`)
and two special pseudo-variables (`Index`, `_`) are recognized by
dedicated equality checks in one place (`IsBuiltinKeyword`,
`IsPseudoVar`) rather than scattered string comparisons throughout the
walk — addressed directly at the two points that need to distinguish
"user symbol" from "not a real, checkable name": `_` is always treated as
defined (matching `compiler/resolver.py`'s explicit `if e.name == "_":
return` — a deliberate static allowance, not the bootstrap's silent
bare-word fallback this stage was explicitly told not to reintroduce —
see the semantics audit §7-8), and `Index` uses `IndexDepth` (above).

## Known limitation, found during adversarial testing: nesting/collection capacity

`self_host/typecheck.kuro`'s expression and value-list walkers are, like
the rest of it, real Kuro `Action` calls executed by `compiler/
interpreter.py` — which enforces its own `_MAX_CALL_DEPTH` (200,
ADR-0009's recursion guard) to turn pathological recursion into a
structured `E6005` instead of a Python stack overflow. Each *logical*
level of nesting in the *source being analyzed* costs several levels of
the self-hosted walker's *own* call depth (a single parenthesized
sub-expression passes through `TCResolveExpr` → `TCResolveTerm` →
`TCResolveFactor` → `TCResolveAtom` before recursing again), and each item
in a comma-separated value list costs one more tail-recursive call
(`TCCheckValueList`). So the self-hosted implementation has materially
*lower* practical capacity for deeply nested expressions or large
value-lists than the Python oracle, which recurses natively rather than
through an interpreted, depth-guarded call stack — found directly, not
assumed: an initial adversarial test using 60 levels of nested parens and
a 200-item collection (both realistic-looking numbers) hit `E6005` on the
self-hosted side while the equivalent would run fine in Python. Test
depths were adjusted down to what the self-hosted path can actually
handle (`tests/self_host/test_semantic_fuzz.py`), and a dedicated test
confirms the failure mode past that capacity is `E6005`, not a crash or a
hang. This is a real, load-bearing capacity difference between the two
implementations, not a bug to fix here — it will matter again once a
native/self-hosted backend removes the Python-interpreter safety net
underneath the self-hosted tools themselves (Stage 8+).

## Compatibility impact

None on the language. This ADR is entirely about how the self-hosted
implementation is internally organized; the diagnostics it produces are
required (and tested) to match the Python oracle's for the same programs.

## Testing strategy

`tests/self_host/test_resolver_cross.py` and
`tests/self_host/test_typecheck_cross.py` (or one combined file, given the
combined-pass decision above makes a hard split between "resolver-only"
and "typecheck-only" self-hosted test cases somewhat artificial) compare
a canonical semantic result — symbol resolution outcomes and diagnostic
(code, line, column) tuples — between the Python pipeline
(`resolve()`+`typecheck()`) and the self-hosted one, across valid and
invalid programs, nested scopes, actions, loops, and the legacy `Entered`
form, per this session's task requirements.
