# Stack-safe fixed initializer compilation

A fixed 272-integer initializer can now pass through both the hosted Kuro-authored compiler and a freshly native-built Kuro compiler. The repair removes one retained Action frame per initializer value from **two assignment-only tails**; it does not raise a global recursion ceiling or change native storage admission.

This increment stacks directly on verified, open/unmerged [PR #94](https://github.com/Shibukedang27/Kuro/pull/94), exact head `9941db0c574f844d46a182876b9481308eb09a6a`, whose eight check runs succeeded. No merge is authorized.

## What failed, and why two loops are necessary

On that parent, `Items = 0, 1, ...;` followed by a print succeeds with 190 values and fails with 191. The executable boundary regressions were run before editing production code: **2 passed, 4 failed**, covering typed and untyped assignments at 190, 191 and 272. The failures are the hosted interpreter's controlled E6005 (`maximum recursion depth exceeded`), surfaced by `compile_with_kuro_driver` as `SelfHostError`. This is a program-shape-specific boundary, not a universal maximum list length: surrounding statement/block frames also matter.

`ParseValueListTail` recursively consumed each comma and expression, retaining one frame per remaining value. It now loops while parsing has not failed, returns when the current token is not a comma, and consumes one expression per comma. `ParseExpr` can recursively parse parentheses, unary operators and arithmetic, but cannot reach a statement or another assignment value list. No scratch value is needed after calling it. This non-reentrancy is why iteration is safe here; it does **not** justify replacing reentrant block/expression loops throughout the parser.

The parser-only experiment reached canonical AST parity at 272 but still failed end-to-end compilation. Independent call-graph inspection and the focused run exposed a second tail: `LowerAssignTail` retained one frame per assignment value. It now loops over the same expression sequence, advances past `END_VALUES` exactly once, and stops when `LowerFailed` is set. `LowerValue` walks expression tokens, not assignments, so it cannot overwrite an active `LowerAssign` through re-entry. Bytecode encoding already iterates over instructions; it needed no repair. Neither partial experiment is final acceptance evidence.

The parser loop stops immediately when `ParseFailed` is already set, rather than consuming one additional comma after an earlier failure. Recovery remains minimal and fail-closed: malformed inputs need not retain the old incidental cascade or partial AST. No new syntax or diagnostic category is added.

## What the regressions prove

`test_initializer_list_stack.py` checks canonical AST parity against the reference parser and explicitly constructed complete bytecode at 190, 191 and 272 values, for typed and untyped assignments. It also checks nested arithmetic, mixed literal kinds, successive lists, scalar assignment and assignments inside nested blocks/Actions. Those grammar checks are not claims that the restricted collection generator admits Text, Actions or branches.

Malformed 272-value lists cover trailing and doubled commas, EOF after a comma, a bad operand, a malformed parenthesized expression and a missing semicolon. Hosted parsing must terminate with structured E2003/E2002 diagnostics, and the hosted compiler must reject the source. Fresh native compilation must return exit status 1 with only `kuro.compile-error/1`, never a bytecode artifact. A deeply nested expression still fails with the hosted recursion error, and `_MAX_CALL_DEPTH` remains 200.

The existing capacity module now requires **complete hosted/native token equality for every accepted source-compilation witness**, retaining both streams and a fresh compiler image hash in its artifact records. The 190/191/272 boundaries execute through the actual freshly built Kuro generator and linked Linux x86-64 output. The inherited large-owner witnesses compare reference execution and the Kuro-authored VM, preserve owner-local bounds, and exercise single-owner and aggregate 272-cell acceptance versus 273-cell generation rejection, sixteen/seventeen owners, negative GET and invalid SET, and adjacent owner isolation. Compilation of 273 values is not storage admission: generation must still fail with empty assembly.

## Verification and independent review

Final Linux local results (counts overlap, not add):

| Gate | Result |
| --- | --- |
| Fresh-artifact focused parser/lowering/bytecode/storage/compiler/generator gate | **706 passed, 19 skipped in 192.35s** |
| Complete suite | **1,815 passed, 20 skipped in 912.79s** |
| Independent initializer/capacity run, fresh compiler/generator images | **44 passed in 17.98s** |
| Independent adjacent parser/diagnostics/lowerer/compiler-driver run | **127 passed in 6.64s** |
| Changed Python files parsed using Python 3.10 grammar; `git diff --check` | Passed |

Independent production review approved both non-reentrant loop transformations with no actionable findings. It checked call graphs, global scratch lifetime, failure flags, preserved generator/host boundaries and regression coverage; no files were edited by the reviewer. The independent runs used separate trees under `/workspace/kuro-list-stack-review`. The earlier parser-only run and its unfinished 40-parenthesis guard fixture were not accepted as final evidence; the final guard regression uses 60 nested parentheses and passes without changing any recursion limit.

Acceptance requires all eight GitHub check runs on the exact final documentation-updated head; earlier-head checks do not qualify. The PR's final immutable head and check-run records, summarized in its verification record, are authoritative. The PR must remain open and unmerged.

```sh
.venv/bin/python -m pytest -q tests/self_host/test_initializer_list_stack.py tests/self_host/test_parser_cross.py tests/self_host/test_parser_diagnostics.py tests/self_host/test_lower_cross.py tests/self_host/test_bytecode_cross.py tests/self_host/test_native_integer_storage_capacity.py tests/self_host/test_native_integer_storage.py tests/self_host/test_native_source_composer.py tests/self_host/test_recursive_expression_operators.py tests/self_host/test_native_codegen.py tests/self_host/test_native_collection_bounds.py tests/self_host/test_collection_index_semantics.py tests/self_host/test_native_indexed_state_contract.py tests/compiler/test_native.py --basetemp=/workspace/kuro-list-stack-focused-final --durations=15
.venv/bin/python -m pytest -q --basetemp=/workspace/kuro-list-stack-full-final --durations=20
git diff --check
```

Each suite uses fresh artifact directories, rather than earlier compiler/generator images. Successful/trapping generated programs retain compiler records, bytecode, generator output, assembly and executable evidence; rejected native compilation retains its source and failure publication. These development artifacts are not committed binaries or evidence of a reproducible seed-free bootstrap.

## Limits and next path

The generator remains straight-line, fixed integer storage on explicitly qualified **Linux x86-64 execution and output**: 272 aggregate cells, sixteen owners, sixteen scalar slots including `_`, and the existing 4,096-token ceiling. Owner lengths, minimum initializer size, literal validation, overflow traps, stack balance and all host guards remain unchanged. No growth, aliases, rebinding, collection control flow or other element support is introduced. Longer syntactically valid lists may compile, but native generation must still enforce its independent budget.

Expression depth, operator tails, argument/parameter lists, block recursion and other lowerer walks retain their existing behavior and limits. This is not a general stack-safety or parser-reentrancy rewrite. The next storage/control-flow step still needs proofs for owner initialization, scalar kinds and operand-stack agreement on every admitted path; growth and aliases need reviewed length/capacity and identity/ABI state. The full analyzer and its artifact/global-slot constraints remain unresolved.

Fresh native images still depend on the Python-authored bootstrap seed, and generated assembly still uses Clang to assemble/link. **Strict independence remains unfinished.**
