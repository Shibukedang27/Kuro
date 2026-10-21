# Indexed state in the bounded Kuro loop analyzer

This test-only increment stacks on [PR #86](https://github.com/Shibukedang27/Kuro/pull/86), inspected open and unmerged at `155b44fd676d91113684ab8e9ab1fc6342c008e6`, with all eight checks successful. The [Kuro analyzer](../../tests/self_host/loop_use_flow.kuro) replaces four physical mask components and four name fields with explicitly bounded indexed storage for **16 distinct exact names**. Production compiler/runtime code, production acceptance and CI configuration are unchanged. Strict compiler/runtime/toolchain independence remains unfinished.

## Larger state, unchanged write language

Exact identifiers still follow `[A-Za-z_][A-Za-z0-9_]{0,31}`, excluding the reserved `BC_` namespace. Both reads and literal stores participate in dry-pass discovery. Repeated names reuse the same index; a seventeenth distinct name rejects, including in an unreachable arm or zero-trip body. The complete identity mapping is frozen before evidence emission. This capacity is separate from the production generator's 64-global-slot limit.

The accepted input language remains optional literal stores followed by one literal-count Repeat (0–9), containing literal stores, immediate LOADVAR/PRINT observations and literal-condition If/Else statements. Both arms are conservatively visited. The 128-token and 16-nested-If bounds remain. Copies, general expressions, nested/additional loops, computed counts and all other operations remain rejected; no production permission is inferred from this analyzer.

## Explicit indexed snapshots, not aliased vectors

The name and mask collections each have exactly 16 logical cells. All masks begin at unknown `1`, including cells whose names have not yet been discovered. Snapshot storage has 17 depth rows, four kinds per depth and 16 slots per kind: **1,088 numeric cells**. Its offset is `(depth * 4 + kind) * 16 + slot`. Depth zero/kind zero stores prefix state. Active If depths 1–16 use kinds 0, 1 and 2 for entry, Then and Else; the fourth kind is reserved padding. These ranges are disjoint. All snapshot cells are initialized to unknown before parsing.

Save, restore, copy and join helpers check depth, kind, slot and flattened offsets against their logical bounds before indexing. The ordinary mask helpers reject negative and one-past-capacity indices. Snapshot operations visit all 16 cells, not just currently discovered names. They copy numeric elements explicitly; assigning one collection variable to another would alias in the interpreter and is not a valid snapshot implementation. Native collection bounds do not replace the Kuro-owned logical checks.

On entering an If, save entry. After Then, save Then. Before Else, restore entry; without Else, explicitly copy entry to the Else row. Join Then and Else pointwise into the live mask vector. Nested Ifs use distinct depth rows; helpers do not call sequence evaluation, so their shared numeric scratch cannot be overwritten by a recursive branch traversal. Depth-specialized sequence parsers remain, avoiding a separate proof about recursive action-local storage. The global name table is never restored with state.

A name first discovered after an enclosing snapshot therefore already has an unknown cell in that snapshot. Restoring an Else cannot leak a Then write. Dry-pass mutations are discarded by restoring the complete prefix row before execution, preserving prefix-written masks while body-only names start unknown. Fixed storage is materialized with bounded initialization loops before analysis; this does not bound the external token transport or native backing allocation.

## Why two analyzed trips still suffice here

For each fixed physical component, a complete-body transfer remains either `F_s(S) = C_s` or `F_s(S) = S_s union C_s`. Literal overwrites cannot read another slot. Composition and conservative pointwise branch union preserve this restricted form, giving `F(F(S)) = F(S)`. Thus every trip after the first has the same abstract incoming vector as trip two. Indexed addressing changes storage, not the transfer language or convergence argument.

Evidence remains keyed by raw load PC, exact name and entry/backedge origin, with masks `?=1`, Integer `2`, Decimal `4`, and zero for unreachable. A later write cannot repair an earlier use. Zero-trip loads have zero evidence at both origins; one-trip loads have zero backedge evidence. Full validation precedes any USE or decision output, so malformed or over-capacity input rejects without partial evidence.

## Validation and publication

The focused analyzer/fresh-generator gate passed **430 tests in 277.71 seconds**. The complete local suite passed **1,486 tests / 20 skipped in 782.24 seconds**. The new indexed regression module independently passed **15 tests**. Python 3.10 syntax parsing of both changed Python modules and `git diff --check` passed. Counts overlap; native execution tests are platform-gated.

Independent implementation review found no analyzer soundness blocker. An independent high-index nested witness with all 16 prefix names produced Else-read entry/backedge masks `2/6` and post-join masks `6/6` for physical slot 15. A second review confirmed every indexed helper rejects negative/one-past-end slot, depth and kind boundaries. Valid save/restore probes recovered slot 0 mask `2` and slot 15 mask `4`; flattened cells 0 and 1,087 remained distinct, and a depth-16 join produced mask `6` without error. Its representative 16-slot hosted-native image returned zero with empty stderr and complete stdout parity, matching 32 hand-expected evidence records and a successful decision.

The first focused run had **424 passes / 6 failures**, all in new fixtures: five finite-path cases exceeded 128 tokens, and a capacity test incorrectly treated the spelling `slot16` alone as overflow without 16 preceding distinct names. The fixtures were corrected, not the analyzer widened: finite paths now stay within the token budget and unprefixed names start unknown. Hand-checked nested writes/restoration at physical indices 4–7 were added. The corrected focused and full gates above completed successfully; the implementation was unchanged by these repairs.

Publication is verified only once all eight checks succeed on the exact final documentation-updated head; the PR metadata records that immutable SHA and outcome. Earlier-head results are not sufficient. This PR and its predecessors must remain open and unmerged.

The [indexed regressions](../../tests/self_host/test_native_indexed_slot_flow.py) supplement the existing analyzer, dynamic-name and production regression suites. They exercise beyond-four identities, independent masks, capacity and overflow, snapshots, finite-path evidence, malformed input and hosted-native parity. Fresh-generator probes retain existing Decimal execution, depth/global-slot/token boundaries and ARM64 source emission.

## What this does not establish

The hosted Python compiler/interpreter remain trusted. Hosted-native analyzer execution tests that hosted backend, not the Kuro-owned generator's ability to compile the analyzer. The fresh-generator probes cover existing production behavior, not an independent clean-checkout Python-free bootstrap. Native C-string/arbitrary-byte input safety and independently bounded token transport remain unproved. The analyzer uses fixed logical arrays atop the hosted runtime's backing storage; it does not introduce a new standalone memory allocator.

The next narrow path is to establish the indexed analyzer's execution through the Kuro-owned generator, or another separately reviewed reduction of its hosted dependencies, while preserving this restricted transfer language. Copies or general expressions require a new convergence argument or monotone CFG/worklist machinery with evidence that changes after trip two; production changes additionally require storage, stack, exit-representation and integration proofs.

The subsequent [actual-generator boundary regression](native-analyzer-generator-boundary.md) submits the complete analyzer artifact to a fresh native Kuro generator and records rejection, not analyzer execution. It identifies size and collection-lowering gaps without widening production acceptance.

## Reproduce

```sh
.venv/bin/python -m pytest -q \
  tests/self_host/test_native_indexed_slot_flow.py \
  tests/self_host/test_native_dynamic_slot_flow.py \
  tests/self_host/test_native_loop_use_flow.py \
  tests/self_host/test_native_loop_obligations.py \
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
git diff --check
```
