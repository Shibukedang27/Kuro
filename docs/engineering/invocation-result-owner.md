# Invocation-owned results

This implementation is stacked on open, unmerged [PR #101](https://github.com/Shibukedang27/Kuro/pull/101), exact verified head `313973fdc884c1d6c56e1acec9385aa0d8f3f1f6` (eight successful checks rechecked). The owner delegated the semantic choice. The selected direction implements the [prior owner proposal](result-publication-contract.md#proposed-result-only-protocol-for-the-next-implementation), with an explicit policy for source writes. Keep this PR and its ancestors open and unmerged. **Strict independence remains unfinished.**

## The behavior being repaired

Previously, an Action's captured or parameter `_` could keep returning 17 after `Call Answer` had successfully produced 42. Producers wrote a shared global binding, but reads could prefer an immutable overlay. A failed outer call could also leave its inner successful result in the root. Modern Python engines now give every executing Action a writable result owner, rather than making successful results compete with an old overlay.

The term **producer-owned** describes where producer completion publishes: the executing invocation owns the destination. It does not mean that only producers may write `_`. Explicit assignment and mutation of `_` remain legal and target the same owner. A distinct producer-only write policy would require a new classification boundary, despite the existing shared `STORE_LIST` lowering; this patch deliberately chooses the coherent writable-slot policy without changing opcodes or image formats.

## Exact modern Python rules

These rules apply equally to the reference IR interpreter and the serialized JSON BytecodeVM, not to the frozen bootstrap oracle.

| Boundary | Selected rule |
| --- | --- |
| Main/root | Its optional `env["_"]` binding is the main result owner; external embedding APIs can still seed and inspect it. |
| Direct Action entry | Copy the caller's effective result **presence and value**, before pushing the frame. No dynamic lookup into older frames afterward. |
| Closure invocation | Copy the creation-time effective result snapshot. An absent snapshot stays absent even if globals or older frames have a result. |
| `_` parameter | An actually supplied argument initializes the new owner's slot, overriding inherited/captured state. It is not an immutable overlay. Ordinary arity behavior is unchanged. |
| No producer/write | An absent slot reads as `None` without creating a binding. Present `None`, zero, and other values retain their presence. |
| Successful Call/Get/Length | Replace only the executing owner's slot, after the operation succeeds. Arguments and explicit Return operands are evaluated before exit/publication. |
| Explicit `_` writes | Assignment, Update, Add, Input, Append and text Set use the same owner. An absent Add starts from zero; present `None` is not absence. Collection mutation remains shallow/shared. |
| Explicit/implicit return | Explicit Return returns its operand; fall-through still returns `None`, not the callee's last result. A successful **source** Call publishes that returned value, including present `None`, to its caller. |
| Host call API | Returns a value without source-level publication. Its nested producers modify its Action owner, not the root. The root's original presence/value survives. |
| Failure | Pop the callee's owner with its frame and skip that Call's success publication. Completed inner producers do not leak into the caller's slot. This is not rollback of ordinary globals, files, channels or shared heap mutation. |
| MakeClosure | Snapshot the effective result once, **before** publishing the new closure handle. Merge ordinary captures as before, remove any merged `_`, then include only the current owner's present slot. |
| Repeated/deferred Invoke | Each invocation starts from the original snapshot. Spawn/Await does not use ambient await-time state. Ordinary captured collections remain shallow aliases. |

The representation needs no new sentinel or parallel frame stack: a frame's optional `_` key carries presence, while a present key may hold `None`. Result lookup does not fall back to globals when a frame lacks that key. Entry and finally cleanup therefore share the existing Action-frame lifetime. Ordinary bindings retain their previous global-write/overlay policy; Index and hygienic loop bookkeeping are not changed.

## Supported native paths

The Kuro-authored VM implements the same **scalar direct-call ownership** rule using its existing frame-result/value-display arrays: entry copies the parent's value and Decimal display, a `_` parameter initializes the frame result, scalar VMStore writes replace it, and a failed VMInvoke does not publish or push a success result after popping its frame. The root remains numeric zero before a result; this VM has no separate absent/None representation. Fall-through remains zero. No new opcode, framed-bytecode or image format is introduced. These changes run both in the hosted composition and through a freshly built native authored-VM launcher.

| Executable boundary | Modern Python | Authored VM, including native launcher | Python-hosted direct native / Kuro generator |
| --- | --- | --- | --- |
| Root result 17, direct reader with no producer | 17 | 17 (previously zero) | Direct x86-64: 17; ARM64 static-route ambient read rejects |
| `_` parameter 17 at entry | 17 | 17 (previously zero) | Existing admitted parameter-local paths: 17 |
| Parameter 17, then successful Answer returning 42 | 42 (previously stale 17) | 42 | Existing admitted paths: 42 |
| Parameter 17, then assignment/Update/Add to 23 | 23 (previously stale 17) | 23 | Direct x86-64: 23; static ARM64 rejects STORE_LIST/UPDATE/ADD; typed generator assignment control: 23 |
| Inner result 42, implicit outer return | `None` | Zero | Existing zero-comparison control succeeds |
| Ambient root 17, caller's `_` parameter replaced with 42, nested no-parameter Read | Reads caller-owned 42 | Reads caller-owned 42 | Direct native retains ambient 17; this complex fixture selects ARM64's already-admitted dynamic route |

The last row is an **outstanding migration boundary**, not parity. Its bounded source branches on `@_ == 17`: direct native is expected to print `1`, the authored launcher prints `0`. ARM64 route selection matters: a top-level call to the simple Read Action uses the static evaluator and rejects its ambient read; the complex Outer Action contains nested calls and selects the existing dynamic emitter, which admits its Read helper. The three simple explicit-write Actions instead use the static evaluator and reject their unsupported STORE_LIST/UPDATE/ADD. Portable tests now assert all four exact static rejection messages and successful dynamic-route function emission even on Linux; actual ARM64 execution belongs to CI. Safely migrating `compiler/native.py` requires an owner channel across native nested/recursive calls, captures and return/failure boundaries; changing just parameter lookup or global writes would conceal that gap. This increment deliberately leaves that backend's production code unchanged rather than silently broadening native admission or claiming complete adoption.

The Kuro-written native generator also stays unchanged. Typed `_ : Integers` parameter programs already use one local slot for entry, successful publication and explicit assignment. The real compiler → generator → assembly/link → executable tests verify 17, 42 and 23 for those admitted cases. Their **untyped** counterparts still reject with `NativeFailed == 1`, `NativePrepareParamType == "NONE"` and empty `NativeOut`; no unsupported output is executed. The generator tests are hosted by the reference interpreter and linked with Clang, not evidence of native generator self-construction. Local execution is Linux x86-64; Darwin ARM64 execution belongs to CI.

Authored closure snapshots, absent-vs-present `None`, collection-valued `_` writes and general native failure/exception unwinding are not admitted by this scalar migration. A raw malformed-opcode regression checks the authored VM's own `VMFailed` path after an entered outer Action completes an inner result of 42: root 17 survives, frame depth/entries return to zero, later output does not execute, and ordinary global `Side = 99` survives. Division by zero currently escapes through the hosted interpreter instead, so the test does not claim that unsupported error path was repaired. Nested Decimal publication separately checks both value `3.25` and display text `"3.25"`.

## Verification

The new and revised tests use explicit expectations rather than engine agreement alone. Counts overlap and must not be added. The retained characterizations were openly revised to the selected policy; the new boundary file additionally restores absent-top-owner snapshot resurrection coverage beneath older None/zero/17 frames and tests absent Add/Append, no-producer direct entry, deferred snapshots and host-root presence on success/failure.

| Gate | Evidence |
| --- | --- |
| Corrected final seven result contract/regression files | **180 passed in 5.22s** |
| Same 180 cases copied into detached exact-parent worktree, importing its own compiler | **104 failed, 76 passed in 3.92s**, expected old/new failures |
| Corrected final contracts plus all runtime/IR tests, fresh artifacts | **256 passed in 5.61s** |
| Focused fresh native/compiler/runtime/IR gate | **570 passed, 19 skipped in 130.95s**; collected before the last strengthened boundary cases, which the final 256-case gate covers |
| Authored failure-isolation witness separately | Candidate passes; exact parent fails because root is 42 instead of 17 |
| Fresh production bootstrap and Python-free smoke | Passed, including full compiler-bytecode reproduction |
| Candidate/bootstrap production-source identity | All **67** tracked compiler/authored/bootstrap files byte-identical |
| Changed/new Python files parsed with Python 3.10 grammar, `git diff --check` | Passed; actual Python 3.10 execution belongs to CI |
| Independent final read-only review and runtime/all-result rerun | **247 passed in 5.46s**; no remaining blocking production defect |
| Complete fresh suite before ARM64 expectation correction | **2,112 passed, 20 skipped in 816.79s** |
| Corrected native result contracts and portable ARM64 admission cases | **30 passed in 4.98s** |
| Complete fresh suite after correction | Final result recorded in the PR verification comment against the immutable head; acceptance is not claimed by this table |

The parent proof includes generator-file assertions that fail in the Python reference control before reaching unchanged native generator code. It is not evidence that every native generator case was broken. Authored-entry/parameter/scalar-write and failed-publication witnesses independently fail on the parent VM itself. Rejections and unchanged native-boundary controls remain passing evidence, not repaired capabilities.

Fresh bootstrap ran in `/workspace/Kuro-owner-bootstrap`, a detached exact-parent checkout with only the candidate's three production-file diffs applied. Imports were checked to use that checkout, not the development checkout. SHA-256 comparisons covered all 67 tracked production files. Generated images stay outside the commit and per-test artifact directories. The full fresh-suite run was deliberately restarted after strengthening tests, rather than treating its earlier partial collection as complete evidence.

```sh
.venv/bin/python -m pytest -q tests/runtime tests/ir \
  tests/self_host/test_vm_result_publication_contract.py \
  tests/self_host/test_result_native_path_contract.py \
  tests/self_host/test_result_codegen_contract.py \
  --basetemp=/workspace/kuro-owner-contracts-corrected-head
.venv/bin/python -m pytest -q \
  --basetemp=/workspace/kuro-owner-full-corrected-final --durations=20
# Fresh candidate-production checkout, not pre-existing images:
make native-hosted-bootstrap PYTHON=/workspace/Kuro/.venv/bin/python NATIVE_TARGET=x86_64-linux
sh tests/self_host/python_free_native_smoke.sh
```

**Final acceptance requires eight successful CI checks on the exact final documentation-updated head**, the complete fresh-suite result, and an independent review. Record acceptance in a PR comment without changing that commit; earlier-head checks and this opening evidence are not acceptance. Keep the PR open and unmerged.

### CI-discovered admission correction

Initial implementation head `0210e540c6d1c8cc3369e6aa2d954271ba9009d9` passed the complete Linux suite but failed macOS CI on four new test assumptions: one dynamic-route witness was wrongly expected to reject, while three static-route write Actions were wrongly expected to compile. The correction changes only tests and this documentation: assert existing static rejections, execute the admitted dynamic case, and cover route selection portably. No production change, new skip/xfail or expanded admission is used to make CI pass. All eight checks must rerun successfully on the corrected documentation-updated head; earlier results do not count. The fresh corrected-tree full rerun and correction review are recorded in the final PR verification comment.

## Limits and next path

The frozen `bootstrap/python/kuro.py` remains a compatibility oracle with its historical syntax and behavior. General lexical capture ownership, Index precedence, BytecodeVM Repeat admission and broad exception/resource cleanup are separate work. Python still seeds native images and Clang still assembles/links them. Python-free execution and compiler-bytecode reproduction do not establish independent clean-checkout construction.

Next, continue from the explicitly admitted native result boundaries, then resume full analyzer/compiler/runtime admission, Kuro-built native images and a repository-owned object/executable writer. Do not infer strict independence from this result-slot repair.
