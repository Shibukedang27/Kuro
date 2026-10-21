# Kuro derives bounded loop-read facts from raw tokens

This test-only slice follows [PR #83](https://github.com/Shibukedang27/Kuro/pull/83), inspected open/unmerged at `d1280290eaef45d8cba286cd95cc0f192df99b56` with all eight checks successful. Unlike the [preceding obligation reducer](native-loop-use-obligations.md), the new [Kuro analyzer](../../tests/self_host/loop_use_flow.kuro) discovers reads, parses branches and derives their origin-labelled kind evidence itself. Python supplies raw tokens, not a CFG, read identities, reachable-origin declarations or flow facts. Production compiler/runtime code, acceptance rules and CI configuration are unchanged. Strict compiler/runtime/toolchain independence is not complete.

## A deliberately small complete input language

The complete stream is an optional literal assignment to `Fresh`, followed by exactly one literal-count `Repeat 0` through `Repeat 9`, with no trailing instructions. Body statements are literal assignments to `Fresh`, `LOADVAR Fresh` immediately followed by `PRINT`, and literal-condition `If` statements with optional `Else` and nested bodies. Both arms are conservatively analyzed regardless of literal truth, matching the test oracle's nondeterministic branch abstraction; these are not claims of concrete arm reachability.

Literals are an explicit whitelist: integer text `0` through `9`, and Decimal text `0.0`, `0.5`, through `9.0`, `9.5`. Other valid Kuro numeric literals are intentionally unsupported. Every literal must be immediately consumed by a store or an If condition. Standalone/extra constants, unfinished expression stacks, other slots, arithmetic, computed counts, While, nested/repeated outer loops, Actions, result slots, external reads and trailing code reject. Unsupported or malformed code inside a zero-trip body or either branch also rejects.

The analyzer validates the entire stream before emitting any facts. It checks token arities, operand spelling, nested delimiters, full input consumption, at most **128 raw tokens** and **16 nested Ifs**. Truncation produces `REJECT`, not a runtime indexing error. Inputs at both bounds are accepted when structurally valid; exceeding either rejects, without truncating read discovery. The token bound also bounds read count, parser work and emitted output. Input serialization/materialization happens before this check and is not an independently bounded external transport.

Kuro Action scratch variables are shared globals. Seventeen explicitly depth-specialized sequence Actions avoid pretending recursive scratch variables are stack-local; a regression checks that the sixteen callable transitions do not drift. The last level rejects further nesting. This verbose test implementation is not proposed as a production parser architecture.

## Why later overwrites cannot repair earlier reads

Kinds are sets encoded as masks: unknown/uninitialized `?=1`, Integer `I=2`, Decimal `D=4`; zero means no reachable evidence for that origin. Each `USE` record contains the original raw load-token PC, origin `E` or `B`, and its incoming mask. There is only one loop and one canonical slot, so the containing loop and slot are unambiguous from the validated input. Repeated records have union semantics. A `DECISION` succeeds only if every reachable observation is exactly Decimal. Unknown, Integer and mixed observations fail even when all final exits become Decimal.

Each branch arm starts from the same incoming slot mask. Its read records are emitted independently and never restored with the slot snapshot. The merge unions outgoing masks; a missing Else contributes the unchanged incoming state. The join implementation is tested against all **64 mask pairs**, including unreachable masks as a helper-level check.

Count zero emits both origins as unreachable for every syntactically discovered load. Count one emits entry facts and unreachable backedge facts. Counts two through nine emit first-trip entry facts and second-trip backedge facts. This is sufficient **only for this language**: a whole-body slot transfer has the form `F(S)=C` when every path overwrites, or `F(S)=S union C` when an unchanged path exists. Literal stores, identity reads and conservative branch unions preserve this form, so `F(F(S))=F(S)`. Every trip after the first therefore has the same incoming mask as trip two, and every read-prefix transfer is deterministic on that mask. Second-trip evidence equals the union over all later finite trips; it is not a general loop-header fixed-point algorithm.

The [Python CFG oracle](../../tests/self_host/loop_flow_facts.py) remains an independent comparator. Its globally converged boundary seeds and positive-loop overapproximation are not universally exact finite-trip semantics. Equality is asserted only for this restricted overwrite/identity language. An additional independent three-trip event enumeration checks all 25 pairs from a five-arm event alphabet, rather than relying only on agreement with that oracle.

## Trusted boundary and exclusions

The harness supplies a complete immutable sequence of Text tokens, runs the analyzer once, and decodes output records. The empty token stream is serialized as empty Text because a type declaration alone does not create an empty collection; it is rejected by Kuro. The Python harness does not prevalidate or fill in omitted identities/origins. Malformed-token and all-proper-prefix tests bypass any well-formed fixture assumptions.

The analyzer is hosted through the Python bootstrap compiler/interpreter. Two Linux x86-64 probes compile and execute the **analyzer itself** with the hosted native backend and compare complete stdout with interpreted execution: a safe read and a branch read-before-write counterexample. They do not show that the Kuro-owned generator can compile this analyzer, nor establish native malformed-input or capacity coverage on every target. The separate fresh-generator gate protects existing production behavior, including unsupported multitrip branch initialization.

This is complete per-use origin evidence for the stated bounded language, not a complete analysis of Kuro bytecode. General slots, arbitrary numeric expressions, nested loops, While, Action/result-slot effects, stack joins, store compatibility and exit representation invariants are excluded. The prior reducer is not wired into production, and this producer does not widen any permission.

## Validation and review

The new analyzer module passed **44 tests**. The focused/fresh-generator gate passed **303 tests in 192.46 seconds**; the complete suite passed **1,359 tests / 20 skipped in 660.29 seconds**. Counts overlap. The focused gate includes the predecessor's per-use, positive Repeat, flow-fact, loop/branch-join and obligation modules, plus fresh-generator Decimal storage, depth/slot/token limits and ARM64 source emission. Existing fresh-generator rejection probes retain exit 1 with empty stdout/stderr; accepted controls execute with exact output. `git diff --check` passed.

Independent design review emphasized whole-stream validation, separate origin identities and finite-count semantics rather than general fixed-point claims. Hardening replaced an incomplete hand-written join table with bit-membership union, rejected pending literals across statement/branch boundaries, and added bounds-checked peeks after a truncated nested branch exposed a runtime indexing error. Regression tests cover every proper prefix of a nested program, malformed bodies even under count zero, all mask pairs, complete input consumption and inclusive resource bounds. Independent review of the final implementation and its 44 passing tests found no remaining blocker within the stated contract, while retaining the maintenance risk of depth-specialized Actions and the hosted-bootstrap limitation. Its recurrence argument agrees with the restricted overwrite/identity proof above, not a general-bytecode solver claim.

Publication is verified only when all eight checks are successful on the exact final documentation-updated head, recorded in the PR metadata. Earlier-head green checks do not substitute; the PR remains open/unmerged.

```sh
.venv/bin/python -m pytest -q tests/self_host/test_native_loop_use_flow.py
# Run the predecessor's documented focused/fresh-generator command with
# tests/self_host/test_native_loop_use_flow.py added to its module list.
.venv/bin/python -m pytest -q --durations=20
git diff --check
```

## Next bounded path

Extend the Kuro-owned producer with explicit multi-slot state and original identities before considering general expressions or inner loops. Retain whole-stream validation and independent finite-path witnesses, and prove each added transfer preserves the origin evidence instead of assuming the current idempotence argument survives. General loop support requires a real monotone worklist/CFG solution with reviewed entry/backedge cuts and resource failure. Production multitrip branch permission still needs separate store/exit/stack proofs and an independently reviewed integration proposal; it is not authorized by this test slice.
