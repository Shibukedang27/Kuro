# Action returns through authored VM loops

This increment is stacked directly on verified open/unmerged [PR #95](https://github.com/Shibukedang27/Kuro/pull/95), exact head `db3cc086e50cfb65700b3b8313571afacc6d80b2` (8/8 checks). Keep the new review PR open and unmerged. Strict independence is not complete.

## Why this slice

PR #95's initializer-list repair exposed an existing authored-VM limitation: an Action's `Return` sets `VMReturnPending`, but the loop drivers continue stepping its body. #95 safely avoided in-loop Return in the compiler, so its existing full bytecode-stage self-rebuild already works. This increment closes the demonstrated runtime-semantic gap; it does **not** claim to newly unblock that self-rebuild or to make the generator capable of rebuilding native compiler/runtime images.

Before editing production code, minimal While and Repeat return regressions both failed on #95. Each printed forbidden `901` sentinels after Return; Repeat also executed further iterations. Independent critical-path assessment recommended fixing both loop drivers as a bounded runtime-correctness slice rather than starting a broad assembler/backend implementation without a design.

## The repair

`VMRunWhile` and `VMRunRepeat` now include `VMReturnPending == 0` in both body and iteration guards. While takes no backedge after a pending return or VM failure. Neither driver consumes or clears the signal. The existing `VMInvoke` restores the caller's bytecode position and frame, and `BC_CALL_END` consumes only the completed callee's return signal, allowing the caller's enclosing loops to continue.

Repeat also needs reentrant live state: its old shared remaining-count/body-done scalars are overwritten when a nested loop or called Action runs Repeat. The driver now keeps these two mutable values in depth-indexed integer collections, following While's existing approach. Scratch values are refreshed from the current depth after nested stepping and before decrementing the counter. Each active positive-count driver releases its depth on return, failure or ordinary completion; zero-count Repeat follows the existing skip path. Ten initial entries grow one entry at a time at the existing collection boundary; this is not a newly claimed arbitrary-depth guarantee or a new iteration-limit policy.

An initial **rejected local trial** attempted to use mutable Action parameters for Repeat state. The reference IR interpreter reads parameters through immutable overlays and writes assignments to globals, so that trial was unsound: a later-iteration return missed its branch and ran the post-loop tail. It was not pushed or accepted. Depth-indexed state replaces that approach; no mutable-parameter implementation remains. Two initial test expectations were also corrected to existing behavior: the reference prints `3.250` as `3.25`, and implicit no-Return reference Actions produce `None` rather than the authored VM's zero. Current differential fixtures use `3.25` and an explicit skipped-loop fallthrough return; neither existing discrepancy is silently repaired or claimed as parity.

## Executable contract and oracle boundary

[`test_vm_loop_return.py`](../../tests/self_host/test_vm_loop_return.py) contains 20 explicit output contracts, executed through the hosted authored VM, a framed artifact launcher, and one fresh native launcher per module. Fourteen also run against the reference interpreter. Coverage includes unconditional and later-iteration conditional returns, Text and Decimal values/display, repeated calls, nested While/Repeat combinations, nested If, recursion, caller continuation after a callee returns, ordinary nested Repeat completion, skipped loops, and depth 9/10/11 unwind/reuse around the initial Repeat state capacity. Hosted VM assertions require frame entries, Action depth, While depth, Repeat depth and return signal to be restored, with the final instruction position at the end.

**Do not use the reference interpreter as an oracle for reentrant Repeat calls yet.** Its lowerer names hidden counters `__repeat_i{lexical_depth}` and stores them globally; different Actions/main can therefore reuse the same live counter. A bounded 10,000-instruction trace of a three-iteration caller invoking an early-returning Repeat Action exhausts that budget. A normally completing two-iteration callee produces only one caller iteration instead of three. These were isolated before final gates; the initial broad local test timed out because it invoked that unsafe reference path before reaching the VM. Contract-only fixtures explicitly exclude that oracle. The reference lowerer is unchanged, and general loop parity is not claimed.

The contract-only subset also exercises a recursive Repeat Action called from Repeat and depth-growth/reuse witnesses. All 20 contracts require exact output/status through all three authored runtime paths; the reference limitation is not a skipped authored-runtime case.

## Verification

Final corrected-code results (counts overlap and must not be added):

| Gate | Result |
| --- | --- |
| Initial corrected-code return module, including fresh native launcher | **74 passed in 9.64s** |
| Fresh-artifact compiler/VM/launcher/generator/storage gate | **474 passed, 18 skipped in 205.87s** |
| Complete suite, fresh per-test artifacts | **1,890 passed, 20 skipped in 976.03s** |
| Independent final return module and inherited VM parity | **98 passed in 16.23s** |
| Fresh production hosted bootstrap and Python-free smoke, including exact full compiler bytecode reproduction | Passed |
| Python 3.10 syntax grammar and `git diff --check` | Passed |

Independent final review found no implementation blocker in signal propagation, caller continuation, depth-indexed state or the explicit oracle boundary. It requested relabeling the stale older roadmap entry from “Current review boundary” to “Historical review checkpoint”; that documentation correction is included before publishing the final review head. No production/test changes followed these passing gates. The prior failing mutable-parameter trial and the unsafe reference-oracle timeout are not acceptance results.

Commands:

```sh
.venv/bin/python -m pytest -q \
  tests/self_host/test_vm_loop_return.py \
  tests/self_host/test_vm_cross.py \
  tests/self_host/test_artifact_launcher.py \
  tests/self_host/test_compiler_driver.py \
  tests/self_host/test_native_codegen.py \
  tests/self_host/test_native_integer_storage.py \
  tests/self_host/test_native_integer_storage_capacity.py \
  tests/self_host/test_initializer_list_stack.py \
  tests/self_host/test_recursive_expression_operators.py \
  --basetemp=/workspace/kuro-loop-return-focused-final --durations=15
.venv/bin/python -m pytest -q \
  --basetemp=/workspace/kuro-loop-return-full-final --durations=20
make native-hosted-bootstrap NATIVE_TARGET=x86_64-linux
sh tests/self_host/python_free_native_smoke.sh
```

The capacity gate includes a fresh compiler/launcher and exact full compiler bytecode-stage reproduction, not just a small probe. The production smoke rebuilds images first, then blocks Python and host assembly/link tools on PATH during use and compares complete stage-1/stage-2 compiler artifacts. This is Python-free **use of hosted-seeded images**, not Python-free clean-checkout native image construction. Generated tracked `dist/` artifacts are restored, not committed.

Final acceptance requires all eight GitHub checks successful on the exact documentation-updated review head. The PR's exact-head verification record is authoritative; an implementation-head green result does not verify a later documentation head.

## Limits and next path

Only the authored VM loop runners and their state are changed. Compiler parsing/lowering, artifact admission, native generator, platform guards, owner/cell/scalar/token capacities, overflow/bounds behavior, loop-count rules and iteration/depth policies remain unchanged. No growth, aliases or collection control flow is added to the Kuro-owned native generator. Its fixed integer-storage execution/output path remains Linux x86-64-only. Native launcher tests on other platforms require genuine CI execution, not inference from Linux or cross-assembly.

The next runtime boundary is the reference lowerer's reentrant hidden Repeat-counter collision, with explicit save/restore and early-return cleanup obligations before differential parity can be claimed. Do not undo #95's loop-flag workaround merely because this VM repair exists. Then resume the larger codegen path: explicit indexed-storage entry/backedge/exit facts and safe collection control flow, full analyzer/compiler/runtime bytecode admission, Kuro-built native images, and a designed repository-owned object/executable writer to remove the external assembler/linker. Python still seeds production native images, and Clang still assembles/links them. **Strict independence remains unfinished.**
