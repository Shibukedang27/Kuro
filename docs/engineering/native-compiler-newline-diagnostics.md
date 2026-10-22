# Safe native compiler errors after a newline

This repair is stacked directly on verified, open/unmerged [PR #104](https://github.com/Shibukedang27/Kuro/pull/104), exact parent `271e6557da45d28b969e53798fd6c15a6e4b04d0`, with eight successful checks. Keep this increment and its ancestors open and unmerged. **Strict toolchain independence remains unfinished.**

## What went wrong

The [fixed-owner Length report](kuro-owned-fixed-collection-length.md) recorded a native-compiler crash while testing an invalid `Print` statement. The crash is real, but neither Length nor collection storage causes it. The minimal witness is a newline followed by `Print 1;`. Print requires a period, not a semicolon. The compiler should reject that source, not dereference an integer as a string pointer.

On the exact parent, a freshly built native compiler terminates with signal 11 for the newline witness. Without the preceding newline, `Print 1;` already exits 1 and prints exactly `kuro.compile-error/1\n`. A debugger trace of the inherited production image locates the crash in `_kuro_strlen` with address `1`. Its generated `ComputeLineCol` newline branch calls string-length and concatenation machinery for `ComputeLineCol_Line + 1` even though both operands are integer counts.

The x86 native emitter's Action `LOADVAR` path treats a name ending in `line` as a strong Text hint unless it has an explicit numeric-use constraint. That hint overrides the initialized numeric kind here. This is a diagnostic-location computation defect, not evidence that Print with a semicolon is valid or that collection Length needs a different lowering.

## The bounded repair

Only [self_host/parser.kuro](../../self_host/parser.kuro) changes in production. The newline branch now uses the existing explicit integer operation `Add 1 to ComputeLineCol_Line;` instead of overloaded `+`. It expresses the intended increment and supplies the native emitter's existing hard numeric constraint. The column reset, character scan, diagnostic records, parsing rules and publication gate are unchanged.

Malformed inputs covered by the regression suite now produce exactly the compile-error frame, exit 1, and empty stderr from the native compiler. They do not publish a bytecode header, retain partial bytecode, or die from a signal. A separate instrumented native compiler checks the numeric diagnostic line and column; portable tests check complete diagnostic code/location lists and nonempty messages. The instrumentation is test-only and does not change production output.

The compiler running as bytecode through the authored VM also publishes only the compile-error frame. Its existing launcher exit convention is **0** for that compiler-published error frame, unlike the direct native compiler's exit 1. This repair does not silently change that convention.

## What stays unchanged

Print still requires a period. No previously invalid syntax is admitted. The valid multiline, repeated integer-collection Length witness must produce complete identical native/hosted authored-compiler tokens and authored-VM output `2`, `4`, `2`. The generator's collection admission restrictions remain those of the parent.

There is no change to Python validation, the Python native emitter, bytecode encoding, frozen bootstrap source, runtime, generator, result ownership or platform admission. The native regression images are freshly built and executed on Linux x86-64; other platforms retain portable parser coverage and existing CI, not a new native-execution parity claim. This is an authored-compiler workaround for one demonstrated inference hazard, not a general correction of all name-based native type inference.

## Verification

The [new regression file](../../tests/self_host/test_native_compiler_diagnostics.py) covers four newline-prefixed malformed Print forms, the existing line-one rejection control, portable complete diagnostic code/location lists, first native diagnostic locations, bytecode-hosted compiler rejection, and complete valid repeated-Length token/output parity. Native diagnostic instrumentation checks the first location, not full native diagnostic-list parity.

| Gate | Final local evidence |
| --- | --- |
| Independent read-only final review and separate fresh regression rerun | No blocking defect; **15 passed in 3.74s** |
| Same final regressions in detached exact-parent checkout, rebuilding its compiler and probe | **8 failed, 7 passed in 3.86s**; all eight failures are signal 11, not syntax-assumption failures |
| Focused compiler/runtime/IR/parser/authored-toolchain gate | **779 passed, 20 skipped in 468.67s** |
| Complete fresh suite | **2,190 passed, 20 skipped in 960.13s** |
| Initial existing parser/diagnostic/driver gate | **102 passed in 5.53s** |
| Separate fresh four-image bootstrap, blocked-toolchain smoke and full compiler-bytecode reproduction | Passed |
| Additional native parent/candidate source matrix, including the original malformed repeated-Length witness | **10** inherited SIGSEGV cases now reject safely; **5** valid controls retain complete identical bytecode |
| Independent native location probes, each executed twice | **7** sources preserve expected line/column after repeated newlines, indentation, a valid prefix and EOF |
| Candidate/bootstrap compiler/authored/bootstrap source identity | All **67** tracked files byte-identical |
| Python 3.10 grammar and `git diff --check` | Passed; actual Python 3.10 execution belongs to CI |
| Exact final documentation-updated head | Required **8/8 successful CI checks**; immutable SHA and final outcome recorded in the PR verification comment |

The seven parent controls include the four portable diagnostic cases, unchanged line-one rejection, bytecode-hosted rejection and valid collection-Length parity. The counts overlap and must not be added. Focused/full suites and independent review cover the final production/test tree; only evidence documentation was finalized afterward. Fresh test artifacts and binaries are not committed. The parent differential is at `/workspace/Kuro-print-parent`; matrix inputs, binary hashes and exact outputs are in `/workspace/kuro-print-crosscheck/results.json`.

The fresh bootstrap checkout is `/workspace/Kuro-print-bootstrap`; all four old production executables were deleted before rebuilding. Python/toolchain-blocked smoke tests, native-versus-bytecode compiler probe parity, full compiler-bytecode reproduction, and an additional restricted-PATH malformed/valid source probe passed. All 67 tracked compiler/authored/bootstrap files were byte-identical to the candidate. Additional exact input/output evidence is retained outside the repository under `/workspace/kuro-print-bootstrap-evidence`.

Reproduce with fresh, distinct artifact directories:

```sh
.venv/bin/python -m pytest -q tests/self_host/test_native_compiler_diagnostics.py \
  --basetemp=/workspace/kuro-print-regression-rerun
.venv/bin/python -m pytest -q tests/compiler tests/runtime tests/ir \
  tests/self_host/test_native_compiler_diagnostics.py \
  tests/self_host/test_parser_cross.py tests/self_host/test_parser_diagnostics.py \
  tests/self_host/test_compiler_driver.py tests/self_host/test_initializer_list_stack.py \
  tests/self_host/test_recursive_expression_operators.py \
  tests/self_host/test_native_integer_storage_length.py \
  tests/self_host/test_native_codegen.py \
  --basetemp=/workspace/kuro-print-focused-rerun --durations=12
.venv/bin/python -m pytest -q \
  --basetemp=/workspace/kuro-print-full-rerun --durations=20
# In a separate source-identical checkout, stop on any build failure:
rm -f dist/kuro-compiler dist/kuro-runtime dist/kuro-bytecode dist/kuro-codegen
make native-hosted-bootstrap PYTHON=/absolute/path/to/python NATIVE_TARGET=x86_64-linux &&
sh tests/self_host/python_free_native_smoke.sh
```

## Limits and next path

This does not establish fail-closed handling of every malformed source program. Existing hosted compiler composition can continue lowering after a parser failure and encounter undefined intermediate output for some malformed inputs; stage gating deserves its own minimized, cross-path robustness slice. The portable diagnostic helper also has an inherited empty/whitespace-only input limitation (`TokenKinds` undefined), while native compilation of that input publishes an empty bytecode artifact successfully. The existing native name-inference heuristic remains a separate backend issue. None is silently broadened into this repair.

Next, reconcile the Python reference frontend's Text-only Length validation with the already-authored collection-Length operation as an explicit language-contract slice. Before adding collection branches or loops, separately prove owner initialization, identity and logical length on every admitted path. Do not raise token ceilings or weaken analyzer input to imply full analyzer execution.

Python still seeds native production images; Clang/LLVM still assemble and link them. Python-free use and compiler-bytecode reproduction demonstrate continuity, not clean-checkout independent image construction. Python-free seeding and an owned assembler/linker remain required for the strict goal.
