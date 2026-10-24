# Bounded native Text concatenation chains

The Kuro-owned native code generator now accepts left-associative chains of Text literals in top-level straight-line code, such as `Print "a" + "b" + "c".` Each accepted `+` writes to its own fixed native buffer, and the chain result remains on the operand stack until it is printed. This is emitted native runtime concatenation, not compiler-time folding.

## Accepted boundary and storage proof

Every leaf participating in a concat must be a NUL-free Text literal shorter than 1,000 Kuro characters. The first `+` joins two such literals; each later `+` may use the previous accepted concat result on the left, but its right operand must again be an immediate Text literal. The generator keeps a fixed 128-entry stack side table: zero means the value is not proven safe for this feature, while a positive entry records the statically bounded character count plus one. Variable loads and Action results clear that proof; only a proven literal or accepted concat establishes it.

Each concat reserves `4 * (left character bound + right character bound) + 1` bytes, covering UTF-8 code points and the final NUL. A site is accepted only at or below 7,993 bytes (at most 1,998 Kuro characters). The existing shared literal-pool limit of 64 entries and concat-site limit of 32 remain. Exceeding any bound rejects the whole program with empty assembly.

Buffers are distinct static BSS objects, not heap allocations. The previous result is read only as the next expression operand; it is not stored, reloaded, captured, or passed to an Action. With control flow and Action bodies excluded, each accepted static site executes once and cannot re-enter. Bounds are proven before emission, so the generated copy loops cannot overrun their buffers. This slice adds no runtime allocation or allocation-failure path.

## Deliberate exclusions and remaining prerequisite

Shared or dynamic Text loads, variable storage, Action parameters/results/bodies, right-nested concat trees, collections, control flow, mixed kinds, non-`+` operators, embedded NULs in concat operands, over-limit literals/results, and excess pool/site counts remain fail-closed. Safety is not inferred from the Text kind alone. This avoids assumptions about allocator behavior, aliasing, escape lifetimes, reentrancy, and failure semantics.

The complete compiler artifact still does not generate native assembly. The rebuilt Python/toolchain-blocked audit observed 9,119 artifact lines, 73 `BC_FUNC_BEGIN` markers, and 294 `BC_CALL_BEGIN` markers; the authored native generator returned its normal rejection status 1 with empty stdout/stderr. The immediate admission ceiling remains 4,096 tokens, so the full compiler artifact is still too large for this generator. Beyond a bounded large-program admission/scanning strategy, native support for the compiler's shared/dynamic Text and Action paths requires a consistent storage/allocation and failure contract plus alias/lifetime/reentrancy proofs. This increment does not type `RecordDiag.Message` as Text and does not remove Python-seeded image construction or Clang/LLVM assembly/linking. Hosted/IR native backends retain their own allocation behavior; this change does not alter them.

## Verification results

- Focused final concat/call-result regressions: 15 passed, 1 platform-gated skip.
- Complete `tests/self_host/test_native_codegen.py`: 220 passed, 21 skipped. The three target assembly checks passed; Linux x86-64 native execution passed with Unicode and multiple independent chains. ARM64 macOS runtime remains gated to a matching runner.
- Full repository suite: 2,717 passed, 23 skipped.
- Fresh hosted-bootstrap rebuild of compiler, runtime, bytecode launcher, and codegen images for x86-64 Linux passed.
- The bootstrap-gap audit passed with Python and toolchains blocked. It confirmed a small native codegen control succeeds while the 9,119-line full compiler artifact fails normally with no partial assembly.
- The Python/toolchain-blocked smoke passed for runtime, compiler, bytecode launcher, and codegen. Stage 1 matched stage 0 on a probe, reproduced the full compiler bytecode, rejected non-Text `Length`, and preserved Text `Length`.
- Independent safety review found no blocker. It specifically checked stack provenance resets for variable loads and Action results, the plain Text-returning Action rejection test, cumulative bounds, and reuse of the result-length scratch value.

No generated `dist/` artifacts are part of this increment; the rebuilt tracked outputs were restored after verification.
