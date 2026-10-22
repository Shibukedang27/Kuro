# Reuse one-character constants during VM decoding

**DRAFT / BLOCKED — local Linux gates pass; cross-platform CI has failed. Not verified; do not merge.** [PR #108](https://github.com/Shibukedang27/Kuro/pull/108) is stacked directly on draft, open [PR #107](https://github.com/Shibukedang27/Kuro/pull/107), exact parent `1dc7eebadd042175eb9bd54eba824ead545601df`. That parent remains unverified and unchanged. Its verified predecessor is open [PR #106](https://github.com/Shibukedang27/Kuro/pull/106), `f3b053c987524d0ee1807464198ca236c52468df`. All PRs remain open and unmerged.

## The small change that unblocks reproduction

[VMDecodeConstant](../../self_host/vm.kuro) already knows the input length. When it is exactly one character, the original Text is itself the whole character: pass it directly to `VMDecodeDigit` rather than extracting another Text with `Get Value 0`. A failed single-character digit returns the original Text immediately instead of scanning it again. No other decoder path changes.

Digits still return the same Integer. A non-digit returns every original byte unchanged, with `VMNumericOk = 0`, `VMDecodedFloat = 0`, and empty `VMDecodedDisplay`. These last two are reset at entry. The single dot is still malformed Text, not a new accepted decimal: the parent temporarily enabled its float flag during the redundant scan but reset it before returning. Empty input preserves the inherited numeric flag, just as before. Multi-character numbers, malformed text, repeated dots and existing display spellings retain the parent algorithm, including its existing quirks; this is not a syntax cleanup.

The original input already has a valid lifetime for the parent decoder's malformed return. Reusing it neither mutates storage nor introduces a borrowed pointer to a new temporary. Hosted Text length counts Unicode characters; native Text length counts UTF-8 bytes. A native multi-byte character therefore still uses the unchanged multi-character path. No encoding conversion or truncation is introduced.

The native `Get` implementation allocates two character-arena bytes per extracted byte. Single-byte digits previously extracted once; single-byte non-digits extracted twice. This fast path needs neither extraction. Removing those allocations intentionally removes their possible arena-exhaustion failure. It does **not** promise identical failure at the same resource-consumption point; that would contradict an allocation reduction. Decoded results, ordinary malformed-input behavior, outputs and existing bounds/capacity checks are preserved. No ceiling, VM operation, Repeat behavior, parser admission rule or native emitter is changed.

## Evidence against the exact parent

The unchanged fresh test `test_fresh_bytecode_stage_compiler_reproduces_self_and_large_initializer` fails on the exact parent with exit 1 and empty stdout/stderr during the full compiler self case. A scratch-only symbolized launcher, with the original arena sizes and generated instructions, stops at the overflow handler with the character cursor at **2,097,150**, the inherited guard for the 2,097,152-byte arena. Debugger symbol changes are not production changes.

With only the decoder patch applied, the same fresh test passes both full compiler-bytecode self-reproduction and the complete 272-literal initializer witness. No partial source, reduced initializer or higher budget replaces that gate.

The candidate's scratch-only symbolized launcher completes the full self case with exit 0, **870,724 character-arena bytes** and **2,192,152 text-join-arena bytes** consumed. Its stdout is byte-identical to stage 1. These are separate arenas, with unchanged capacities of 2 MiB and 16 MiB respectively; the numbers are not an increase to either budget or a prediction for arbitrary future source.

The parent's directly compiled full compiler bytecode and the candidate's are byte-identical: **9,118 tokens**, SHA-256 `ba848047248d8f4af2f3bd7661ef064d8b0234f8a4196b1b2134148b3a1f2a09`. Complete `(exit, stdout, stderr)` comparisons also match for Integer arithmetic, Decimal spelling, UTF-8 Text Length, the 272-literal initializer, and known non-Text Length rejection.

[Decoder parity regressions](../../tests/self_host/test_vm_decode_allocation.py) retain an inline exact-parent reference so CI does not depend on Git history or an external checkout. They compare successful and malformed decoding, flags, original input and retained results. The corpus deliberately preserves the inherited repeated-dot acceptance rather than quietly changing it.

## Local gates and independent review

- Full local suite before the new parity file was collected: **2,349 passed, 20 skipped**. The parity file is also run separately; its outcome is not silently included in that count.
- Fresh whole-compiler/272-initializer gate: **passed** on the candidate, **failed** on the exact parent.
- All four production images rebuilt in a fresh exact-parent worktree with only the decoder patch: compiler, runtime, bytecode launcher and code generator.
- `tests/self_host/python_free_native_smoke.sh` using those fresh images: **passed**, including complete compiler-bytecode reproduction, frontend non-Text rejection and Text acceptance, with Python and compiler toolchains absent from PATH.
- Parity regressions plus the existing artifact-launcher suite: **43 passed**. Fresh native parent/candidate production-composed launchers compare complete UTF-8 output bytes, decoded result spelling, original input, numeric/float flags and decimal display. Hosted assertions retain results across later calls; isolated native cases use one decode per process to avoid relying on inherited native action-frame reuse behavior. Full self-reproduction separately exercises repeated decoding in the production route.
- Independent implementation review: **approved**, with no blocking decoder regression found. Its non-blocking request for stronger native returned-value/display assertions was addressed before the final push.

These are local results, not a substitute for the required **eight successful checks on the exact final documentation-updated head**. Until that gate is confirmed, this increment and dependent Length work are not marked verified. The historical failure record in the parent's frontend note remains accurate for that parent; this note describes the separate descendant fix.

## Why this remains blocked

CI on code-and-documentation head `a97b66ace0644c75db93a0bab5bedc685020c996` failed the macOS suite. [Python 3.11 job](https://github.com/Shibukedang27/Kuro/actions/runs/39831768590/job/120009462318) reports **3 failed, 1,983 passed, 385 skipped**. The failures are `test_native_backend_runs_kuro_authored_compiler_probe`, `test_native_compiler_image_compiles_arbitrary_source_from_stdin`, and `test_native_compiler_matches_kuro_authored_driver`. ARM64 assembly generation raises `NativeBackendError: native dynamic ADD requires numeric operands` at `compiler/native.py:568`; this is not a decoder-test assertion or a linking failure.

Independent investigation reproduced the identical failure from the exact parent without a macOS linker: compile `native_compiler_source()` to IR, then call `emit_macos_arm64(result.ir)`. The offending instruction is `ADD LCParamPos t533`; the literal operand is numeric, but `LCParamPos` is incorrectly inferred Text. `LCFrameAction` is explicitly declared `Integers` in `lengthcheck.kuro`, yet the ARM64 emitter infers its element kind as Text. That kind flows through `Get LCFrameAction LCFrameTop` into `LCActionStart`, then `LCParamPos`, whose numeric increment is rejected. The numeric ADD guard is not bypassed.

The [exact parent's own macOS job](https://github.com/Shibukedang27/Kuro/actions/runs/39828484334/job/119998007065) reports the same three failures. The decoder patch cannot repair this: native compiler composition includes lexer, parser, Length checker, lowerer, encoder and compiler, **not the VM**. `compiler/native.py`, `compiler/self_host.py` and `self_host/lengthcheck.kuro` are unchanged from the parent. The final follow-up commit only records this blocker; no implementation repair or eight-check success is claimed for its updated head.

## Limits and next path

The parent's aggregate collection accounting predicted only **55 spare entries** under the unchanged 65,536-entry backing-store limit. This patch does not alter compiler source/bytecode or add scanner metadata, so it is not a new aggregate-storage budget for more semantic passes. Character-arena relief likewise is not permission to broaden validation without fresh accounting.

The next prerequisite is a separately scoped ARM64 element-kind propagation regression/fix preserving declared numeric collection kinds through GET, including the exact parent compiler's assembly-generation witness. Preserve numeric ADD admission, all ceilings and malformed-input behavior; do not weaken the gate or silently fold that emitter repair into this decoder change. Rerun full fresh reproduction and all eight checks on its final documentation head before marking dependent work verified.

After that gate passes, reconcile the descendant evidence with the draft frontend's historical blocker before advancing any additional semantic rule. Full resolver/typechecker integration, unknown aliases/shape inference and reference-validator scope differences remain separate. Strict independence is still unfinished: **Python seeds production images; Clang/LLVM assemble and link them**. Blocked-toolchain use after seeding is continuity, not Python-free clean-checkout construction.
