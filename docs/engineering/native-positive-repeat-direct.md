# Direct Decimal initialization in a positive Repeat

This increment is directly stacked on [PR #80](https://github.com/Shibukedang27/Kuro/pull/80), whose open/unmerged head `9eaa78604275b4fb771802229eb9289fc39ec353` was inspected with all eight checks successful before editing. It promotes only the direct unconditional store candidate from the [loop-flow witnesses](native-loop-flow-facts.md). It does not finish compiler/runtime/toolchain independence.

## What now works

A function-free program can first initialize a named Decimal slot directly in a top-level `Repeat 2` through `Repeat 9`. The count must be an adjacent parsed `BC_CONST` with exactly one of those canonical Integer tokens. Literal `Repeat 1` keeps its previous behavior, including its separately proved branch joins.

```kuro
Repeat 2;
    Fresh = 1.25;
    Fresh = Fresh + 0.25;
    Print Fresh.
Done.
Print Fresh.
```

This prints `1.5` three times. The initializer executes afresh on each trip; this is not an implicit accumulator or a declaration hoisted before the loop. Several direct initializers may depend on already established Decimal slots.

## Why one traversal is sufficient for this slice

The production proof is Kuro-owned in [native_codegen.kuro](../../self_host/native_codegen.kuro). It is a restricted dominance/invariant proof, not the Python reference model becoming a production pass, and not a general loop fixed-point analysis.

**Entry.** Literal provenance is consumed/reset at each parsed opcode and requires the literal to have been pushed onto an empty stack. The top-level Repeat header rechecks function-free mode, a single Integer count operand and the adjacent-literal flag. Exact canonical counts 2–9 have the same positive representation on all supported targets, guarantee body entry and decrement safely without counter overflow. No constant folding or runtime-bound recovery is used.

**First-entry uses.** Permission is recomputed only for `BC_STORE_LIST` at control depth one, Repeat depth one and If/While depth zero. A previously unknown slot can become Decimal at this unconditional store, but an earlier unknown load fixes its kind to Integer (or fails under the pre-existing eligible branch rules). An Integer or Text slot cannot change to Decimal. Therefore an earlier read, including an earlier read in a nested or skippable region, cannot be rescued by a later store. The value's existing stack-kind checks still apply; no slot is pre-seeded with its eventual kind.

**Backedges.** Once a slot is Decimal, every subsequent store must keep it Decimal. Established Decimal `Add`/`Update` operations keep their existing operand checks. Those mutation opcodes cannot establish a fresh Decimal slot: they never receive the new direct-store permission. Thus each accepted use of a newly initialized Decimal slot is dominated by its direct store on the first trip and on every repeated trip. Uses before that store would require a conflicting earlier kind and cause rejection. The test-only witnesses separately expose entry `{?}`, backedge `{D}`, post-store reads `{D}` and exit `{D}`.

**No forgetting through branches.** The new positive-count active flag is deliberately separate from `NativeRepeatOneActive`. Only the latter can enable If snapshots and all-path branch initialization inside a Repeat. Multitrip branches do not snapshot/reset slot kinds, so a pre-store unknown read cannot disappear at Else. A dedicated regression covers a then-arm read, an Else arm, and a later direct initializer; this must remain rejected even when a later overwrite makes the exit Decimal. Extending snapshot permission would need a separate proof.

**Normal exits.** The positive loop has no zero-trip path. Every normal completion crosses the direct initializer, and the invariant preserves Decimal through the last backedge/test and into post-loop reads. Source has no break/continue; unsupported raw abrupt opcodes and top-level Return remain rejected. Any future abrupt-exit feature must revisit this argument. Nontermination in a nested region does not create a normal exit.

The active flag survives nested regions only so that a later direct outer-body store can be considered. Depth checks prevent nested initialization from inheriting it. Closing the outer Repeat clears it; each sibling top-level Repeat recomputes it. Existing region nesting, empty statement-boundary stacks, 16-frame limits, 64 global slots and the 4096-token limit remain enforced.

## Deliberate exclusions

Zero, negative, dynamic, computed, Decimal and Text counts do not gain fresh initialization support. Neither do noncanonical spellings or positive literal counts outside 1–9. This is a conservative permission boundary, not a claim that larger counts are inherently unsafe. Existing loops over already established Decimal slots retain their previous acceptance.

Fresh initialization under branches, nested loops or While is unchanged; complete branches under multitrip Repeat remain rejected. Action-containing programs, shared Action storage, `_` result-slot kind changes, value-stack joins and mixed representations gain no permission. Existing established-Decimal operations inside nested regions are not new initialization proofs.

The [negative-count interpreter/VM discrepancy and While development guard](native-exact-once-repeat.md#actual-loop-behavior) remain unchanged. Hosted Python bootstrap, clean-checkout Python-free rebuilding, and repository-owned assembly/linking remain unfinished.

## Verification

The [new fixture module](../../tests/self_host/test_native_positive_repeat.py) covers every newly allowed count, dependent slots, reassignment, negative zero, established-slot operations, sibling state, post-loop reads and a source fixture shared by interpreter, Kuro VM and native execution. Its raw rejection matrix includes first-entry reads, Integer-entry/Decimal-backedge conflicts, branch-read forgetting, mutation-before-store, skipped/runtime bounds, noncanonical counts, nested/branch initializers, Actions, `_`, malformed regions, residual stacks and raw Return/break/continue after initialization at counts two and nine. The three old direct `Repeat 2` rejection fixtures are migrated to explicit positive coverage; the formerly inherited exact-once-wrapper/nested-loop variant is retained as an explicit rejection, and unsafe witnesses remain negative.

The [fresh-generator gate](../../tests/self_host/test_native_codegen.py) compiles the modified generator into a native executable, executes all new raw positives and the source fixture, rejects all new unsafe witnesses with exit 1 and empty output, and tests multitrip depth/slot boundaries. Hosted emission cross-assembles for x86-64 Linux, x86-64 macOS and ARM64 macOS. CI additionally executes native ARM64/macOS coverage where available. Final measured local results and review outcome are recorded below.

## Next bounded step

Do not combine branch joins with multitrip permission. First design explicit per-use entry/backedge facts that survive branch snapshot restoration and demonstrate that no earlier read can be erased. An analysis/test increment for that interaction is preferable to widening flags. Larger positive counts can be considered separately with validated literal/range semantics. General loop initialization and full independence remain open work.

## Reproducing the local gates

```sh
.venv/bin/python -m pytest -q \
  tests/self_host/test_native_positive_repeat.py \
  tests/self_host/test_native_loop_flow_facts.py \
  tests/self_host/test_native_repeat_branch_joins.py \
  tests/self_host/test_native_loop_init.py \
  tests/self_host/test_native_branch_joins.py \
  tests/self_host/test_native_codegen.py::test_kuro_owned_x86_linux_codegen_runs_decimal_storage \
  tests/self_host/test_native_codegen.py::test_kuro_native_codegen_keeps_if_depth_limit_at_sixteen \
  tests/self_host/test_native_codegen.py::test_kuro_native_codegen_keeps_global_slot_limit_at_sixty_four \
  tests/self_host/test_native_codegen.py::test_kuro_native_codegen_enforces_exact_4096_token_boundary \
  tests/self_host/test_native_codegen.py::test_native_codegen_source_emits_with_macos_arm64_backend \
  --durations=10
.venv/bin/python -m pytest -q --durations=20
```

The new raw matrix contains 18 positive cases and 42 negative cases, checked against hosted emission for all three targets and against the freshly compiled native generator on the executing host. Publication is not considered verified until all eight CI checks succeed on the exact final documentation-updated head; PR metadata records that immutable head after CI, without changing the checked commit.

## Independent review and local outcome

Independent design review and a separate complete-diff soundness review found no blocker in this restricted permission. Both emphasized that the multitrip flag must never enable If snapshots or branch joins. The exact then-read/Else/later-direct-store counterexample is now a rejection fixture. A subsequent migration/documentation review confirmed that the three formerly rejected direct-store shapes have positive coverage and the nested wrapper remains rejected; its request for explicit multitrip abrupt-opcode tests was addressed at counts two and nine.

The first broad local run exposed one additional legacy direct `Repeat 2` rejection still present in the branch corpus; it was migrated rather than suppressing the failure, and its nested variant was preserved. No production widening was needed to resolve that mismatch. Final reruns with the added abrupt-exit witnesses passed: **216 focused/fresh-generator tests in 143.95 seconds**, and **1,272 full-suite tests passed / 20 skipped in 556.70 seconds**. The focused command includes fresh native generator execution and ARM64/macOS source emission; cross-assembly covers all three targets. `git diff --check` also passed.
