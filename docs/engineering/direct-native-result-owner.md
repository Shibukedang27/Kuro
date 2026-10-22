# Direct-native invocation results: bounded x86 channel

This increment is stacked directly on open, unmerged [PR #102](https://github.com/Shibukedang27/Kuro/pull/102), parent `504d6cc00db4f862df0d4a0c95240be66b85ea33`. The live stack was inspected before work: #102 still targets #101, and its exact head has eight successful CI checks. Keep this increment and every ancestor open and unmerged. **Strict toolchain independence remains unfinished.**

## What changes

The [previous result-owner increment](invocation-result-owner.md) deliberately left a direct-native boundary: a no-parameter Action could read the ambient root result instead of its caller's writable `_` slot. For example, after a caller's `_` parameter is replaced by a successful producer returning 42, its nested reader could still see root 17.

The shared x86-64 emitter now gives each Action an eight-byte, stack-frame-local result slot, including Actions with no `_` parameter. Direct callers load their current slot into the hidden incoming `%rax` channel **after** setting all six possible argument registers and the independent `%r10` environment channel. The callee saves the incoming value before parameter stores; a supplied `_` parameter therefore overrides it. Recursion gets a fresh slot with each ordinary native stack frame. This uses the existing native return register, with entry and exit meanings separated by the call boundary; it adds no source parameter, opcode, bytecode field, image format, or global owner-pointer stack.

Every scalar native load/store of `_` in an Action resolves to that local slot. Existing lowered `STORE_LIST _` publication after a successful Call/Get/Length and explicit scalar assignment/Update/Add therefore share one destination. Return evaluates its operand from the current frame and returns it in `%rax`; native fall-through remains zero. A raw IR `CALL` does not itself publish into its caller's slot: the source Call's following store does. Completed nested producers cannot mutate the root merely by executing in a callee. Ordinary globals and shared heap effects are not rolled back.

Main retains a separate zero-initialized BSS result owner, including when main never explicitly names `_`. Existing captured-result entries, where already admitted by capture analysis, are copied into the Action's local slot rather than written back to the environment snapshot. This is not a migration of general closure creation-time result capture.

## Admission stays bounded

The new hidden channel transports one word, **not a runtime kind or collection-length pair**. Inherited-owner reads are admitted only when a conservative rejection-only analysis proves an integer channel. The analysis first follows control flow until a definite owner overwrite to find Actions that actually depend on their entry result. It distinguishes literal `"_"` (used throughout the authored VM) from a variable read. Noninteger provenance then flows monotonically through existing globals/locals, explicit assignments, call parameters, hidden-owner edges, and return operands. Decimal/Text constants, input, collection access and opaque builtin results cannot silently become integer-owner evidence. Facts union across branches and successive writes; this can reject safe programs rather than guess a type.

An inherited reader reached with a potentially noninteger result rejects native emission with `result owner ... requires an integer-only channel`. Programs combining inherited readers with Invoke/Spawn/Await reject rather than acquiring unproved closure/task channel semantics. A collection- or input-backed `_` together with Actions also rejects before assembly output, because those existing buffer representations collide with the scalar owner. This intentionally narrows ambiguous shapes; it does not add backend capability. Existing explicit parameter/type paths that do not depend on an inherited owner retain their prior admission rules, not a new general type-safety guarantee.

The production change is only in `compiler/native.py`. ARM64 emission and its static/dynamic route selection are unchanged, as are the Kuro-authored generator, compiler, VM, and frozen bootstrap oracle. The old nested witness now prints `0` on executed x86-64 and still expects `1` on the admitted ARM64 dynamic route. Static ARM64 ambient-read and STORE_LIST/UPDATE/ADD rejections remain exact portable tests. Neither assembly text nor Linux output establishes ARM64 owner parity. The x86 macOS emitter shares this lowering, but execution evidence must be identified by platform rather than inferred from that sharing.

## Success, failure, and exact regressions

`tests/self_host/test_direct_native_result_owner.py` exercises actual Linux x86-64 executables for direct inheritance, `_` parameter precedence, successful replacement before another nested read, distinct recursive owners, explicit writes, inner/outer return boundaries, and the raw-IR no-publication boundary. The revised cross-path contract independently runs the authored compiler/VM launcher and pins the unchanged ARM64 boundary. Portable rejection cases prevent Decimal/Text inherited reads and collection/input owner collisions from silently producing executables.

Direct native currently has **fail-stop**, not recoverable Action exceptions. Bounds/resource failure exits the process and integer division failure traps; subsequent source publication/output cannot execute. Failure witnesses check process failure and the completed output prefix only. They cannot inspect a caller/root after process death and are not evidence of recoverable unwinding, cleanup, or rollback. The existing authored VM's separate failure-isolation proof remains in the parent documentation; it is not a substitute for an unimplemented direct-native exception mechanism.

## Verification and acceptance

Evidence is recorded against the final immutable, documentation-updated head in the PR verification comment. Acceptance requires all of the following, without treating earlier-head checks or stale images as final evidence:

| Gate | Final local evidence |
| --- | --- |
| Exact native owner/cross-path contracts, independent reviewer rerun | **28 passed** |
| Same final tests copied into a detached exact-parent checkout, importing that checkout's compiler | **9 failed, 19 passed in 2.45s** |
| Focused compiler/runtime/IR/native-generator/result gate, fresh artifacts | **634 passed, 20 skipped in 400.15s** |
| Complete fresh suite | **2,130 passed, 20 skipped in 850.39s** |
| Independent read-only review of final ABI and admission proof | No remaining blocking correctness issue; additional alias/wrapper/branch rejection and definite-overwrite admission probes passed |
| Separate fresh bootstrap checkout | All four native images rebuilt after deleting old executables; Python/toolchain-blocked smoke and full compiler-bytecode reproduction passed |
| Candidate/bootstrap source identity | All **67** tracked compiler/authored/bootstrap files byte-identical |
| Python 3.10 grammar and `git diff --check` | Passed; actual Python 3.10 execution belongs to CI |
| Exact-final-head CI | Required **8/8** successful checks; final immutable-head outcome belongs in the PR verification comment, not an earlier-head claim |

The nine parent failures distinguish four newly enforced rejection cases from five ownership/publication witnesses (including the revised cross-path witness). The other nineteen are unchanged controls, not newly repaired capabilities. Counts overlap and must not be added. The bootstrap ran in `/workspace/Kuro-direct-owner-bootstrap`; per-test artifacts and generated production images remain outside the commit. The complete-suite gate above covers the final production and test tree; only evidence documentation was updated afterward.

Reproduction commands (fresh, distinct `--basetemp` paths are required):

```sh
.venv/bin/python -m pytest -q tests/compiler tests/runtime tests/ir \
  tests/self_host/test_native_codegen.py \
  tests/self_host/test_direct_native_result_owner.py \
  tests/self_host/test_result_native_path_contract.py \
  tests/self_host/test_result_codegen_contract.py \
  tests/self_host/test_vm_result_publication_contract.py \
  --basetemp=/workspace/kuro-direct-owner-focused-final --durations=10
.venv/bin/python -m pytest -q \
  --basetemp=/workspace/kuro-direct-owner-full-final --durations=20
# Separate candidate-production checkout; stop if construction fails:
make native-hosted-bootstrap PYTHON=/workspace/Kuro/.venv/bin/python NATIVE_TARGET=x86_64-linux &&
sh tests/self_host/python_free_native_smoke.sh
```

- Exact-parent regression proof importing the parent compiler, with repaired cases failing there and unchanged controls distinguished from repairs.
- Focused native/compiler/runtime/IR and real compiler-to-generator tests with fresh per-test artifacts, followed by a complete fresh test suite.
- Independent read-only review of both the owner ABI and rejection-only admission analysis, with blocking findings resolved.
- A separate candidate-production checkout, all tracked compiler/authored/bootstrap sources compared byte-for-byte, newly rebuilt native compiler/runtime/bytecode-launcher/generator images, and Python/toolchain-blocked smoke including full compiler-bytecode reproduction.
- Python 3.10 grammar checks, clean diff checks, and **eight successful CI checks on the exact final head**. Actual supported macOS execution belongs to CI; a skipped Linux-only executable test is not macOS parity evidence.

The initial independent review exposed missing noninteger-kind and collection-owner safeguards; those findings led to the explicit rejection boundary above. An early scanner version also confused literal `"_"` with a variable read and rejected the authored VM build. That version is not acceptance evidence. Fresh build verification must stop on any construction failure and must not smoke-test old images after a failed rebuild.

## Next path

Extend the result channel only alongside a proved native kind/presence/length representation and executable regression evidence. Closure/task creation-time snapshots, Decimal/Text inherited-owner operations, collection-valued results, recoverable failure unwinding, and ARM64 ownership remain separate work. The full analyzer/compiler/runtime still needs broader owned-backend admission. Python still seeds production native images, and Clang/LLVM still assemble and link them. Python-free execution and complete compiler-bytecode reproduction demonstrate useful bootstrap continuity, **not independent clean-checkout construction**. Python-free image seeding and repository-owned or explicitly owned assembler/linker output remain required; do not claim full independence or merge this stack without explicit owner instruction.
