# Result-register initialization and caller publication

This contract-only increment is directly stacked on verified open/unmerged [PR #99](https://github.com/Shibukedang27/Kuro/pull/99), exact head `b36fbc61eeac0b6c672e61e047180600e3a5682c` (eight successful checks). It changes no production code, opcode, bytecode format, or runtime semantics. Keep its review PR open and unmerged. **Strict independence remains unfinished.**

## Finding: observable stale results, but no uniquely justified initialization repair

There is a source-visible stale-result problem: seed `_` with `17`, create a closure, then execute `Call Answer` returning `42` inside it. `Return @_` still returns the captured `17`. Both the reference interpreter and serialized JSON BytecodeVM reproduce it. The [previous ownership contract](reference-binding-ownership.md) already established this; the new witnesses distinguish **invocation entry**, **successful producer completion**, and **caller publication**, rather than treating them as one operation.

The safe next step is not a one-line capture filter. The admitted Kuro-authored VM has a different, already observable entry/default-return policy. Also, `_` is an admitted Action parameter, so a direct Action—not just a closure—can hide fresh global results. Choosing an initialization policy, making a parameter writable, or changing implicit return values is a language decision. This increment records the exact boundary and a concrete proposed protocol below, without claiming that proposal is implemented or approved.

## What the execution paths actually do

[`compiler/lower.py`](../../compiler/lower.py) emits each `Call`, `Get`, and `Length` producer followed by a separate `STORE_LIST "_"` consuming the producer's temporary. The producer executes first. A source-level Call publishes only after the callee has returned and its frame has been popped. Arguments are evaluated before the Call; Return evaluates its operand before exiting. A failing producer never reaches its following result store.

| Boundary | Reference interpreter and JSON BytecodeVM | Kuro-authored VM, admitted direct-call cases |
| --- | --- | --- |
| Main entry, absent `_` | Read as `None`; read alone does not create a global binding | Result bookkeeping starts at numeric zero |
| Direct Action entry | No explicit result slot initialization; parameter overlay, then live-global fallback | Frame result explicitly initialized to zero |
| Closure Invoke entry | Copy capture, then overlay parameters; captured `_` (including zero/None) hides global; an absent capture falls through to live global | Not admitted by these tests; no closure-parity claim |
| Successful Call/Get/Length | Following lowered store writes global `_`; an existing captured/parameter `_` still wins reads | `VMSetResult` writes current VM frame result, or main result at depth zero |
| Explicit Return | Return value transported to caller; caller's following store writes global `_` | Return value transported, frame popped, then caller result set |
| Implicit Action fall-through | Returns and publishes `None`, not the callee's last result | Returns and publishes zero, not the callee's last result |
| Nested direct callee reading entry result | Reads global result, not caller's effective captured/parameter value | Starts at zero, not caller's result |

Sources: [`interpreter.py`](../../compiler/interpreter.py) `_read`, `_write`, `call`, and `_execute`; [`bytecode.py`](../../compiler/bytecode.py) corresponding read/write/call/dispatch paths; [`self_host/vm.kuro`](../../self_host/vm.kuro) `VMLoad`, `VMSetResult`, `VMInvoke`, `BC_FUNC_END`, and `BC_CALL_END`. The architecture document's bootstrap-era “most recent result” description is not a complete current initialization specification.

A concrete direct-call mismatch is `Call Seed` returning `17`, followed by an Action whose first operation is `Return @_`: the Python paths return `17`; the hosted execution of the authored VM returns `0`. A nested `Call Answer` returning `42`, followed by calling that same reader, yields `42` versus `0`. Successful explicit nested publication itself agrees: after a callee returns `42`, the caller can read `42` and return a different `9` to main.

## Executable evidence, not a semantic repair

[`test_result_publication_contract.py`](../../tests/runtime/test_result_publication_contract.py) adds 43 passing cases: 40 execution cases across the reference IR interpreter and JSON-round-tripped BytecodeVM, plus three explicit lowering-shape checks. Expectations are independently specified for both engines; merely agreeing with each other is not acceptance. Every execution shares a 10,000-dispatch budget across calls. Successful completion checks empty frames and no dollar-suffixed bookkeeping leaks. Fixtures deliberately omit Repeat and Index because BytecodeVM still lacks SAVEVAR/RESTOREVAR execution.

The cases cover absent/present zero/None entry values; closure snapshot presence versus changed caller-global value; source-seeded stale captures; an Action parameter named `_` on direct and closure calls; a nested direct reader; explicit Return versus implicit fall-through; and caller-side publication rather than host API return. Calling the interpreter's `call` or VM's `_call` from Python returns a value but does not itself publish it into `_`; source lowering supplies that publication.

The source-level direct-entry cases assert `_` is present **after** `Call Read`; that binding is created by the caller's lowered store, not evidence of entry initialization. The no-initialization finding also relies on inspecting Action entry/lookup and a supplemental direct-host probe in each Python engine: compile an Action containing only `Return @_;`, invoke it with an empty environment, and require return `None`, absent global `_`, and empty frames before/after. That probe passed; it is separate from the 47 committed cases.

Failure witnesses cover Get out of bounds, Length of an untyped parameter holding an integer, and Call to an Action dividing by zero. They prove only that the failed producer's publication is skipped, frames are popped, and a previously completed inner `Call Answer` remains globally visible as `42`. They do **not** promise transactional rollback or general exception-safe binding unwind. Budget exhaustion is never an accepted runtime outcome.

[`test_vm_result_publication_contract.py`](../../tests/self_host/test_vm_result_publication_contract.py) adds four small authored-runtime cases: three deliberate direct-call discrepancies and one successful explicit-publication agreement. They use the established source → authored lexer/parser/lowerer/encoder/VM harness with a two-million **host-IR instruction** budget and 10,000-iteration While guard. The trace bounds the whole hosted composition across internal Actions; it does not count authored bytecode dispatches directly. They require `VMFailed == 0`, exact expected output, empty host frames and zero authored frame depth/entry count. This is hosted execution of authored code, **not** a fresh native semantic-parity claim.

All 47 tests pass with unchanged parent production sources. None demonstrates a parent failure/candidate runtime repair, and no expected-failure marker hides an unresolved assertion.

## Proposed result-only protocol for the next implementation

The following is a concrete candidate for review, **not an approved language specification or an implemented guarantee**. Its purpose is to make the next patch falsifiable instead of selecting behavior implicitly while editing lookup code.

1. Give main and each executing Action invocation one explicit result owner. Represent presence separately from value; an absent result reads as `None`, not as a fallback into an older frame. Preserve an absent slot until a successful producer publishes to it.
2. Initialize a direct Action from a copy of the caller's effective result presence/value. Initialize a closure invocation from its creation-time effective result snapshot. If a parameter is named `_`, its argument supplies the initial present slot, retaining current entry precedence; later successful result producers replace that slot. A parameter named `_` is therefore an initializer, not an immutable shadow of the result owner. This is a deliberate compatibility change that requires explicit old/new witnesses.
3. On successful Call/Get/Length, replace only the currently executing owner's slot. Builtins need no additional Action owner. Evaluate call arguments before entering the callee. Evaluate explicit Return's operand before leaving its owner. After the callee exits, publish that returned value as a present value in the caller's slot. Keep implicit Action return as `None` for an initial Python-engine implementation; do not silently coerce it to zero to match the authored VM.
4. MakeClosure snapshots the **current effective** result presence/value exactly once, before its own successful Call publishes the new handle. Explicitly omit `_` from the existing env/all-frame merge, then add the current owner's value only if present. Otherwise an older frame could resurrect a binding that the owner says is absent. Keep ordinary user captures shallow and unchanged. Repeated Invoke starts anew from the same snapshot; deferred Spawn/Await also starts from that snapshot, not await-time ambient state.
5. Preserve the distinction between a host API returning a value and a source producer publishing it. On exceptional exit, pop the result owner with the Action frame and do not perform that Call's success publication. Do not add transactional rollback of ordinary global/object side effects. The current evidence does not establish this proposed caller-result isolation under failure; it needs its own tests before implementation.

Under this candidate, the source-seeded closure that calls Answer then returns `@_` changes from `17` to `42`; a parameter `_ = 17` also changes from returning `17` after `Call Answer` to `42`. A closure that performs no producer retains its creation-time result, including captured zero/None. A direct nested reader inherits the caller's effective slot rather than an unrelated global write. A fall-through Action still publishes `None`. These are **future acceptance expectations**, not assertions that pass against a new implementation in this increment.

An absent creation-time result also changes deliberately: a closure with no producer reads `None`, even if the caller has since produced `42`. It no longer falls through to the live global `42`. This must be an explicit old/new witness, not an unnoticed consequence of introducing the owner.

The smallest sound implementation experiment would change result-owner entry/exit, result reads/writes, and snapshot construction together in **both** Python engines, without an IR opcode change. It must update affected compatibility expectations openly and add bounded old/new regressions for all three producers, nested/repeated Invoke, `_` parameters, absent versus present None, snapshot absence beneath older present frames, deferred execution and failed calls. Filtering `_` alone, mutating every capture, or changing only `_read` is insufficient. An implementation must not be called cross-runtime admitted until an explicit authored/native policy and corresponding executable tests exist.

## Verification

Counts overlap; do not add them. Production sources are unchanged from the exact parent. Acceptance additionally requires all eight GitHub checks successful on the exact final documentation-updated review head; earlier-head CI is not sufficient. Record CI acceptance in a PR comment without changing that head. No merge is authorized.

| Gate | Result |
| --- | --- |
| New bounded initialization/publication cases | **47 passed in 0.79s** |
| Independent read-only review and rerun | **47 passed in 0.85s**; no material blocker |
| Fresh compiler/VM/launcher/generator/storage gate | **622 passed, 18 skipped in 204.92s** |
| Complete suite with fresh per-test artifacts | **1,993 passed, 20 skipped in 973.99s** |
| Fresh production bootstrap and Python-free smoke, including complete compiler-bytecode reproduction | Passed |
| Supplemental absent-result direct-host probes, both Python engines | Passed; no global result binding created |
| Python 3.10 syntax grammar and `git diff --check` | Passed; Python 3.10 runtime coverage belongs to CI |

Independent review inspected the test harnesses, lowering, Python call/read/write paths and authored VM boundaries without editing files. It found no material blocker; this final text clarifies the direct-entry evidence limitation and host-IR budget terminology it flagged. The concrete owner protocol remains a proposal, not a result of these passing tests.

Bootstrap/smoke ran in detached `/workspace/Kuro-result-publication-bootstrap` at the exact parent, with production sources identical to the candidate. SHA-256 identities of the interpreter, JSON VM, lowerer and authored VM were checked against the candidate. Generated images remain outside the review commit and do not race per-test artifacts.

```sh
.venv/bin/python -m pytest -q \
  tests/runtime/test_result_publication_contract.py \
  tests/self_host/test_vm_result_publication_contract.py \
  --basetemp=/workspace/kuro-publication-contracts --durations=8
.venv/bin/python -m pytest -q \
  tests/runtime tests/ir \
  tests/compiler/test_first_class_closures.py tests/compiler/test_concurrency.py \
  tests/self_host/test_vm_loop_return.py tests/self_host/test_vm_cross.py \
  tests/self_host/test_vm_result_publication_contract.py \
  tests/self_host/test_artifact_launcher.py tests/self_host/test_compiler_driver.py \
  tests/self_host/test_native_codegen.py tests/self_host/test_native_integer_storage.py \
  tests/self_host/test_native_integer_storage_capacity.py \
  tests/self_host/test_initializer_list_stack.py \
  tests/self_host/test_recursive_expression_operators.py \
  --basetemp=/workspace/kuro-publication-focused --durations=15
.venv/bin/python -m pytest -q \
  --basetemp=/workspace/kuro-publication-full --durations=20
# Separate detached parent worktree, with identical production sources:
make native-hosted-bootstrap PYTHON=/workspace/Kuro/.venv/bin/python NATIVE_TARGET=x86_64-linux
sh tests/self_host/python_free_native_smoke.sh
```

## Limits and next path

No stale-result behavior is repaired here. No Index precedence changes, mutable-capture redesign, recursive Invoke resource guarantees, BytecodeVM Repeat support, direct-native cleanup, or general exception unwind are included. Fresh production bootstrap and Python-free smoke guard their existing contracts, not these new result semantics. Python still seeds native images, and Clang still assembles/links them; Python-free execution and complete compiler-bytecode reproduction are not independent clean-checkout native construction.

Next: review the explicit result-owner candidate, implement only its admitted Python-engine slice with old/new regressions if accepted, and independently select authored/native initialization and implicit-return policy. Keep Index loop-versus-capture/parameter precedence separate. The broader independence work still includes indexed-storage control-flow facts, full analyzer/compiler/runtime bytecode admission, Kuro-built native images and a repository-owned object/executable writer.

The subsequent [cross-path protocol review](result-protocol-review.md), stacked on this increment's exact verified head, finds that explicit source writes to `_`, host-root visibility and native parameter handling are additional unresolved decisions. It does not approve this proposal or implement a runtime repair. The verification above remains this increment's historical evidence.
