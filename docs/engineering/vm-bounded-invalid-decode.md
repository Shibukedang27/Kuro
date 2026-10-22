# Stop short malformed-number decodes after failure

## A real but narrow allocation reduction

This increment is directly above [PR #112](https://github.com/Shibukedang27/Kuro/pull/112), exact parent `1933b5e67cb0b6447a6a36fb805de85345a4c05e`. It changes production [VM decoding](../../self_host/vm.kuro), not collection ownership: once a digit is invalid, the recursive numeric decoder returns immediately **only when the complete input has fewer than 19 characters on that target**. The sole external caller discards the numeric result after invalidity and returns the original Text.

The change avoids unnecessary native character extractions. It does **not** reclaim Text, share collection generations, compact rows, change storage ceilings, integrate semantic passes, or complete toolchain independence. Python still seeds production images; Clang/LLVM still assemble and link them. This PR and all ancestors remain open/unmerged.

Most importantly, **full compiler self-reproduction gets no measured saving**. Its aggregate ledger remains 65,481 rows with just 55 spare. The bounded malformed-input witness saves 3,400 character-arena bytes; that is not a claim of compiler headroom, speed, RSS improvement, or collection compaction.

## The exact production change

After `VMDecodeDigit` sets `VMNumericOk` to zero, `VMDecodeNumber` checks `Count < 19` and returns zero. There is no early return for valid numeric inputs, and spellings of length 19 or more retain the parent decoder's complete path, including its existing arithmetic and failure behavior.

The length bound is intentional. For at most 18 positions, the old nonnegative integer accumulator never exceeds `10^18 - 1`. The decimal divisor is at most `10^18` (more tightly bounded when a dot consumes a position), remains nonzero, and fits signed 64-bit arithmetic. Repeated dots do not multiply the divisor. Consequently, after an invalid character the skipped bounded suffix cannot introduce integer overflow or zero division. Removing work on arbitrarily long malformed inputs would require a different proof; this increment does not do that.

`VMNumericOk` is sticky inside a decode: `VMDecodeDigit` can clear it but never sets it back to one. On return, `VMDecodeConstant` checks that flag, clears `VMDecodedFloat` and `VMDecodedDisplay`, ignores the helper's numeric result, and returns its original `Value`. Empty and one-character inputs never enter the changed branch. Valid Decimal values retain their original display spelling and repeated-dot acceptance. Native length/indexing remains byte-based; hosted Unicode behavior is not silently substituted for native behavior.

## Why roots and aliases remain safe

The production call graph is bounded: `BC_CONST` calls `VMDecodeConstant`; that calls `VMDecodeNumber`, which only recurses into itself and calls `VMDecodeDigit`. There is no callback, scheduled work, VM instruction dispatch, collection publication, or captured object transfer within the skipped suffix. Repository call-site inspection finds no other external caller of `VMDecodeNumber`.

The original Text remains reachable through the outer decoded `BytecodeOut`, the caller's `Value`, and the decoder parameter. No source, pointer, arena cursor, collection ID, or collection cell is overwritten, rewound, moved, recycled, or released. An extracted character is used only for dot/digit classification on this path; skipped suffix characters are never published into the interpreted program. A previously extracted character may remain in private helper scratch storage, but neither that scratch value nor the discarded numeric helper return is a program-visible VM binding. Bytecode names live in the VM's separate name/value tables, not the outer helper globals.

On an invalid decode, the same original raw Text is passed to `VMPush`, with the same scalar kind and cleared Decimal display state. Earlier scalars, collection cells, stack slots, Action arguments, returned values, result slots and output retain their existing immutable Text references. Native and hosted closures are outside this helper and unchanged. No lifetime inference is made from current collection owners.

All collection code is unchanged: late stack-name resolution, eager assignment snapshots, display copies, mutation isolation, reset/deactivation generations, global-collection/frame precedence, kind erasure across Actions, and partial multi-store publication retain their existing implementation. The concrete [publication regressions](../../tests/self_host/test_vm_publication_roots.py) and [retained Text/copy regressions](../../tests/self_host/test_vm_storage_lifetime.py) run against the candidate, not just the model.

### Resource-exhaustion boundary

Avoiding an allocation can let a workload succeed where the parent exhausted its native character arena. **Identical allocation-overflow timing or identical success/failure for all near-capacity programs is not claimed.** The configured character, Text-join and collection ceilings are unchanged; the optimization does not reserve a virtual charge for bytes it no longer allocates. This is the same distinction between an allocation optimization and a complete resource-failure refinement.

For executions whose baseline decoding completes within its resource bounds, the bounded arithmetic/call-domain argument establishes the same decoded values and public metadata. Existing bytecode semantic failures and partial-store mechanics are untouched and tested. A stronger requirement to preserve every parent resource-exhaustion outcome would block this production optimization until an explicit allocation-budget contract is implemented. Do not present the tests as proving that stronger claim.

## Fresh before/after measurements

The [machine-readable receipt](vm-bounded-invalid-decode-census.json) includes six fresh censuses, exact-parent and candidate source/input/assembly/image/output hashes, and all 71 production/compiler/bootstrap/wrapper/Makefile source hashes. All runs stop at the explicit normal epilogue, report zero VM/runtime/inferior status, empty stderr and synchronized ledger columns. Parent and candidate use identical inputs and have byte-identical stdout for each pair.

| Workload / monotonic retained allocation | Exact #112 parent | Candidate |
| --- | ---: | ---: |
| Full self: rows per ledger column | 65,481 | 65,481 |
| Full self: character bytes | 870,724 | 870,724 |
| Full self: Text-join bytes | 2,192,152 | 2,192,152 |
| Complete 272-literal control: rows | 4,189 | 4,189 |
| Complete control: character bytes | 347,354 | 347,354 |
| Complete control: Text-join bytes | 1,188,633 | 1,188,633 |
| 100 bounded malformed constants: rows | 0 | 0 |
| Malformed witness: character bytes | 17,832 | 14,432 |
| Malformed witness: Text-join bytes | 56,435 | 56,435 |

The malformed witness is `kuro.bytecode/1\n` followed by 100 repetitions of `BC_CONST\nxabcdefghijklmnopq\nBC_PRINT\n`. Its 18-byte spelling fails at its first character. Native Text `Get` allocates two bytes per extracted byte, so skipping 17 suffix positions saves 34 bytes per decode, exactly matching the measured 3,400-byte reduction. Both outputs are exactly 100 repetitions of `xabcdefghijklmnopq\n`. Artifact-loader allocations remain included in both measurements.

The self and control inputs/output also match a separate fresh reproduction test, not only their paired diagnostic runs. Candidate ordinary launcher assembly is byte-identical to the accounting script's pre-symbolization assembly and to the separately rebuilt four-image checkout. Only `self_host/vm.kuro` differs among the 71 parent/candidate production files. Character and Text-join cursors are monotonic, so their successful final values are retained-allocation peaks; they are not live Text or RSS measurements. No ARM64 runtime-memory measurement is asserted.

## Verification and the remaining implementable path

The [new differential tests](../../tests/self_host/test_vm_bounded_invalid_decode.py) use the existing hash-pinned parent decoder, checked against the exact #112 source modulo empty lines. They cover 122 distinct values: all strings of lengths zero through three over a four-character alphabet, malformed positions at lengths 17–20, leading zeroes, repeated dots, retained Text, Unicode and safe longer numbers. Hosted results also match an independent small semantic oracle. Batched production-launcher native runs compare full stdout, status and stderr; direct native helper-only probes are not substituted for the actual launcher.

Verification includes the existing concrete ownership/lifetime witnesses, a complete fresh suite, separate full self-reproduction and complete initializer control, all four images rebuilt after removal, blocked Python/toolchain smoke, independent review, and eight successful push/PR checks on the final immutable head. Exact gate outcomes and final head belong in the PR verification receipt; pending checks must not be described as passed.

The compiler-row blocker is unchanged: every one of the 65,481 measured rows still has a current owner. Removing obsolete owners cannot help this workload, and guessed phase liveness is not a proof. `IROut`, `BytecodeOut`, and snapshot `CompilerOutput` each retain 9,118 cells. To reduce those rows safely, the next implementable prerequisite is an explicit production publication/capacity contract: preserve late-bound names separately from snapshot generations; define logical allocation charges and partial-copy failure behavior; then introduce stable generation references with reviewed Set/Append detachment and pinned in-flight copy/scan sources. All access/mutation/publication sites must use that protocol before sharing a generation. The [#112 obligations](vm-publication-cow-model.md) remain binding; this decoder change does not discharge them or authorize COW promotion.
