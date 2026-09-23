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
Kuro's in-house implementation policy is documented in
[`docs/architecture/in-house-implementation.md`](docs/architecture/in-house-implementation.md).

- `bootstrap/python/` — the original 425-line reference interpreter this
  project started from, frozen and unmodified as the compatibility oracle.
- `compiler/` — the current Python-hosted bootstrap compiler: lexer, parser, name
  resolution, type checking, an IR, an interpreter, artifact tooling, and native
  image construction.
- `self_host/` — Kuro source written *in Kuro itself*, run by `compiler/`
  and cross-tested against it (the self-hosting effort, spec section 5):
  `lexer.kuro` (Stage 5), `parser.kuro` (Stage 6, full grammar parity plus
  structured diagnostics), `resolver.kuro`/`typecheck.kuro` (Stage 7,
  name resolution and type checking), and the Stage 8 `lower.kuro`,
  `bytecode.kuro`, `compiler.kuro`, `vm.kuro`, `runtime.kuro`,
  `artifact_loader.kuro`, and `native_codegen.kuro` bootstrap path — see
  `docs/architecture/self-hosted-semantics.md` and `docs/engineering/ADR-0012` through
  `ADR-0014`). The Kuro-authored compiler now compiles its complete source into
  bytecode, and the Kuro-owned launcher executes that artifact without Python.
  Python remains the bootstrap/reference oracle for constructing native images,
  while the system assembler/linker remains part of native image construction.
- `cli/kuro.py` — `kuro run <file>` / `kuro check <file>` / `kuro emit-ir <file>` /
  `kuro build <file>` (validated portable IR artifact) / `kuro bundle <file>`
  (portable `.kuro.app` bundle) / `kuro exec` / `kuro self-host` / `kuro repl` /
  `kuro debug` / `kuro profile`.
- `tests/` — lexer, parser, semantic, IR, runtime, and regression suites.

## Running a program

```bash
python3 cli/kuro.py run examples/hello.kuro
```

To install the development tool locally and make `kuro` available on your
`PATH`:

```bash
python3 -m pip install -e .
kuro run examples/hello.kuro
```

The installable package currently provides the hosted compiler and IR
interpreter. To create a reproducible compiled IR artifact:

```bash
kuro build examples/hello.kuro --output build/hello.kuro.ir
kuro bundle examples/hello.kuro --output build/hello.kuro.app
kuro exec build/hello.kuro.app
kuro self-host examples/hello.kuro
```

The application bundle is a portable validated artifact and can be launched
with `kuro exec`. The launcher currently uses the hosted Kuro runtime; a
runtime compiled entirely from Kuro remains a separate self-hosting milestone.

Start an interactive session with `kuro repl`. Use `.check`, `.clear`, and
`.exit` inside the session.

On macOS arm64, Linux x86_64, and macOS x86_64 cross-targets, `kuro native
<file.kuro>` builds a native executable for the supported Kuro subset. Pass
`--target` to select a target explicitly. For a no-Python production image,
use `kuro native-runtime <file.kuro>`; it embeds the Kuro-authored lexer,
parser, bytecode pipeline, VM, and runtime entrypoint. `kuro native-compiler
<file.kuro>` produces the corresponding native Kuro compiler image and accepts
the same target flag. Running either resulting executable does not invoke
Python; the Python frontend is currently retained only for bootstrap image
construction and development commands.

The macOS x86-64 compiler and bytecode launcher also pass a full self-compile
and second-stage execution test under Rosetta. Linux x86-64 images cross-build
as ELF, but Linux execution is not yet verified. The Kuro-authored generator
can also be built to emit x86-64 macOS or Linux assembly independently of the
CPU running its image. The checked-in `kuro-native codegen` image still emits
macOS arm64; the x86-64 targets require a separately built generator image.

The checked-in production launcher exposes a complete Python-free
source-to-bytecode-to-execution path:

```bash
./bin/kuro-native compile examples/hello.kuro > build/hello.kurobc
./bin/kuro-native exec build/hello.kurobc
./bin/kuro-native codegen build/literal-print.kurobc > build/literal-print.s
./bin/kuro-native doctor
```

`compile` emits a strict `kuro.bytecode/1` artifact. The native compiler and
launcher return a nonzero operating-system status for rejected source or an
invalid artifact. `codegen` runs the Kuro-authored native generator image; its
current capability-checked integer subset includes variables, `+`, `-`, `*`,
guarded `/`, comparisons, `If`/`Else`, `Repeat`, `While`, assignment, `Add`,
and printing, and emits macOS arm64 assembly. Literal text printing is also
supported. Unsupported programs exit nonzero.

The native build also publishes `dist/kuro-compiler.source.kuro`, the exact
deterministic Kuro source used to create the compiler image. `doctor` feeds
that complete source back through `dist/kuro-compiler` and requires a valid
multi-thousand-value bytecode artifact, providing a full-source self-compile
gate without invoking Python during verification.

Use `kuro debug <file.kuro>` to run with an instruction-level trace showing
the call depth, program counter, operation, and visible environment.

Use `kuro profile <file.kuro>` to report execution time, instruction counts,
and maximum call depth.

Create a starter project with `kuro init my-app`. The scaffold includes a
`kuro.package` manifest, `src/main.kuro`, README, and build ignores.

Native code generation is available for the documented subset. Modules and
application libraries are also available through the local toolchain.
Relative source imports are supported:

```kuro
Import "lib.kuro";
```

The imported module is compiled as part of the same Kuro program; cycles and
missing modules are reported as compiler diagnostics.

## Running the tests

```bash
python3 -m venv .venv && .venv/bin/pip install pytest
.venv/bin/python -m pytest tests/ -q
```
