# Decimal initialization through nested branches

This increment is stacked directly on [PR #76](https://github.com/Shibukedang27/Kuro/pull/76), verified open/unmerged at `7b00d2bea7859b30997d27460b37e29ba9d04dda`, based on PR #75 at `5a13fdcdeac0bda001aa36d7b7851d012de91995`. All eight checks on that exact base head passed. It extends Kuro-authored native code generation, not the hosted parser or Python lowering. It does not complete toolchain independence.

## What is now accepted

A previously untouched named scalar slot may first acquire a Decimal representation inside a nested, explicit `If/Else` tree in a function-free program. Every path through each containing region must establish Decimal before that region ends. The existing 16-If-depth bound remains; the current shared-global bound is 266 slots in a separate static arena. Direct top-level branch joins retain their earlier behavior.

For example, a fresh `Balance` can be initialized by both inner arms in the outer then arm and initialized directly in the outer else arm. The inner join establishes Decimal for the current outer arm; the outer join then proves that both outer outcomes establish Decimal. Both outer arms can instead contain further nested joins. Reads and Decimal-preserving mutations after a successful inner join are supported within that arm, and after the outer join they are supported unconditionally.

An absent `Else` has a real skipped path. Its state is the region-entry state, not the state left by the last emitted statement. A fresh Decimal assignment in a no-else inner branch therefore rejects, even when the source condition is constant or a later unconditional assignment would overwrite it. This deliberately conservative rule rejects at the first unsupported join rather than performing a broader lifetime or dead-store analysis. A no-else nested branch may preserve or mutate an already-established Decimal slot.

## Why the all-path guarantee holds

The generator still scans structured bytecode linearly, but its kind state is no longer shared accidentally between nested alternative paths. Each eligible If frame owns separate entry and then-exit snapshots. At entry, all preregistered global kinds are copied to the frame. At `Else`, the then-exit state is saved and the same frame's entry state is restored before the else arm is emitted. At `Done`, the frame joins its two exit states; with no `Else`, its second exit is explicitly the entry snapshot. The joined state feeds the enclosing arm.

For a slot unknown on entry, a Decimal exit is accepted only when both exits are Decimal. A Decimal/unknown exit rejects, as does a Decimal/Integer or Decimal/Text exit in either order. Existing representation-conflict checks prevent a Decimal slot changing representation inside a path. Thus direct stores establish the leaf fact, and each enclosing accepted join preserves that fact on every path. This is a structural induction over the supported If tree, not an inference from source/emission order or a favorable runtime condition.

Snapshots are flattened Text collections indexed by `frame * global_slot_count + slot + 1`, not arrays of snapshot strings. The global slot count is fixed by the preparation pass before emission. Frames allocate only as needed, at most 16 × 266 entries in each snapshot collection; sibling regions overwrite their own frames while parent snapshots remain untouched. This follows the existing bootstrap-compatible scalar collection representation.

A small function-free region-kind stack also validates the nesting of raw If/Repeat/While delimiters. Separate construct counters alone cannot prove that an If closes before its enclosing loop, or that an `Else` belongs to the currently innermost region. Crossed delimiters now fail rather than allowing stale or ineligible region snapshots to masquerade as a proof. The stack checks structure only; it does not perform loop assignment analysis or change valid source lowering.

The first prototype used an empty region marker alongside one-character markers. Hosted tests passed, but a fresh compiled Linux generator rejected even a simple Integer print before reaching the new nested cases. A diagnostic-only build localized the rejection to the new structure checks: the hosted bootstrap tracks Text lengths in emission order and retained a one-character branch assignment when the runtime marker was empty. The corrected source uses the fixed-width markers `?`, `I`, `R`, and `W`; it does not broaden or modify hosted backend inference. The fresh generator then passed the storage/control-flow/direct/nested positive and rejection gate. Diagnostic assembly is not shipped or counted as fresh-source verification.

## Limits kept in place

- No first Decimal initialization under any active `Repeat` or `While`, including a zero-count loop, a constant condition, or an otherwise complete nested If tree. Established Decimal slots can still be used in existing supported loops.
- No Action-shared Decimal slots, even with an unused Action. Calls, ordering, recursion, and cross-Action initialization need separate analysis.
- No new `_`/stack-result kind joins, value-stack dataflow, or nonempty statement-region joins. Existing guards remain.
- No new mixed-kind joins, declared-type lowering, multi-value storage, or general definite-assignment guarantee for Integer/Text. Legacy one-sided non-Decimal behavior is not promoted into a broader Text-safety claim.
- Unknown-slot reads inside eligible nested arms reject instead of supplying an inferred Integer zero. Existing unknown-read behavior outside eligible regions is not generalized.
- No parser redesign, loop fixed point, new allocator, libc dependency, or generated-program fallback to the hosted compiler. Rejection sets `NativeFailed` and clears native output.

## Verification

Final full local suite at the historical #76 head: **1,185 passed, 20 skipped in 518.08s (8m38s)**. Final focused branch/bounds/fresh-generator/ARM64-source-emission gate: **128 passed in 37.08s**. That historical focus included a newly built Linux Kuro generator, generated Linux programs with no undefined symbols, all eight nested branch outcomes, and all 36 raw rejection cases. Its 16-depth/64-slot fixture exercised all 1,024 snapshot positions per collection. The current implementation retains that fixture, adds a 266-slot snapshot regression and rejects slot 267; depth 17 remains rejected. These runs overlap; do not add their counts. Genuine macOS ARM64 compiled-generator execution remains a final-head CI gate, not a local Linux claim.

The nested positive fixture exercises outer and inner outcomes, deeper nesting, multiple slots, sibling frame reuse, established Decimal no-else branches and post-join arithmetic. The negative matrix exercises missing/skipped/one-sided/mixed/early-read paths, later-overwrite ambiguity, enclosing loops, Actions, result/value-stack exclusions and crossed delimiters. The shared compiled-generator storage gate runs the nested positive and rejection corpus as well as the prior direct-join and invariant-control-flow fixtures. Linux execution, three-target assembly and ARM64 instruction emulation remain distinct from genuine Darwin execution.

```sh
.venv/bin/python -m pytest -q tests/self_host/test_native_branch_joins.py --durations=10
.venv/bin/python -m pytest -q --durations=20
```

Counts from overlapping runs must not be added together. Acceptance requires all eight checks on the final documentation-updated review head; pending, cancelled, timed-out, or earlier-head results do not count. Keep this PR and its dependency stack open and unmerged.

Independent final review rechecked the snapshots, bounds and Darwin execution guards. It also found that crossed main-region delimiters with an unrelated Action bypass this increment's explicitly function-free structure validator. A baseline comparison confirmed that both PR #76 and this candidate accept the same malformed Action-containing input and emit the same 1,227 bytes; it is not a new regression or a route around the existing Action/Decimal rejection. General raw-bytecode structural validation for Action-containing programs remains separate work. The new validator is not advertised as a whole-language bytecode verifier.

## Next work

Analyze loop entry, zero iterations, skipped bodies and backedges separately before considering loop-first initialization. Analyze Action-shared Decimal slots and call ordering separately before relaxing the function-free restriction. Result-slot and operand-stack joins remain separate proofs. Do not promote the dense-presence/sparse-payload experiment: PR #76 measured less memory but slower execution, not a net-benefit result.

Full clean-checkout Python-free compiler/runtime builds, repository-owned assembly/linking, broader runtime/standard-library parity and genuine target validation remain unfinished. The existing PR #68 final-head CI gap is not retroactively repaired by this increment's tests or CI.
