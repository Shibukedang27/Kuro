# Dynamic slot names in the bounded Kuro loop analyzer

This test-only increment stacks directly on [PR #85](https://github.com/Shibukedang27/Kuro/pull/85), inspected open/unmerged at `b688d1ae7c8003b47e345819bcf12e13eac98652` with all eight checks successful. The [Kuro analyzer](../../tests/self_host/loop_use_flow.kuro) now discovers up to four exact identifier names instead of whitelisting `Fresh`, `Other`, `Third`, and `Fourth`. Python supplies raw tokens, not a symbol table, state vector, branch snapshots, read identities or transfer facts. Production code, production acceptance and CI configuration are unchanged. Strict compiler/runtime/toolchain independence remains unfinished.

## A small symbol table, not a larger write language

Names follow `[A-Za-z_][A-Za-z0-9_]{0,31}` with the entire `BC_` namespace reserved. Equality is exact and case-sensitive: `alpha` and `Alpha` are different slots. No normalization, hashing, truncation or spelling-based kind inference is used for input names. A valid name first seen by either a store or a read receives the next free physical index. Repeated exact names reuse their index. The fifth distinct name rejects, including in an Else arm or a zero-trip body. The capacity is **four**, not the production compiler's separate 64-global-slot bound.

Discovery occurs only while structurally validating the entire prefix/body. Registration is global to that validation and is never undone by branch restoration. Before evidence emission, the mapping is complete; resolution is lookup-only when `FlowEmit` is set. Invalid input emits only `REJECT`, never partial USE evidence or a successful decision.

The input still consists of optional literal stores followed by exactly one literal-count `Repeat 0` through `Repeat 9`. Loop bodies allow literal stores, immediate `LOADVAR name; PRINT` observations and nested literal-condition If/Else statements. Conditions conservatively visit both arms. Literal integers remain `0` through `9`, and Decimal spellings remain `0.0`, `0.5`, through `9.0`, `9.5`. The **128 raw-token** and **16 nested-If** bounds are unchanged. Copies, arithmetic, computed counts, nested/additional loops, While, Actions, result slots and trailing code remain rejected, even when unreachable.

## Discovery must not change a saved state

The physical mask vector remains four explicit numeric components, each initialized to unknown `1` before any name is discovered. The legacy internal variable labels `FlowFresh`, `FlowOther`, `FlowThird`, `FlowFourth` now denote indices 0–3, not input-name identities. Every specialized branch frame snapshots all four components, including unused capacity. Discovery adds only a string-to-index association; it does not initialize, reset or reuse an occupied component.

Consequently a name first discovered inside Then already has unknown `1` in every enclosing entry snapshot. Restoring Else cannot leak the Then store. The same holds for missing Else and names discovered for the first time by a read. Pointwise joins combine only corresponding physical indices. Prefix masks are saved for all four components; after the dry traversal they replace the dry-pass state before execution. Body-only names thus start unknown, while prefix-written names retain their actual prefix masks. The table itself is not restored or rebuilt between trips.

For example, `If ... Then store Decimal late Else read late` yields unknown entry evidence and unknown-or-Decimal backedge evidence for the Else read: masks `1` and `5`, not `4`. A missing-Else store followed by a read yields `5` at both origins. Read-only discovery in either arm remains `1` at both reachable origins.

## Why the existing two-trip argument still applies

The finite set of discovered names is fixed before execution. For every component, a complete-body transfer is still either `F_s(S)=C_s` or `F_s(S)=S_s union C_s`; stores are literal overwrites and cannot read another slot. Composition and pointwise branch union preserve this form, hence `F(F(S))=F(S)`. Every later trip has the same abstract incoming vector as trip two, and deterministic read-prefix transfer gives the same per-use masks. Dynamic spelling adds no dependency between components.

USE records retain `(raw load PC, exact name, E/B origin, incoming mask)`. Branch restoration cannot erase earlier evidence; later writes cannot repair it. Zero-trip uses emit zero masks for both origins, one-trip uses emit zero backedge masks, and a decision succeeds only if every reachable mask is exactly Decimal `4`. Rejecting `BC_` operands prevents an identifier from masquerading as a load opcode during the validated zero/one-trip raw-token evidence scan. At most 41 reads / 82 origin keys fit in the token budget.

## Validation

The focused/fresh-generator gate passed **415 tests in 261.71 seconds**. The complete local suite passed **1,471 tests / 20 skipped in 736.43 seconds**. The analyzer modules contain **156 tests**, including 18 hosted-native executions on Linux x86-64. Counts overlap. `git diff --check` and Python 3.10 syntax parsing of both changed Python modules passed. The fresh-generator gate retains Decimal storage execution, production depth/global-slot/token boundaries, ARM64 source emission and inherited loop/branch/positive-Repeat acceptance and rejection probes.

Independent design review identified missing read-only late-discovery and nested native witnesses; these were added. Independent implementation review found no blocker and separately passed all 156 analyzer tests in 84.38 seconds, confirming complete snapshots, frozen exact-name lookup, fail-closed validation and the restricted two-trip argument. Native execution coverage remains platform-gated. The larger background job wrappers were later reported terminated, but their saved logs contain complete successful pytest summaries (written at 17:56 and 18:04 local time); inspection found no remaining pytest processes. No successful gate was inferred merely from a wrapper status.

Publication is verified only when all eight checks are successful on the exact final documentation-updated head; PR metadata records that SHA. Earlier-head green results do not substitute. The review PR must remain open/unmerged.

The new [dynamic-slot regressions](../../tests/self_host/test_native_dynamic_slot_flow.py) exercise exact identity, all 24 discovery-order permutations, read-only discovery, nested opposite-arm discovery after snapshots, ordered prefix masks, all count classes, global capacity failures, unreachable malformed operands, identifier length/character boundaries, prefix truncation, token/depth bounds, evidence density and lookup-only table freezing. Independent finite-path enumeration tracks four dynamically named slots for counts 0, 1, 2, 3 and 9 without a CFG solver. Hand-stated late-discovery and nested masks supplement the Python CFG comparator. Existing four-slot regressions are retained, with only formerly invalid-but-now-valid names replaced in malformed-name fixtures.

During initial validation, the new module had 51 passes and four fixture failures: Python's default JSON Unicode escaping was not Kuro string syntax, so non-ASCII and NUL operands reached the analyzer as different ASCII spellings such as `u00e9`. The harness now inserts non-ASCII text without JSON Unicode escapes and preserves an actual NUL in its interpreted fixture. It does not reject legitimate identifiers merely because they resemble an escape spelling. Native probes exercise actual non-ASCII input; the NUL fixture is interpreted-only. This does not establish arbitrary-byte input safety for the hosted native C-string runtime or an external transport.

## Trusted boundary and next narrow step

The analyzer still uses the hosted Python compiler/interpreter. Hosted-native probes compile the analyzer through that hosted backend and compare full stdout, including hand-checked nested evidence and fail-closed capacity/name paths. The separate fresh Kuro-generator gate exercises existing production acceptance, rejection and target emission. It does **not** show that the Kuro-owned generator can compile this analyzer. Neither gate establishes a clean-checkout Python-free bootstrap. Materialization of input tokens and their byte lengths before validation remain outside an independently bounded external transport.

The next bounded step is a reviewed indexed state/snapshot representation that scales capacity without depth-specialized four-component copies, retaining the same literal-only language and evidence identities. Before copies or general expressions, supply a new convergence argument or a monotone CFG/worklist solution, including finite-trip witnesses whose evidence changes after trip two. Production permission changes require separate storage, stack, exit representation and integration proofs; this test-only slice authorizes none.

## Reproduce

```sh
.venv/bin/python -m pytest -q \
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
