# Decimal initialization in an exact-once Repeat

This increment starts directly from [PR #77](https://github.com/Shibukedang27/Kuro/pull/77), verified open/unmerged at `83aa221805b1c5ab4ff1c6249c51998ad52fb013`, with all eight checks successful. It is a deliberately smaller step than general loop definite-assignment analysis. Full clean-checkout Python-free compiler/runtime construction and repository-owned assembler/linker remain unfinished.

## What is accepted

Only a function-free, top-level `Repeat 1` may establish a previously untouched named scalar Decimal slot, and only with a `BC_STORE_LIST` directly in that loop's body. The parsed native bytecode must have the exact adjacent sequence `BC_CONST`, `1`, `BC_REPEAT_BEGIN`, with exactly one Integer operand on entry. For example:

```text
Repeat 1;
    Balance = 1.25;
    Add 0.25 to Balance;
Done.
Print Balance.
```

Variable counts, computed counts, other literal counts, While, enclosing branches/loops, Actions, `_`, mixed representations and nonempty value-stack joins do not gain first-initialization support. A complete nested If inside the loop still cannot establish a fresh Decimal; it can preserve a slot already initialized directly in the body. This is intentionally more restrictive than all semantically safe programs: even `Repeat 2` and `Repeat 0 + 1` remain rejected for fresh Decimal initialization.

## Actual loop behavior

The [hosted parser](../../compiler/parser.py) and [AST](../../compiler/ast_nodes.py) implement `Repeat expression; ... Done.` and `While condition; ... Done.`. There is no separate do-while, repeat-until or bounded-conditional syntax. A Repeat containing an If is still a counted, pretested Repeat, not a posttested loop.

The [hosted lowerer](../../compiler/lower.py) evaluates a Repeat count once before its header, checks that it is nonnegative, compares an increasing hidden counter against that saved value, and saves/restores `Index`. Changing the source count variable in the body does not change the saved bound. The [Kuro lowerer](../../self_host/lower.kuro) likewise places count evaluation before `REPEAT_BEGIN`. The [Kuro VM](../../self_host/vm.kuro) and [native emitter](../../self_host/native_codegen.kuro) consume the count once and use private loop-counter state. The native path tests the captured count before the first body entry, decrements it at the end and retests at the header. **Repeat is not generally at-least-once:** a zero count skips the body.

There is a pre-existing negative-count discrepancy. The hosted interpreter raises `E6004`, while the Kuro VM and native emitter skip a negative count. A regression records that difference explicitly rather than advertising general Repeat parity. This change neither fixes nor relies on that behavior. Native source/bytecode acceptance is a different question from this runtime discrepancy; fresh Decimal initialization with negative counts remains rejected.

While evaluates its condition before the first body entry and again at every backedge. False initially means zero body executions. Its native invariant region starts at `BC_WHILE_BEGIN`, before condition evaluation and `BC_WHILE_TEST`. Condition reads and stores cannot be treated as an unconditional post-loop initializer. The hosted interpreter's `LOOP_GUARD` raises `E6006` after a configured number of condition attempts; the native emitters and Kuro VM do not provide an equivalent cap. That development-runtime guard is not a general bounded-loop proof.

## Why the exact-once rule is safe

The literal Integer one has the same exact representation on all three supported generator targets. Its initial signed comparison passes. On normal completion of the body, the only backedge decrements the private counter from one to zero and jumps to the test; that test exits without re-entering the body. No second body-entry kind state needs to be unified. This does not prove anything about Repeat 2, runtime counts, large or overflowing constants, or While.

Within the direct body, any normally returning nested regions before a direct store must finish before the store is reached. Nontermination or a runtime fault does not create a normal post-loop read. A direct store therefore executes before any subsequent normal exit/read; a prior unknown-slot read still establishes the existing conservative Integer representation and prevents later Decimal promotion. The existing same-kind guards reject incompatible writes before or after the first Decimal store. Several direct stores can initialize several named scalar slots.

The source parser/IR provide no break or continue statement/opcode. An Action Return can bypass loop backedges, so all Action-containing programs remain excluded from this new permission, including unused Actions and Action-local loops. The native emitter rejects `BC_RETURN` outside function mode and rejects unsupported raw `BC_BREAK`/`BC_CONTINUE`. No new exit handling is introduced.

A future language extension adding abrupt exits must revisit the proof rather than inherit this permission automatically. General multitrip loops would need entry/backedge facts, compatible representations at every reachable use, and post-loop joins that account for zero iterations and every exit; source/emission order alone is insufficient.

## State and fail-closed boundaries

`NativeRepeatOnePending` is set only while successfully parsing `BC_CONST` with exact value `1` into an empty operand stack. The next parsed instruction consumes that provenance into `NativeRepeatOnePrevious` and resets Pending; arithmetic, loads, prints and every other intervening opcode lose it. This is not a text lookbehind that could confuse operands with opcodes.

Only a top-level, function-free Repeat with that provenance, one operand and explicit Integer-kind validation sets `NativeRepeatOneActive`. Eligibility for a fresh store is recomputed at each instruction and requires `BC_STORE_LIST`, control-flow depth one, Repeat depth one, and zero If/While depth. Nested regions cannot inherit the outer permission. The Active flag survives nested regions, is cleared when the outer Repeat closes, is recomputed for each sibling loop, and is reset for every straight-line emission. The implementation does not change emitted Repeat control flow, loop counter layout, branch snapshots, or existing kind checks.

All earlier representation limits remain: no Action-shared Decimal slots, new `_` kind joins, other new kinds, value-stack joins or general definite assignment. Nested If initialization outside loops retains PR #77's frame snapshots and all-path rules. All existing 16-construct-depth, 64-global-slot, 4096-token and statement-stack guards remain. Invalid programs set `NativeFailed` and clear native output.

The first fresh-generator gate exposed a bootstrap-only crash that hosted emitter tests missed: a numeric provenance flag named `NativeRepeatOneInput` was assigned the hosted backend's Text naming fallback. Even an empty Repeat then called `_kuro_strlen` on a numeric value; GDB localized the fault to that comparison. Renaming the flag to `NativeRepeatOnePrevious` avoids the existing heuristic without changing hosted backend inference or widening the requested feature. A new fresh build accepted the minimized empty/zero/two/exact-once Repeat probes and the inherited control-flow fixture; only the corrected final-source tests count toward acceptance. The initial focused gate was 20 passed/1 failed and is not presented as successful verification.

## Verification

The new [regression corpus](../../tests/self_host/test_native_loop_init.py) exercises exact-once initialization, signed zero, same-kind mutation, established Decimal nested regions, a fresh direct store after nested regions close, sibling loops and post-loop arithmetic. It checks interpreter/VM behavior, all three targets' assembly and rejection behavior, and hosted Linux native execution. The captured-count and While-pretest/retest source fixture is separate from the supported Decimal slice. Negative-count behavior is explicitly recorded as a known discrepancy.

The raw negative corpus covers skipped zero/negative counts, Repeat 2, variable/computed counts, literal-one provenance loss, non-Integer one, nested/conditional/one-sided stores, While body/condition stores, stale sibling flags, prior reads, both representation-conflict directions, Actions, `_`, abrupt exits and stack imbalance. These cases must fail with empty assembly; they are not prefixed with another established Decimal that could mask the actual loop rule.

The existing [fresh-generator storage gate](../../tests/self_host/test_native_codegen.py) also runs the new source fixture, semantic probes and rejection corpus through a newly built Kuro generator. That shared gate preserves storage, invariant control flow, all eight nested If outcomes, the 16-depth/64-slot snapshot fixture and depth-17/slot-65 rejection tests. Genuine Darwin execution remains a macOS CI gate, distinct from Linux execution, cross-assembly and ARM64 instruction emulation.

The corrected final-source focused gate passed **148 tests in 67.08s**, including the fresh Linux generator, 28 new raw loop rejections, all 36 inherited raw branch rejections, all eight nested branch outcomes, and the new loop/slot plus inherited If/slot/token bounds. A prior inherited-only branch/control-flow run passed **219 tests in 50.69s**; these counts overlap and must not be added. The full local suite is still running at this checkpoint; its final result will be recorded before acceptance. Acceptance also requires all eight checks at the final documentation-updated review head; pending, cancelled, timed-out and earlier-head results do not count. Keep the PR directly stacked on #77, open and unmerged.

## Next work

Do not generalize this proof to multitrip or potentially skipped loops. First design explicit loop-entry, backedge, exit and use-site facts, including condition timing and any future break/continue/Return paths. Separately resolve negative-count behavior and the runtime-only While cap discrepancy before claiming general cross-backend loop parity. Action sharing, result/value-stack joins, full Python-free construction and owned assembly/linking remain separate unfinished work.
