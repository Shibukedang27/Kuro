# Logical Length in the Kuro-owned integer generator

This increment is stacked directly on verified, open/unmerged [PR #103](https://github.com/Shibukedang27/Kuro/pull/103), exact parent `faf51505f8055bdc739ec52903e5f275332e0312`, with eight successful checks. Keep this increment and its ancestors open and unmerged. **Strict toolchain independence remains unfinished.**

## Why this next step

The [fixed integer-storage backend](kuro-owned-integer-storage.md) can initialize an owner, read and replace its cells, and compute and print integers, but it rejected even `Items = 11, 22; Length Items; Print @_.`. This is a missing operator in the Kuro-authored generator itself, not another extension of the Python-authored backend. Logical lengths are already recorded for the bounds checks. Reading that proved metadata is a smaller, sounder next step than adding dynamic collections or changing an unexecuted ARM64 owner ABI.

The [complete analyzer boundary](native-analyzer-generator-boundary.md) remains: its full artifact exceeds 4,096 tokens and needs further collection/control-flow support. A small executable Length witness is not execution of that analyzer.

## What is admitted

Within the existing isolated, straight-line fixed-integer-collection path, `BC_LENGTH <owner>` now pushes that owner's immutable logical cell count as one Integer. The owner must already have a validated literal initializer in the initialization prefix. The existing lookup selects its own count, not the number of owners, total cells, backing capacity, scalar value, or Text byte length.

The generated code materializes the count and pushes one word without consuming earlier operands. It does not read collection memory or modify cells. SET cannot change the count; append, rebinding, aliases and conditional initialization remain rejected. The existing compiler lowers source Length to `BC_LENGTH owner` followed by `BC_STORE_LIST _`; that separate store publishes the result to the existing scalar result slot. Raw generator bytecode does not acquire implicit result publication. This is the generator's existing GET/store protocol, not a claim that raw authored-VM instructions have identical side effects.

Only `self_host/native_codegen.kuro` changes in production. No source syntax, bytecode encoding, runtime, Python emitter, frozen bootstrap, assembly/linker or result-owner ABI changes. The historical Length rejection is replaced by a scalar-Length rejection, with the old fixed-owner source represented by positive executable regressions.

**An existing frontend discrepancy remains explicit.** The Python reference frontend infers these integer initializers as `Integers` and rejects `Length Items` with E3009 (`Length target must be Text, found Integers`). The Kuro-authored compiler already accepts and lowers the source, and the Kuro-authored VM already computes collection length. The new native witnesses require complete hosted-versus-native **authored-compiler token parity** and compare execution against that authored VM. They do not disable the Python typechecker or claim reference-source parity; a separate test pins its unchanged rejection. Resolving reference validation versus the existing authored collection operation is separate language-contract work, not silently included in this backend permission.

## Boundaries stay closed

Both generator execution ABI and output must be qualified `x86_64-linux` for the collection path. macOS x86-64, ARM64 and unverified execution remain rejected; no platform parity is inferred from assembly. Owner initialization still requires at least two literal cells, at most sixteen owners and 272 cells in total. The existing sixteen scalar slots and 4,096 bytecode-token ceiling are unchanged. Length's ordinary `_` publication consumes a scalar slot just like GET.

A missing operand, unknown or scalar name, alias, unsupported element type, growth, Action, branch or loop causes rejection with empty assembly. Operand-stack underflow and residual values retain their existing rejection rules. Bounds/overflow failures in admitted generated code remain process-level fail-stop, not recoverable exceptions or cleanup/rollback evidence.

## Verification

The [new regression file](../../tests/self_host/test_native_integer_storage_length.py) compares complete fresh-native/hosted authored-compiler tokens, executes those tokens in the authored VM, invokes a freshly built native Kuro generator, externally links its assembly, checks for undefined symbols, and executes the resulting freestanding Linux x86-64 image. Positive witnesses cover two and 272 cells, 200/72-cell distinct owners, sixteen owners totaling 272 cells with different endpoint lengths, cell mutation, repeated publication, computed positive and negative indices, stack preservation, and explicit raw publication. Native bounds failure checks exact completed output followed by exit 1. Portable and actual-generator rejections retain empty assembly; all twelve execution/output qualification combinations are exercised.

| Gate | Final local evidence |
| --- | --- |
| Independent read-only final review and separate fresh executable rerun | No blocking defect; **45 passed in 11.04s** |
| Same final tests in detached exact-parent checkout, importing its compiler/generator | **14 failed, 31 passed in 10.47s** |
| Focused compiler/runtime/IR/native-generator/storage/result gate | **819 passed, 20 skipped in 531.46s** |
| Complete fresh suite | **2,175 passed, 20 skipped in 934.65s** |
| Separate fresh bootstrap checkout, old executables deleted first | All four production images rebuilt; Python/toolchain-blocked smoke and full compiler-bytecode reproduction passed |
| Additional fresh native compiler + Linux-output generator under restricted PATH | Compiles/emits fixed-owner Length with Python/toolchains blocked; externally linked image executes exact `2\n3\n2\n22\n` output, no undefined symbols |
| Candidate/bootstrap source identity | All **67** tracked compiler/authored/bootstrap files byte-identical |
| Python 3.10 grammar and `git diff --check` | Passed; actual Python 3.10 execution belongs to CI |
| Exact final documentation-updated head | Required **8/8 successful CI checks**; immutable SHA and final outcome recorded in the PR verification comment |

The fourteen parent failures are positive capability witnesses that the previous generator rejected, including the qualified Linux admission control; the thirty-one passing cases are unchanged rejection/reference controls. Counts overlap and must not be added. Full/focused results cover the final production and test tree; only evidence documentation was updated afterward. Bootstrap and pytest artifacts are outside the commit. The separate bootstrap used `/workspace/Kuro-owned-length-bootstrap`; the additional probe retained source, native compiler bytecode, emitted assembly, linked image and exact output under `/workspace/kuro-owned-length-bootstrap-probe`.

Initial test-harness corrections are not acceptance evidence: a raw arithmetic probe used statement `BC_ADD` instead of `BC_BINOP +`, a qualification control omitted the existing mandatory print, and a repeated-source fixture used `Print` with a semicolon rather than its required period. The malformed source exposed an inherited native-compiler crash, not a change in this generator branch. Attempted Python-source differential checks exposed the existing E3009 rejection described above; final comparisons explicitly use the authored VM and separately pin the reference boundary. No typecheck was disabled and no production fix was inferred from these invalid probes.

Reproduce with fresh, distinct artifact directories:

```sh
.venv/bin/python -m pytest -q tests/compiler tests/runtime tests/ir \
  tests/self_host/test_native_codegen.py \
  tests/self_host/test_native_integer_storage.py \
  tests/self_host/test_native_integer_storage_capacity.py \
  tests/self_host/test_native_integer_storage_length.py \
  tests/self_host/test_result_native_path_contract.py \
  tests/self_host/test_direct_native_result_owner.py \
  tests/self_host/test_result_codegen_contract.py \
  tests/self_host/test_vm_result_publication_contract.py \
  --basetemp=/workspace/kuro-owned-length-focused-final --durations=12
.venv/bin/python -m pytest -q \
  --basetemp=/workspace/kuro-owned-length-full-final --durations=20
# Separate source-identical checkout; stop on any construction failure:
rm -f dist/kuro-compiler dist/kuro-runtime dist/kuro-bytecode dist/kuro-codegen
make native-hosted-bootstrap PYTHON=/workspace/Kuro/.venv/bin/python NATIVE_TARGET=x86_64-linux &&
sh tests/self_host/python_free_native_smoke.sh
```

Native image construction remains hosted seeding. The additional restricted-PATH operator probe builds a separate `build_native_codegen(..., target="x86_64-linux", output_target="x86_64-linux")` image, then uses the fresh compiler and generator without Python or compiler tools on PATH. Linking is deliberately performed afterward, outside that restriction. This is not Python-free construction or an owned linker claim. ARM64/macOS collection routes remain rejected, not merely untested successes.

## Next path

Resolve the existing reference Text-only Length validation versus authored collection-Length behavior as an explicit, separately tested language-contract slice. Separately minimize and repair native-compiler malformed-Print handling before claiming fail-closed source parsing; this increment's rejection guarantee is for the bounded generator artifact path, not every invalid source program.

A useful next storage increment needs a separate proof of initialized owner identity and length on every admitted path before branches or loops; growth additionally needs logical-length/capacity mutation and reset rules. Text token/name collections, aliases and Action parameters need their own representation and ABI contracts. Do not raise the token ceiling or remove analyzer Actions to turn a small operator witness into an apparent full-analyzer success.

Python still seeds native production images; Clang/LLVM still assemble and link generated output. Python-free use and full compiler-bytecode reproduction verify bootstrap continuity, not clean-checkout independent construction. Python-free image seeding and an owned assembler/linker remain required for the strict goal. ARM64 result ownership and recoverable native failure unwinding remain separate unfinished work.
