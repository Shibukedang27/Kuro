# Reference Index and result-register ownership contracts

This tests-and-design increment is stacked directly on verified open/unmerged [PR #98](https://github.com/Shibukedang27/Kuro/pull/98), exact head `4c74b15366376b18db17799eee3e2ebb34fe2a7b`, with eight successful checks. It deliberately changes **no production code or runtime semantics**. Keep its review PR open and unmerged. **Strict independence remains unfinished.**

## Why characterize before repairing

The [private-counter repair](reference-closure-repeat-capture.md) excludes only hygienic compiler-private Repeat counters from new snapshots. Extending that filter to `Index` or `_` would be a source-visible semantic change, not another hygiene correction. Both names can already be captured, and parameters can override captured values. This increment makes those boundaries executable before selecting a different ownership protocol.

The reference interpreter has three distinct mechanisms:

| Binding operation | Current reference behavior |
| --- | --- |
| Ordinary read, including `Index` and `_` | Read the **top frame only**, then global environment; an absent `_` reads as `None` without creating a binding. Lower frames are not searched. |
| Ordinary store, Repeat's active Index, Call/Get/Length result | Write the global environment, not the frame. |
| MakeClosure | Copy globals, merge **all** active frames from oldest to newest, then exclude exact private Repeat counters. This is a shallow snapshot, not deep object copying. |
| Invoke | Copy that snapshot into a frame, then overlay arguments by parameter name. Pop the frame on completion or exception. |
| Repeat cleanup | Save/restore the **global** Index and hidden counter; it does not rewrite a captured/parameter overlay. Explicit Return evaluates its operand before emitted cleanup. |

These are observations of [`interpreter.py`](../../compiler/interpreter.py) and [`lower.py`](../../compiler/lower.py), not promises of lexical scope or other-engine parity. In particular, MakeClosure's all-frame merge and ordinary reads' top-frame-only lookup are different operations.

## What the bounded witnesses establish

[`test_index_ownership_contract.py`](../../tests/runtime/test_index_ownership_contract.py) characterizes Index capture, parameter precedence, loop writes and restoration. [`test_result_ownership_contract.py`](../../tests/runtime/test_result_ownership_contract.py) characterizes result-register presence (including captured zero and `None`), producer writes, nested/repeated invocation and deferred execution. Every fixture compiles through the normal source pipeline and runs with an external 10,000-instruction budget. Successful runs require empty Action frames and exact preservation of pre-existing dollar-suffixed global bookkeeping, with none newly leaked.

A fully source-seeded result witness first calls an Action returning `17`, then creates a Worker closure. Worker calls an Action returning `42`, but `Return @_` returns its captured `17`. The outside `Call Invoke` stores that returned `17` in the global result register. Paired fixtures with `_` absent at snapshot creation read the newly written global `42` instead. Captured zero and `None` are present bindings, not fall-through cases.

The producer tests use a direct helper to observe global results immediately after Call, Get and Length. That helper has its own frame and reads the actual new global result, while the invoking closure resumes reading the old captured result. A nested snapshot can again retain the outer stale result despite an intervening global write. Spawn/Await preserves creation-time snapshot behavior; it does not refresh capture data at await time.

These are **compatibility characterizations**, not regression repairs. They pass on the exact parent implementation. Passing them does not mean stale result reads or hidden loop indices are desirable, and a deliberate later repair should revise affected expectations openly rather than preserve a defect forever. No expected-failure markers or instruction-budget exhaustion count as acceptance.

## Next protocol: separate ownership, not wholesale capture mutation

A future repair should give special execution bindings an explicit scoped owner rather than make every capture writable or add blanket exceptions to `_read`:

1. **Result register:** first specify whether an invocation starts with its captured result, the caller's live result, or an unset register. Then define a call-local writable result slot used consistently by Call, Get and Length, and how a completed call publishes its result to its caller. A missing slot must have a deliberate `None`/fallback rule. Merely filtering `_` would stop stale reads but still leave shared global result storage and nested-call effects unspecified.
2. **Index:** define whether an active Repeat's scoped Index shadows a captured value or an Action parameter named Index. A candidate loop-local owner can save/restore the prior *effective* binding on a LIFO stack, but that changes the current parameter/capture-priority contract. Decide this before adding an opcode or mutating an Invoke frame. Preserve zero-count behavior, Return operand evaluation order, reentrancy, and unset-vs-present state explicitly.
3. **Snapshot boundary:** specify whether MakeClosure snapshots the current effective special binding or excludes it. Its existing merge of all active frames must not accidentally resurrect an older special binding after a scoped owner has been introduced. Ordinary user captures and shared mutable object references must remain outside the repair unless separately specified.

These are design constraints and a recommended decomposition, **not an approved or implemented new language specification**. The narrow next implementation should select one binding (preferably the result register), add explicit old/new behavioral witnesses and cross-runtime admission limits, and only then introduce its scoped protocol. Index is a separate follow-up. Do not combine this work with BytecodeVM Repeat support, direct-native cleanup or exception unwinding.

## Verification

Counts overlap and must not be added. The production tree is byte-for-byte unchanged from the exact parent; all twenty-two new tests pass with that parent implementation, rather than showing a parent failure/candidate repair.

| Gate | Result |
| --- | --- |
| New bounded Index/result cases, independent final review | **22 passed in 0.12s**; no blocking issue found |
| New and inherited reference cleanup/capture/interpreter contracts | **78 passed in 0.20s** |
| Fresh compiler/VM/launcher/generator/storage gate | **575 passed, 18 skipped in 215.84s** |
| Complete suite with fresh per-test artifacts | **1,946 passed, 20 skipped in 1,010.50s** |
| Fresh production hosted bootstrap and Python-free smoke, including complete compiler-bytecode reproduction | Passed |
| Python 3.10 syntax grammar and `git diff --check` | Passed |

Independent review inspected the new witnesses against the interpreter and lowerer without editing files. It confirmed actual global producer observations, top-frame read priority versus all-frame capture merging, parameter precedence and successful cleanup, and found no blocking issue in the stated reference-only characterization scope. Exceptional exits, mutable-object aliases and Invoke resource guarantees remain outside the evidence.

Commands:

```sh
.venv/bin/python -m pytest -q \
  tests/runtime/test_result_ownership_contract.py \
  tests/runtime/test_index_ownership_contract.py \
  tests/runtime/test_closure_repeat_capture.py \
  tests/runtime/test_repeat_cleanup.py tests/runtime/test_interpreter.py \
  --basetemp=/workspace/kuro-binding-contracts
.venv/bin/python -m pytest -q \
  tests/runtime tests/ir \
  tests/compiler/test_first_class_closures.py tests/compiler/test_concurrency.py \
  tests/self_host/test_vm_loop_return.py tests/self_host/test_vm_cross.py \
  tests/self_host/test_artifact_launcher.py tests/self_host/test_compiler_driver.py \
  tests/self_host/test_native_codegen.py \
  tests/self_host/test_native_integer_storage.py \
  tests/self_host/test_native_integer_storage_capacity.py \
  tests/self_host/test_initializer_list_stack.py \
  tests/self_host/test_recursive_expression_operators.py \
  --basetemp=/workspace/kuro-binding-focused --durations=15
.venv/bin/python -m pytest -q \
  --basetemp=/workspace/kuro-binding-full --durations=20
make native-hosted-bootstrap PYTHON=/workspace/Kuro/.venv/bin/python NATIVE_TARGET=x86_64-linux
sh tests/self_host/python_free_native_smoke.sh
```

Production bootstrap/smoke ran in detached `/workspace/Kuro-binding-ownership-bootstrap` at the exact parent, whose production sources are identical to this tests/docs-only candidate. The interpreter and lowerer SHA-256 identities were checked against the candidate. Generated images are not included in the review commit and do not race the test suites' artifacts.

Acceptance additionally requires all eight GitHub checks successful on the exact final documentation-updated head. Earlier-head CI does not verify a later documentation commit. No merge is authorized.

## Explicit limits

This increment adds reference-interpreter evidence only. It does not fix stale captured Index/result reads, general mutable captures, lexical scope, recursive Invoke resource limits, or exception-safe global-binding unwind. It adds no opcode, bytecode representation, native image capability or runtime feature. BytecodeVM still lacks SAVEVAR/RESTOREVAR execution; direct-native Action cleanup and authored-runtime closure parity remain separate boundaries. Fresh authored-runtime/native gates preserve their existing contracts, not these new reference capture semantics.

Python still seeds production native images, and Clang still assembles/links them. Python-free execution and complete compiler-bytecode reproduction demonstrate use of hosted-seeded artifacts, not clean-checkout independent image construction. After the bounded ownership work, the broader path remains indexed-storage control-flow facts, full analyzer/compiler/runtime bytecode admission, Kuro-built native images and a repository-owned object/executable writer. Strict independence is not complete.
