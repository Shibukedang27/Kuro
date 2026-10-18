# Decimal kinds through function-free control flow

[PR #67](https://github.com/Shibukedang27/Kuro/pull/67) is stacked on [PR #66](https://github.com/Shibukedang27/Kuro/pull/66), verified at `736229f` with all eight checks successful. It extends the Kuro-authored native generator, not the hosted backend's language support, and does not complete toolchain independence.

## What changed and why

Named Decimal slots can now flow through `If`/`Else`, `Repeat`, and `While` regions when their Decimal representation was established unconditionally before entering the region. Loads, arithmetic, same-kind assignment, Integer/Decimal `Add`, Decimal `Update`, comparisons, and printing reuse the existing scalar lowering. The representation stays Decimal regardless of which branch executes or how many times a loop runs.

The generator tracks combined control-flow depth alongside its existing per-construct label stacks. At depth zero, an untouched slot may establish its Decimal kind. At positive depth, a Decimal store is accepted only if that slot is already Decimal. Existing checks reject non-Decimal overwrites of Decimal slots and Decimal overwrites of previously non-Decimal slots. Unknown reads still commit the conservative Integer-zero kind. These rules provide an invariant join rather than treating emission order as execution order: no accepted region introduces a new named Decimal representation, so a skipped branch or zero-iteration loop cannot leave an Integer-zero value mislabeled Decimal.

A first Decimal assignment after a completed, unrelated region is permitted if that slot remains untouched. Conditional non-Decimal stores or reads conservatively prevent later Decimal promotion. No allocator, Python code, libc call, or new generated-program dependency is introduced.

## Deliberate rejection boundary

- All named Decimal storage remains function-free. Even an unused Action causes rejection; Action-shared kind inference, call ordering, and recursion are deferred.
- First Decimal initialization inside any control-flow region is rejected, including both-arm Decimal assignments, statically true branches, and positive-count loops. This is intentionally more conservative than a path-sensitive definite-assignment analysis.
- Conflicting Decimal/Integer/Text representations are rejected even in unreachable arms. Decimal `Update` still requires a Decimal operand; Decimal `Add` accepts only Integer or Decimal operands.
- Main-program `_` stores inside regions must preserve the slot's entry kind, including across zero-iteration loops. Its existing mutation lowering remains Integer-only within regions, so non-Integer `_` mutation is rejected rather than generalized.
- Function-free regions must join at empty operand-stack statement boundaries (one condition/count operand at `If`/`Repeat` entry). Raw bytecode carrying values across these joins is rejected; a general value-stack dataflow analysis is not claimed.
- Existing bounds remain: 64 shared slots, 4096 bytecode tokens, and the existing per-construct nesting limits. Action result-slot joins, type-changing non-Decimal behavior, multi-value storage, and declared-type lowering are not generalized here.

Rejection sets `NativeFailed` and clears assembly output; it does not silently fall back to the hosted compiler.

## Verification

- Corrected native-codegen, Decimal storage/control-flow, and VM gate: **327 passed, 18 skipped in 2966.13s (49m26s)**. This includes a fresh compiled Linux Kuro generator; fixture setup took **2892.16s (48m12s)**. The generator implementation was unchanged during this final gate.
- Final exact Linux portable-suite command: **703 passed in 64.53s**. Linux backend/CLI subset: **12 passed**, 69 deselected. Counts overlap the native/VM gate and must not be added together.
- During correction, the focused Decimal/storage/VM subset passed **152 tests in 33.60s**; subsequent adversarial cases are included in the final 327-test gate. Hosted native-codegen selection: **109 passed, 11 skipped**, 58 deselected.
- The initial prototype native/VM gate passed **264 tests, 18 skipped in 2773.14s**, but preceded the result-slot and stack-join corrections. It is not final-head verification.
- Final independent static review found no remaining actionable Decimal-plus-flow miscompile. Whitespace checks pass. Acceptance requires all eight GitHub checks on the final documentation-updated head; the PR's exact-head check summary is authoritative and must not be replaced by results on its base or prototype.

The independent safety review found that merely relaxing the named-slot guard newly admitted a conflicting `_` branch-kind miscompile. The first native gate passed but was insufficient evidence for this case. The correction rejects main result-slot kind changes inside regions and adds branch/zero-loop/mutation regressions, plus statement-boundary checks for raw operand-stack joins. Fresh-generator verification must cover the corrected implementation, not just the earlier passing prototype.

The new source regression covers taken and untaken `If`/`Else` arms, an untaken branch without `Else`, zero- and multiple-iteration `Repeat`, a Decimal-controlled `While`, mixed nested regions, an Integer counter, post-join loads, and negative zero. Its expected output is `2.0`, `3.0`, `3.5`, `5.0`, `2.0`, `1.75`, `2`, and `-0.0`, one value per line.

Cross-assembly covers Linux x86-64, macOS x86-64, and macOS ARM64. Linux native execution and ARM64 instruction emulation are distinct checks: adapting Mach-O sections/relocations, entry names, and syscall numbers for Linux ELF is not a claim of Darwin execution. The existing genuine macOS ARM64 compiled-generator test now executes this same control-flow source. Fresh compiled-generator gates also require zero undefined executable symbols and reject conditional first initialization and conflicting branch writes with status 1 and no assembly output.

## Next path

The follow-up [bounded both-arm initialization design](native-definite-branch-joins.md) implements the first top-level, function-free `If/Else` slice. The rejection boundaries and verification above describe PR #67 itself, not the follow-up.

Add bounded definite-assignment/kind joins for first initialization in both branch arms, with explicit handling of skipped branches and loop backedges. Separately analyze Action-shared slots and initialization across calls rather than relaxing the Action guard. Broader native compiler/runtime lowering, formatter parity, and bootstrap performance remain open.

A clean checkout still cannot rebuild native production images independently of Python. Generated images are still constructed with host assemblers/linkers. Repository-owned object/executable construction, broader runtime/standard-library parity, and genuine target validation remain necessary. Keep this PR and the dependency stack open and unmerged.
