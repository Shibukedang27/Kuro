# Fixed integer storage for a 16×16 snapshot

Follow-up: the [assignment-list stack-safety repair](stack-safe-initializer-lists.md) addresses the hosted parser/lowerer recursion blocker recorded below. This document preserves the original #94 checkpoint and its validation evidence; it does not describe that later fix as part of #94.

The Kuro-authored generator's fixed integer-storage budget grows from 32 to **272 cells**: sixteen mask lanes plus 256 flattened snapshot cells. This is a capacity increment for the existing straight-line Linux x86-64 backend, not execution of the full analyzer, dynamic collections, broader platform support or strict toolchain independence.

The increment stacks directly on verified, open/unmerged [PR #93](https://github.com/Shibukedang27/Kuro/pull/93), exact head `5f646ac78a67db94382d9dca214b6f23cafebc9f`, whose eight checks succeeded. No merge is authorized.

## Why this bound is useful and safe to isolate

The [earlier indexed-state contract](native-indexed-state-contract.md) describes sixteen mask lanes and a 16×16 snapshot, but initializes them with appends and uses control-flow guards. Those complete historical programs remain unsupported. New witnesses use **fixed literal initialization**, followed only by the already-admitted integer calculations, scalar assignment, GET, SET and printing. They do not bypass an unsupported opcode or claim to execute the earlier analyzer.

Both the per-initializer admission bound and aggregate admission bound become 272. The aggregate budget is shared by all owners; it is not 272 per owner. A single owner may occupy all 272 cells, or sixteen owners may share the budget. Each owner still needs at least two literal cells. Owner count remains sixteen, scalar slots remain sixteen including `_`, and the flat-token ceiling remains 4,096. All literal spelling, arithmetic-overflow, stack-balance, initialization-order and fail-closed grammar rules are unchanged.

The representation is unchanged: each owner has its own labelled `.quad` region and recorded logical length. GET normalizes negative indices once and checks the owner's length; SET rejects negative indices and checks the same length before scaled addressing. The maximum admitted element byte offset is now 2,168, from index 271 times eight. Addresses still use a checked register index scaled by eight, not a narrow immediate displacement. Capacity is never used as an owner's logical length. No allocation, growth, alias/copy, rebinding, Text/Decimal element, Action, branch or loop support is added. Both generator execution and output must still be explicitly qualified as Linux x86-64.

## Source compilation exposed a separate boundary

An initial larger-source regression did **not** reach the generator: the Kuro-authored parser running inside the Python-hosted interpreter raised `maximum recursion depth exceeded` on a long literal list. The interpreter deliberately caps Action call frames at 200 (`_MAX_CALL_DEPTH` in `compiler/interpreter.py`); recursive value-list parsing reaches that separate boundary, raising **E6005** at the call guard. The public `compile_with_kuro_driver` wrapper converts the runtime error to a `SelfHostError` message, which the portable regression asserts. Increasing Python's recursion limit does not change this guard; neither limit is changed here. That failure is not waived or described as source parity.

A freshly native-built Kuro compiler successfully compiles the same 272-cell initializer to framed bytecode. The new executable tests therefore use the **actual native Kuro compiler** for these larger source fixtures, then feed its complete output to a freshly native-built Kuro generator, assemble/link the emitted assembly with Clang, check that no undefined symbols remain, and run it. Reference execution and direct Kuro-authored VM checks are documented with the final results below. The tests do not change Python recursion settings or pretend the hosted-driver path supports these larger source lists.

The compiler and generator images are still seeded by the Python-authored compiler/native emitter, and Clang remains the assembler/linker. Running these images proves the specified source/compiler/generator/storage path, not a seed-free self-build.

## Reject before looking up an owner

The first revised capacity module recorded **13 passed, 1 failed**. Although native execution rejected 273 cells, the hosted raw-bytecode generator test exposed an inherited rejection-path bug: after refusing an oversized first initializer, the generator still tried to look up `NativeIndexedName` before that name had been read. The hosted interpreter reported an undefined value instead of clean generation failure. That result was not accepted.

Owner lookup now happens only while `NativeIndexedValid` remains true. This does not admit new malformed input or supply a default owner: it prevents metadata access after rejection. Portable tests require clean failure with empty assembly for oversized, truncated, empty and singleton initialization. Native rejection and duplicate-owner tests remain in the inherited suite. Parent inspection also corrected prototype test preconditions (explicit target metadata, required printing, two-cell rather than scalar owner declarations, complete trailing output and separate artifact directories); those unfinished test versions were not validation evidence.

## Verification and review

The new capacity tests cover first, last and interior runtime-computed snapshot positions, untouched cells and cross-owner isolation; single-owner and split-owner 272/273 admission; sixteen/seventeen owners; valid negative GET, the maximum-offset SET followed by GET, invalid GET/SET bounds at large lengths; and logical bounds for a small owner next to a large owner. Existing 32/33-cell cases now both require successful execution, retaining the old boundary as a compatibility regression.

For larger executable fixtures, expected output and bounds errors are compared with the Python-authored reference compiler/interpreter and the Kuro-authored VM **fed the fresh native compiler's tokens directly**. This intentionally does not run those larger sources through the hosted authored parser. The full 272-element initializer token prefix is checked explicitly, in addition to first/last/interior value and mutation witnesses. The seventeenth-owner rejection has a valid print suffix, so absence of required output cannot explain rejection.

Final Linux local results (fresh artifact directories; counts overlap, not add):

| Gate | Result |
| --- | --- |
| Final capacity/storage/compiler/generator/bounds/composer focused gate | **553 passed, 19 skipped in 178.61s** |
| Complete suite | **1,790 passed, 20 skipped in 894.15s** |
| Independent final capacity plus inherited storage run | **131 passed** |
| Earlier inherited focused gate, before the rejection-guard repair | **534 passed, 19 skipped in 174.60s**; not final-code evidence |
| Changed Python files parsed using Python 3.10 grammar; `git diff --check` | Passed |

Both final parent gates build fresh compiler/generator images rather than reuse prior executables. Independent production review approved the admission-bound change and preserved representation/ABI invariants. A separate final review found the code/tests correct, independently passed 131 tests, and withheld publication approval only until this evidence section and the precise E6005 guard/wrapper distinction were completed. Final documentation review is recorded in the PR verification record before publication.

```sh
.venv/bin/python -m pytest -q tests/self_host/test_native_integer_storage_capacity.py tests/self_host/test_native_integer_storage.py tests/self_host/test_native_source_composer.py tests/self_host/test_recursive_expression_operators.py tests/self_host/test_native_codegen.py tests/self_host/test_native_collection_bounds.py tests/self_host/test_collection_index_semantics.py tests/self_host/test_native_indexed_state_contract.py tests/compiler/test_native.py --basetemp=/workspace/kuro-capacity-focused-final --durations=15
.venv/bin/python -m pytest -q --basetemp=/workspace/kuro-capacity-full-final --durations=20
git diff --check
```

Each successful or bounds-trapping executable retains source, compiler/bytecode, generator, assembly and image evidence in its temporary test directory. Rejected generation retains its submitted artifact separately; it is not reported as execution. These local files are test evidence, not committed binaries or a reproducible-bootstrap claim.

Final acceptance requires all eight GitHub checks to succeed on the exact final documentation-updated head, with the PR open and unmerged. Earlier-head green checks do not qualify; the PR's immutable head and check-run records are authoritative.

## Limits and next path

At the original #94 checkpoint, the hosted interpreter's authored-parser call-depth boundary remained a separate follow-up candidate. The [assignment-list repair](stack-safe-initializer-lists.md) now addresses that parser/lowerer blocker with reproduced boundary failures and hosted/native list witnesses, without raising the guard. Before adding branches/loops to storage, prove owner initialization, scalar kinds and operand-stack agreement on every path. Growth needs reviewed logical-length/capacity state and reset rules; aliases and parameters need identity/ABI proofs. Text-name storage and the full analyzer's artifact/global-slot limits remain unresolved.

**Strict independence remains unfinished.**
