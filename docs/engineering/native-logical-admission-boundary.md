# Logical admission needs a backend-aware failure boundary

## What this increment establishes

This test-only increment starts directly above [PR #115](https://github.com/Shibukedang27/Kuro/pull/115), exact parent `df94f4f0d729c83bf9e8a436d66374bc23a9a9cb`. The [reservation model](vm-publication-reservation-model.md) gives a candidate accounting invariant, but it does not supply a native failure mechanism. The new [executable boundary probes](../../tests/self_host/test_native_logical_admission_boundary.py) investigate that missing mechanism without changing production helpers, compiler lowering, collection capacities or publication behavior.

The important distinction is between an **experimental native fail-stop surrogate** and a **portable production implementation**. A deliberate out-of-range collection Set can terminate a native process without allocating a dummy row. It is not suitable for activation in the shared authored VM: hosted execution would acquire a new limit and raise a different error. Keeping this experiment outside production is intentional, not a claim that admission or COW has shipped.

## Why a logical debit is not an Append

The production [VM](../../self_host/vm.kuro) retains three parallel row columns. `VMAppendCollectionItem` fills two seeded slots, then appends owner, raw value and display, and finally increments `VMCollectionEntryCount`. `VMCopyCollection` resolves the source, resets a distinct destination, and admits copies one row at a time through that helper. Reset and deactivation never refund historical allocations; same-name copy returns before looking up its source.

Native Append checks its collection's actual length against **65,536**. Once publication stops physically copying rows, that length cannot by itself enforce the earlier eager logical debit. Appending sentinel values to a second ledger would spend real collection storage to represent virtual reservations. Merely setting `VMFailed` would instead replace native process death with a recoverable authored error. Neither is the desired mechanism.

The experimental helper uses a scalar monotonic logical counter and, on exhaustion, attempts `Set VMCollectionOwners 65536 to 0`. The index is outside every valid native length of that column. Native bounds checks run before the write and terminate with status one. Successful logical reservations do not append to any row column. This is a bounds-failure surrogate, **not the native Append-overflow branch** and not a new native instruction.

## What the probes compare—and what they do not

The test driver retains the complete unchanged production VM. Its eager arm allocates real filler rows and calls production copy helpers. Its experimental arm reserves filler rows logically and scans the real two-cell source to debit a copy without publishing a destination. Common operation markers and logical row receipts compare the successful instruction prefix and terminal outcome at the actual limit. Separate physical-column receipts distinguish physical allocation from logical debit; successful virtual reservation must not be mistaken for a collection assignment.

An additional native witness admits the last virtual row, prints logical count 65,536 with two retained rows, and exits inside the next rejected debit before its continuation marker. Another shows integer-owner index one remains readable and index two remains out of bounds after those virtual reservations. The latter checks actual owner length without introducing unsupported Integer `Length` syntax. The Text-column lengths and entry counter are printed independently. Hosted edge observations deliberately disable the native trap and inspect a sticky test-only failure flag; continuing after that flag is not a claim that native execution resumes after exhaustion.

These probes do not implement sharing, generation bindings, detachment, a write barrier, source pinning under reentry or rollback. They do not observe memory after a process exits, and they do not prove synchronization or exact contents of a failed partial destination. Full-budget Set exercises the unchanged production helper on its ordinary source, not mutation of an implemented shared generation. The [production publication-root tests](../../tests/self_host/test_vm_publication_roots.py) remain the separate evidence for late-bound stack markers, raw/display lifetime and malformed multi-store partial publication.

The hosted controls are deliberately negative evidence for adopting the surrogate. Hosted collections do not inherit the native fixed capacity, while out-of-range Set raises `E6001`. A native status-one observation does not authorize imposing that new hosted boundary. Source/emitter inspection and cross-assembly are not substitute evidence for running an executable on a target.

## The next production slice

Introduce a small explicit, backend-aware admission operation rather than hiding a trap inside a normal collection access. Its native lowering must compare the logical debit with the unchanged configured capacity and reach the native terminal-overflow protocol without allocating a row. Hosted and Python-bytecode execution must retain their existing absence of the native row ceiling. The source/IR interface and treatment of invalid operands need a reviewed contract before implementation; this note does not add a magic helper name, parser keyword or intrinsic.

First wire that operation to one-row admission while retaining eager physical copies, and test exact-fit, short-by-one and full-budget boundaries. Preserve the copy's instruction-prefix behavior, no-debit self-copy before source lookup, invalid-source failure, and no refunds. Do not silently replace per-row admission with an atomic bulk publication or claim postmortem state parity. Only then migrate all Get/Length/Print, Copy, Set, Append, reset, scalar-overwrite and multi-store paths to one reviewed stable-generation protocol, with explicit in-flight protection, before enabling sharing.

Eager-compatible admission still cannot increase the set of programs admitted by the old logical ceiling. The historical full-compiler peak remains **65,481 rows, 55 spare**; this increment does not measure a new storage census or saving. Allocation-on-demand would be a separate deliberate resource-behavior decision, not a conclusion from this experiment. Python seeding and Clang/LLVM assembly/linking remain strict-independence blockers. PR #107/#108 remain individually unverified. Keep this increment and its ancestors draft/open/unmerged.

## Verification

The final focused boundary run passes **seven tests in 5.22 seconds** on Linux x86-64: three native eager/candidate copy boundaries, a native last-row/first-rejected-row witness, a native owner-length witness, hosted monotonic edge observations and the hosted-over-limit/surrogate distinction. An earlier tightening attempt used unsupported Integer `Length` syntax and was corrected to the explicit owner-bound witness before this passing run; it was not a production compiler change. Independent review also caught an implicit native-target default that would not select Intel Darwin correctly. The fixture now selects an explicit matching target for each admitted Linux/Darwin architecture, rather than changing production's default target policy.

The inherited capacity, reservation-model, COW-model and publication-root gates pass **49 tests in 7.71 seconds**. A separate fresh compiler-bytecode self-reproduction and complete 272-literal initializer gate passes **one test in 76.69 seconds**. These are unchanged-production regression gates, not evidence that the experimental mechanism is installed in the VM.

All **75 tracked production/compiler/CLI/bootstrap/wrapper/Makefile files** compare byte-for-byte equal to exact #115. The only proposed changes are the new boundary test, this engineering note and the running status index. Python 3.10 grammar parsing passes; local execution uses Python 3.12.3 on Linux x86-64.

The immutable-head PR receipt will separately record final focused probes, independent review, full-suite results, a fresh four-image rebuild and blocked-toolchain smoke, and all eight exact-final-head CI checks. Pending tests, review, rebuilds and CI are not successful gates. A Linux runtime result alone does not certify Darwin runtime support; each native-host probe must execute on its actual CI host before that narrower evidence can be claimed.
