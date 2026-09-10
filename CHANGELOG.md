# Changelog

All notable changes to Kuro are recorded here. Format loosely follows
Keep a Changelog; versioning follows spec section 38 (SemVer, pre-1.0).

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
