# Changelog

All notable changes to Kuro are recorded here. Format loosely follows
Keep a Changelog; versioning follows spec section 38 (SemVer, pre-1.0).

## [0.8.0-dev] — Stage 7: self-hosted resolver + typechecker

### Added
- `self_host/resolver.kuro` and `self_host/typecheck.kuro`: name
  resolution and type checking, written in Kuro. `docs/architecture/
  self-hosted-semantics.md` audits the Python oracle's actual behavior
  first (not assumed) - including three real findings that contradicted
  the obvious reading of the source (a nested `Decl` is semantically
  inert; a nested `Action` is parsed and checked but never callable; the
  resolver's own `E2005` check is dead code in practice, since the
  parser's copy always fires first). `ADR-0012` formalizes the scope
  model precisely (one flat scope, plus `Index`/Action-parameter as the
  only two narrow, temporary exceptions). `ADR-0013` is the Golden Rule's
  required process for a genuine semantic expansion: six new type checks
  (`E3006`-`E3011` - comparison operand compatibility, call argument
  types against typed parameters, `Repeat`'s count, `Length`'s target,
  `Get`/`Set`'s index, and closing a real gap where `Text + Text` string
  concatenation was invisible to type inference), each individually
  justified, implemented in `compiler/typecheck.py` (the Python oracle)
  first. `ADR-0014` records the key architectural finding: Stage 6's
  canonical AST text (`AstOut`) is *not* walkable back into structure for
  expressions (proven concretely - two different programs produce
  identical leading postfix token sequences, differing only in a trailing
  tag a linear walker cannot know to expect), so the self-hosted resolver
  and typechecker independently re-scan the token stream instead, and
  combine what Python keeps as two separate passes (resolver pass 2, then
  typecheck) into one, for code-size reasons specific to Kuro having no
  closures/function values to share a grammar walk.
- `compiler/semantic_canon.py`: the Stage 7 analog of `compiler/
  ast_canon.py` - a deterministic, order-independent summary of
  `resolve()` + `typecheck()`'s result, for differential comparison.
- 108 new self-hosted tests: 15 for the resolver's pass 1 alone, 44 for
  the combined pass 2 (26 valid programs across every statement kind and
  every documented scoping edge case, 18 invalid programs covering every
  E4xxx and all 9 E3xxx codes), 11 adversarial/fuzz cases (deep nesting,
  recursion, mutual recursion, large collections - no hangs, no crashes),
  13 resolver/interpreter consistency cases (a validated program must
  both compile clean AND run to the exact expected output, not just "not
  crash").

### Fixed
- A genuine, previously-undiscovered **crash** in `compiler/lower.py`: a
  nested `ActionDecl` (valid, resolvable Kuro source, already established
  as parsed-but-uncallable rather than rejected) had no case in
  `Lowering._lower_stmt` and hit its `AssertionError` fallback, crashing
  compilation entirely instead of compiling the program. Found via
  Stage 7 differential testing, not by inspection.

### Known limitation (documented, not fixed)
- The self-hosted resolver/typechecker's own recursive walk runs through
  `compiler/interpreter.py`'s call-depth guard (`E6005`, 200), so it has
  materially lower practical capacity for deeply nested expressions or
  large value-lists than the Python oracle, which recurses natively. See
  ADR-0014.

## [0.7.0-dev] — Stage 6 completion: full grammar parity + self-hosted diagnostics

### Added
- `self_host/parser.kuro` now covers the complete currently-supported
  Kuro grammar: `Take`, `Get` (direct and indexed), `Length`, `Set`,
  `Append`, `Compare`, and the legacy `Entered ... then ... otherwise
  ...;` one-liner, following `compiler/parser.py`'s exact grammar (see
  ADR-0011). `docs/spec/grammar-coverage.md` records the audit that
  confirmed no other phase (resolver/typecheck/lower/interpreter/
  ast_canon) had any remaining gap.
- Structured diagnostics for the self-hosted parser: `DiagCodes`/
  `DiagLines`/`DiagCols`/`DiagMessages`, reusing `compiler/diagnostics.py`'s
  existing E2xxx codes rather than a second taxonomy. `self_host/lexer.kuro`
  gained `TokenStarts` (each token's character offset, additive — all 23
  Stage 5 cross-tests re-verified unmodified) so the parser can compute a
  real line:col for any diagnostic by scanning `Source` on demand —
  entirely without the integer-to-text conversion ADR-0008 assumed would
  be required, since positions are stored as plain Integers, never printed.
- `ExpectIdent`, a validated identifier-consuming helper, added after
  malformed-input testing found several places blindly accepted *any*
  token as a name (`Action Add A, ,;` silently took a comma as a
  parameter). Applied at every name-reading site in the file.
- 78 new tests: 20 `ast_canon` unit tests, 15 dedicated fixtures + 8
  realistic combinations + 29 malformed-input cases for the new
  constructs (`tests/self_host/test_parser_cross.py`), 15 diagnostic tests
  covering every required category and source-location correctness across
  multiple lines/columns (`tests/self_host/test_parser_diagnostics.py`).

### Fixed
- `compiler/resolver.py`'s `ActionDecl` handling had the same scoping bug
  already fixed for `RepeatStmt`: a full child scope for the whole body
  meant an ordinary (non-parameter) variable assigned inside one Action
  was invisible to resolution afterward and to *other* Actions, even
  though the interpreter's storage is flat and it runs fine. Fixed with
  the same pattern — only parameters are scoped to the call.

## [0.6.0-dev] — Stage 6: control-flow gate + self-hosted parser

### Added
- `While <condition>; ... Done.` (ADR-0009): a condition-bounded loop,
  evaluated against Kuro's own design principles rather than added by
  default. `Break`/`Continue` were deliberately **not** added — `Action`/
  `Return` already provide multi-level unwind, and every mid-body-exit
  case folds into a `While` condition. Implemented across every compiler
  phase (AST, parser, resolver, `compiler/lower.py`'s new `LOOP_GUARD` IR
  instruction, interpreter) with a configurable max-iteration safety cap
  (`E6006`) since it's the first Kuro construct that can fail to terminate
  by construction.
- `compiler/ast_canon.py`: a canonical flat-list AST encoding, letting a
  Kuro program (which has no structs/records) prove it built the "same"
  AST as `compiler/parser.py` by producing the identical flat token
  sequence. Required two non-obvious corrections, both because an
  append-only single pass can't retroactively insert a tag before tokens
  it already emitted: binary/comparison/logical nodes had to become
  postfix (children before tag), and every variable-length list had to
  become end-marker-terminated instead of leading-count-prefixed. See
  ADR-0010.
- `self_host/parser.kuro`: Stage 6's self-hosted recursive-descent Kuro
  parser. Covers literals, variable refs, full arithmetic precedence,
  comparisons/`and`/`or`/is-class conditions, `Decl`/`Assign`/`Add`/
  `Update`/`Print`/`Return`/`Call`/`Action`/`If`-`Else`/`Repeat`/`While`.
  `Take`/`Get`/`Length`/`Set`/`Append`(statement)/`Compare`(statement)/
  legacy `Entered` are explicitly deferred, not silently missing (see
  ADR-0010's grammar-scope section). 32 differential tests
  (`tests/self_host/test_parser_cross.py`) comparing its output against
  `compiler/parser.py`'s canonical AST, all passing, plus 6 malformed-input
  cases proving it doesn't hang or crash.
- `self_host/lexer.kuro` extended additively (ADR-0010's Decision 3): it
  now also builds `TokenKinds`/`TokenValues` arrays via `Append`, so the
  parser can read tokens programmatically instead of only through its
  existing `Print` stream. Every original `Print` call, and all 23 Stage 5
  cross-tests, are unchanged.

### Fixed (real bugs, found and fixed during this stage's work, not just
new features)
- `Repeat`'s negative-count check (`E6004`) was reserved in the
  diagnostics registry but never actually wired up after the Stage 1-4
  rewrite — `Repeat -1;` silently ran zero iterations instead of erroring
  like the bootstrap engine did.
- Parser error recovery (`compiler/parser.py::_synchronize`) could
  infinite-loop: it treated `Done`/`Else` as universal synchronization
  stop points instead of only stopping on them when they belonged to the
  block actually being recovered, so an orphaned terminator one nesting
  level shallower than expected made `block()` call `stmt()` on the same
  unconsumed token forever.
- A Kuro-level design/implementation lesson, not a compiler bug: an early
  draft of `self_host/parser.kuro` used the lexer's "bounded loop plus
  flag" idiom and broke immediately, because Kuro Actions have no true
  local variables — a loop-control flag is a global, and gets clobbered by
  any *reentrant* call sharing its name (even calls to the very same
  Action, like `ParseBlock` parsing a nested block inside a block it's
  already parsing). Fixed by writing every repeated construct in the
  parser as tail recursion instead, which needs no state to survive a
  nested call at all. Full account, including why per-Action-name variable
  prefixing alone wasn't enough, in ADR-0010's Decision 4.

### Test count
- 221 passed, 0 failed: 22 lexer, 59 parser (36 from Stage 0-5 + 9 new
  `While` cases + 14 AST-canonicalizer cases), 24 semantic (+3 for
  `While`), 11 IR (+4 for `While`), 28 runtime (+9 for `While`), 22
  regression (unchanged — the full bootstrap fixture suite still passes
  byte-for-byte), 55 self-hosting cross-tests (23 Stage 5 lexer + 32
  Stage 6 parser).

## [0.5.0-dev] — Stage 0-5 rebuild

### Added
- `docs/architecture/current-state.md`: full audit of the pre-existing
  bootstrap implementation.
- `compiler/`: new modular Python compiler frontend — lexer, recursive
  descent parser, AST, structured diagnostics with error codes, name
  resolution, type checking, a flat three-address-code IR, and an IR
  interpreter (`compiler/pipeline.py` wires all of them together).
- `cli/kuro.py`: `kuro run`, `kuro check`, `kuro emit-ir`, `kuro version`.
- Language additions (each with its own ADR in `docs/engineering/`):
  arithmetic expressions (`+ - * /`, parens), `and`/`or` condition
  combinators, `>=`/`<=`-equivalent comparisons, `Append value to Target;`,
  character-class predicates (`X is digit/alpha/space/alnum/quote`), typed
  `Action` parameters (`A: Integers`), typed inline declarations
  (`Age : Integers = 25;`).
- Paren-less `Action`/`Call` syntax is now canonical; the original
  parenthesized form is still accepted (ADR-0002).
- 150 tests total: 22 lexer, 36 parser, 21 semantic, 7 IR, 19 runtime,
  22 regression (replaying all 16 original bootstrap fixtures against
  captured golden output), 23 self-hosting cross-tests. All passing.
- `self_host/lexer.kuro`: the first self-hosting milestone (Stage 5) — a
  Kuro tokenizer written in Kuro, run by `compiler/`, cross-tested token
  for token against `compiler/lexer.py` on 21 real `.kuro` fixtures plus a
  hand-written all-punctuation snippet (`tests/self_host/`). Scope and
  known limitations recorded in ADR-0008.

### Changed / Breaking
- `Get`/`Length` no longer print their result as a side effect (ADR-0007).
  Use `Print @_.` if the value needs to be shown.
- An undefined bare-word value is now a name-resolution error (`E4001`)
  instead of silently evaluating to its own text (was an undocumented
  fallback in the bootstrap interpreter, not a designed feature — see
  `docs/architecture/current-state.md` section 6).

### Preserved
- `bootstrap/python/kuro.py` is unmodified and remains the compatibility
  oracle for `tests/regression/`.
