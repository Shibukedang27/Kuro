# Native self-hosting: the verified Text gates

## Current result

At the verified PR #133 baseline—open, draft, unmerged at `6f1232a8c2ef25ebe184e0651626695c973e9422`, directly above #132, with all eight exact-head checks passing and a clean worktree—the exact self-compile bytecode artifact contains **9,118 tokens (about 88 KB)** ([artifact accounting](vm-storage-lifetime-accounting.md)). The separate source-composition [audit](python-free-bootstrap-gap.md) reports **9,119 source lines** (73 functions and 294 calls); these counts describe different artifacts. The native loader limit is 65,536 tokens. The 4,096-token checks are scan/work bounds, not the first blocker.

A fresh native-codegen run rejects with status 1 and empty output during preparation at the third function, `RecordDiag`. Its `Message` formal has kind `NONE`; the current [preparation gate](../../self_host/native_codegen.kuro#L1406-L1421) admits only Integer, Text, or Decimal formals. Generic `NONE` must remain fail-closed. The [earlier bootstrap audit](python-free-bootstrap-gap.md) and [bounded-concat-chain note](native-codegen-literal-text-concat-chains.md) correctly preserve what their earlier probes observed; this exact-artifact result supersedes their interpretation of the 4,096 bound as the immediate blocker.

## Why annotating `Message` is not enough

All six fixed [parser call sites](../../self_host/parser.kuro#L233-L1071) pass Text at the language level: three literal messages, two literal-plus-parameter messages, and one token-dependent message. The two parameter-built messages and the input-dependent message use shared scratch globals. Their Text kind is not preserved by current shared loads, which default to Integer unless Decimal is proven. The concat lowering added through #133 accepts only bounded literal chains in top-level straight-line code, not these Action paths. `RecordDiag` also appends `Message` to `DiagMessages`, but native `BC_APPEND` has no lowering/storage path. The untyped `ExpectKind.ExpectedKind` and `ExpectWord.ExpectedWord` Action formals need their own safe callsite treatment. Consequently, adding only a `Text` annotation to `Message` would not make this composition compile safely.

A valid 9,216-token stress input on a temporary higher-limit build exhausted the 1 GiB arena at about 1.05 GiB peak RSS. The accepted 4,096-token case used about 786 MiB. Raising the ceiling alone is therefore not a safe fix.

## Next proof gates

1. Prove conservative Text-kind propagation across shared writes and loads and Action arguments, without weakening generic `NONE` rejection.
2. Define bounded dynamic Text concatenation with explicit allocation, failure, aliasing, lifetime, and reentrancy guarantees.
3. Add a safe Text `BC_APPEND` and diagnostic-storage path, including capacity and failure behavior.
4. Separately establish safe contracts for other untyped Action formals, including `ExpectedKind` and `ExpectedWord`.
5. Re-run the exact self-compile and stress/resource checks against the resulting codegen; do not treat a larger numeric bound as proof of safety.

The prior no-change audit at unchanged #133 reported 18 focused regressions passed, the full suite at 2,717 passed and 23 skipped, and the restricted-toolchain audit passed. Those are baseline results, **not tests run on this documentation commit**. Python-seeded image construction and Clang/LLVM assembly/linking also remain unfinished; this note does not claim completed toolchain independence.
