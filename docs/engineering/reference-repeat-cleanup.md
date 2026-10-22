# Reference Repeat cleanup across direct Action calls

This increment is stacked directly on verified open/unmerged [PR #96](https://github.com/Shibukedang27/Kuro/pull/96), exact head `92dcd40980e2e11aa493cb4d818b9ad58d29ad04` (8/8 checks). Keep the new review PR open and unmerged. Strict independence remains unfinished.

## Why this repair

The [authored VM loop-return repair](authored-vm-loop-return.md) exposed a separate reference-lowerer defect. Every Action and main used globally stored `__repeat_i{lexical_depth}` counters. A Repeat-owning callee could overwrite a caller's live counter: a normally completing two-iteration callee reduced a three-iteration caller to one iteration; an early-returning callee exhausted a bounded 10,000-instruction trace instead of completing. Return also bypassed the normal `Index` restoration.

The production change is confined to [`compiler/lower.py`](../../compiler/lower.py). It makes ordinary direct and recursive Action calls safe for this counter/return boundary. It does not establish general closure invocation, Index semantics or direct-native Action parity.

## What changes

Each Repeat saves its hidden counter and then `Index` in invocation-local IR temporaries before initialization. Normal completion restores `Index` and then the counter. This preserves existing values and removes previously unset bindings in the reference interpreter, rather than leaving hidden counters in its global environment. Skipped loops use the same restoration path; negative-count validation still occurs before either save.

The lowerer keeps a static stack of active Repeat bindings while lowering each body. Before a Return, it first lowers the value expression, then emits restoration for every active binding in reverse nesting order, then emits the unchanged Return operand. `Return Index` therefore captures the current iteration value before restoring outer bindings. Emitting cleanup for one Return does not consume the static stack: sibling branches and later returns still receive their own correct cleanup. The stack is released in `finally` when lowering a body finishes. Actions are lowered separately from main and nested declarations do not lower inline, so their cleanup contexts cannot be confused.

Counters now use `__repeat_i{depth}$`. The lexer does not allow `$` in source identifiers, so a source global or parameter named `__repeat_i1` cannot shadow the internal counter. Depth distinguishes nested loops; save/restore, not naming alone, handles reentrant direct calls. Ordinary assignments still write shared globals. No opcode, parameter-overlay policy, runtime frame limit or loop-count rule changes.

## Bounded regression evidence

[`test_repeat_cleanup.py`](../../tests/runtime/test_repeat_cleanup.py) adds ten reference-interpreter tests with a 50,000-instruction trace budget. They cover completing and early-returning callees in a caller Repeat, recursive and repeated calls, nested Repeat/While/If cleanup, `Return Index`, zero-count loops, existing/unset Index and counter restoration, source global/parameter name collisions and shared ordinary global writes. Successful runs require clean Action frames and no newly leaked internal counters.

Loading the unchanged lowerer from exact base `92dcd40` in a separate process, without changing the worktree, produces **seven failures and three passes** in this new module. Two failures exhaust the bounded trace; the others expose truncated output, overwritten source state or leaked counters. These are baseline witnesses, not acceptance results.

The existing [twenty authored-runtime output contracts](../../tests/self_host/test_vm_loop_return.py) now all execute against the repaired reference interpreter, including the six previously excluded reentrant/depth fixtures. Its reference runner has a 10,000-instruction budget so a future counter regression cannot hang the suite. The same twenty explicit contracts still execute through hosted authored VM, framed launcher and a fresh native launcher. The ten new Index/environment-specific tests are reference-only; these do not silently claim broader Index parity.

## Verification

Final local verification and independent review results follow. Counts across gates overlap and must not be added.

| Gate | Result |
| --- | --- |
| Reference cleanup, IR and twenty contracts across authored runtime paths | **102 passed in 10.28s** |
| Fresh compiler/VM/launcher/generator/storage gate | **480 passed, 18 skipped in 218.53s** |
| Complete suite, fresh per-test artifacts | **1,906 passed, 20 skipped in 1,044.26s** |
| Independent final reference cleanup, IR, authored contracts and inherited VM parity | **126 passed in 17.14s** |
| Fresh production hosted bootstrap and Python-free smoke, including exact full compiler bytecode reproduction | Passed |
| Python 3.10 syntax grammar and `git diff --check` | Passed |

Independent final review found no blocking issue within the stated direct/recursive-call scope. It inspected nested `Return Index` IR and sibling If paths: value capture precedes inner-to-outer restoration, Return does not mutate the static lowering context, and normal exits retain their own cleanup. Review explicitly identified the closure, Index-parameter, direct-native and error-path boundaries below; they were not silently treated as parity. No production or test changes followed the passing final gates.

Commands:

```sh
.venv/bin/python -m pytest -q \
  tests/runtime/test_repeat_cleanup.py tests/ir \
  tests/self_host/test_vm_loop_return.py \
  --basetemp=/workspace/kuro-repeat-cleanup-contracts-final --durations=10
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
  --basetemp=/workspace/kuro-repeat-cleanup-focused --durations=15
.venv/bin/python -m pytest -q \
  --basetemp=/workspace/kuro-repeat-cleanup-full --durations=20
make native-hosted-bootstrap NATIVE_TARGET=x86_64-linux
sh tests/self_host/python_free_native_smoke.sh
```

Production images were rebuilt before the smoke. During use the smoke blocks Python and host assembly/link tools on PATH, and compares complete compiler stage-1/stage-2 bytecode. This proves Python-free use of hosted-seeded images, not clean-checkout independent native image construction. Generated tracked `dist/` artifacts are restored and not committed.

Final acceptance requires all eight GitHub checks successful on the exact documentation-updated review head. The PR's exact-head verification record is authoritative; an earlier implementation-head result does not verify a later documentation commit.

## Remaining boundaries and next path

- **Closure capture is not invocation-safe yet.** `MakeClosure` snapshots the environment, including an active hidden counter. `Invoke` reads captures through an immutable priority overlay, while loop writes target globals. A closure made inside Repeat and invoking a Repeat-owning Action at the same depth can repeatedly read a stale captured counter. An independently reviewed witness compiled but exhausted a 500-instruction trace; the parent reproduced exhaustion at instruction 501. This defect predates the new counter spelling. Do not treat these programs as safe differential oracles. A minimal witness is `Action Worker Dummy: Integers; Repeat 2; Print 7. Done. Return 0; Done. Repeat 1; Call MakeClosure "Worker"; Handle = @_; Call Invoke Handle, 0; Done.` Run it only with an external instruction budget until repaired.
- **A source parameter named `Index` still has overlay priority.** `Action Pick Index: Integers; Repeat 2; Return Index; Done. Return 0; Done. Call Pick 42; Print @_.` prints `42` in the reference interpreter. This existing binding issue is not repaired by hygienic hidden counters.
- **Direct-native Actions are not the acceptance path for this cleanup contract.** Native main SAVEVAR/RESTOREVAR lacks the reference interpreter's unset sentinel, and the x86-64 Action emitter currently skips these operations. Fresh native *artifact launcher* tests execute Kuro bytecode through the authored VM; they are not evidence that direct native Action emission implements this IR cleanup. Native backends remain unchanged.
- **No exception-safe unwind is added.** Runtime errors bypass emitted Return cleanup. There is no language-level recovery/continuation being introduced; any future recovery design needs explicit unwind obligations. Implicit no-Return values and noncanonical Decimal display remain separate reference/authored-runtime discrepancies.

The next runtime increment should isolate closure-capture/invocation binding ownership and cleanup, including compiler-private counter state, before claiming general Repeat differential parity. Keep #95's compiler loop-flag workaround. Then resume explicit indexed-storage entry/backedge/exit facts and safe collection control flow, full analyzer/compiler/runtime bytecode admission, Kuro-built native images and a designed repository-owned object/executable writer. Storage capacities, overflow/logical bounds, Linux x86-64-only fixed-storage qualification, other runtime/platform limits and artifact admission remain unchanged. Python still seeds production native images and Clang still assembles/links them. **Strict independence remains unfinished.**
