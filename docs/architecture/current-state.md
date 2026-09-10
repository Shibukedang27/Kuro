# Kuro Architecture Audit — Current State (Stage 0)

Date: 2026-09-10
Author: Compiler engineering session (Claude Code)
Scope: `bootstrap/python/kuro.py`, the only implementation found prior to this session.

## 1. What exists

A single 425-line Python 3 file, `kuro.py`, implementing lexer, parser, a tree-walking
semantic checker, and an interpreter ("Engine") in one process. No build system, no
package metadata, no git history. It was found at `~/Downloads/kuro_v0.4_stage4`
(not inside any repository) and has been copied verbatim into `bootstrap/python/`
in this repository as frozen reference infrastructure — see Compatibility Policy
(spec §52): it is not being deleted, only superseded.

`bootstrap/python/TEST_REPORT.txt` claims "Regression tests: 16/16 PASS". Verified
in this session: `bootstrap/python/tests/*.kuro` contains 16 `.kuro` files; running
each through `kuro.py` reproduces that count, all exiting with the expected 0/1
status for positive/negative cases. Golden output for every existing test file was
captured in this session (`bootstrap_golden_raw.txt` in the working scratchpad)
before any code was changed, so the new implementation can be checked against the
old one byte-for-byte during migration.

## 2. Pipeline (as implemented)

```
source text -> strip_comments (per line) -> lex() -> list[Tok]
            -> Parser (recursive descent, hand-rolled) -> list[Stmt] (AST via @dataclass)
            -> Engine.semantic() (single pass, mutates self.types/self.actions)
            -> Engine.exec() (tree-walking evaluator over the AST directly)
```

There is no separate IR: `Engine.emit()` appends human-readable strings (e.g.
`"STORE Name"`) to `self.ir` purely for the `KURO IR v0.4` trailer printed at the
end of a run. It is not consumed by anything — it is a debug log, not an
intermediate representation in the compiler sense.

## 3. Lexical structure (observed, not previously specified)

- Line-oriented: comments are stripped per physical line before tokenizing
  (`#...` and `//...`, respecting `"..."` string boundaries). No block comments.
- Token kinds: `STRING`, `NUMBER` (int or float, decided by presence of `.`),
  `WORD` (identifier or keyword — keywords are not reserved, they are just words
  the parser recognizes positionally), single-char punctuation
  `= , ; . ( ) @`, and `EOF`.
- String escapes: `\n \t \r \" \\`; unknown escape passes the following character
  through unchanged (not an error).
- No block/multi-line strings, no unicode-identifier policy defined, no numeric
  literal forms beyond `[0-9]+(\.[0-9]+)?` (no exponents, no separators, no hex).
- Source spans: `Tok` carries `line`/`col`, but column is a byte offset into the
  *comment-stripped* line, not the original line — a diagnostic pointing at a
  column after a stripped trailing comment would be correct, but there is no
  span *length*, only a start point. Errors report `line:col` only.

## 4. Grammar (observed)

Statement forms, all hand-matched by keyword peeking in `Parser.stmt()`:

| Form | Terminator |
|---|---|
| `Name is Type;` (declaration) | `;` |
| `Name = v1, v2, ...;` (assignment) | `;` |
| `Take [user] N1 [and N2 ...];` (input) | `;` |
| `Print v.` | `.` |
| `Add v to N;` | `;` |
| `Update N to v;` | `;` |
| `Get N [idx];` | `;` |
| `Length N;` | `;` |
| `Set N idx to v;` | `;` |
| `Compare Name L op R;` | `;` |
| `If L is op R; ... [Else; ...] Done.` | block, `Done.` |
| `Repeat n; ... Done.` | block, `Done.` |
| `Action Name(a, b, ...); ... Done.` | block, `Done.` — **requires parentheses**, unlike the target spec's paren-less examples (`Action AddNumbers A, B;`). This is a real divergence between the informal spec and the implementation, flagged and resolved this session (ADR-0002): paren-less becomes canonical, parens remain accepted for compatibility. |
| `Return v;` | `;` |
| `Call Name(a, b, ...);` | `;` — same parenthesization note as `Action`. |
| `Entered N is op R then Print v otherwise Print v;` (legacy one-line conditional) | `;` |

Values (`Parser.value()`) are only: string/number literals, `@name` (explicit
variable reference), or a bare `WORD` (either a variable reference or, if
unresolved at runtime, the literal word itself — see §6). **There is no
expression grammar**: no binary operators, no arithmetic beyond the `Add v to N`
statement, no boolean combinators, no parenthesized sub-expressions. The spec's
own example `Return A + B;` (§10) does not parse against the current grammar.

Comparison operators (`Parser.op()`) are word phrases: `greater than`,
`less than`, `equal to` / `equals to`, `not equal to`. No `>=`/`<=` equivalent
exists.

## 5. Type system (observed)

Four nominal base types: `Integers`, `Decimals`, `Text`, `Symbols`. Inference:
- `Decl` (`Name is Type;`) declares a type up front.
- A bare `Assign` with no prior `Decl` infers a type from the literal(s) on the
  right if all listed values share one Python-level type
  (`Engine.semantic()`); a mixed-literal list is left untyped (no error raised —
  a silent gap, not a designed feature).
- `compatible()` allows `Integers -> Decimals` widening only; everything else
  must match exactly. There is no explicit conversion syntax at all currently
  (the spec's `Age = Integer("25");` form does not exist).
- `Symbols` is used as the return type of `Compare` (i.e. it is Kuro's boolean).
  Python `bool` values are classified as `Symbols` by `type_of()`.
- Lists are typed by their first element (`type_of(x[0])`); heterogeneous lists
  are not rejected at construction, only at the point a `Set`/`Assign` would
  violate the declared element type — and even then only for variables that
  went through an explicit `Decl`.

## 6. Semantics/name resolution (observed)

`Engine.semantic()` and `Engine.sem()` are a single combined pass doing name
collection, "declared before use" checking (`checkval`), and the type rules
above, all together, walking the AST once. There is no symbol-table/scope
object — `self.types` (a flat dict) is the only symbol table, and it is
**global**: `Action` parameters are checked as a `locals_` set threaded through
recursive calls, but there is no per-scope shadowing model, and nested blocks
(`If`/`Repeat` bodies) do not get their own scope — they share the enclosing
one. `Index` (the Repeat loop variable) is injected into the `locals_` set
textually rather than modeled as a real binding.

`resolve()` (used at execution time, not semantic time) has a **silent
fallback**: an unresolved bare `word` value resolves to its own string image
rather than erroring, e.g. a genuinely undefined bare word in a position the
semantic pass didn't check will print itself as a string instead of raising —
this is a real bug class inherited from treating "declared before use" checking
and "evaluation" as two separate mechanisms that don't fully agree (see
`checkval` vs `resolve`).

## 7. Runtime (observed)

`Engine.exec()`/`exec1()` walk the AST directly (no IR execution). State is a
single flat `self.env` dict for all variables (again, no lexical scoping —
`Action` locals are passed as a separate `locals_` dict per call, shadowing
`self.env` lookups inside `resolve()`, but a called `Action` can still read
and mutate the *global* `self.env` directly, e.g. `Update` inside an `Action`
body writes to `self.env`, not to `locals_`). Recursion works only by accident
(each `Call` gets a fresh `locals_` dict, but shares the single mutable
`self.env`), and there is no call-stack depth guard — infinite/deep recursion
will hit Python's native `RecursionError`, which is not caught, so it currently
crashes uncontrolled rather than raising a `KuroError` (a real robustness gap:
violates spec §33's "must not crash on malformed/adversarial input", although
recursion depth is a runtime rather than parse-time case).

`@_` / bare `_`: implemented as `self.env["_"]`, set by `Get`, `Length`, and
`Call` — matches the spec's `@_` "most recent result" concept, though `Get`
and `Length` also unconditionally `print()` their value even when not asked to
(that print is not requested by any syntax in the spec — it looks like a
debug convenience baked into the reference implementation, not a designed
statement in the language, and is not carried forward).

## 8. Diagnostics (observed)

Four flat exception classes (`KuroLexError/ParseError/SemanticError/RuntimeError`),
each just `Exception` with a formatted string message; no error codes, no
severity levels, no secondary/related spans, no hints, and no error recovery —
the first error anywhere aborts the entire run. `main()` catches `KuroError`
and prints `KURO ERROR: <msg>` to stderr with exit code 1; anything else
(e.g. an uncaught `RecursionError`, or a Python `KeyError` from a missing
`self.env` lookup that no semantic check happened to catch) propagates as a
raw Python traceback to the user.

## 9. What does not exist yet (honest inventory, not a roadmap)

Modules system, package manager, standard library, LSP, formatter, linter,
REPL, debugger, profiler, any IR beyond a debug-print log, any backend beyond
this single tree-walking evaluator, memory-management design, concurrency,
generics, records/enums/Optional/Result, closures, and self-hosting. None of
these are stubbed in this repository; per spec §55/§53, nothing here claims
to exist until it is real.

## 10. Immediate consequences for this session's plan

1. `bootstrap/python/kuro.py` is preserved unmodified as the bootstrap
   reference and its golden test outputs, and remains the correctness oracle
   for the new implementation during migration (`tests/regression/`).
2. The new implementation lives in `compiler/` as a proper multi-module
   Python package (lexer/parser/AST/diagnostics/resolver/typecheck/IR/
   interpreter as separate files — spec §19–22), not a rewrite-in-place of
   `kuro.py`.
3. Known bugs/gaps identified above (silent bare-word fallback, uncaught
   recursion, `Get`/`Length` auto-print, missing scoping) are **not** carried
   into the new implementation; each such decision is recorded as an ADR in
   `docs/engineering/`.
4. The paren-less `Action`/`Call` grammar becomes canonical (ADR-0002); the
   parenthesized form remains valid input for compatibility, per spec §52.
