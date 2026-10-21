# Collection indexes: preserve compatibility before lowering storage

## The existing rule is clear

The negative-index disagreement is an implementation defect, not an invitation to design new language semantics. [README](../../README.md) names the frozen `bootstrap/python/` interpreter as the compatibility oracle. [ADR-0012's Golden Rule](ADR-0012-scope-semantics.md#the-golden-rule-applied) requires reproducing Python compiler semantics unless an explicit language change goes through the documented change process. No indexing change superseding that rule was found.

The [frozen interpreter's GET and SET](../../bootstrap/python/kuro.py) establish a deliberately asymmetric compatibility contract for a collection of logical length `L`:

- GET accepts `-L <= index < L`. A negative index reads position `L + index`; `-L` reads the first element and `-1` the last. Empty collections have no valid index.
- SET accepts only `0 <= index < L`. A negative write is invalid, even where the analogous read succeeds.
- Neither operation may access unused backing capacity. SET does not append or grow the collection. [ADR-0005](ADR-0005-append-statement.md) explicitly rejects that interpretation of an out-of-range SET.

The hosted IR interpreter and serialized Python bytecode VM already implement these rules. Their `E6001` errors and the Kuro VM's failure flag are different interfaces to failed accesses, not identical diagnostic implementations. The frozen interpreter's extra GET printing/debug trailer was deliberately removed by ADR-0007; preserving index behavior does not restore that output.

## This increment repairs one runtime discrepancy

This work starts directly from verified, open/unmerged [PR #89](https://github.com/Shibukedang27/Kuro/pull/89), exact head `66de09e1028f136953966cb76d1e96133c22fc41`, with all eight checks successful. It must remain a separate stacked review PR, open and unmerged.

The only production change is in [VMGetCollectionItem](../../self_host/vm.kuro). For a negative GET it obtains the current collection's logical length using the existing owner-specific `VMLengthCollection`, normalizes the requested position, then uses the existing item/display lookup. Positions below `-L` remain negative and never match a stored element; one-past-end and positive overflow continue to fail. Nonnegative GET and all SET behavior remain unchanged. No host interpreter, native backend, generator, element-kind rule, capacity or analyzer acceptance is changed.

The additional scan happens only for negative reads. It is a correctness correction, not a performance claim. Using owner-specific logical length matters because the VM retains historical entries after reassignment and interleaves entries from different collection identities. Counting the backing arrays or all historical entries would be wrong.

## Evidence and honest boundaries

[The numeric index matrix](../../tests/self_host/test_collection_index_semantics.py) checks first/last positions, negative boundaries, one-past length and native capacity boundaries across the hosted IR interpreter, JSON-round-tripped Python bytecode VM, and Kuro compiler/VM stages hosted in the interpreter. Linux x86-64 also executes the Python-authored native backend's existing collection behavior and a native-built Kuro runtime. Frozen-oracle checks tie the compatibility decision to executable evidence rather than only prose. Append, reassignment and interleaved-owner witnesses exercise logical length rather than a fixed literal or backing-storage size.

The frozen lexer predates unary-minus source syntax. Its negative-index witnesses therefore parse an ordinary positive-index AST, replace only the access node's index with the negative integer literal, and execute the unmodified frozen Engine. They compare resulting environments and exceptions, not bootstrap debug printing. This is runtime-oracle evidence, not a claim that the frozen frontend accepts the modern negative-literal source spelling. The current hosted/bytecode/Kuro VM paths receive the real negative-index source.

The previous [indexed-state regression](../../tests/self_host/test_native_indexed_state_contract.py) now requires VM negative-GET parity instead of preserving its known defect. Its guarded integer storage witnesses, Text-name reference witness and fresh actual-generator boundary remain unchanged: the scalar arithmetic control generates, links and executes; complete collection artifacts still reject. This increment adds no Text collections to the Kuro generator and does not execute the full analyzer there.

**The Python-authored native backend is still nonconforming for unguarded collection indexes.** Linux GET/SET compare against backing capacity instead of logical length and reject valid negative GET. The matrix labels those observations separately; they are not a native parity oracle or evidence of sound bounds. Source inspection finds capacity checks in the ARM64 path too, but Linux execution is not Darwin execution. Native Action/captured-collection paths need their own metadata audit: the Linux backend explicitly lacks captured-collection LENGTH/APPEND metadata. A main-program-only patch would not establish general native safety, and inventing capture length/identity storage in this small VM repair would broaden the change. Those native corrections are deferred explicitly, not silently treated as solved.

## Validation

Final local evidence (overlapping counts):

- New numeric compatibility module: **33 passed**; the independent final reviewer reproduced **33 passed in 8.27s**.
- New module plus inherited indexed-state/fresh-generator boundary: **53 passed in 14.77s**.
- Focused native/analyzer/VM/conformance gate: **787 passed, 18 skipped in 387.59s**. This includes fresh generator construction, actual scalar generation/link/execution, and continued rejection of complete collection artifacts; it does not include the new non-`test_native*` module, which the preceding gate covers explicitly.
- Complete suite on finalized code/tests: **1,540 passed, 20 skipped in 808.90s**.
- Python 3.10 syntax parsing for both changed/new Python test modules and `git diff --check`: passed.

Independent authority audit identified the existing compatibility rule. Independent production review found normalization, scratch-variable separation, owner-specific counting and item/display propagation sound. Final independent test review found no remaining blocker and executed the exact Linux native VM witness **20/20 times**, each with exit 0, exact output `11\n33\n11\n44\n7\n11\n` and empty stderr. Empty logical length was reviewed from the source, not tested via an empty literal (the frontend does not expose that spelling here). An additional reviewer smoke check preserved existing Decimal display strings, but this change adds no new Decimal or Text storage support.

The initial review caught concurrently edited oracle fixtures comparing different source indexes and incorrect frozen-parser punctuation; those fixtures were corrected before final runs. It also reported a multi-operation native prototype crash on both current and base builds. The exact earlier reproducer was not retained, so the final reviewer could not independently classify it; the finalized witness above is stable. No general native-runtime crash repair or broader safety result is claimed.

```sh
.venv/bin/python -m pytest -q tests/self_host/test_collection_index_semantics.py tests/self_host/test_native_indexed_state_contract.py --durations=10
.venv/bin/python -m pytest -q tests/self_host/test_native*.py tests/self_host/test_vm_cross.py tests/regression/test_execution_conformance.py --durations=20
.venv/bin/python -m pytest -q --durations=20
git diff --check
```

Linux CI explicitly includes the new module in its native codegen/VM execution gate; the normal suite discovers it too. Linux-only tests are gated and Linux execution is not Darwin execution. Publication is not verified until all eight checks succeed on the exact documentation-updated PR head; the PR's head and checks are the authoritative publication record.

## Next safe path

1. Correct existing native collection GET/SET using actual logical length, including negative-read normalization and nonnegative-only writes. Audit main, Action, capture, alias/copy and target-specific paths; unsupported representations must fail closed rather than fall back to capacity checks. Keep unsupported Text/Decimal/capture storage changes separate and reviewed.
2. Design bounded integer-only storage for the Kuro-owned generator with explicit element kind, logical length and capacity. Prove initialization and GET/SET bounds before append/length, identity and broader mutation forms. Preserve compatibility even if an initial admitted source subset uses explicit nonnegative guards.
3. Only after that proof, separately review Text-name/token storage. Then address full-analyzer decomposition, its 16,392-token artifact and global storage constraints; require real generator assembly/link/run and exact evidence parity.

Strict independence remains unfinished. Hosted bootstrap construction and the external assembler/linker are still dependencies. Do not merge this PR or its predecessors without explicit owner approval.
