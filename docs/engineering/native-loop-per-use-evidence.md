# Keeping loop reads visible through branch joins

This test-only increment is stacked directly on [PR #81](https://github.com/Shibukedang27/Kuro/pull/81), whose open/unmerged head `b70b6e9223f324d128c1d1445a0a227d808bc8a3` was inspected with all eight checks successful before editing. It follows the [direct positive Repeat proof](native-positive-repeat-direct.md#next-bounded-step). No production generator, acceptance flag, runtime or language semantics changes here. Strict compiler/runtime/toolchain independence remains unfinished.

## The important counterexample

Consider an unknown slot read in one branch, followed by an unconditional Decimal initializer later in the loop. The exit is Decimal, and the backedge carries Decimal, but the earlier read still sees an unknown slot on entry. A later store must not retroactively repair that read. Restoring an If-entry snapshot while emitting Else must not erase its evidence either.

The [new witnesses](../../tests/self_host/test_native_loop_use_evidence.py) put that read in then, else, missing-else and nested arms. They also put reads before complete two-arm initializers, before sibling joins, behind an unknown inner Repeat and in a revisited While condition. The current native gate must continue rejecting these cases, including when both final branch arms become Decimal. Safe, previously accepted controls initialize the slot before the reads, or use the already proved exact-once branch rule.

## What the model records

The existing [bounded test oracle](../../tests/self_host/loop_flow_facts.py) first solves its complete structured CFG to a fixed point. Each loop then gets two independent local solves:

1. Seed the loop's entry target with its converged entry-edge state.
2. Separately seed the backedge target with its converged backedge state, if reachable.
3. In each solve, cut that selected loop's backedge and normal-exit edges. Keep nested regions and their cycles, solving them to a local fixed point.
4. Record every static `BC_LOADVAR` in that region by original token PC and slot name, with separate `entry_kinds` and `backedge_kinds`. `None` means that origin cannot reach the use; it does not mean unknown kind. The union is the use's `kinds`. When neither origin reaches a static read, both fields are `None`, their union is empty, and there is no corresponding reachable global load fact.

Facts belong to each read site, not to the eventual slot state. Transfer operations copy their input maps; an overwrite changes its successors, not an earlier read record. Both branch edges remain conservatively possible regardless of the literal condition. There is no mutable branch-snapshot restoration in this model. Its purpose is to state the evidence a future Kuro-owned production analysis must preserve, not to authorize production joins.

For an early read followed by a direct Decimal store, the read gets entry `{?}`, backedge `{D}`, union `{?, D}`. A post-store read gets `{D}` from both origins. Integer entry gives `{I}` versus `{D}` at the early use. A missing initializer path retains unknown evidence. A zero-count body has no reachable uses, and an exact-once loop has no backedge-origin facts. A structurally present backedge nested beneath a zero-count outer loop also has no reachable boundary facts; a regression checks that no evidence is fabricated. While entry/backedge propagation begins at the condition, not just its body.

## Why this remains deliberately bounded

The seeds come from the original merged fixed point. These are **boundary-origin facts**, not an exact unrolling of first and subsequent iterations. An inner loop's entry edge may already merge several outer iterations: its entry-origin read can therefore contain both unknown and Decimal even when the inner loop is exact-once. A dedicated regression makes that distinction explicit.

The union of local per-use facts is **not guaranteed to equal** the original global fact for arbitrary supported arithmetic. Partitioning delays a nonrelational merge. For example, entry `A=I, B=?` and backedge `A=?, B=I` each make `A+B` unknown; the globally merged header can additionally invent the cross-phase pair `I+I`. The local union at a later read of that sum is therefore `{?}`, strictly more precise than the global `{?, I}`. An explicit regression checks this under all four schedules. Neither result is a production acceptance proof; the local union remains conservative for paths in the model, but equality with the less precise global solution is only a checked property of the named dominance/branch corpus below.

The model is nonrelational: it loses correlations between slots, branches and iteration counts. A positive literal loop's global CFG still overapproximates an arbitrary positive number of trips, rather than encoding an exact finite counter. Cutting the selected backedge prevents one local pass from reclassifying recurrent evidence as entry evidence; retaining nested cycles preserves their conservative merges. The finite kind lattice and monotone union joins guarantee termination for the supported equal-height stacks. Unsupported and malformed bytecode retains the prior explicit failures; validation of unreachable operands and general bytecode semantics remain outside the oracle's contract.

This is not a production implementation, a proof of all source programs, a replacement bootstrap compiler or a decision to permit multitrip branch initialization. Action sharing, `_` result-slot changes, stack joins, skipped/runtime loops, nested-loop first initialization and larger-count acceptance stay unchanged. The inherited negative Repeat interpreter discrepancy and While guard discrepancy also remain unresolved.

## Checks that exercise the distinction

The corpus checks separate facts at each early and late read, not just an eventual exit type. For the named old/new loop corpus, it also checks that the union of the two boundary-origin facts reconstructs the original global fact for each regional use; the separate arithmetic precision witness above intentionally does not satisfy that equality. The whole named corpus is solved under FIFO/LIFO worklists and forward/reversed sorted successor order, requiring exact result equality in all four schedules.

An independent finite event interpreter enumerates all arm-choice histories for 100 generated combinations: five then-arm event sequences × five else-arm sequences × two entry kinds × two actual Repeat counts (two and three). It compares the exact entry/recurrent read evidence against the model for this stabilizing subset, without reusing the oracle parser, CFG builder or transfer function. This finite exact match is not a general relational or finite-counter proof.

All 19 new rejection witnesses and three accepted controls run against hosted generation for x86-64 Linux, x86-64 macOS and ARM64 macOS. They are also integrated into the fresh native-generator gate: rejection requires exit 1 with empty stdout/stderr, while accepted controls are compiled, linked and executed with exact output. Existing focused tests retain cross-assembly, region/slot/token limits and the previous acceptance boundaries.

## Reproducing the gates

```sh
.venv/bin/python -m pytest -q \
  tests/self_host/test_native_loop_use_evidence.py \
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

## Next bounded path

Before any production multitrip branch permission, design a Kuro-owned representation of per-use obligations that cannot be restored away with slot-kind snapshots. Show how an entry path containing unknown or conflicting representation rejects that use even when later assignments and every normal exit are Decimal. Check the production representation against these boundary-origin witnesses, keep exact-once and multitrip permission separate, and independently review the resulting invariant before widening acceptance. General loop fixed points and whole-toolchain independence remain separate unfinished work.

## Review and measured results

Independent design review found no mathematical blocker for this bounded boundary-origin model and requested explicit coverage of a structurally present but unreachable nested backedge. That regression now distinguishes absent origin facts (`None`) from unknown kind (`{?}`). A separate exact-diff review confirmed no production acceptance expansion and independently reproduced the arithmetic precision counterexample. The strict-subset regression, corpus-scoped equality assertion, nearby implementation comment and explicit limitation above address that finding rather than assuming a general distributivity property.

Targeted independent re-review confirmed that those exact changes resolve the arithmetic finding, with no remaining blocker in that finding. Final-head CI remains a separate publication gate.

The final local runs passed **232 focused/fresh-generator tests in 155.16 seconds** and **1,288 full-suite tests / 20 skipped in 577.13 seconds**. These runs include the added arithmetic witness. The earlier exploratory focused run was deliberately interrupted to add that witness; it is not counted as verification. `git diff --check` also passed. No production sources changed.

Publication is verified only after all eight CI checks pass on the exact final documentation-updated head. The PR remains open/unmerged; its metadata records the immutable verified head without changing the checked commit.
