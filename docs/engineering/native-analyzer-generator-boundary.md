# The loop analyzer reaches a real generator boundary

The unchanged indexed loop analyzer compiles through the **Kuro-authored compiler stages**, but the Kuro-authored native generator cannot yet turn it into an executable. The compiler emits **16,392 bytecode tokens**, over the generator's **4,096-token program ceiling**. Size is a disqualifying limit, not the only diagnosed incompatibility or an instrumented explanation of which rejection branch fires first: the analyzer also requires unsupported collection lowering. The generator rejects with exit 1, empty stdout and empty stderr; no analyzer assembly or executable is produced. This is a verified boundary, not successful analyzer execution or strict self-hosting.

This test-only increment stacks directly on [PR #87](https://github.com/Shibukedang27/Kuro/pull/87), inspected open and unmerged at `18d942b4b54fe3d35b8bfc4dd349bf4683b846bb` with all eight checks successful. Production compiler/runtime/generator sources, capacity limits, expression semantics and acceptance rules remain unchanged. CI explicitly adds the boundary regression to its existing Linux native-generator gate.

## What actually runs

The [regression](../../tests/self_host/test_native_codegen.py) is `test_kuro_owned_generator_records_analyzer_execution_boundary`. It uses `compile_with_kuro_driver`, which composes `lexer.kuro`, `parser.kuro`, `lower.kuro`, `bytecode.kuro` and `compiler.kuro`. Those Kuro stages execute in the hosted Python interpreter. Python frames their complete `CompilerOutput`; it does not translate the analyzer directly to native code or remove unused Actions.

The native generator fixture builds a fresh image from `artifact_loader.kuro` plus `native_codegen.kuro`, with the output target set to `x86_64-linux`. Image construction still uses the hosted `compile_source` / `build_native` bootstrap. The test executes that native generator process with the full framed artifact on stdin. It does not substitute interpreted `run_codegen` for this invocation.

A separate small control, `Value = 1.5; Print Value.`, passes through the same Kuro compiler and generator image. The exact captured control assembly is linked with `clang -nostdlib`, and that resulting executable runs with exact stdout `1.5\n`, exit zero and empty stderr. `nm -u` must report no undefined symbols. This proves that the image is live and its emitted assembly can execute, **not** that any part of the raw-token analyzer executed.

Each run retains, in pytest's temporary directory, the composed generator source, each submitted source and framed bytecode artifact, captured assembly, the control executable and `generator-boundary-provenance.json`. The manifest records compiler-stage hashes, composed generator-source and image hashes, source/artifact/assembly hashes, token counts, generator exits, and the identity/hash of the control image actually executed. Every full-analyzer case explicitly records `embedded_analyzer_program_executed: false`; the generator's own validation does run. These are temporary local diagnostics, not checked-in binaries, uploaded CI artifacts or a reproducible-binary claim.

## Fail-closed cases and separate limits

The complete unchanged analyzer, a safe raw-input specialization, a truncated raw program, a zero-trip body discovering 17 distinct names, and a 129-raw-token input all compile to programs above 4,096 tokens and are rejected by the actual native generator without assembly output. These results do **not** prove native analyzer handling of malformed input or its 16-name/128-token bounds: those validations are never reached. Existing hosted/interpreted/hosted-native analyzer tests remain the evidence for those behaviors.

The 129-token constructor uses a bounded source `Repeat` to append raw tokens, rather than 129 consecutive source statements. An initial fixture with 129 consecutive appends hit the hosted Kuro compiler/parser's recursion limit before submission to the generator. Only the fixture constructor changed; the analyzer and its input grammar did not.

Below-ceiling probes separately check typed collection declaration, append, get and set forms, and truncated generator bytecode. These also reject without assembly. Each source probe asserts its expected opcode is present in the compiler output. The append/get/set probes start from an ordinary Text value, not a typed declaration, so a declaration rejection cannot mask their opcode boundary. These probes establish rejection of these concrete forms only, not an exhaustive explanation of all remaining analyzer incompatibilities. Scanner recognition of an opcode is not implementation of its lowering. The existing actual-generator 4,096/4,097-token boundary regression remains the isolated capacity evidence. The production generator now has a separate bounded 266-slot scalar BSS arena; function/parameter and analyzer-collection constraints remain separate integration limits.

## The next useful proof

Do not raise the token ceiling or silently delete depth-specialized parser Actions just to make this test pass. First establish separately reviewed native lowering and freestanding storage/typing/bounds behavior for the analyzer's Text token/name collections and indexed numeric state/snapshot operations, using small executable witnesses and malformed/boundary probes under the existing limit. Preserve independent entry/backedge evidence and literal-only writes.

Then design and prove a generator-compatible analyzer decomposition or control-flow representation that addresses its whole-program size, shared Action scratch and global-slot requirements. Re-run the **complete** raw-token analyzer through the real generator with safe, unsafe, malformed and exact/over-capacity inputs, comparing complete evidence stdout. Success requires an analyzer executable, not only compiler output or an executable control. Neither that future result nor this boundary test alone removes the hosted compiler/generator bootstrap, external assembler/linker or toolchain trust. Strict independence remains incomplete.

## Validation

The final focused analyzer/fresh-generator gate passed **432 tests in 307.40 seconds**. It includes the new real-generator boundary regression, the inherited production Decimal/branch/loop gates, logical depth/global-slot bounds, interpreted and actual-generator exact 4,096/4,097-token boundaries, and ARM64 generator-source emission. The complete local suite passed **1,487 tests / 20 skipped in 772.81 seconds**. Counts overlap. Python 3.10 syntax parsing and `git diff --check` passed. Native execution here is Linux x86-64, not Darwin execution; the new test is platform-gated and explicitly selected in Linux CI.

The final provenance records these complete compiler outputs:

| Submitted source | Bytecode tokens | Actual generator result |
| --- | ---: | --- |
| Small Decimal control | 7 | Emits 31,451 assembly bytes; linked image executes `1.5\n` |
| Unchanged analyzer | 16,392 | Rejects; no assembly |
| Safe raw-input specialization | 16,436 | Rejects; embedded analyzer not executed |
| Truncated raw-input specialization | 16,396 | Rejects; embedded analyzer not executed |
| 17-name zero-trip specialization | 16,680 | Rejects; embedded analyzer not executed |
| 129-raw-token specialization | 16,400 | Rejects; embedded analyzer not executed |
| Declaration / append / get / set probes | 3 / 8 / 14 / 10 | Each rejects below the token ceiling |
| Truncated generator bytecode | 1 | Rejects; no assembly |

Two independent reviews found no blocker for this bounded negative regression and executable control. Both independently ran the real-generator regression successfully. Their refinements were incorporated: assert each expected collection opcode, identify the exact captured control assembly/image, distinguish embedded-analyzer execution from the generator's own analysis, and avoid assigning a unique cause to a rejection shared by several incompatible features. No production source or analyzer semantics changed. The initial fixture-construction failure described above was not a native analyzer result.

Publication requires all eight checks on the exact final documentation-updated head; the PR metadata records that immutable SHA and outcome. Earlier-head CI is insufficient. This PR and its predecessors remain open and unmerged.

## Reproduce

```sh
.venv/bin/python -m pytest -q \
  tests/self_host/test_native_codegen.py::test_kuro_owned_generator_records_analyzer_execution_boundary \
  --basetemp=/tmp/kuro-generator-boundary --durations=5
.venv/bin/python -m pytest -q --durations=20
git diff --check
```
