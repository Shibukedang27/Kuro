# Preserve operators across nested expression parsing

The Kuro-authored compiler must preserve an outer arithmetic operator while recursively parsing its right operand. Previously, `Value = 0 - (2 + 1)` compiled to postfix `0 2 1 + +`, returning `3` instead of `-3`. This increment corrects that compiler defect without changing the bounded storage backend or expanding its platform support.

The review increment stacks directly on verified, open/unmerged [PR #92](https://github.com/Shibukedang27/Kuro/pull/92), exact head `fe3f92862db0f665863a28f61ffcd180135e9828`, whose eight checks succeeded. No merge is authorized.

## Why it happened

The defect originates in [parser.kuro](../../self_host/parser.kuro), before the later AST-to-IR lowering pass. `ParseTermTail` saves `+` or `-` in global scratch, then parses the right factor before emitting that operator. Parentheses can re-enter the same tail, overwriting the outer operator. `ParseFactorTail` has the same defect for `*` and `/`. Different Action-name prefixes prevent collisions between Actions, not between recursive invocations of one Action. Existing same-operator nesting tests could not distinguish the overwritten value.

## Small fix, no new storage mechanism

Two operand helpers capture the chosen operator in a typed Text Action parameter before parsing the right operand. Parameters already have call-frame isolation; ordinary assigned scratch variables do not. Each helper emits its saved parameter after the recursive operand finishes. Token consumption, operator precedence, left associativity, expression terminators, and the existing parse-failure circuit breaker are retained. There is no global save/restore table, new nesting limit, parser rewrite, Python compiler workaround, or generated-assembly patch.

The later lowering pass already forwards postfix operators without retaining them across nested operand traversal, so it needs no production change.

## Regression evidence

The regression suite checks canonical AST parity, exact postfix IR and bytecode, and hosted/Kuro-VM values for nested subtraction and mixed operators. Freshly built native compiler coverage exercises the parameter mechanism in compiled execution rather than only through the hosted interpreter. The earlier executable discrepancy witness is changed to demand the corrected `+,-` bytecode and `-3` result; a test asserting the wrong answer is not retained as an acceptance gate.

Actual-generator storage regressions include a nested negative GET, nested SET index and value, deeper mixed integer nesting, and rejection of a nested negative write that previously became positive index `1`. They compile source through the Kuro-authored compiler stages, build a fresh actual Kuro generator, assemble/link its output, and execute it. The inherited endpoint, overflow, owner/cell limits, logical-bounds, malformed-input and host-boundary tests remain in place.

Against a temporary copy of the verified base parser, without replacing shared production source, the regression author independently reproduced wrong outer operators in AST/IR/bytecode for `10 + (3 - 1)`, `20 * (12 / 3)` and `20 / (3 * 2)`. The corrected parser passes all nine discriminating cases, plus the fresh native compiler framing test.

Independent review **approved** the exact production fix and both test files. The reviewer inspected parameter-frame semantics in the hosted interpreter, bytecode VM and native emitter, preserved parse-failure control flow, and confirmed the storage/backend platform guard was unchanged. Independent runs passed **194 tests** for storage/parser, **10** for recursive expressions, **39** for parser diagnostics/VM, and **19** in a native recursion/parameter/Text selection. These counts overlap the final gates; they are not additional full-suite coverage.

Final Linux local results, with fresh temporary artifact directories:

| Gate | Result |
| --- | --- |
| Broad focused parser/compiler/VM/native-generator/storage gate | **685 passed, 19 skipped in 183.91s** |
| Complete suite | **1,771 passed, 20 skipped in 864.21s** |
| Earlier fresh storage/composer gate | **136 passed in 18.03s** |
| Initial parser/diagnostic/lowering/compiler gate | **127 passed in 7.05s** |
| Changed Python test syntax with Python 3.10 grammar; `git diff --check` | Passed |

The focused gate includes all of `test_recursive_expression_operators.py`, `test_parser_cross.py`, `test_parser_diagnostics.py`, `test_lower_cross.py`, `test_compiler_driver.py`, `test_vm_cross.py`, `test_native_integer_storage.py`, `test_native_codegen.py`, `test_native_collection_bounds.py`, `test_collection_index_semantics.py`, `test_native_indexed_state_contract.py`, `test_native_source_composer.py`, and `tests/compiler/test_native.py`. The full and focused runs both build fresh native compiler/generator artifacts; neither relies on an old executable. Counts overlap, not add.

```sh
.venv/bin/python -m pytest -q tests/self_host/test_recursive_expression_operators.py tests/self_host/test_parser_cross.py tests/self_host/test_parser_diagnostics.py tests/self_host/test_lower_cross.py tests/self_host/test_compiler_driver.py tests/self_host/test_vm_cross.py tests/self_host/test_native_integer_storage.py tests/self_host/test_native_codegen.py tests/self_host/test_native_collection_bounds.py tests/self_host/test_collection_index_semantics.py tests/self_host/test_native_indexed_state_contract.py tests/self_host/test_native_source_composer.py tests/compiler/test_native.py --basetemp=/workspace/kuro-operator-focused-final --durations=15
.venv/bin/python -m pytest -q --basetemp=/workspace/kuro-operator-full-final --durations=20
git diff --check
```

Final acceptance additionally requires all eight GitHub checks on the exact documentation-updated head. The PR record is authoritative for that immutable head and its check URLs; earlier green implementation heads do not qualify. Keep the PR open and unmerged.

## Limits and next safe step

This repairs two arithmetic operator lifetimes, not all parser reentrancy or all source-language parity. It does not establish arbitrary nesting capacity, change malformed-input recovery, or add new arithmetic operations to the bounded generator. Division regression coverage belongs to the existing compiler/VM path; integer collection generation still rejects division.

The collection path remains restricted to **Linux x86-64 generator execution and Linux x86-64 output**, sixteen owners, 32 total cells, sixteen scalar slots, and straight-line checked signed-integer operations. Other execution/output ABIs reject collection artifacts cleanly. No platform metadata, native backend, composer, representation, allocation, bounds, or arithmetic-overflow guard changes in this increment.

Next, audit remaining scratch values that survive recursive calls using similarly distinguishing witnesses. Before extending bounded collection support to loops or branches, prove owner initialization and scalar/operand-stack agreement on every path; growth or aliases need explicit length/capacity and identity rules. Full-analyzer execution remains blocked by other artifact/storage boundaries. Python-hosted bootstrap seeding and an external assembler/linker are still required. **Strict independence remains unfinished.**
