# Result ownership: cross-path review and the unresolved decision

**Historical review:** The owner subsequently delegated the semantic choice. The [invocation-owner implementation](invocation-result-owner.md) selects the writable owner policy and records its actual admitted paths and regressions. The observations below describe this review's unchanged parent behavior, not the implementation's new contract.

This review is directly stacked on verified open/unmerged [PR #100](https://github.com/Shibukedang27/Kuro/pull/100), exact head `52408a7e07468623b1812db2a991d9f08936a25d` (eight successful checks rechecked live). It changes tests and documentation only. No production behavior, Index precedence, opcode or image format changes. Keep the review PR open and unmerged. **Strict independence is unfinished.**

## Finding first: the owner proposal is not a compatibility-preserving repair

The [previous result-only protocol](result-publication-contract.md#proposed-result-only-protocol-for-the-next-implementation) is a useful design candidate, not an approved implementation plan. It combines several independent observable changes: direct-entry inheritance, closed-over absence, writable `_` parameters, owner-local intermediate results, snapshot construction and failed-call isolation. A patch implementing all of these would select language semantics, not merely repair a stale read. Existing passing evidence does not justify that selection.

This review adds two especially important missing boundaries. First, source programs can explicitly assign, Update and Add to `_`; it is not just an internal producer destination. Second, an invocation whose capture lacks `_` can read live-global `42` while a nested MakeClosure captures an older frame's `17`, zero or present `None`. Ordinary reads and capture construction are different operations. A blanket capture filter, frame write or lookup exception cannot resolve these contracts by itself.

## All retained Python engines

The current engines are [`Interpreter`](../../compiler/interpreter.py) and serialized [`BytecodeVM`](../../compiler/bytecode.py). Both read the top frame then globals, write globals, construct closures by merging globals and all frames, and publish source Call/Get/Length results with a separate lowered store. Direct host call APIs return a value without publishing that return; source producers executed inside those calls still write global results. The new tests make this distinction executable, including absent entry without a created global binding.

The retained [`bootstrap/python/kuro.py`](../../bootstrap/python/kuro.py) is also an actual executable Python engine, but README explicitly freezes it as a compatibility oracle. It uses its own parenthesized syntax and lacks the modern closure protocol. Its locals override globals, direct entry uses live globals, and implicit return is `None`; an absent `@_` errors rather than reading `None`. Its Get/Length autoprint and debug IR trailer are historical differences, not proposed new semantics. It must not be silently migrated as part of a modern owner implementation.

[`test_result_bootstrap_contract.py`](../../tests/regression/test_result_bootstrap_contract.py) runs four bounded subprocess witnesses against that frozen engine, with its real syntax and explicit output/error expectations. [`test_result_protocol_review.py`](../../tests/runtime/test_result_protocol_review.py) adds 43 cases across the modern engines and lowering: explicit writes with a parameter overlay, hidden-frame snapshot resurrection, absent/seeded host entry versus nested source publication, direct-reader ambient state, repeated/deferred snapshots including absence/zero/None, and shallow ordinary collection aliases. All are current-behavior characterizations, not parent failures or an implemented fix.

## Authored VM and native pathways are not one policy

[`test_result_native_path_contract.py`](../../tests/self_host/test_result_native_path_contract.py) adds five source-level cases across two native routes plus one portable ARM64 admission regression: the Python-hosted native backend compiling source IR, and a freshly built native launcher executing the Kuro-authored compiler's framed bytecode. Each output or compile rejection has an explicit path-specific expectation. The authored compiler composition has a two-million host-IR instruction budget and 10,000 While-iteration guard; native execution has a 30-second timeout. One module-scoped launcher build avoids redundant builds.

| Source boundary | Modern Python IR/JSON VM | Python-hosted direct native | Native authored-VM launcher |
| --- | --- | --- | --- |
| Seed 17, then direct Action first reads `@_` | 17 | 17 on Linux x86-64; macOS ARM64 compilation rejects | 0 |
| Action parameter `_ = 17`, first reads `@_` | 17 | 17 | 0 |
| Same parameter, then successful `Call Answer` returning 42 | 17 | 42 | 42 |
| Action falls through after calling Answer | `None` | Integer-zero comparison succeeds | Integer-zero comparison succeeds |
| Explicit nested result 42, then outer Return 9 | 42 then 9 | 42 then 9 | 42 then 9 |

The Python observations are established by inherited/new bounded engine tests, not by executing Python inside the native-path test. In particular, the implicit-return native witness compares the result to zero before printing; it does not assert a full dynamic representation or `None` parity.

The first review head `007dedc15e19f5a12851ea9af2a8fb293557779a` passed the Linux suite but failed macOS CI because the new direct-entry test assumed ARM64 admission. `emit_macos_arm64` instead attempts to evaluate the zero-argument Read Action during compilation and raises `NativeBackendError: native action 'Read' reads a dynamic value`. The corrected witness asserts that exact rejection and no executable on macOS ARM64, then still executes the authored-launcher half. The additional portable test calls the ARM64 emitter even on Linux, so this admission mismatch is now caught locally. It is neither skipped nor repaired by changing production code; no ARM64 runtime value is invented for an image that does not exist. Earlier-head CI is not acceptance for the correction.

The authored VM's `VMLoad` special-cases `_` ahead of ordinary frame parameters; `VMInvoke` initializes the frame result to zero, and `VMSetResult` replaces that result on successful producers. Merely adopting its owner storage in Python would discard `_` arguments at entry, not preserve them as initializers. The Python native backend has a different rule: parameter-local reads and stores make successful publication replace the parameter. These are three observable policies, none uniquely selected by the language's older “most recent result” wording.

The Kuro-written native generator is another implementation path, not the same as the native launcher. Its function-mode load resolution searches parameters before the local result slot; implicit function return emits integer zero. Its result-kind analysis is also not a presence representation. Static load precedence alone does not establish immutable parameter ownership, because stores can replace the same slot.

[`test_result_codegen_contract.py`](../../tests/self_host/test_result_codegen_contract.py) adds four bounded compiler-to-generator witnesses. The two **untyped** `_`-parameter programs encode `BC_PARAM _ NONE`; the generator rejects them during parameter preparation with `NativeFailed == 1` and empty `NativeOut`. The tests pin that rejection, rather than conditionally accepting either rejection or future support. The corresponding **explicitly typed** `_ : Integers` controls generate, assemble/link and execute real output: entry-only reads print `17`, while Call Answer followed by `Return @_` prints `42`. The modern Python interpreter prints `17` for both typed controls. Thus admitted typed generator behavior agrees with direct native parameter replacement, not the Python overlay policy. Compiler/reference/generator interpretation shares a two-million host-IR instruction budget; successful host frames are empty and native subprocesses have 30-second timeouts.

Execution is qualified only on Linux x86-64 here, with Darwin ARM64 execution belonging to CI; other hosts skip the generator execution witnesses. The generator is hosted by the reference interpreter in these tests, then its assembly is linked by Clang. They do not prove native generator self-construction, native-image-generated output parity or general closure/error behavior. Do not generalize the untyped rejection to typed Actions or describe static parameter priority as proof of a stable parameter after publication.

## Why “producer-only” is not yet a complete policy

With `_ = 23`, `Update _ to 23` or `Add 6 to _` inside `Action Outer _` called with `17`, current Python reads remain `17`. A direct observer sees the global write `23`. Add reads the effective parameter `17` before writing its sum globally. After Return, the source caller publishes `17` again. The same cases are tested through direct and closure calls with explicit expectations.

The lowerer emits the same `STORE_LIST "_"` operation for explicit scalar assignment and successful producer publication. The new lowering witness pins that fact. A change keyed only on the opcode and destination cannot mean “update the owner only for producer completion” without also affecting explicit assignment. Update/Add also flow through generic variable writes. A producer-only rule therefore needs a deliberate classification/publication boundary; a uniform special-register rule needs an explicit policy for every source write. Neither should be smuggled into `_write` under the heading of capture hygiene.

The proposal's effective-snapshot rule is coherent only when entry, read, write, absence and frame cleanup use the same owner. The absent-top-frame witness demonstrates the old all-frame merge problem. It does not by itself decide whether a future direct Action inherits the caller's effective result, reads globals or starts unset/zero. Ordinary collection captures remain shallow aliases; a result fix must not copy or mutate all capture data.

## The decision needed before a production patch

The narrowest currently justified contract is the executable compatibility baseline, with discrepancies recorded rather than normalized. Before changing production, the owner/language specification must decide:

1. **What is `_`?** Is it a normal source binding whose parameter/capture overlay can remain stable, a uniform writable invocation register (including explicit assignment/Update/Add), or a special producer-publication slot distinct from ordinary writes? The prior proposal implicitly selects the second for producer completion but does not finish specifying explicit writes.
2. **What is entry state?** Direct calls currently use live globals in Python, while authored VM calls start at zero. Copying the caller's effective result is a third policy. For closures, preserving absent-snapshot fallback versus freezing absence as `None` is separately observable. Present zero and present `None` must not be treated as absent.
3. **What escapes an unsuccessful or implicit call?** Python publishes `None` on fall-through and retains completed inner global results after a later failure. The authored VM uses zero for fall-through. Caller-owner isolation under failure is an additional semantic change, not general exception cleanup or transactional rollback. A host call's root result is another boundary: its return does not publish, but nested source producers currently overwrite the root's global result; both absent and pre-seeded root cases are now tested.

A narrowly staged implementation can preserve Python entry, implicit-return and global-side-effect behavior while changing only successful publication's treatment of an existing overlay—but even that changes admitted `_` parameters/captures and needs explicit approval and old/new witnesses. It is not automatically the preferred language design. Conversely, approving the full owner model requires accepting all its documented compatibility breaks together and completing explicit-write and native admission rules. Do not silently infer approval from this tests-only PR.

Once a policy is selected, implement the same admitted slice in both modern Python engines, revise compatibility assertions openly, add old/new regression expectations for all producers and explicit writes, and separately admit authored/native behavior. Do not change Index precedence or ordinary capture ownership. Reusing the current tests as proof of a future owner implementation would be incorrect: their purpose is to make the semantic choice visible.

## Verification and limits

Acceptance requires eight successful CI checks on the exact final documentation-updated head, recorded in a PR comment without modifying that head. Counts overlap and must not be added.

| Gate | Result |
| --- | --- |
| Corrected final new bounded review cases | **57 passed in 2.93s** |
| Corrected new cases plus native compiler regression gate | **137 passed, 1 skipped in 32.50s** |
| Focused fresh toolchain/runtime gate, collected before final additions | **648 passed, 18 skipped in 198.85s** |
| Complete suite with fresh artifacts, before CI admission correction | **2,049 passed, 20 skipped in 934.60s**; corrected-tree rerun recorded in the PR verification comment |
| Independent initial final read-only review and separate per-file reruns | **56 passed**; no material blocker; correction review recorded separately |
| Fresh production bootstrap and Python-free smoke, complete compiler-bytecode reproduction | Passed |
| Production identity, all 67 tracked compiler/authored/bootstrap files | Identical to exact parent |
| Python 3.10 syntax grammar and staged `git diff --check` | Passed; actual Python 3.10 runtime execution belongs to CI |

Fresh production bootstrap and Python-free smoke passed in detached `/workspace/Kuro-result-protocol-bootstrap` at the exact parent, including full compiler-bytecode reproduction. Production sources remain unchanged; generated images stay outside the review commit and the per-test artifact directories.

Independent read-only reviews examined modern and frozen Python engines, authored/native paths, source/IR write classification, bounds and CI portability. The final reviewer reran the four new files separately with isolated artifacts: runtime **43 passed in 0.15s**, bootstrap **4 in 0.35s**, native paths **5 in 1.29s**, and generator **4 in 1.44s**. It found no material blocker and requested only final verification bookkeeping, now recorded here. No reviewer approved a language policy; the owner proposal remains unselected.

The focused gate ran the inherited runtime/IR, closure/concurrency, authored VM, launcher/compiler driver, native codegen/storage/capacity, initializer and expression suites with fresh per-test artifacts: **648 passed, 18 skipped in 198.85s**. It collected the first 26 Python review cases; the final new-case gate and complete suite cover subsequent additions separately. Production identity was checked across all 67 tracked `compiler/`, `self_host/` and `bootstrap/` files against the detached parent.

```sh
.venv/bin/python -m pytest -q \
  tests/runtime/test_result_protocol_review.py \
  tests/regression/test_result_bootstrap_contract.py \
  tests/self_host/test_result_native_path_contract.py \
  tests/self_host/test_result_codegen_contract.py \
  --basetemp=/workspace/kuro-protocol-final-contracts --durations=8
.venv/bin/python -m pytest -q \
  --basetemp=/workspace/kuro-protocol-full --durations=20
# Detached exact-parent worktree, production tree identical to candidate:
make native-hosted-bootstrap PYTHON=/workspace/Kuro/.venv/bin/python NATIVE_TARGET=x86_64-linux
sh tests/self_host/python_free_native_smoke.sh
```

This increment repairs no stale-result behavior, introduces no runtime capability, and does not claim full engine parity. Python still seeds images, and Clang still assembles/links them. BytecodeVM Repeat admission, direct-native cleanup, general exception unwinding, full analyzer/compiler/runtime admission, Kuro-built images and a repository-owned object/executable writer remain separate work. **Strict independence is not complete.**
