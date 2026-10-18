# Named Decimal storage and mutation

This slice builds on PR #65. It gives function-free, straight-line programs named scalar Decimal storage in the Kuro-owned native generator. It is not completion of compiler or toolchain independence.

## What changed and why

The generator already moves scalar slots as 64-bit words, but named non-parameter loads were always tagged as Integer and Decimal stores were rejected. A bounded kind table now accompanies the existing 64 shared slots. `BC_STORE_LIST` can establish a named Decimal slot; subsequent loads preserve its Decimal kind, and same-kind assignment preserves binary64 bits without conversion. Existing arithmetic, comparisons, argument-independent printing, and the freestanding formatters can consume those loads.

`BC_ADD` reuses the existing floating-point mutation lowering for established Decimal slots, accepting Decimal or Integer operands and converting Integer operands to binary64. `BC_UPDATE` requires a Decimal replacement. Initialization through Decimal `BC_ADD`/`BC_UPDATE` alone is still unsupported: establish the slot with `BC_STORE_LIST` first.

The kind table is indexed by the already bounded global-slot registry, not by another unbounded variable-name search. No Python, libc, allocator, C compiler, or external formatter is added to the generated program.

## Safety boundary

Named Decimal storage is accepted only when the whole program contains no Actions and no `If`, `Repeat`, or `While` control-flow regions. The preparation pass discovers these constructs before emission, so adding a function or branch after an otherwise valid Decimal assignment still rejects the program. Even unused Actions and unrelated control flow are outside this first slice.

A first read of a registered but not yet written slot observes the existing Integer-zero representation and commits that slot to the non-Decimal path. A slot previously written as Integer or Text cannot later become Decimal. Established Decimal slots cannot be overwritten or updated with Integer or Text, and cannot accept Text through `Add`. Rejection clears `NativeOut`; there is no hosted fallback. Existing non-Decimal behavior and Action-parameter Decimal paths are retained rather than claiming a general type-system correction.

These restrictions deliberately avoid pretending emission order is execution order across branches, loops, calls, or recursion. The existing `_` result slot keeps its earlier special handling; general dynamic-kind joins for `_` are not fixed here. Multi-value storage, containers, declared-type lowering, and arbitrary type-changing variables are not added.

## Verification

- Native-codegen, initial storage regressions, and VM gate: **208 passed, 18 skipped in 2734.33s (45m34s)**. This includes a fresh Linux compiled Kuro generator; its fixture setup took **2683.85s (44m44s)**. No generator implementation changed during this gate.
- The subsequently strengthened storage/VM gate: **77 passed in 17.12s** (**54 storage cases plus 23 VM cases**), including three-target rejection cases and ARM64 instruction execution. These overlap the preceding gate; the counts must not be added together.
- Linux backend/CLI subset: **12 passed**, 69 deselected. Existing hosted/cross-target native regressions: **110 passed, 5 skipped**, 62 deselected.
- Source programs pass through the self-hosted compiler driver and Kuro-authored generator, then assemble for Linux x86-64, macOS x86-64, and macOS ARM64. Linux hosted-emitter output and fresh compiled-Kuro-generator output execute with exact stdout `3.75`, `1.25`, `2.5`, `3.0`, and `-0.0`, one value per line. This exercises nonzero Integer and Decimal addends, copy independence, computed replacement, reassignment, and signed-zero storage.
- The emitted ARM64 storage/mutation/formatter instructions execute under qemu after adapting only Mach-O sections/relocations, entry naming, and Darwin syscall numbers to Linux ELF. Its static image has no undefined symbols. This is instruction-level execution evidence, **not Darwin runtime verification**.
- Fresh compiled Linux and macOS ARM64 generator checks execute the storage program, require no undefined executable symbols, and reject type conflicts, Text addends, late branches, and late unused Actions with status 1 and no assembly output. macOS ARM64 execution is covered by the existing genuine-host CI test, not claimed as a local Linux result. The compiled Linux storage test is required explicitly by Linux CI.
- Independent implementation/test review found no actionable defects. Whitespace checks pass. Final acceptance requires all eight GitHub checks on the documentation-updated head; PR checks and the PR verification summary are authoritative for that exact commit, not checks on its base.

## Next path

Extend kind analysis across global Action accesses and control-flow joins, with conservative rejection of conflicting representations and explicit initialization semantics. Then broaden Decimal storage/mutation conformance and general compiler/runtime lowering. Hosted ARM64 `%g` display differences, x86 formatter fallback/literal fast-path differences, substantial hosted bootstrap build cost, and the 4096-token native-generator limit remain separate concerns.

Clean-checkout native production-image rebuilding without Python is still unfinished. Host assemblers/linkers are still required to construct generated images; a repository-owned object/executable construction path, broader runtime/standard-library parity, and genuine platform validation remain necessary for the strict independence goal. Keep the review stack open and unmerged.
