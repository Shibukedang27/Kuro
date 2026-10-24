# Native codegen: parser peek offsets are explicitly integers

This bounded follow-up is based directly on the open, draft, unmerged PR #136 head `aa0f966c9d073183630646c0ce5d06351528213f`. It makes no inference rule for general untyped parameters.

## What the full-artifact run showed

A fresh x86-64 Linux compiler image built from that exact parent compiled its complete composed source into a valid `kuro.bytecode/1` artifact with 9,118 tokens. A fresh x86-64 Linux native code generator consumed that artifact, exited with status 1, and emitted no assembly or diagnostics.

A temporary, instrumented copy of the same generator localized the first failure in `NativePrepareProgram`: at token 1218, the header for `PeekKind` contains `BC_PARAM Offset NONE`. The parameter validator accepts only `Integers`, `Text`, or `Decimals`; it does not infer a kind from callers. This is the observed earliest gate on the exact #136 artifact, not an assumption based on an earlier status note.

## The narrow change

`PeekKind.Offset` and `PeekValue.Offset` are now explicitly declared `Integers`. Their complete fixed callsite sets are pinned in [the focused regression](../../tests/self_host/test_native_peek_offset_contracts.py): `PeekKind` has three callers (`CurKind` passes 0; `IsDeclAhead` and `ParseStatement` pass 1), and `PeekValue` has three (`CurValue` passes 0; `IsDeclAhead` passes 1 and 2). The test verifies the exact call scopes, integer-literal producers, parameter types, and read-only use of each offset in token-index arithmetic. No dynamic dispatch, shared mutable offset, or additional caller is admitted by this source composition.

The language's ordinary type checker now enforces those two fixed contracts. Generic `NONE` behavior is unchanged; the contracts do not add Text concatenation or collection-append lowering.

## What remains blocked

After these two contracts, the freshly reproduced artifact still has 9,118 tokens and the native generator still exits 1 with empty assembly. The next instrumented rejection is at token 1332, `BC_FUNC_BEGIN IsWord`. That action has three `BC_RETURN` instructions. Native preparation currently accepts only its specially checked one-, two-, or four-return shapes, so this is a distinct control-flow-shape gate—not another missing type annotation.

The next technical prerequisite is to prove and test a safe lowering for this exact nested three-return shape (or a semantics-preserving source normalization), including return-path joins; simply allowing a return count of three would be unsafe. Dynamic Action-local Text concatenation, native `BC_APPEND`/diagnostic collection storage, the existing work and memory bounds, Python-seeded image construction, and external assembly/linking remain separate limits. This increment does not claim native compiler-image generation, full self-hosting, or strict toolchain independence.
