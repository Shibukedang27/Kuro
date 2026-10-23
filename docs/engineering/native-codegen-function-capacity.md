# Bounded native-codegen function table

## What changed

This follow-up is stacked directly above draft/open [PR #127](https://github.com/Shibukedang27/Kuro/pull/127), exact parent head `3d080f7032a6b644395dbcdd0dd581c01ec6d33c`. It raises the Kuro-authored native code generator's fixed function-metadata capacity from 32 to 128 entries. The parser now uses one named `NativeFunctionCapacity` bound, and the body-start, body-end, parameter-count, return-count, and inferred-return-kind arrays all have exactly 128 slots.

The change is deliberately bounded rather than dynamic: the guarded compiler artifact has 73 functions, while the old limit rejected even otherwise-supported programs with 33 empty actions. The increment adds no new opcode lowering, parameter-kind assumptions, build target, generated image, or failure-policy change. Programs above 128 functions still fail closed without assembly.

## Evidence and results

At the parent codegen, valid compiler-generated programs with 31 and 32 empty actions plus `Print 7.` produced assembly; the same program with 33 actions exited 1 and emitted no assembly. The rejection matched the explicit `< 32` preparation guard and the five 32-entry metadata arrays.

The updated source-level tests accept 32, 33, 73, and 128 function blocks, and reject 129 with an empty `NativeOut`. A Linux x86-64 native codegen image was also built from the updated Kuro source and emitted assembly for a 73-action program whose last action is called. Clang linked that assembly as a freestanding executable, which printed `73`. The native image accepted 128 empty actions and rejected 129 with status 1, empty stdout, and empty stderr.

Fresh Linux production images built through the existing Python-hosted path. The Python/toolchain-blocked bootstrap audit still verified the 9,119-line compiler artifact (73 function markers, 294 call markers) and observed its normal status-1, empty-output codegen rejection. The blocked-toolchain smoke passed, including stage-1 compiler reproduction of the complete stage-0 bytecode. No generated image is part of this change.

The full local repository suite passed **2,666 tests, 20 skipped**. Two final Text/Decimal semantic cases and the metadata-array length invariant were added after that run began; the full affected native-codegen module was rerun with those additions and passed **173 tests, 18 skipped**.

## Remaining blocker

The function-table increase does **not** make the full compiler codegen succeed. Even with a 128-slot table for the artifact's 73 functions, the guarded artifact still fails closed during `NativePrepareProgram` on its first action, `ComputeLineCol`: its first parameter is emitted as `BC_PARAM TargetPos NONE`. The native code generator currently accepts only the explicit parameter kinds `Integers`, `Text`, and `Decimals`.

A minimal Kuro source control confirms the boundary: an untyped `Identity Value` action emits `BC_PARAM Value NONE` and is rejected with no assembly; the same action explicitly typed `Integers` is accepted. Hosted-runtime controls also confirm that the untyped action returns both text and decimal arguments, while native codegen rejects those signatures. Treating every `NONE` parameter as an Integer would therefore be unsound. Safe support would require call-site kind evidence and a defined fail-closed rule for unknown or conflicting callers.

## Next safe path

First map all call sites of `ComputeLineCol` and reduce that action to the smallest supported inference case. If implementing untyped-parameter support, infer only a single proven kind across every call site, then test integer, text, decimal, mixed-kind, missing-call-site, and recursive cases; unknown or inconsistent kinds must continue to fail without partial output. Re-run the full compiler artifact audit after each minimal change. Only a successful codegen should trigger a temporary native compiler build and exact stage-1/stage-2 bytecode comparison.

The function limit remains an explicit 128-slot safety bound; the regression rejects 129. The change does not remove the Python-hosted image-construction dependency or Clang/LLVM assembly/linking. The PR stack remains open and unmerged pending independent review and exact-head CI.
