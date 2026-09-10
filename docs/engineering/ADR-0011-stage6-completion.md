# ADR-0011: Stage 6 completion — deferred statements, and self-hosted diagnostics

## Problem

Stage 6 (ADR-0010) shipped a self-hosted parser covering a deliberately
bounded subset of the grammar — 11 of 17 statement kinds, no self-hosted
diagnostics. This ADR covers finishing it: the remaining 7 statement forms
(`Take`, `Get`, `Length`, `Set`, `Append`, `Compare`, legacy `Entered`) and
a real diagnostic system, so the self-hosted frontend reaches functional
parity with `compiler/`'s Python frontend for the entire currently-
supported grammar.

## Audit findings (Phase 1)

Documented in full in `docs/spec/grammar-coverage.md`; the short version:
every Python-side phase (resolver, typecheck, lower, interpreter,
`ast_canon`) already had complete coverage of all 17 statement kinds
before this session — the gap was entirely in `self_host/parser.kuro` and
the total absence of self-hosted diagnostics. No other phase mismatch was
found. A parse-order audit (the same discipline ADR-0010's Decision 4
established for `ADD`/`APPEND`) confirmed `compiler/ast_canon.py` needed
no encoding changes for any of the 7 remaining statements — they were
already implemented there, just never exercised by the self-hosted side.

## Deferred statements (Phase 2-4)

Implemented following `compiler/parser.py`'s exact grammar — not a second
interpretation. Two things worth calling out specifically:

- `Get`'s direct-vs-indexed distinction (`Get N;` vs `Get N idx;`) is
  preserved by checking whether the token right after the target name is
  `;` (matching `compiler/parser.py`'s `idx = None if ... SEMI else
  self.expr()`), encoded as the same `"0"`/`"1"` flag `compiler/ast_canon.py`
  already used.
- Legacy `Entered`'s left operand is a **bare identifier only**
  (`compiler/parser.py` calls `self.ident()`, never `self.expr()`, for
  that position) — the self-hosted parser replicates this exact
  restriction rather than a more permissive reading of the informal
  syntax, and desugars to the identical canonical `IF` encoding a real
  `If`/`Else` would produce (verified by
  `tests/parser/test_ast_canon.py::test_entered_legacy_desugars_to_if_encoding`
  asserting byte-for-byte equality between the two forms' canonical
  output).

35 new differential/combination tests (`tests/self_host/test_parser_cross.py`)
all passed the first time these were run — the careful parse-order audit
paid off, unlike ADR-0010's first implementation attempt.

## Bug found: unvalidated identifier consumption (Phase 5)

Malformed-input testing (`Action Add A, ,;`) found a real gap: many places
read `CurValue` and unconditionally consumed it as an identifier without
checking the token was actually `IDENT` — so a stray comma silently became
a parameter name instead of failing, unlike `compiler/parser.py`'s
`ident()`, which checks token kind first. Fixed by adding `ExpectIdent`
(the same shape as `ExpectKind`/`ExpectWord`) and auditing every "read a
name" call site in the file to use it. 29 malformed-input cases across
every category the task specified (missing semicolon/period/Done,
unexpected Done/Else/EOF, incomplete forms of all 7 new statements,
malformed expression/Action/Call/nested-block) all confirmed to fail
cleanly with no hang and no crash.

## Bug found: `ActionDecl`'s resolver scoping (found building diagnostics)

While wiring up diagnostics (`ComputeLineCol` sets globals `DiagCurLine`/
`DiagCurCol`; a *different* Action, `RecordDiag`, reads them), type
checking failed with a false "undefined value" — the exact same bug class
already fixed for `RepeatStmt` (the "Fix resolver" commit between Stage 5
and Stage 6): `compiler/resolver.py`'s `ActionDecl` handling used a full
child scope for the entire body, so an ordinary (non-parameter) `Assign`
inside one Action's body was invisible to resolution both after the
`ActionDecl` and inside a *different* Action, even though the
interpreter's storage is flat and it runs fine (every STORE-shaped
instruction targets the global env regardless of which Action, if any, is
currently executing — `docs/architecture/current-state.md` section 7).
Fixed with the identical pattern used for `Index`: only parameters are
genuinely scoped to the call (and must not leak — verified by the existing
`test_action_locals_do_not_leak`), while ordinary `Assign`s share the
enclosing scope. Two new regression tests
(`test_ordinary_variable_assigned_inside_action_is_visible_after_it`,
`test_variable_assigned_in_one_action_visible_in_another`) lock this in.

This is now the *second* time building genuinely nontrivial self-hosted
Kuro exposed a resolver bug in exactly this scoping-shape (Repeat, then
Action) that no earlier test happened to exercise. Worth naming as a
pattern: any future Kuro statement with a per-invocation binding (a loop
variable, a call parameter) needs this same audit — does the resolver
scope *only* the binding itself, or does it accidentally trap ordinary
assignments inside the same child scope too?

## Diagnostic architecture (Phase 6)

**Data model**: four parallel lists — `DiagCodes`/`DiagLines`/`DiagCols`/
`DiagMessages` — appended to together by one helper, `RecordDiag(Code,
Message)`, mirroring the `TokenKinds`/`TokenValues` shape `self_host/
lexer.kuro` already established. No new Kuro capability was needed to
store them: `Append` already works on any value type, so `DiagLines`/
`DiagCols` hold plain Integers directly, never rendered to text.

**Source locations**: `self_host/lexer.kuro` was extended (third additive
extension after `TokenKinds`/`TokenValues`) with `TokenStarts` — each
token's starting character offset into `Source`, captured once per token
at a single point (right after the current character is read, before any
branch consumes it — `Pos` provably doesn't move again until some branch
decides to consume characters, so one capture point is correct for all 16
token kinds). `self_host/parser.kuro`'s `ComputeLineCol` converts an
offset to line:col on demand by scanning `Source` for `"\n"` — an O(n)
scan per diagnostic, the same complexity trade-off ADR-0008 already
accepted for the lexer itself (correct, not fast). This directly
supersedes ADR-0008's stated limitation ("no source locations — would
need integer-to-text conversion"): that conversion was never actually
required, because a diagnostic's line/col only needs to be *stored*, not
*printed*, by the Kuro program itself.

**Codes**: every `RecordDiag` call site reuses `compiler/diagnostics.py`'s
existing E2xxx family (`E2001` unexpected token/expected identifier,
`E2002` expected a specific token or keyword, `E2003` expected a value,
`E2004` expected a comparison operator) — not a second taxonomy, per the
task's explicit instruction. `E2005` (duplicate Action parameter) is not
implemented on the self-hosted side — a known, named gap (see "Known
limitations" below), not silently missing.

## Diagnostic compatibility policy

Message *text* is not required to match `compiler/parser.py`'s wording
byte-for-byte, and does not in practice (e.g. Python's `E2002` messages
name the exact expected token; the self-hosted version's are close but
independently worded). What's compared, and tested
(`tests/self_host/test_parser_diagnostics.py`), is:

- **Error code** — from the same registry, always.
- **Category** — the same situation (missing token, unexpected token,
  malformed expression, ...) produces a code from the same family on both
  sides.
- **Source location** — line and column must correspond to the actual
  source, verified across multiple lines/columns in the test suite, not
  just at the start of a file.

Message text is allowed to differ because the self-hosted parser's error
*recovery* is intentionally less precise than the Python parser's (see
below), so the two sides don't always fail at the exact same point for
the exact same reason on every input — comparing codes and locations is
the meaningful, stable thing to check.

## Error recovery (Phase 7)

Deliberately minimal, matching the task's stated bar exactly: no crash, no
hang, a useful structured diagnostic. `ParseFailed` remains the circuit
breaker introduced in ADR-0010 — once any check fails, `RecordDiag` sets
it, and block-parsing loops stop cleanly rather than continuing to spray
diagnostics for a source region that's already known to be broken. This
means a single malformed construct can still produce a short cascade of 2-3
diagnostics (the first real failure, then one or two follow-on "expected
X, found (whatever the parser was stuck on)" reports) rather than exactly
one — bounded, not perfectly deduplicated. `compiler/parser.py`'s
`_synchronize`-based recovery (skip to the next plausible statement
boundary and keep parsing) is *not* replicated here; that remains real
future work, named rather than silently absent.

## Known limitations

- No self-hosted duplicate-Action-parameter check (`E2005`) — not in the
  task's minimum diagnostic category list, and not added speculatively.
- No self-hosted token-level error recovery/synchronization — `ParseFailed`
  stops the current block cleanly but does not attempt to resume parsing
  after a malformed construct the way `compiler/parser.py` does.
- Message text is intentionally not required to match Python's; see the
  compatibility policy above.

## Compatibility impact

None on the language: no grammar changes, no new syntax. Both lexer
extensions (`TokenStarts`) and the resolver fix are strictly corrective/
additive — every prior test (Stage 0-6, 294 total before this ADR's own
new tests) continues to pass, and the Stage 5 lexer cross-tests were
re-run unmodified to confirm `TokenStarts` didn't change any existing
`Print` output.

## Testing strategy

- `tests/parser/test_ast_canon.py`: 20 tests covering the previously-
  Python-only-exercised statement encodings (`Take`/`Get`/`Length`/`Set`/
  `Compare`/`Entered`).
- `tests/self_host/test_parser_cross.py`: 15 dedicated fixtures for the
  new constructs, 8 realistic combinations (not just isolated grammar
  rules), 29 malformed-input cases across every required category.
- `tests/self_host/test_parser_diagnostics.py`: 15 tests — every required
  diagnostic category, source-location correctness across multiple
  lines/columns (not just line 1), and a check that every emitted code
  actually exists in `compiler/diagnostics.py`'s registry.
- `tests/semantic/test_semantic.py`: 2 new regression tests for the
  `ActionDecl` resolver fix.
