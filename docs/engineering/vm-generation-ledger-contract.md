# Stable generations need an accounting and reader contract

## What this increment establishes

This test/design-only increment starts directly above draft/open [PR #117](https://github.com/Shibukedang27/Kuro/pull/117), exact parent `a42691986f178002fc605dd6b5fde5885013e76f`. That parent has eight successful exact-head checks. Its native one-row preflight remains installed; this increment changes no production source, resource ceiling, eager copy, or hosted allocation behavior.

The next production change is not justified merely by adding another counter. A separate logical ledger must preserve the exact eager debit history, while stable generation bindings must protect both published snapshots and any in-flight readers. This increment records the current eager generation/debit behavior and an executable boundary on the earlier sequential reservation model. It installs neither a separate ledger nor sharing.

## Stable identity is not an immutable snapshot

The [new counterexamples](../../tests/self_host/test_vm_copy_nonreentry_contract.py) borrow a generation ID from the [sequential reservation model](../../tests/self_host/test_vm_publication_reservation_model.py), then mutate its sole bound name. Set changes the borrowed generation's raw/display pair; Append changes its sequence. The ID remains stable in both cases. These are intentional observations of the model's excluded reentry domain, **not production bugs or a newly failing model invariant**.

A local borrowed ID does not participate in that model's binding-based reference count. Retaining an ID, retaining its cells, and preserving a snapshot are three different promises. If a future operation can yield after resolving its source, a callback could mutate the source while it appears uniquely bound. A pin must affect write-detachment decisions, or the operation must prohibit such reentry. Merely retaining old generation IDs does not solve this.

The debited-binding control copies a one-cell source into a second bound name, filling a two-row logical budget while retaining one physical cell. A Set then detaches the writer, preserves the snapshot's raw/display pair, and consumes the already-paid credit without another logical debit. That control is still model-only; its two-row capacity is not a native limit or a patched VM.

An uncharged reader pin cannot simply be counted as another paid alias in the prior inequality. For example, one uniquely bound cell at logical capacity one has no spare credit for another retained physical cell. The prior proof covers bound, eagerly debited aliases; a general reader-pin protocol needs its own lifetime, credit, release and failure argument. This increment deliberately does not invent or activate one.

## What the authored helpers demonstrate

The [four new hosted behavioral witnesses](../../tests/self_host/test_vm_generation_ledger_contract.py) execute the complete production VM source plus bounded direct-helper drivers. Reset/deactivate/reactivation advances IDs without refunding historical rows; marking an already active collection creates no generation. Repeated eager copies allocate fresh destination generations and pay again, while old raw/display rows remain retained. Mutation, reset and deactivation of the source preserve copied snapshots; a stack-held name instead resolves the replacement source when consumed. Empty copy spends no rows, inactive self-copy returns before lookup, and a missing source preserves the destination. Invalid Set is observed before a later successful write, so that write cannot mask corruption.

These hosted helper tests are not a native allocation, unbounded generation-ID, or concurrency proof. Calling another helper after sticky `VMFailed` characterizes direct helper behavior; it does not assert that ordinary bytecode dispatch continues after failure. The inherited production-root and real-capacity witnesses remain separate gates for late-name deactivation, partial publication and native fail-stop.

## Why the current copy is narrower

The [production eager helper](../../self_host/vm.kuro) resolves and retains the source ID before resetting the destination. Each matching row's raw value and display are loaded before its eager append. The destination receives a fresh ID; the growing historical row scan therefore does not mistake its own appended destination rows for source rows. Historical IDs/rows are retained rather than reused.

The new IR-level regression tripwire checks the complete reachable helper call graph from `VMCopyCollection`: `VMFindCollection`, `VMResetCollection`, `VMFindCollectionSlot`, `VMMarkCollection`, `VMAppendCollectionItem`, and the private `__KuroAdmitRow` leaf. It requires the current exact call edges, an acyclic helper graph and a closed set of current IR effects. No edge reaches bytecode dispatch, user Actions, input, or output. A future edge or opcode must trigger review rather than silently inherit the current scratch-lifetime argument.

This is a check of the authored helper graph under today's synchronous execution, not a theorem about concurrency, arbitrary forged IR, native intrinsic internals or future opcode semantics. It does not authorize reentry, native metadata reclamation, moving Text, or replacing late-bound stack names with frozen handles.

## Contract for the next implementation

Keep a separately reviewed monotonic logical count equal to the rows eager execution would have admitted. Copy charges one row at a time at the eager publication point; Append charges one; Set, reset, deactivation and self-copy refund nothing. Native overflow remains terminal at 65,536 rows. Hosted execution must not acquire that ceiling. Do not replace native fail-stop with `VMFailed`, or make partial publication transactional.

Introduce stable generation metadata without sharing first, with explicit bounds/overflow behavior for its own metadata and monotonically allocated IDs. Demonstrate that every consumer and mutator uses the same protocol: Get (including negative logical-end reads), Length, Print, Copy, Set, Append, reset, scalar overwrite, result/frame behavior and incremental multi-store. Preserve late name resolution and raw/display capture. Either retain the reviewed no-reentry discipline throughout publication or separately prove in-flight pin ownership and credit before adding a callback/yield boundary. Only then consider sharing and detachment.

## Verification and honest limits

The initial counterexample/call-graph gate plus inherited reservation model passes **14 tests in 1.99 seconds**. The combined new contracts plus inherited reservation/COW, root, real-capacity and admission modules pass **137 tests in 17.92 seconds** (eight new cases). Independent review, complete-suite results, fresh compiler reproduction/272-literal control, fresh four-image rebuild, blocked-toolchain smoke and exact-final-head CI belong in the immutable-head PR receipt. Pending gates are not verified results; parent checks certify only the parent.

No new compiler storage census or headroom gain is claimed. The historical complete-compiler peak remains **65,481 rows, 55 spare**; preserving eager logical admission cannot expand that budget. Python bootstrap seeding and external Clang/LLVM remain strict-independence blockers. The authored compiler's complete semantic gate and scalar type provenance remain unfinished; PR #107/#108 remain individually unverified. Keep this increment and all ancestors open/unmerged.
