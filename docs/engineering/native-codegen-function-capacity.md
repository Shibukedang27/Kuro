# Bounded native-codegen function table

## What changed

This follow-up is stacked directly above draft/open [PR #127](https://github.com/Shibukedang27/Kuro/pull/127), exact parent head `3d080f7032a6b644395dbcdd0dd581c01ec6d33c`. It raises the Kuro-authored native code generator's fixed function-metadata capacity from 32 to 128 entries. The parser now uses one named `NativeFunctionCapacity` bound, and the body-start, body-end, parameter-count, return-count, and inferred-return-kind arrays all have exactly 128 slots.

The change is deliberately bounded rather than dynamic: the guarded compiler artifact has 73 functions, while the old limit rejected even otherwise-supported programs with 33 empty actions. The increment adds no new opcode lowering, parameter-kind assumptions, build target, generated image, or failure-policy change. Programs above 128 functions still fail closed without assembly.

## Evidence and results

At the parent codegen, valid compiler-generated programs with 31 and 32 empty actions plus `Print 7.` produced assembly; the same program with 33 actions exited 1 and emitted no assembly. The rejection matched the explicit `< 32` preparation guard and the five 32-entry metadata arrays.

The updated source-level tests accept 32, 33, 73, and 128 function blocks, and reject 129 with an empty `NativeOut`. A Linux x86-64 native codegen image was also built from the updated Kuro source and emitted assembly for a 73-action program whose last action is called. Clang linked that assembly as a freestanding executable, which printed `73`. The native image accepted 128 empty actions and rejected 129 with status 1, empty stdout, and empty stderr.

Fresh Linux production images built through the existing Python-hosted path. The Python/toolchain-blocked bootstrap audit verified the 9,119-line compiler artifact (73 function markers, 294 call markers) and observed its normal status-1, empty-output codegen rejection. The blocked-toolchain smoke passed, including stage-1 compiler reproduction of the complete stage-0 bytecode. No generated image is part of that change.

On the parent PR, the full local repository suite passed **2,666 tests, 20 skipped**. The affected native-codegen module passed **173 tests, 18 skipped** after its final Text/Decimal semantic cases and metadata-array invariant were added.

## Remaining blocker

The function-table increase did not make the full compiler codegen succeed. The first blocker was `ComputeLineCol.TargetPos`, emitted as `BC_PARAM TargetPos NONE`. This follow-up adds an explicit `Integers` contract only after mapping the complete fixed-composition call set and its shared-global write paths. The [callsite proof and scope limits](native-codegen-computelinecol-kind-contract.md) show two direct callers in the production composition, both fed integer source offsets; the resolver's third source-tree call also supplies a token offset but is outside that composition.

This is not general inference for `NONE`: arbitrary untyped action parameters remain polymorphic, and native codegen continues to reject them rather than guess. Recompiling the exact fixed compiler source after the annotation yields 9,118 bytecode tokens, 73 function blocks, and 294 call blocks. The first remaining untyped formal is `RecordDiag.Code`. A temporary native codegen image rejected that full artifact with status 1 and empty stdout/stderr, so no full compiler image or partial assembly is claimed.

## Next safe path

Analyze each remaining untyped formal and all reachable callers individually, including shared variables and possible dynamic routes. Add support only where every reachable value has one proven compatible kind and the runtime/failure behavior remains explicit; otherwise keep the preparation gate fail-closed. A successful full codegen remains a prerequisite for a temporary compiler build and exact stage-1/stage-2 bytecode comparison.

The function limit remains an explicit 128-slot safety bound; the regression rejects 129. Neither this PR stack nor the `ComputeLineCol` annotation removes the Python-hosted image-construction dependency or Clang/LLVM assembly/linking. The PRs remain draft/open/unmerged pending independent review and exact-head CI.
