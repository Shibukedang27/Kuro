# Stop the generation-tail migration until its backend proof exists

## Decision: no production slice is safe yet

This test/design-only increment is stacked directly above draft/open [PR #125](https://github.com/Shibukedang27/Kuro/pull/125), exact parent `599e21c6c316794a676e6b3328ea36d44f61f47f`. **No production improvement is made or claimed.** This increment changes no runtime, compiler, standard-library, generated distribution artifact, resource limit, failure policy, or hosted behavior.

The requested ID/history-preserving tail slice is not present in production, so there is no actual candidate tail code to measure or certify. Adding a tail write or switching a single reader would create a mixed representation with new mutation and failure boundaries, not a safe incremental optimization. Keep the append-only owner ledger and current scan behavior unchanged until a complete candidate is exercised through the real backend and its compatibility obligations are proved.

## What the current implementation actually does

The unchanged [VM helpers](../../self_host/vm.kuro#L221-L364) have no next-link or head/tail metadata. `VMAppendCollectionItem` admits one row, writes owner/raw/display, then advances the logical count. `VMGetCollectionItem`, `VMLengthCollection`, and `VMSetCollectionItem` scan the historical owner rows. `VMCopyCollection` captures the source ID before resetting the destination, then scans the growing global row count; for each match it captures raw and display before calling Append. These are concrete current algorithms, not timings or a future layout.

The [IR regression guards](../../tests/self_host/test_vm_collection_consumer_contract.py#L84-L162) pin the current nested-call scratch, append admission/write/count order, Copy's source-ID and scalar-pair capture order, Get's ID across negative-index Length, and Set's raw/display write order. The [bounded row-replacement probes](../../tests/self_host/test_vm_row_replacement_lifetimes.py) run the unchanged helpers on hosted and Linux x86-64 native execution. They show captured dynamic raw/display pairs and eager snapshots surviving Set or retained-row reset, while also measuring current Copy/Length scan endpoints. The native Text arena is monotonic and nonmoving; these probes do not prove moving storage, reclamation, arbitrary allocation-failure behavior, or other backends.

The helper-call graph is currently closed, synchronous, nonrecursive and contains no user callback or VM-dispatch edge. That bounds today's local captures, but a linked reader must additionally capture the next-row link before publishing a destination row. It must preserve late name resolution: collection stack markers carry names, and `BC_PRINT`/list-store resolve those names when consumed rather than retaining a row ID or descriptor. The authored VM has Action frames but no closure object/capture table; these helper tests do not certify the compiler's separate closure machinery.

## Publication is ordered, not transactional

Current Append has one logical admission point, then writes the owner, raw cell and display cell, and increments the row count last. Copy resets its distinct destination before row-by-row publication. `BC_STORE_MULTI` similarly resets only after it has more than one value, then publishes sequentially. Existing tests and the [row-funded model](../../tests/self_host/test_vm_row_funded_metadata.py#L209-L250) pin eager prefixes and destructive failure order at their respective scopes.

The [real-capacity native probe](../../tests/self_host/test_vm_publication_capacity.py) reaches the actual 65,536-row x86-64 boundary and checks exact fail-stop status and output. Native admission terminates the process, so it cannot inspect postmortem VM memory; the probe does not prove multi-column atomicity or system-allocation-failure equivalence. The small hosted controls intentionally do not emulate the native capacity. A production tail would add at least a next-link write and head/tail/length updates around this existing order. Their exact order, failure visibility, and any remaining prefix must be established in the emitted candidate, not inferred from Python lists or the current non-linked helpers.

## History and backend constraints are still material

The [history compatibility gate](vm-generation-history-compatibility.md) remains in force. Empty resets advance the private ID without paying a row; negative native IDs mean inactive; and seeded reuse shows that an old owner ID can become visible through a later name. The linked-row model preserves common short histories, but does not execute natural wrap or prove that a per-name tail descriptor reproduces the current owner-ID alias behavior after ID reuse. The counter-free layout is therefore still ineligible under the current conservative gate. A replacement may not silently discard the observable activity, contents, failure, or publication effects of these histories.

The [metadata budget measurement](vm-native-metadata-budget.md) records 4,194,336 bytes of extra Linux x86-64 zero-fill reservation for four ordinary Integer metadata arrays because the backend emits a per-element length sidecar as well as each value buffer. This is not an actual linked implementation, a prediction for every candidate, an RSS measurement, or a headroom improvement. Tail storage, descriptors, text/code size and write costs still need a real candidate build. Hosted storage must continue to grow dynamically rather than inherit the native ceiling.

Python seeding and the external Clang/LLVM toolchain still block strict independence, only Linux x86-64 native execution is available in these probes, and #107/#108 remain individually unverified. None of those limits is waived here.

## Evidence required before changing production

A later increment may proceed only after it contains actual candidate tail code emitted and run by the unchanged backend, not another Python-only layout model. Its tests and review must cover:

- ID and history behavior, including empty resets, negative/inactive transitions, seeded reuse/alias cases, and the unresolved source/destination ID-collision Copy traversal;
- actual chain writes and reads under interleaved generations, including head/tail/length invariants, Set, Append, Get with negative offsets, Length, Print, eager Copy, and retained historical rows;
- reader lifetimes: capture source head/length and each successor before destination publication, retain raw/display snapshots, preserve scalar/result/Action-frame behavior and late name lookup, and avoid claiming closure or moving-Text safety without separate evidence;
- exact native admission, fail-stop and partial-publication ordering for row data plus link and descriptor metadata, alongside hosted dynamic growth; and
- fresh native image/layout measurements, all focused and full tests, independent frozen-head review, fresh four-image rebuild, blocked-toolchain smoke, compiler reproduction/272-literal control, and all eight CI checks on the exact published head.

Until those proofs exist, a partial helper or metadata column would add cost and risk without replacing the old scans or delivering a demonstrated user-visible gain. Retain current production storage and semantics; keep this PR and its ancestors draft/open/unmerged.
