# Native collection bounds follow logical length

Native collection GET and SET must not expose spare backing storage. This increment corrects the existing Python-authored native backend; it does **not** add collections to the Kuro-owned generator or complete strict independence.

It is stacked directly on verified, open/unmerged [PR #90](https://github.com/Shibukedang27/Kuro/pull/90), exact head `d21d7de8f79f93a53f5202da3bef57a11625ac3a`, with all eight checks successful. Its base is the negative-read compatibility correction, not an older stack head. No PR is merged by this work.

## Exact behavior

The [established compatibility rule](collection-index-compatibility.md) remains unchanged. For logical length `L`, GET accepts `-L <= index < L`; negative GET normalizes to `L + index`. SET accepts only `0 <= index < L`. SET never grows the collection. A two-element collection rejects index `2`, even though its fixed buffer reserves 65,536 elements. APPEND changes the logical end; literal reassignment resets it.

[The native backend](../../compiler/native.py) now checks the existing owner-specific length word before scaled addressing in Linux x86-64 main and Action code, and in the dynamic macOS ARM64 main and Action paths. The x86-64 macOS wrapper retains the x86 guards. ARM64's separate constant-folding path now permits negative collection GET; it still rejects invalid constant accesses during emission. Text indexing is not given negative-index semantics by this patch.

Dynamic failed accesses retain the existing native bounds-error path: exit status 1, without a new diagnostic string or subsequent execution. Hosted/bytecode runtimes retain their `E6001` exceptions, and the authored Kuro VM retains its failure flag. These are behavioral failure parity, not identical error interfaces.

## Missing metadata fails closed

A collection pointer is not an owner/length pair. Existing Linux captured collection GET/SET previously accepted a pointer and checked only fixed capacity; that was not sound logical bounds. Those operations now reject during native emission when logical-length metadata is unavailable. Existing captured SET element-kind and Text item-length rejections retain their diagnostic precedence. Captured LENGTH/APPEND remain unsupported.

A conservative, rejection-only provenance scan follows existing LOADVAR/SAVEVAR, singleton STORE_LIST, UPDATE/RESTOREVAR, direct Action argument and return edges. Known collection aliases and parameters cannot fall through to byte-oriented Text access or borrow an unrelated static buffer's length. Parameter names colliding with a static collection name do not establish storage ownership. The scan is monotone over finite existing names; it may conservatively reject a variable used for a collection on any path, even if another path overwrites it. It is not a new type system or acceptance analysis, and adds no pointer/length ABI, capture layout, collection copying, nested collection, or generalized element support.

The bounds claim is limited to supported native collection buffers whose emitted logical-length word matches the represented collection. The backend's inherited treatment of singleton STORE_LIST on a statically allocated buffer is not a general proof of hosted scalar-to-collection promotion or representation parity. A scalar reassignment is not a collection-reassignment witness; this increment neither adds scalar kind metadata nor authorizes broader scalar indexing.

**Compatibility cost:** the former pointer-only integer/Text captured-read and integer captured-update success tests now require explicit rejection. This is an intentional fail-closed restriction, not a claim that captured collection storage has been implemented. Restoring it safely requires a separately reviewed identity/length representation.

## Why the arithmetic is safe

For GET, x86 computes a candidate `index + L` in scratch registers, selects it only when the original index is negative, then performs an unsigned comparison against `L`. ARM64 uses a signed comparison of the original index, non-flag-setting ADD, conditional selection, and the equivalent unsigned comparison. A negative input plus bounded nonnegative length cannot overflow signed 64-bit arithmetic. The speculative positive-input sum may wrap but is discarded; its flags do not choose the candidate or admit access. Positions below `-L` stay negative and fail the unsigned check. SET performs no normalization, so negatives also fail unsigned comparison.

Both checks precede multiplication by eight. Initialization and bounded APPEND maintain `0 <= L <= 65536`, so an admitted index yields a byte offset at most 524,280 within the existing 524,288-byte buffer. The helpers preserve value/base registers, do not call another function, and use scratch registers only. Empty logical length admits no index; empty source literals are not newly supported.

## Evidence

[The new native boundary tests](../../tests/self_host/test_native_collection_bounds.py) exercise logical-end versus spare-capacity reads/writes, valid negative reads, invalid negative writes, signed 64-bit extremes, Action runtime indexes, append, collection-only reassignment shrinkage, and interleaved owners. Integer witnesses compare the hosted interpreter, JSON-round-tripped bytecode VM, authored Kuro VM, and actual Linux native execution. Additional tests require pointer-only parameter/alias/copy rejection, verify ARM64 guard emission and constant-folding behavior, and inspect x86 macOS wrapper guards. Linux execution is not Darwin execution.

The inherited [compatibility matrix](../../tests/self_host/test_collection_index_semantics.py) and [indexed-state contract](../../tests/self_host/test_native_indexed_state_contract.py) now require native logical bounds rather than preserving known capacity-based failures. The latter still builds a fresh actual Kuro generator: its scalar control generates, links and runs, while complete integer indexed-state and Text-name collection artifacts reject. Those rejections are unchanged evidence of unfinished generator support, not a new success claim.

Independent review confirmed the bounds arithmetic and scratch-register safety, then blocked an initial provenance implementation that treated every `t`/`__` prefix as a compiler temporary. The legal global alias `target` could consequently reach a Text byte read and segfault. Global alias identity now comes from explicit IR variable assignment targets rather than spelling; regressions cover `target`, `__bag`, `t0` and ordinary names on both emitters. The superseded full-suite run was deliberately stopped and restarted after this fix. An initial test fixture also reassigned a collection to the scalar `4`; it was corrected to the genuine two-element collection `4, 5`, rather than treating a scalar assignment as collection-parity evidence.

The next review found that a global alias first assigned inside an Action was not shared with another Action's rejection scan. The corrected scan conservatively shares non-parameter variable alias targets from every body, not just main. Regressions cover both resolved-IR maker/reader scan orders and GET/SET on both emitters; reversing source declarations itself is not accepted by the frontend. The earlier complete run (1,624 passed, 20 skipped) predates that correction and is not final-head evidence.

Final independent review approved the corrected implementation for the stated static-buffer scope and reproduced **92 passed** in the new module. Final fresh focused/native/generator gate: **225 passed, 1 skipped in 48.44s**. It rebuilt the actual generator, generated/linked/executed the scalar control with exact output `255\n`, and preserved all complete collection-artifact rejections. Counts overlap rather than add.

Final complete suite on the approved production code and finalized tests, with a fresh artifact directory: **1,632 passed, 20 skipped in 809.64s**. All five changed Python files parse using Python 3.10 syntax rules, and `git diff --check` passes. Clang cross-assembles the dynamic Action GET/SET witness for `arm64-apple-macos11` and `x86_64-apple-macos11`; this is assembly validation, not Darwin execution. Six native-host Action/global witnesses are also collected on macOS so CI exercises actual Darwin success/failure paths, not only emitted strings.

```sh
.venv/bin/python -m pytest -q tests/self_host/test_native_collection_bounds.py tests/self_host/test_collection_index_semantics.py tests/self_host/test_native_indexed_state_contract.py tests/compiler/test_native.py --basetemp=/workspace/kuro-native-bounds-focus-final --durations=10
.venv/bin/python -m pytest -q --basetemp=/workspace/kuro-native-bounds-full-final --durations=20
git diff --check
```

Acceptance additionally requires all eight checks on the exact final documentation-updated PR head; the GitHub PR head/check record is authoritative. The PR must remain open and unmerged.

## Next safe step

Design a bounded integer-only representation for the Kuro-owned generator with explicit element kind, logical length and capacity. First prove initialization and GET/SET bounds, including the asymmetric negative-read rule, and reject unsupported aliases, parameters and mutation forms. Add append/length and shared identity only after their storage proof. Restoring native captured collection access also needs explicit owner/length transport rather than capacity fallback.

Text collections, Decimal collection generalization, full-analyzer execution and its artifact/global-storage constraints remain separate work. The Python-hosted bootstrap seed and external assembler/linker remain dependencies. Strict independence is unfinished.
