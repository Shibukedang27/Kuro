# A bounded eight-return ladder for native codegen

Native codegen now accepts one additional, deliberately narrow function shape: the seven-guard early-return ladder used by `ParseAtom`. This is not general support for eight returns or arbitrary multi-return control flow.

## Exact accepted shape

The function must contain exactly seven root-level `If` guards at maximum nesting depth one. Each guard has one returning then-arm and an explicit empty else-arm, represented by `BC_ELSE_BEGIN` immediately followed by `BC_IF_END`. A single top-level fallback `Return` must be the final body operation. The resulting bytecode has eight `BC_RETURN` instructions, seven each of `BC_IF_BEGIN`, `BC_ELSE_BEGIN`, and `BC_IF_END`, and all paths return.

The validator also rejects any `Repeat` or `While` opcode in this shape. It reuses the generator's existing 16-cell branch arrays: the seven arm markers use indexes 1–7 while the depth-one frame uses index 0. No Native-prefixed Kuro state name was added, and the per-call frame/ABI is unchanged.

## Fail-closed boundaries

The tests reject missing or duplicated arm returns, nonempty else-arms, loops, nested eight-return trees, trailing statements after the fallback, an eight-return body without a terminal top-level fallback, a seven-return ladder without a fallback, and eight straight-line returns. Each rejection leaves `NativeOut` empty.

The positive fixture includes a recursive call in one guard arm. It assembles for x86-64 Linux, x86-64 macOS, and ARM64 macOS. On Linux, the generated program executes all eight input paths and prints `10`, `11`, `12`, `13`, `14`, `17`, `16`, and `0`.

## Verification and remaining blocker

The broader native codegen, Decimal, Repeat, branch-join, loop-init, integer-capacity, and formatter modules passed **420 tests with 21 skipped**. After adding the direct terminal-fallback regression, `python3 -m pytest -q tests/self_host/test_native_codegen.py -k eight_return` passed **12 tests**. A fresh four-image Linux-hosted rebuild, the restricted-PATH native smoke, and stage-1 reproduction of the complete compiler bytecode also passed. Tracked `dist/` outputs were restored.

The exact full compiler artifact contains **9,124 instructions in 9,125 lines**, with 73 function markers and 294 call markers. Full-artifact codegen still exits 1 with empty stdout/stderr and no partial assembly. The new ladder lets preparation pass `ParseAtom` (8 returns; function start token 1542). The first remaining rejection is `ParseComparisonOp` at function-start token **2043**; its bytecode contains **10 `BC_RETURN` paths**, which is outside this narrowly accepted shape. General ten-return support is not claimed or attempted here.

Text equality, dynamic Text concatenation, `BC_APPEND` storage, Python-free image construction, and strict native self-hosting remain separate limitations. Cross-assembly is not Darwin runtime evidence; runtime execution was verified on Linux x86-64 only.
