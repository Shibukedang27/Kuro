# Bounded return profiles for native codegen

Native codegen has two deliberately bounded multi-return profiles: the eight-return `ParseAtom` guard ladder from PR #140, and a separate ten-return structural profile for `ParseComparisonOp`. Neither change enables general multi-return trees or admits a function from its return count alone.

## `ParseAtom`: seven guards and one terminal fallback

The function has exactly seven root-level `If` guards at maximum nesting depth one. Each guard has one returning then-arm and an empty else-arm, represented by `BC_ELSE_BEGIN` immediately followed by `BC_IF_END`. One top-level fallback `Return` is the final body operation. The bytecode therefore has eight `BC_RETURN` instructions and seven each of `BC_IF_BEGIN`, `BC_ELSE_BEGIN`, and `BC_IF_END`.

The validator rejects `Repeat` and `While` in this shape. It reuses the generator's existing 16-cell branch arrays: the seven arm markers use indexes 1–7 while the depth-one frame uses index 0. The per-call frame and ABI are unchanged.

## `ParseComparisonOp`: a distinct nested profile

Inspection of a fresh complete compiler artifact found `ParseComparisonOp` at function-start token **2043**, with **zero parameters and ten `BC_RETURN` sites**. Unlike `ParseAtom`, this is not a flat ladder: it has six root guards, nested conditional arms to maximum depth **3**, and 15 `BC_IF_BEGIN`, 15 `BC_ELSE_BEGIN`, and 15 `BC_IF_END` markers.

The ten explicit Text result writes must occur in this exact order: `"ge"`, `"gt"`, `"le"`, `"lt"`, `"eq"`, `"eq"`, `"ne"`, `"ge"`, `"le"`, and the terminal empty string. The 15-node preorder profile is fixed: subtree IF counts `[3,2,1,3,2,1,2,1,2,1,2,1,3,1,1]`; maximum depths `[3,2,1,3,2,1,2,1,2,1,2,1,2,1,1]`; then-arm return counts `[2,1,0,2,1,0,1,0,1,0,1,0,2,1,1]`; and else-arm return counts `[0,1,0,0,1,0,0,0,0,0,0,0,0,0,0]`. Only preorder nodes 2 and 5 have return-only else-arms; the other 13 else-arms must be empty. There is exactly one top-level return, and it must write the empty Text fallback at the end of the function body. Loops and other control-flow topologies are rejected.

This is intentionally a **structural profile**, not a byte-for-byte whitelist of the parser source. The name and zero-parameter signature, all branch/arm boundaries, per-arm return distribution, ordered explicit Text writes, and terminal fallback are checked here. Guard predicates and ordinary statements go through the existing opcode validation and emission path; unsupported operations still fail closed. Linux runtime tests demonstrate that a changed guard constant and supported side effects between roots or inside a returning arm preserve the emitted behavior. This boundary is documented so the profile is not mistaken for support of arbitrary ten-return functions.

## Fail-closed boundaries

Focused tests reject the wrong function name or parameter count, unsupported return counts, loops, a different nested tree, wrong arm distribution, non-Text or wrong literal return writes, nonempty arms that must fall through, a missing or nonempty fallback, statements after the fallback, and malformed branch boundaries. Rejections leave `NativeOut` empty. Positive tests assemble for x86-64 Linux, x86-64 macOS, and ARM64 macOS; runtime execution is verified on Linux x86-64 only.

## Verification and remaining limitations

The final complete `tests/self_host/test_native_codegen.py` run passed **294 tests with 21 skipped**; the ParseComparisonOp-focused selection passed **25 tests**. A prior repository-wide release-check test phase passed **2,806 tests with 23 skipped** before four final ParseComparisonOp-only boundary cases were added; those later cases are included in the final complete native-codegen run.

A fresh four-image Linux x86-64 build with Linux x86-64 codegen output passed runtime/compile/exec checks, freestanding arithmetic and loop assembly/runtime checks, full-source stage-0 compiler self-build, and stage-1 execution of `Print 6 * 7.` (output `42`). The restricted-PATH audit hid Python and toolchains, verified source composition, stage-0 compilation, and the arithmetic codegen control, then reproduced the complete compiler artifact rejection: **9,125 lines**, 73 function markers, 294 call markers; full-artifact codegen exited **1** with empty stdout/stderr and no partial assembly. This audit confirms fail-closed behavior but does not localize the next rejection after the newly recognized profile.

The repository's default release-check generator emits macOS ARM64 assembly, so its host Linux `clang` smoke is not a valid Linux link check. The explicit Linux-output generator passed the equivalent freestanding `_start` smoke; the existing `kuro-native doctor` check itself expects `_main` and is not applicable to that Linux-output image. The default-output image's doctor check passed in the release-check run.

Text equality and dynamic Text/`BC_APPEND` behavior, Python-seeded native-image construction, and the Clang/LLVM toolchain remain separate limitations. These increments do **not** establish full native self-hosting.
