# Preserve Integer scanner-frame kinds on ARM64

> **Later cumulative status:** [The stack reconciliation](semantic-bootstrap-reconciliation.md) records #109 at `5af148a8272dfa40fb6445ba5f5b305c68672dcf` with all eight checks successful. #107/#108 remain open/draft and unverified at their own unchanged heads. Historical blocker and pending-gate language below describes this record’s original checkpoint, not the current cumulative tip.

**DRAFT — not verified until all eight CI checks pass on the exact final documentation-updated head. Do not merge.** This increment is stacked on open, draft [PR #108](https://github.com/Shibukedang27/Kuro/pull/108), exact parent `a97687859e9669745c39e7ddf1eeb2f8938f741b`. Its parent, draft [PR #107](https://github.com/Shibukedang27/Kuro/pull/107), remains historically unverified at `1dc7eebadd042175eb9bd54eba824ead545601df`. The latest previously verified base is open [PR #106](https://github.com/Shibukedang27/Kuro/pull/106), `f3b053c987524d0ee1807464198ca236c52468df`. This work is [PR #109](https://github.com/Shibukedang27/Kuro/pull/109). No ancestor is rewritten, promoted, or merged.

## The actual blocker

The ARM64 dynamic emitter initialized every collection's element kind to Text. Its later `setdefault` calls could not refine an existing entry. Consequently the explicit `LCFrameAction is Integers` declaration was lost: `Get LCFrameAction LCFrameTop` propagated Text into `LCActionStart`, then `LCParamPos`. The unchanged numeric `ADD` guard rejected `Add 1 to LCParamPos` while generating assembly for the complete authored compiler, before assembly or linking and independently of the VM decoder.

The [decoder increment's evidence](vm-single-character-decode.md) remains a record of that exact parent's failures. This repair is separate, not a retroactive claim that #107 or #108 was verified.

## The narrow correction

The hosted frontend does not enforce homogeneous element types on every `Append` and `Set`. Simply labeling Integer collections numeric would let a Text pointer reach integer arithmetic. Checking only the last linear value kind also misses contamination on another branch or a later loop iteration.

[The ARM64 emitter](../../compiler/native.py) therefore proves write provenance **only to select a new numeric initial kind**. Eligible owners must already be allocated collections with resolved `Integers` metadata. That metadata includes explicit declarations and hosted inference from assignments; neither is sufficient write-safety evidence by itself.

The proof unions all definitions, including branch alternatives, collection `APPEND`/`SET`/`STORE_LIST` writes, direct-call arguments and returned values. A dependency fixed point preserves numeric frame cycles while removing Text and unsupported/unknown dependencies. It does not guess a numeric kind from a parameter's spelling. The accumulator `@_` is used only with a known producer in the same straight-line block; control-flow boundaries, calls and untracked accumulator mutations discard that knowledge. Untracked indirect action arguments conservatively invalidate parameter provenance.

**A failed proof retains the exact parent's Text fallback; it does not reject unrelated collections or entire images.** Existing later literal `STORE_LIST` refinement also remains unchanged. This is not a new global element-write policy or a repair of all inherited malformed-write limitations on already-admitted literal collections. In particular, the mixed-write literal-owner regression proves that no new numeric seed is inferred, not that the old literal-refinement path has acquired a new rejection rule.

The complete compiler proves exactly `LCFrameAction` and `LCFrameRepeat` numeric through the new initial-kind path. For newly numeric append-owned paths, Text or unknown writes prevent the refinement and the original numeric `ADD` guard still rejects the cursor increment. Text, Decimal, Symbols and owners without resolved Integer metadata gain no numeric admission. Bounds, capacities, parser and authored compiler/VM source are unchanged. Existing unsupported-alias diagnostics remain first, including source bindings such as `t0` whose spelling can collide with a temporary.

## What CI caught and why the candidate changed

The first #109 code-and-documentation head, `202e995d55075da53856867507d044aca6ad411e`, passed Linux local gates but **failed macOS CI**. The [Python 3.11 job](https://github.com/Shibukedang27/Kuro/actions/runs/39839246340/job/120035596161) reported **13 failed, 1,961 passed, 385 skipped, 29 errors**. An unconditional rejection of every unproven Integer owner was too broad for unrelated VM collections. Runtime, launcher and composed image construction failed with `native Integer collection writes require proven numeric values`.

That global rejection was removed rather than weakening the numeric proof or ADD guard. Only proven owners gain a new numeric initial kind; all others retain the parent behavior. Four assembly-generation regressions now cover the complete production runtime, compiler, bytecode-launcher and code-generator source compositions without requiring a macOS linker. This specifically catches the compatibility gap that Linux executable tests had missed.

## Exact-parent evidence

In a detached worktree at exact parent `a97687859e9669745c39e7ddf1eeb2f8938f741b`, with only the new test file copied in, the six original positive/admission tests give **2 failed, 4 passed**: the small declared-Integer cursor witness and the complete compiler both fail with `native dynamic ADD requires numeric operands`. The candidate passes both. This uses the complete production compiler, not a reduced scanner.

The corrected candidate emits **byte-identical ARM64 assembly to the exact parent** for all three unaffected production compositions: runtime, bytecode launcher and code generator. The compiler, whose parent cannot emit assembly, succeeds. Running the four production-composition regressions on that exact parent gives **1 failed, 3 passed**, with only the compiler failing at the inherited ADD guard. The already-admitted inferred Integer literal-owner witness also emits byte-identical assembly on parent/candidate, SHA-256 `bebfa453340c31c26e22bb3956e90d1622f132a88df1bc73f5b59b16189b05e3`. These are assembly comparisons, not executable runtime-parity claims.

[Regressions](../../tests/compiler/test_arm64_collection_kind.py) assert the actual compiler IR declaration, frame GET and cursor ADD, successful complete compiler assembly, and both proven scanner-frame owners. Removing only `LCFrameAction`'s metadata recreates the old ADD failure; replacing the Integer increment constant with Text still fails that same guard. Negative append-owned witnesses cover Text append/set, branch joins, later writes, action writes/returns, indirect closure arguments and input. Decimal and metadata-absent cases retain their previous rejection. Inferred literal owners have dedicated positive/no-new-seed cases.

Focused final narrowed candidate gate: **26 passed, 76 deselected**, including all four production image compositions and existing ARM64/suffix cases. All four complete production ARM64 assemblies cross-assemble with `clang -target arm64-apple-macos11 -c` into Mach-O ARM64 objects. Neither generation nor object construction proves ARM64 executable runtime parity.

## Final local gates and independent review

- Final narrowed frozen-code full suite: **2,372 passed, 20 skipped**. This includes all **21 new regression cases**, including the four complete ARM64 production-source compositions.
- Final focused ARM64/suffix gate: **26 passed, 76 deselected**.
- Fresh detached exact-parent worktree with only the final behavioral patch and tests: **113 passed** for the new ARM64 regressions and native collection-bounds suite.
- Unchanged fresh whole-compiler bytecode self-reproduction and complete **272-literal initializer** gate: **passed** separately. No reduced source, smaller initializer or enlarged arena replaces it.
- All four production images rebuilt in that fresh worktree using the hosted bootstrap: compiler, runtime, bytecode launcher and code generator.
- `python_free_native_smoke.sh` using those fresh images: **passed**, including full **9,118-value** compiler-bytecode reproduction, frontend non-Text Length rejection and Text acceptance, with Python and compiler toolchains absent from PATH.

These are the final narrowed candidate's rerun results, not results borrowed from the over-broad first candidate. All eight final-head CI checks remain a separate requirement.

The initial independent safety review approved the provenance/alias model. A scope follow-up requested explicit coverage of inferred Integer metadata; that clarification and regression pair were approved. The later CI-discovered fallback correction received its own independent **approval**, with no blocker found and all **21 new regression cases** independently passing. That review did not certify the eight-check CI gate.

An early development run was invalidated by editing source while source-inspection tests were running; it is not counted. Two diagnostic-order regressions for unsupported `t0` aliases found during development were corrected without admitting those aliases. All final full-suite runs keep code frozen.

## Remaining work and limits

Eight successful checks must belong to the exact final documentation-updated head; earlier code-only, failed-candidate or ancestor results do not count. Ancestors remain open/unmerged with their inherited draft history even if this descendant clears the blocker. Linux generation, cross-assembly and emitted-byte comparisons are not ARM64 execution claims.

After the prerequisite clears CI, reconcile descendant reproduction evidence with the draft frontend's historical blockers before another semantic rule. Full resolver/typechecker integration, unknown aliases/shape inference and reference-validator scope differences remain separate. Parent aggregate-storage and arena limits are not increased. The x86-64 emitter function source and all authored `self_host` source remain unchanged.

Strict independence remains unfinished: **Python seeds production images; Clang/LLVM assemble and link them.** Blocked-toolchain execution after fresh seeding verifies continuity, not Python-free construction from a clean checkout.
