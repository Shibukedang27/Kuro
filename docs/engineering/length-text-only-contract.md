# Keep source Length consistent with its Text-only contract

> Historical compiler boundary: the later [bounded frontend Length gate](compiler-length-frontend.md) now rejects known non-Text targets before lowering. The ungated compiler/token evidence below describes PR #106; unknown aliases and the raw VM remain explicitly separate limitations/capabilities.

This increment is stacked directly on verified, open/unmerged [PR #105](https://github.com/Shibukedang27/Kuro/pull/105), exact parent `8db3f29260fcf3b3701ddc6731359ff41b6f8cec`, whose eight checks were successful when inspected. Keep this increment and its ancestors open and unmerged. **Strict toolchain independence remains unfinished.**

## The contract decides the direction

[ADR-0013, decision 4](ADR-0013-type-system-stage7.md) explicitly restricts source `Length` to Text. Its rationale matters: the semantic system records a collection's element type, not its shape. Consequently `Items = 11, 22` and scalar `Items = 11` both carry `Integers`; permitting every Integer target would admit scalar operations that have no length. The ADR explicitly declines collection-shape typing. Both [reference validation](../../compiler/typecheck.py) and the [authored semantic validator](../../self_host/typecheck.kuro) implement the Text-only E3009 rule.

Downstream capability does not supersede that decision. The reference interpreter and bytecode VM apply runtime `len`; the Python-authored native emitter already has collection-length metadata; the authored VM computes collection lengths. [PR #104](kuro-owned-fixed-collection-length.md) added a logical-length operation to the bounded integer-owner native generator, but explicitly left the reference conflict unresolved. No subsequent language decision established collection-shaped source Length.

The compatibility-preserving reconciliation therefore narrows the generator rather than modifying the language contract. A future collection-Length proposal needs explicit shape typing, scalar/collection distinctions, alias and reassignment rules, scope/control-flow handling, and a corresponding contract update in both semantic implementations. It must not be inferred from convenient backend metadata.

## Small production change

Only [self_host/native_codegen.kuro](../../self_host/native_codegen.kuro) changes in production: remove the fixed-integer-owner `BC_LENGTH` success branch added by PR #104. That opcode now follows the existing unsupported-operation rejection in this bounded path. Failure must publish no assembly, including no already-buffered print prefix.

Logical collection lengths remain intact for GET's positive and negative bounds checks. Initialization, cell replacement, scalar result publication, owner identity, 16-owner/272-cell storage limits, 16 scalar slots, the 4,096-token ceiling and Linux execution/output qualification remain unchanged. Aliasing, growth, Actions and control flow stay closed. The raw VM primitive, parser/lowerer, bytecode format, Python compiler, frozen bootstrap and external assembler/linker are not changed.

This deliberately withdraws the PR #104 executable integer-Length capability; it does not replace it with another representation or claim a language extension.

## Exact parity, not a hidden semantic gate

The regression file [test_native_integer_storage_length.py](../../tests/self_host/test_native_integer_storage_length.py) proves complete reference/authored semantic canonical parity for supported typed cases, including Integer collections, a typed alias, scalar controls, mutation, repeated Length, derived indices, growth, Actions and control flow. Known non-Text targets produce E3009; Text scalar and Text-element collections retain acceptance and expected hosted/authored VM output.

**The authored source compiler is still ungated.** Its hosted and native compositions include lexer, parser, lowerer, bytecode encoder and compiler driver, but omit resolver/typecheck. They therefore still publish matching `BC_LENGTH` tokens for semantically invalid Integer Length source. The new tests compare their complete tokens, then require the actual fresh native generator to reject them with exit 1, empty stdout and empty stderr. That is end-to-end native artifact admission, not authored-frontend E3009 diagnostic parity. Integrating semantic validation into the authored compiler is a separate next step.

**Unknown target types remain an inherited gap.** `Alias = Items` does not infer an element type from the VarRef assignment. Both semantic passes accept `Length Alias` when the alias type is unknown. A separate test records that unchanged acceptance; the generator independently rejects alias ownership. This increment does not claim that all source routes reject every non-Text runtime value.

The hosted authored semantic pass also has an inherited recursion limit for a 272-literal initializer. Full semantic differential cases use up to 32 literals; the 272-cell reference rejection and fresh native compiler/generator rejection are tested separately. No recursion or token limits are raised, no input is silently shortened within a claimed maximum-size semantic run.

Portable rejection tests include valid owner Length, explicit publication, direct use, preserved lower stack operands, malformed operands, unknown/scalar names, aliases, growth, Actions, branches, stack underflow and residue. All twelve output/execution qualification combinations reject integer-owner Length. Native tests assert no partial assembly. Raw authored VM collection Length remains tested as a low-level capability, not source-language permission. Fresh linked GET controls at two and 272 cells ensure the restriction did not remove storage or logical bounds metadata. The earlier newline diagnostic regression is retained and explicitly labeled as an ungated compiler/token/raw-VM control.

## Verification

| Gate | Final local evidence |
| --- | --- |
| New contract/native admission regression module | **62 passed in 10.32s** |
| Independent read-only review and separate fresh rerun | No blocking issue; **62 passed in 10.92s**, plus **15 diagnostic regressions passed in 3.97s** |
| Same 62 candidate regressions in detached exact-parent checkout | **13 failed, 49 passed in 10.84s**; the failures expose the integer-owner native admission now withdrawn |
| Focused semantic/compiler/runtime/IR/storage/authored-toolchain suite | **936 passed, 20 skipped in 504.41s** |
| Complete fresh suite | **2,207 passed, 20 skipped in 899.59s** |
| Separate fresh four-image bootstrap, old executables removed first | Passed |
| Python/toolchain-blocked production smoke, stage-1 probe and full compiler-bytecode reproduction | Passed |
| Additional fresh native compiler and Linux-output generator under an empty PATH | Integer-Length generation rejects with no assembly; GET emits; Text Length executes through the native bytecode launcher; malformed Print safely rejects |
| External linking and executable GET control | Exact `22\n` output, no undefined symbols |
| Candidate/bootstrap compiler/authored/bootstrap source identity | All **67** tracked files byte-identical |
| Python 3.10 grammar and `git diff --check` | Passed; actual Python 3.10 execution belongs to CI |
| Exact final documentation-updated head | Requires **8/8 successful CI checks**; immutable SHA and outcome recorded in the PR verification comment |

The counts overlap and must not be added. Full/focused runs and independent review cover the final production/test tree; only evidence documentation was finalized afterward. The independent review noted that no new test claims native-generator acceptance of Text Length; the preserved Text contract is checked through semantic and hosted/authored-VM routes. This is not a new native Text-backend parity claim.

Initial failed test assumptions are not acceptance evidence: the first tests incorrectly assumed VarRef alias inference and maximal hosted semantic recursion capacity; the corrected tests expose those limits explicitly. Fresh binaries and pytest artifacts are not committed. The exact-parent differential is `/workspace/Kuro-length-contract-parent`; the fresh bootstrap is `/workspace/Kuro-length-contract-bootstrap`; restricted-PATH inputs, bytecode, assembly and exact outputs are retained under `/workspace/kuro-length-contract-bootstrap-evidence`.

Reproduce with fresh, distinct artifact directories:

```sh
.venv/bin/python -m pytest -q tests/self_host/test_native_integer_storage_length.py \
  tests/self_host/test_native_compiler_diagnostics.py \
  --basetemp=/workspace/kuro-length-contract-regression-rerun
.venv/bin/python -m pytest -q tests/semantic tests/compiler tests/runtime tests/ir \
  tests/self_host/test_typecheck_cross.py \
  tests/self_host/test_native_compiler_diagnostics.py \
  tests/self_host/test_native_integer_storage.py \
  tests/self_host/test_native_integer_storage_capacity.py \
  tests/self_host/test_native_integer_storage_length.py \
  tests/self_host/test_native_codegen.py \
  tests/self_host/test_result_native_path_contract.py \
  tests/self_host/test_direct_native_result_owner.py \
  --basetemp=/workspace/kuro-length-contract-focused-rerun --durations=12
.venv/bin/python -m pytest -q \
  --basetemp=/workspace/kuro-length-contract-full-rerun --durations=20
# In a separate source-identical checkout, stop on any construction failure:
rm -f dist/kuro-compiler dist/kuro-runtime dist/kuro-bytecode dist/kuro-codegen
make native-hosted-bootstrap PYTHON=/absolute/path/to/python NATIVE_TARGET=x86_64-linux &&
sh tests/self_host/python_free_native_smoke.sh
```

## Next path and independence limits

First close the authored compiler's missing semantic gate through a separately bounded, executable integration slice. Preserve its full compiler-bytecode reproduction and malformed-input rejection while doing so; do not simply add a larger composed artifact and assume it executes. If collection Length is wanted afterward, make an explicit shape-aware language proposal and reconcile both validators before enabling generator admission.

Python still seeds production images, and Clang/LLVM still assemble and link generated output. Python/toolchain-blocked use and full compiler-bytecode reproduction show bootstrap continuity, not independent clean-checkout construction. Python-free seeding and an owned assembler/linker remain required. Full analyzer execution, ARM64 collection/result ownership and recoverable native error unwinding remain unfinished; no ceilings or qualification rules are relaxed here.
