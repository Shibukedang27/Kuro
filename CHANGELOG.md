# Changelog

All notable changes to Kuro are recorded here. Format loosely follows
Keep a Changelog; versioning follows spec section 38 (SemVer, pre-1.0).

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
- 124 tests across `tests/lexer`, `tests/parser`, `tests/semantic`,
  `tests/ir`, `tests/runtime`, and `tests/regression` (the last replaying
  all 16 original bootstrap fixtures against captured golden output).
- `self_host/lexer.kuro`: the first self-hosting milestone (Stage 5) — a
  Kuro tokenizer written in Kuro, run by `compiler/`, cross-tested token
  for token against `compiler/lexer.py` on real Kuro source files.

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
