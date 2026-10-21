# All-path Decimal joins inside exact-once Repeat

This increment extends [PR #78](https://github.com/Shibukedang27/Kuro/pull/78), whose open/unmerged head `a7cb1ca4e3ff1aba2e0747623e3680e57bfb3a0c` was verified with all eight checks successful before editing. It composes the existing nested If proof with the existing exact-once Repeat proof. It does not add general loop definite assignment or finish strict independence.

## What changes

A function-free, top-level literal `Repeat 1` may now initialize a named Decimal through a complete `If/Else` tree in its body, not just through a direct body store. Every normal branch path must establish the same Decimal representation before the value is read or the branch joins. For example:

```text
Repeat 1;
    If 1 is equal to 2;
        Balance = 1.25;
    Else;
        Balance = 2.5;
    Done.
    Add 0.5 to Balance;
Done.
Print Balance.
```

This prints `3.0`. Nested If-only trees work too. Existing same-kind mutations, established-slot one-sided branches, direct body initialization, sibling loops and post-loop reads remain supported.

## Why this is bounded and safe

The unchanged Repeat provenance rule requires adjacent parsed `BC_CONST`, exact Integer `1`, and `BC_REPEAT_BEGIN`, with one operand on entry. The private counter therefore enters the body exactly once on normal execution. There is no second body entry whose kinds need unification, and no zero-iteration normal exit.

Within that body, only If-only descendants gain branch initialization permission. Existing per-If entry snapshots are restored before emitting the Else arm; then/else kind facts are checked at every join. An absent Else uses the entry facts rather than the then-arm emission state. Unknown reads in eligible branch frames remain rejected. A fresh Decimal established in only one path fails immediately at that join, even if a later store would overwrite it. The complete join makes the kind available to subsequent body statements and, because the body executes once, to normal post-loop reads.

Snapshot creation and frame use share the same eligibility rule. The outer exact-once flag must be active, Repeat depth must be exactly one, While depth zero, and control-flow depth must equal If depth plus one. A nested Repeat or While therefore cannot inherit the permission, even when the nested Repeat also has literal count one. Closing a nested region restores the outer eligibility; closing the outer Repeat clears it. The frame storage is indexed by If depth, not total region depth, so the extra outer Repeat does not consume an If snapshot frame.

No emitted branch/loop instructions, loop-counter layout, runtime semantics, operand-stack joins, Action ABI or representation-conflict checks are changed. Existing raw region-order validation still rejects crossed delimiters. Abrupt unsupported exits still fail closed.

## What remains rejected

Zero, negative, multitrip, variable, computed and non-Integer Repeat counts gain no fresh Decimal support. Neither do Repeat under an If, any fresh initialization inside a nested Repeat/While, Action-containing programs, new `_` kind joins, mixed representations, early reads or nonempty statement-boundary stacks. Integer-only legacy behavior is not generalized into a Decimal proof.

The existing per-construct bounds remain: 16 If frames, 16 Repeat frames, 16 While frames, 64 global slots and 4096 bytecode tokens. One outer Repeat plus 16 If frames is supported; this is not a new combined-depth limit. Invalid bytecode must set `NativeFailed` and leave no assembly.

The [negative-count and While-cap discrepancies](native-exact-once-repeat.md#actual-loop-behavior) remain unchanged. General multitrip/skippable loops still need explicit entry, backedge, exit and use-site facts. Action-shared Decimal storage, result/value-stack joins, full clean-checkout Python-free compiler/runtime rebuilding and repository-owned assembly/linking remain unfinished.

## Verification

The [new regression module](../../tests/self_host/test_native_repeat_branch_joins.py) runs all eight depth-three branch outcomes, multiple fresh slots, arithmetic inside and after the loop, signed zero, and established-slot one-sided mutation through the hosted interpreter and Kuro VM. It executes generated Linux images and cross-assembles all eight outcomes for Linux x86-64, macOS x86-64 and macOS ARM64.

Raw tests cover the two newly valid old shapes, nested-region eligibility restoration and sibling frame reset. The inherited unsafe branch corpus is also tested inside an exact-once Repeat, together with complete branches under invalid loop counts/contexts, prior reads, stale flags/snapshots and crossed If/Repeat delimiters. The previously rejected complete nested branch under `Repeat 1` is migrated to explicit positive coverage, while its `Repeat 2` counterpart remains negative. No unsafe rejection is removed without replacement.

The [shared freshly compiled Kuro generator gate](../../tests/self_host/test_native_codegen.py) executes all eight new source outcomes, all new positive raw cases and the 16-If/64-slot boundary; it rejects depth 17, slot 65 and the entire new negative corpus. That gate also retains all earlier storage, control-flow, branch and Repeat tests. Its Linux execution is local; genuine Darwin execution belongs to macOS CI, not cross-assembly.

The focused fresh-generator/bounds/inherited-regression gate passed **194 tests in 101.38s**. The full local suite passed **1,250 tests, with 20 skipped, in 521.28s (8m41s)**. These runs overlap and their counts must not be added. Independent read-only design and final-diff reviews found no actionable correctness or coverage issues. `git diff --check` is clean.

```sh
.venv/bin/python -m pytest -q tests/self_host/test_native_repeat_branch_joins.py tests/self_host/test_native_loop_init.py tests/self_host/test_native_branch_joins.py tests/self_host/test_native_codegen.py::test_kuro_owned_x86_linux_codegen_runs_decimal_storage tests/self_host/test_native_codegen.py::test_kuro_native_codegen_keeps_if_depth_limit_at_sixteen tests/self_host/test_native_codegen.py::test_kuro_native_codegen_keeps_global_slot_limit_at_sixty_four tests/self_host/test_native_codegen.py::test_kuro_native_codegen_enforces_exact_4096_token_boundary tests/self_host/test_native_codegen.py::test_native_codegen_source_emits_with_macos_arm64_backend --durations=10
.venv/bin/python -m pytest -q --durations=20
```

Acceptance requires all eight CI checks on the documentation-updated final review head, confirmed in the PR check record before delivery. Pending, cancelled, failed or earlier-head checks do not satisfy acceptance. The review PR must stay open/unmerged and stacked directly on #78. This document does not claim a future CI outcome.

## Next path

Keep the current no-backedge proof narrow. Before admitting any multitrip or potentially skipped loop, define explicit loop-entry, backedge, exit and use-site facts and test both zero-trip and repeated-entry behavior. Resolve negative-count semantics separately rather than claiming broad cross-backend parity. Strict independence remains an ongoing project, not a completed milestone.
