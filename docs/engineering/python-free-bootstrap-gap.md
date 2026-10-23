# The next bootstrap gate: rebuild a native compiler image

## Result: full-source compilation reaches a codegen boundary

This test-and-audit increment is stacked directly above draft/open [PR #126](https://github.com/Shibukedang27/Kuro/pull/126), exact parent `b691803f9fac28b2bb0272bc670bedf46eaf27fa`. It changes no production compiler, runtime, native backend, generated image, default build target, or failure policy. It does not claim Python-free clean-checkout construction or full toolchain independence.

The repository already has a POSIX shell/awk compiler-source composer. The new [bootstrap gap audit](../../bootstrap/audit-native-bootstrap-gap.sh) runs that composer and a stage-0 compiler with Python and native tool commands removed from `PATH`. It requires the emitted full-source artifact to exceed **9,000 lines**, contain at least **70** exact `BC_FUNC_BEGIN` lines and **290** exact `BC_CALL_BEGIN` lines, and carry the `kuro.bytecode/1` marker. These are deliberate lower-bound guards against a header-only or obviously truncated stream, not a parser-based proof of semantic completeness. The observed Linux stream is **9,119 lines**, with 73 and 294 such lines respectively; it contains no lines equal to `BC_MULTI_BEGIN` or `BC_STORE_MULTI`.

The same stage-0 codegen emits assembly for a small `Print 2 + 3.` control. On the full-source artifact it currently exits **1** with stdout and stderr both empty, so it publishes no partial assembly. The audit accepts only that exact observed rejection shape: a successful codegen, a crash/other status, diagnostic output, or any partial assembly makes the audit fail and requires replacing it with a real temporary image-build/reproduction gate. The counts are text-line observations, not a proof that any one token is the first unsupported operation; the failing artifact still needs minimization before a production lowering change is proposed.

The 4,096-token guard in the authored generator's isolated indexed-collection path is not what this probe establishes: the full-source stream has no `BC_MULTI_BEGIN` or `BC_STORE_MULTI` lines, while it does contain function/call markers. The actual unsupported operation has not yet been isolated.

## What this does not remove

The current tracked seed executables are macOS ARM64 Mach-O images. Linux CI cannot execute them directly: its existing workflow first constructs Linux images with `make native-hosted-bootstrap`, which still uses the Python compiler/backend, then tests those images with Python and toolchains blocked. The new audit runs after that hosted seed step. Existing Python-free smoke tests verify use and bytecode self-reproduction of already-built images; they do not build a native compiler image from the full compiler source.

`Makefile` still routes `native` to `native-hosted-bootstrap`, which calls `compiler.self_host.build_native_*`; those functions call the Python `compile_source` frontend and `compiler.native.build_native`. Native assembly/linking still calls Clang, and Linux cross-linking can use LLVM `lld`. The audit itself needs neither Python nor Clang because it stops at the proven codegen rejection. It is not a replacement image builder and does not remove either construction dependency.

## Safe implementation sequence

1. **Minimize the rejection.** Reduce the full-source artifact to the smallest reproducible Kuro source or bytecode shape that still fails, record the first unsupported opcode/action shape, and keep a nearby accepted control. Distinguish decoder/input limits from specific lowering gaps.
2. **Add only proven codegen capability.** For each minimal shape, compare authored-codegen acceptance and emitted assembly against the hosted/native oracle. Preserve unsupported-program failure behavior and avoid publishing partial assembly as a successful artifact. Do not raise a global capacity or token bound without real memory, time, and failure-boundary evidence.
3. **Prove one native compiler image.** Build the compiler candidate in a temporary directory from shell-composed source using the unchanged stage-0 compiler and Kuro codegen, then assemble/link it with the explicitly named Clang dependency. Execute the candidate on the entire compiler source and require byte-for-byte stage-1/stage-2 bytecode equality, plus valid and invalid source controls. Never overwrite the seed before these checks pass.
4. **Extend to all four images.** Only after compiler reconstruction passes, build runtime, bytecode launcher, and codegen in a temporary directory. Verify each image's protocol, self-build/reproduction where applicable, and failure behavior before promotion.
5. **Close the clean-checkout seed gap.** Provide a runnable stage-0 image for each supported build host or prove a portable seed route. The committed ARM64 Mach-O images do not solve Linux stage-0 execution. Remove Python from the default build only after a clean-checkout test proves it on each claimed host.
6. **Decide the native toolchain boundary.** Strict independence additionally requires replacing the current host assembler/linker dependency with an owned, tested object/executable writer (or explicitly narrowing the independence goal to accept those tools).

## Verification results

- A fresh four-image x86-64 Linux bootstrap passed through the existing **Python-hosted** builder; this is not Python-free construction.
- The new audit passed against those images with Python and compiler/linker commands hidden. It reported the 9,119-line guarded artifact and reproduced codegen status 1 with empty stdout/stderr and no partial assembly.
- `tests/self_host/python_free_native_smoke.sh` passed: runtime, compiler, bytecode launcher, and codegen worked with Python/toolchains blocked; stage-1 compiler bytecode matched the full stage-0 reproduction.
- `tests/self_host/test_native_integer_storage_capacity.py::test_fresh_bytecode_stage_compiler_reproduces_self_and_large_initializer` passed, covering compiler reproduction and the 272-literal initializer control.
- The focused audit module passed **6 tests**, including truncated output, recovered codegen, crash, partial assembly, and stderr diagnostics.
- The full local suite passed **2,658 tests, 20 skipped** before the final stderr-only regression was added. That last regression passed within the six-test focused module; the final exact-head CI run must rerun the complete suite including it.

These results confirm the current boundary, not bootstrap independence. Python-seeded construction and Clang/LLVM assembly/linking remain. PRs #107/#108 remain individually unverified, and this increment does not change that status. Keep this PR and its ancestors draft/open/unmerged. The next engineering step is to minimize the unsupported full-compiler bytecode shape before proposing a production codegen change.
