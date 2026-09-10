# Kuro

Kuro is a small, readable, statement-oriented programming language. This
repository is its compiler, runtime, and (eventually) toolchain.

```
Name = "Kuro";
Print Name.

Action Add A, B;
    Return A + B;
Done.

Call Add 3, 4;
Print @_.
```

## Status

Pre-1.0, actively under construction. See
[`docs/architecture/current-state.md`](docs/architecture/current-state.md)
for an honest inventory of what exists and what doesn't, and
[`docs/engineering/`](docs/engineering/) for the ADRs behind every
non-obvious design decision. Nothing in this repository claims to be more
finished than it is (see `CONTRIBUTING`/spec section 55, "no fake features").

- `bootstrap/python/` — the original 425-line reference interpreter this
  project started from, frozen and unmodified as the compatibility oracle.
- `compiler/` — the current Python-hosted compiler: lexer, parser, name
  resolution, type checking, an IR, and an IR interpreter.
- `self_host/` — Kuro source written *in Kuro itself*, run by `compiler/`
  and cross-tested against it (the self-hosting effort, spec section 5):
  `lexer.kuro` (Stage 5), `parser.kuro` (Stage 6, full grammar parity plus
  structured diagnostics), and `resolver.kuro`/`typecheck.kuro` (Stage 7,
  name resolution and type checking — see `docs/architecture/
  self-hosted-semantics.md` and `docs/engineering/ADR-0012` through
  `ADR-0014`). The Python compiler in `compiler/` remains the bootstrap/
  reference oracle throughout; nothing here is self-*compiling* yet (no
  IR lowering or backend exists in Kuro) — see each ADR's "known
  limitations" for exactly what is and isn't true today.
- `cli/kuro.py` — `kuro run <file>` / `kuro check <file>` / `kuro emit-ir <file>`.
- `tests/` — lexer, parser, semantic, IR, runtime, and regression suites.

## Running a program

```bash
python3 cli/kuro.py run examples/hello.kuro
```

## Running the tests

```bash
python3 -m venv .venv && .venv/bin/pip install pytest
.venv/bin/python -m pytest tests/ -q
```
