# A no-sharing ledger still needs a metadata layout proof

## What changes here

This test/design-only increment starts directly above draft/open [PR #118](https://github.com/Shibukedang27/Kuro/pull/118), exact parent `ff25f04c0348ddf0a7d657a5c8fc01440d8f4fa6`. That parent has eight successful exact-head checks. No production source, checked-in image, resource ceiling, eager copy, or hosted admission behavior changes here.

The [executable protocol model](../../tests/self_host/test_vm_nonsharing_ledger_protocol.py) separates a monotonic logical debit from retained physical rows and generation metadata **without sharing**. It checks 131,072 four-operation traces against the independent eager oracle from the earlier reservation increment. Unlike the sharing model, this model can compare the destructive destination prefix even when its terminal overflow event occurs. Those post-terminal model states are specification evidence, not inspectable native postmortem promises.

The [production-helper metadata-pressure witnesses](../../tests/self_host/test_vm_generation_metadata_pressure.py) add a concrete reason not to install a naive per-generation table. The native Linux x86-64 driver resets one name 65,537 times with zero logical rows, then successfully publishes an empty copy, an appended raw/display pair, and an eager snapshot. It uses the complete unchanged VM source and the real 65,536-row native limit; no helper, emitter, assembly, or capacity is patched. The final history has 65,539 allocated IDs but only two rows and three name slots. A small hosted control checks the same transitions. Neither witness proves unbounded generation IDs or native arithmetic-overflow safety.

## Protocol and credit rules

Each active name binds to its own generation. Generation IDs increase monotonically and are never reused. Reset allocates a fresh empty generation; deactivation removes a binding, not history. Empty copy still gets a fresh destination generation. An equal-name copy returns before lookup, including inactive names; a missing source sets authored failure and preserves the destination.

Every successful Append and every published copy row increments the logical ledger by one at the eager row-publication point. Historical rows remain retained. Set changes the existing raw/display pair without allocating a row or debiting again. Reset, deactivation and scalar-replacement reset refund nothing. There are no shared bindings, no detachments, no paid-alias credit, no reader credit, and no reclamation: **physical rows equal logical debits** throughout the modeled execution.

Copy resolves the source before resetting its destination, borrows the source only for that synchronous helper interval, captures each immutable scalar raw/display pair, and appends one destination row at a time. No bulk reservation makes the copy transactional. When row admission fails, the model records a terminal event with the number of rows already copied. A sequential multi-store control preserves the earlier completed destination and the later partial prefix. The existing real-capacity and production-root tests remain the native/bytecode gates; this model does not replace them.

The model's row ceiling is optional: `None` means hosted admission has no inherited native row ceiling. Tiny finite limits make exhaustive native-style event comparisons tractable; they do not emulate all native resource limits. The unchanged production native preflight remains terminal at 65,536 rows, not a recoverable `VMFailed` or a physical-headroom test.

## Readers are scoped, not paid aliases

A reader token records its generation and length, is valid only during its borrowing scope, and cannot be reused after release or in another model instance. Public helper reentry while any reader is live is an excluded protocol transition. Tests try Set, Append, reset, deactivation and another copy at a full one-row logical budget; each attempted reentry leaves the model unchanged. After release, Set remains legal at that budget and consumes no new row.

`ProtocolViolation` is test-model enforcement of a **no-reentry obligation**, not a proposed runtime lock, new source-language exception, or permission to reject a formerly valid user operation. Copy's internal destination append path does not reenter the public model entry point. The inherited [copy-helper IR call-graph tripwire](../../tests/self_host/test_vm_copy_nonreentry_contract.py) supports only today's synchronous production Copy closure. It does not certify every VM consumer, intrinsic internals, concurrency, arbitrary forged IR, or future effects. The model's `finally` bookkeeping after its terminal event does not promise native cleanup after fail-stop.

If any future reader can yield to a writer, this protocol no longer applies. The [prior borrowed-ID counterexample](vm-generation-ledger-contract.md) still stands: retaining the old snapshot of one uniquely bound cell while publishing a changed cell needs two physical cells, although the one-row logical budget paid for only one. Counting an uncharged reader as an alias cannot create that missing credit. This increment adds neither asynchronous pin ownership nor a detachment-credit policy.

## Why a bounded generation table is not ready

The model optionally gives its candidate metadata allocator a separate finite limit. Four empty generations exhaust a four-entry retained table while logical debit remains zero; the independent eager oracle continues resetting successfully. `MetadataExhausted` explicitly marks a **rejected layout's additional failure**, not a compatible native-row overflow or authored VM failure. Its simulated allocation behavior is not approved failure precedence.

The real native churn witness makes the distinction concrete beyond a toy budget: one generation-metadata entry per historical ID cannot simply inherit the native 65,536-row buffer limit. Increasing that table to another arbitrary finite size does not establish equivalence either. Existing generation IDs are native scalar integers, so this finite witness must not be extrapolated to unlimited IDs.

The Python dictionaries, lists of row indices, immutable scalar cells and unbounded integer IDs in the specification are conveniences, **not deployable native metadata**. A later implementation needs a representation whose allocations and ID-overflow rules fit all previously supported histories, including repeated empty reset/copy, without silently reclaiming an in-flight reader's storage or introducing an unexplained new failure. No owner census justifies dropping metadata.

## Evidence and limits

The initial protocol plus inherited generation/reader/reservation gate passes **33 tests in 6.00 seconds**, including the exhaustive 131,072-trace comparison. The broader generation/reader/reservation/COW/root/real-capacity/admission gate passes **161 tests in 27.15 seconds**, including the real native generation-churn witness. Independent review, complete suite, fresh compiler reproduction/272-literal control, four-image rebuild, blocked-toolchain smoke, and exact-final-head CI are acceptance gates recorded in this PR's immutable-head receipt. Pending gates must not be represented as verified results, and the parent's checks certify only the parent.

The model covers immutable scalar cells, numeric name slots, positive reads, valid/invalid Set, Append, reset, deactivation, replacement, eager copies and sequential multi-store. Its late-name control retains a name slot across replacement, not a full stack/closure/frame implementation. It does not cover marker decoding, moving Text, negative logical-end reads, Print, result/frame/closure roots, metadata atomicity, native generation-ID overflow, or full analyzer completeness. Those consumers and their existing tests must remain visible migration obligations, not implied coverage from an exhaustive small alphabet.

No new compiler census, production ledger, stable-metadata migration, sharing, COW, reclamation, or headroom improvement is claimed. Historical full-compiler peak remains **65,481 rows, 55 spare**, not newly measured here. Python bootstrap seeding and Clang/LLVM assembly/linking still block strict independence. Scalar provenance and the complete authored semantic gate remain unfinished; PR #107/#108 remain individually unverified. Keep this increment and its ancestors draft/open/unmerged.

## Next safe path

Review a native metadata representation and ID-bound protocol against empty-generation churn before production allocation. Then migrate ledger/metadata without sharing and audit every reader/mutator against the same binding and synchronous-lifetime rules: Get including negative logical-end reads, Length, Print, Copy, Set, Append, reset, scalar overwrite, result/frame/closure paths and incremental multi-store. Preserve late resolution, raw/display capture, exact eager debit chronology, native terminal admission and hosted behavior. Only a separate lifetime/credit proof can authorize reentry, sharing or later reclamation.
