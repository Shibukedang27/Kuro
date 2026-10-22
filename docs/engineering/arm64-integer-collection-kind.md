# Preserve Integer scanner-frame kinds on ARM64

**Candidate — not verified until all eight CI checks pass on the exact final documentation-updated head. Do not merge.** This increment is stacked on open, draft [PR #108](https://github.com/Shibukedang27/Kuro/pull/108), exact parent `a97687859e9669745c39e7ddf1eeb2f8938f741b`. Its parent, draft [PR #107](https://github.com/Shibukedang27/Kuro/pull/107), remains historically unverified at `1dc7eebadd042175eb9bd54eba824ead545601df`. The latest previously verified base is open [PR #106](https://github.com/Shibukedang27/Kuro/pull/106), `f3b053c987524d0ee1807464198ca236c52468df`. No ancestor is rewritten, promoted, or merged by this change.

## The actual blocker

The ARM64 dynamic emitter initialized every collection's element kind to Text. Its later `setdefault` calls could not refine an existing entry. Consequently the explicit `LCFrameAction is Integers` declaration was lost: `Get LCFrameAction LCFrameTop` propagated Text into `LCActionStart`, then `LCParamPos`. The unchanged numeric `ADD` guard rejected `Add 1 to LCParamPos` while generating assembly for the complete authored compiler. This happened before assembly or linking and independently of the VM decoder.

The [decoder increment's evidence](vm-single-character-decode.md) remains a record of that exact parent's failures. This repair is deliberately separate, not a retroactive claim that #107 or #108 was verified.

## Why a declaration alone is not enough

The hosted frontend does not currently enforce homogeneous element types on all `Append` and `Set` writes. Simply labeling every declared Integer collection numeric would let a Text pointer reach integer arithmetic. Checking only the emitter's last linear value kind also misses a Text value on another branch or a later loop iteration.

The bounded correction in [the ARM64 emitter](../../compiler/native.py) therefore proves write provenance before assigning the numeric element kind. It considers only collections with resolved `Integers` metadata already allocated by the existing collection discovery. That metadata includes explicit declarations and hosted inference from ordinary assignments; it is not by itself write-safety evidence. The proof unions all definitions, including branch alternatives, collection `APPEND`/`SET`/`STORE_LIST` writes, direct-call arguments and returned values. A small dependency fixed point preserves numeric frame cycles while removing Text and unsupported/unknown dependencies. It does not infer a numeric kind from a parameter's spelling or from its declaration alone.

The accumulator `@_` is used only with a known producer in the same straight-line block; control-flow boundaries, calls and untracked accumulator mutations discard that knowledge. Indirect action arguments are not guessed: closure/invocation/spawn presence conservatively invalidates parameter provenance. Unproven declared Integer collection writes are rejected before the existing literal-refinement path can accidentally relabel them numeric.

The complete compiler proves exactly `LCFrameAction` and `LCFrameRepeat` numeric through this path. Text, Decimal, Symbols and collections without resolved Integer metadata do not gain numeric admission. The existing `ADD` numeric guard, index bounds, fixed collection capacities, arena capacities, parser and authored compiler/VM source are unchanged. Existing unsupported-alias diagnostics are checked first, including source bindings whose spelling collides with a temporary such as `t0`. This is neither general type inference nor a new semantic pass.

## Regressions and exact-parent evidence

[The regression file](../../tests/compiler/test_arm64_collection_kind.py) checks the actual compiler IR declarations, frame GET and cursor ADD, successful full ARM64 assembly generation, and both proven scanner-frame owners. Removing only `LCFrameAction`'s declaration recreates the old numeric-ADD failure; replacing the cursor increment's Integer constant with Text still fails that same guard.

Separate negative cases cover Text collection reads, a Text increment, Decimal and undeclared owners, direct Text append/set, branch-join contamination, writes after an earlier read, action-origin writes/returns, indirect closure arguments and input. These tests run without a macOS linker and make no claim of ARM64 execution.

In a detached worktree at exact parent `a97687859e9669745c39e7ddf1eeb2f8938f741b`, with only the new test file copied in, the six original positive/admission tests give **2 failed, 4 passed**: the small declared-Integer cursor witness and the complete compiler both fail with `native dynamic ADD requires numeric operands`. The candidate passes both. This is a production-parent comparison, not a modified scanner or reduced compiler witness.

Focused final candidate gate: **22 passed, 76 deselected** (new regressions plus existing ARM64/suffix tests). Inferred Integer literal owners have a dedicated positive/mixed-write regression pair. The positive literal-owner witness emits byte-identical ARM64 assembly on the exact parent and candidate, SHA-256 `bebfa453340c31c26e22bb3956e90d1622f132a88df1bc73f5b59b16189b05e3`: preserving that already-admitted numeric list is not new admission.

The generated complete compiler assembly also cross-assembles successfully with `clang -target arm64-apple-macos11 -c` into a Mach-O ARM64 object. Assembly generation and object construction are not executable runtime parity; native macOS results must come from CI.

## Local production gates

- Frozen-code full suite: **2,366 passed, 20 skipped**. The final subsequent changes were comment/scope clarification and the two inferred-owner tests, which are included in the separate final **22-pass** focused result above, not silently added to the full-suite count. No production behavior changed after the frozen full run.
- Clean-process focused regressions, closure source-inspection audits and native collection-bounds suite: **133 passed**.
- Fresh detached exact-parent worktree with the final behavioral patch: new ARM64 regressions plus collection-bounds tests **107 passed**; the unchanged complete compiler-bytecode self-reproduction and full **272-literal initializer** test **passed** separately.
- All four production images rebuilt there from scratch with the hosted bootstrap: compiler, runtime, bytecode launcher and code generator.
- `python_free_native_smoke.sh` using those fresh images **passed**, including complete **9,118-value** compiler-bytecode reproduction, frontend non-Text Length rejection and Text acceptance, with Python and compiler toolchains blocked from PATH.
- Independent safety review approved the provenance and alias-preflight implementation. Its separate scope-contract request—explain inferred Integer metadata and test it—was addressed by the final comment/documentation clarification and regression pair. Final independent follow-up **approved** that correction and independently ran all **17 new regression cases** successfully; it did not certify CI.
- The x86-64 Linux and macOS emitter function source and all authored `self_host` source remain byte-identical to the exact parent.

Superseded declaration-only experiments are not evidence for the final implementation. An earlier full run was invalidated by editing source while source-inspection tests were running; its results are not counted. A clean-process rerun exposed two diagnostic-order regressions for unsupported `t0` aliases; both were corrected without admitting those aliases. The successful full run used frozen code.

## What remains unfinished

Eight green checks must belong to the exact final documentation-updated head; earlier code-only or ancestor results do not satisfy that gate. Ancestors remain open/unmerged with their inherited draft history even if this descendant clears the blocker. No executable ARM64 runtime parity is claimed from Linux assembly generation or object construction.

After this prerequisite clears CI, reconcile descendant reproduction evidence with the draft frontend's historical blockers before advancing another semantic rule. Full resolver/typechecker integration, unknown aliases/shape inference, and the reference-validator scope differences remain separate work. The aggregate-storage and character-arena limits discussed in the parent note are not increased here.

Strict independence is still unfinished: **Python seeds production images; Clang/LLVM assemble and link them.** Running freshly seeded images with Python and toolchains blocked verifies continuity after seeding, not Python-free construction from a clean checkout.
