# Independent slot facts in the bounded Kuro loop analyzer

This test-only increment stacks directly on [PR #84](https://github.com/Shibukedang27/Kuro/pull/84), inspected open/unmerged at `dc4a2588b9adc0c547828b430f521912a6c232bd` with all eight checks successful. It extends the [raw-token analyzer](../../tests/self_host/loop_use_flow.kuro) from one slot to four explicitly named slots: `Fresh`, `Other`, `Third`, and `Fourth`. Python still supplies only raw tokens; Kuro validates structure, discovers reads and derives their entry/backedge kind masks. Production compiler/runtime code, acceptance rules and CI configuration are unchanged. Strict compiler/runtime/toolchain independence remains incomplete.

## What the bounded language now accepts

The entire stream consists of zero or more literal stores to the four whitelisted names, followed by exactly one literal-count `Repeat 0` through `Repeat 9`, without trailing instructions. Within the loop, statements are literal stores, immediate `LOADVAR name; PRINT` observations, and literal-condition Ifs with optional Else and nested bodies. Both branch arms are analyzed conservatively regardless of literal truth. Every literal must be consumed immediately by its store or condition.

The numeric whitelist remains integer text `0` through `9` and Decimal text `0.0`, `0.5`, through `9.0`, `9.5`. The entire input remains bounded by **128 raw tokens** and **16 nested Ifs**, including prefix stores. No slot table is supplied by Python: name validation and state selection are Kuro-owned. The four-name bound is a deliberately fixed language, not a general symbol table with silent truncation; any other name rejects even in an unreachable arm or zero-trip body. Input token byte lengths and serialization/materialization before the token-count check are not independently bounded external transport.

Copy assignments between slots, expressions combining slots, arbitrary names, computed counts, While, nested/additional loops, Actions, result slots and trailing code remain unsupported. In particular, cross-slot *interleaving* of literal stores and reads is supported; cross-slot *value transfer* is not. Treating a copy as an identity or constant transfer would invalidate the proof below and is expressly rejected.

## State and evidence stay separate

The state is a four-component vector of masks: unknown/uninitialized `?=1`, Integer `I=2`, Decimal `D=4`. All slots start unknown. A prefix or body store changes only the named component. Each branch takes a complete entry snapshot, evaluates Then, restores the complete entry vector for Else, and unions corresponding outgoing components. Missing Else contributes the entry vector. Depth-specialized Action scratch variables avoid shared-global recursion clobbering; a structural regression compares every callable specialization modulo depth.

Each five-line `USE` record carries the original raw load PC, exact slot name, origin `E` or `B`, and incoming mask. Repeated records union only for the same `(pc, name, origin)`. Evidence is printed independently of branch state restoration: a later write to the same or another slot cannot erase an earlier unsafe read. `DECISION` succeeds only when every reachable read is exactly Decimal. Count zero emits both origins as zero/unreachable; count one emits actual entry evidence and zero backedge evidence. Counts two through nine use first-trip entry and second-trip backedge evidence.

The full input is validated in a dry pass before any evidence or decision is emitted. Invalid streams produce only `REJECT`, including malformed zero-trip bodies. Resource excess rejects instead of truncating read discovery. Once validated, scanning for unreachable reads is unambiguous because opcode spellings cannot occur as valid slot or literal operands. The token bound also bounds records: at most 41 load-print statements fit after the outer loop header/end; each emits two origin records, hence at most 82 five-line records plus the two-line decision.

## Why two trips still suffice here

For each slot `s`, every complete-body abstract transfer has one of two forms: `F_s(S)=C_s` when all paths overwrite `s`, or `F_s(S)=S_s union C_s` when some path preserves it. Literal stores change no other component, reads change none, and branch union is pointwise. Sequence composition preserves these forms. Therefore `F_s(F(S))=F_s(S)` for each component and `F(F(S))=F(S)` for the complete vector.

Every trip after the first thus has the same abstract incoming vector as trip two. Deterministic read-prefix transfer then gives identical evidence for each later trip. This is a finite-trip argument for this nonrelational literal-overwrite language, not a general CFG worklist solver or a proof for copies, arithmetic or correlated path semantics. The [Python CFG oracle](../../tests/self_host/loop_flow_facts.py) remains an independent comparator, not the justification for this argument.

## Validation and review

The final analyzer module contains **96 passing tests**, including nine hosted-native executions. The focused/fresh-generator gate passed **355 tests in 218.73 seconds**; the complete local suite passed **1,411 tests / 20 skipped in 690.38 seconds**. Counts overlap. `git diff --check` passed. The fresh-generator gate includes Decimal storage execution, depth/global-slot/token boundaries, ARM64 source emission and the inherited per-use/loop/branch/positive-Repeat acceptance and rejection matrices. Existing production rejection probes retain exit 1 with empty stdout/stderr; accepted controls execute with exact output.

Regressions cover each slot and count class, interleaved cross-slot literal writes, explicit read identities, nested pointwise joins/restores, slot renaming, every proper prefix of nested multi-slot input, invalid names/literals, copy/expression rejection, oversized numeric operands, exact and over token/depth bounds, and maximum-density discovery of all 82 origin keys. An independent finite-path witness enumerates every branch-choice sequence for counts 0, 1, 2, 3 and 9, tracking all four slots without a CFG solver. Ordered prefix overwrites additionally have direct hand-stated expected masks, rather than relying only on the Python comparator.

Independent design and implementation review found no blocker for the bounded pointwise proof or fail-closed grammar. After the native failure below was corrected, independent re-review again found no blocker and separately passed 16 selected native, finite-path and ordered-prefix cases. The earlier nonblocking prefix-witness coverage gap was addressed. The remaining maintenance risk is verbose depth-specialized state; this is not a proposed production parser architecture.

Publication counts as verified only after all eight checks pass on the exact final documentation-updated head, recorded in PR metadata; the PR remains open/unmerged. Earlier-head green checks do not substitute.

The first implementation passed interpreted evidence tests but failed four hosted-native probes; the first focused run was **345 passed / 4 failed**, and the first full run was **1,401 passed / 20 skipped / 4 failed**. A debugger located the crash in `_kuro_strlen` with integer mask `4` as a pointer. The inherited hosted x86 backend's identifier heuristic interprets a `Kind` suffix as Text inside Actions. Numeric scratch variables were renamed from `FlowUseKind` / `FlowPrefixKind` to `FlowUseMask` / `FlowPrefixMask`, with explicit numeric initialization, entirely within the test analyzer. Merely adding numeric seeds without renaming did not fix the inherited inference behavior. All seven then-existing hosted-native probes passed after renaming; one-trip origin coverage and ordered prefix-kind probes were subsequently added. No generated assembly patch, production-backend modification or skipped failure is part of the fix.

## Trusted boundary and next path

The analyzer still runs through the hosted Python compiler/interpreter. Native probes compile the analyzer itself through the hosted native backend and compare complete stdout, including safe four-slot evidence, cross-slot unsafe reads, zero-trip records, malformed names and token overflow. These are not evidence that the Kuro-owned generator can compile the analyzer. A separate fresh-generator gate protects existing production acceptance and target-source emission; neither gate establishes a clean-checkout Python-free compiler bootstrap.

The next bounded extension should establish a reviewed Kuro-owned symbol table and bounded state/snapshot representation for dynamically discovered slot names, retaining literal-only writes and per-use identities before adding cross-slot value transfer. A copy-capable language needs a new convergence argument or real monotone worklist/CFG solution, plus finite-trip witnesses where evidence first changes after trip two. Production permission changes still require separate store compatibility, stack, exit representation and integration proofs; this test slice authorizes none.

## Reproduce the local gates

```sh
.venv/bin/python -m pytest -q \
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
