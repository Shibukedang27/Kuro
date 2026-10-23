# Generation history has different helper and public-dispatch bounds

## What changes—and what does not

This tests/documentation increment starts directly above draft/open [PR #123](https://github.com/Shibukedang27/Kuro/pull/123), exact parent `e8a0eb0f648cac1963f20076ed0288b24015bbf9`. It installs no replacement ledger, collector, sharing, new resource ceiling, overflow rule, or production semantic change. The [history compatibility gate](vm-generation-history-compatibility.md) remains in force: preserve backend-observable exhaustion/history behavior unless a separate contract decision authorizes otherwise. A bounded public-dispatch argument is not permission to erase direct-helper history behavior or silently narrow the migration contract.

The useful distinction is between an outer helper that can reset an empty name repeatedly and the inner bytecode program, whose generation-creating paths publish rows. The existing 65,537-empty-reset native witness is real unchanged-helper execution, not proof that public bytecode can reset an empty collection for free. Neither it nor the new controls execute a complete generation cycle.

## Where natural history can come from

The VM starts with zero logical names, rows and next ID; its two physical seed slots have inactive IDs and are not public collections ([startup](../../self_host/vm.kuro#L26-L41)). Public bytecode names belong to a separate environment; naming a variable `VMNextCollectionId` does not write the outer counter, and an undeclared bytecode Action cannot invoke the outer reset helper. The earlier [consumer controls](vm-collection-consumer-contract.md) remain evidence for that separation.

The production generation-creating call sites are small enough to audit:

| Public dispatch path | Work and publication boundary |
| --- | --- |
| `BC_STORE_MULTI` | Requires more than one stack value; then resets the destination and publishes cells in sequence. Zero/one-value multi-store fails without resetting it. An invalid collection-kind cell can fail after the reset or a paid prefix. |
| `BC_STORE_LIST` with a collection marker | Resolves a name late and calls eager Copy. Same-name Copy returns before lookup or reset. A distinct destination resets only after a successful source lookup, then copies rows. |
| `BC_APPEND` to a name absent from the scalar environment | Calls Mark, then Append. Mark on an already active name consumes no generation; a newly marked generation publishes one row if the step completes. This one-row path prevents claiming that every generation costs two rows. |
| Scalar store/deactivation, Set, Get, Length, Print, declaration metadata | Do not allocate a generation. Set replaces cells without refunding rows. Deactivation does not reclaim rows. `BC_DECLTYPE` only consumes metadata; it does not create an active empty collection. |

See [ledger helpers](../../self_host/vm.kuro#L180-L364), [store dispatch](../../self_host/vm.kuro#L1123-L1181), [Append dispatch](../../self_host/vm.kuro#L1417-L1445), and [fail-stop run](../../self_host/vm.kuro#L1470-L1482). This is a frozen-source control-flow argument, not a theorem for arbitrary future opcodes, custom embeddings, reentry, corrupted state, or all host resource failures.

Starting from normal initialization, each completed generation-creating public step leaves a nonempty new generation and has paid at least one fresh historical row. Existing active generations are nonempty; copying them cannot create an empty destination on success. No public deletion operation removes a cell or refunds the append-only row count. Thus successful public generation allocations are bounded by paid rows on this implementation. A terminal failed step can already have assigned one additional generation before publishing any row; fail-stop prevents continuing with that empty partial destination. Do not strengthen this into an atomic-failure guarantee.

Under the native 65,536-row admission ceiling, that argument bounds normal successful public generation allocations by 65,536, with at most one additional allocation in a terminal failed step. This is far below signed exhaustion. It is not a newly enforced limit and does not apply to the outer helper driver, seeded counters, restart/resume embeddings, or hosted dynamic storage. The public controls below sample the paths; the bound depends on the complete source audit and its stated assumptions, not on extrapolating a seven-iteration test.

The [eight public-dispatch checks](../../tests/self_host/test_vm_generation_dispatch_churn.py) execute framed input through the complete unchanged artifact launcher, hosted and Linux x86-64 native. Seven-iteration repeat loops publish seven two-row generations, fourteen reset/copy generations, or eight one-row generations; literal traces check contents, counter, name slots, rows and failure/exit state. A separate empty multi-store control fails with zero generations and zero rows. No counter is injected or helper replaced.

Three [IR audit tripwires](../../tests/self_host/test_vm_generation_reachability_contract.py) pin all callers of Mark/Reset/Copy, the only counter mutation sites, and the nonrefundable row-debit mutation sites. They deliberately require re-review if the call graph changes; they do not infer branch semantics or automatically prove the funding invariant.

## Why a complete cycle is not a practical test

`VMResetCollection` on an existing helper name needs no new row or name slot. Native lowering ignores the hosted While guard; a constant-condition helper loop can keep incrementing without a ledger-allocation barrier. The Linux x86-64 backend uses 64-bit addition, while activity checks require nonnegative IDs. This supports a backend-specific control-flow/arithmetic argument, not a completed natural execution, a portable signed-overflow specification, or a guarantee of uninterrupted machine lifetime.

From counter zero, the first negative ID would be assigned on reset number **9,223,372,036,854,775,809**; owner zero would be assigned again on reset number **18,446,744,073,709,551,617**. Even a hypothetical billion increments per second takes about **292.27 years** to the first signed crossing and **584.54 years** to a complete counter cycle. These are illustrative arithmetic, not measured speed, timing lower bounds, or an execution claim. Tests must use bounded churn and explicitly labeled seeded boundaries rather than pretend to certify that duration.

Hosted integers do not wrap at either native boundary. The default reference runner also limits each lowered While guard to 10,000,000 iterations per IR invocation ([interpreter](../../compiler/interpreter.py)); nested calls can have separate guard accounting, so that number is not a universal process-wide generation bound. Neither raising the guard nor constructing a much longer hosted history demonstrates native ID reuse.

The seeded alias witness from #123 remains separate. In particular, we still do **not** execute Copy with a destination ID colliding with the captured source ID: its global scan can follow its own newly appended rows. Natural public nonreachability under the audited initialized path does not erase that preservation obligation for a broader helper-compatible replacement.

## Actual row overwrite versus retained reset history

The [new unchanged-helper witnesses](../../tests/self_host/test_vm_row_replacement_lifetimes.py) cover five scenarios on hosted execution and Linux x86-64 native execution:

- Set replaces the raw/display pair in physical row zero without changing its owner, paid-row count, remaining row order, or eager snapshot. A scalar pair captured before Set remains the old pair.
- Reset, with or without prior deactivation, retains physical row zero and appends the replacement generation at row four. The source name selects the new row; the captured scalar pair and eager snapshot retain the old values.
- An at-length Set failure changes neither cell, clears Set display scratch, and remains sticky through later successful reads.
- Self-copy spends neither a generation nor a row.

The original raw value and display are built from dynamic Text concatenation, not only static literals. Each scenario performs 64 later dynamic joins before checking the captured pair. Hosted state inspection verifies every one of the four original owner/value/display rows and the fifth row where present; native traces check the observable pairs, physical first row, counts and failure state. No invalid Get fallback is printed as Text. Scratch predicates use explicit tags instead of rendering empty Text.

These are **actual current row-cell replacement and capture tests**, not an implementation or safety proof for replacing the storage representation. The native concatenation paths in [`compiler/native.py`](../../compiler/native.py) append into a monotonic text heap and do not move or reclaim the old bytes. Changing a row's pointer is not freeing its Text. The checks therefore establish bounded capture survival in today's nonmoving backend, not moving-GC rooting, asynchronous pins, reclamation, all arena-failure cases, ARM/Darwin behavior, or authored-generator parity.

## Reader work, tails and publication costs

The same witnesses observe that current Copy of a two-row source ends its scan at position four: it visits the two source rows and the two rows it appended to a distinct owner. Length scans all four or five paid rows, including rows no longer selected by the source name. These are concrete bounded scan endpoints, not wall-clock benchmarks or a full workload cost profile. Current Append performs name lookup and constant ledger publication rather than a historical-row tail scan.

The alternatives still have different unproved costs:

| Layout | Established cost | Missing production evidence |
| --- | --- | --- |
| Current owner ledger | One owner/raw/display row per publication; retained history; global owner scans for readers and Copy. | No gain is delivered here. |
| Counter-free links without tails | Existing model counts 32,640 next-link reads for 256 appends. | Actual backend performance/lifetimes; still fails the broader history-preservation gate. |
| Row-funded ID-preserving descriptors with tails | Model adds three fields per retained name and one link per row: 2,097,152 extra payload bytes if all four extra columns are preallocated at 65,536 64-bit cells. | Native image/residency, allocation-failure compatibility, tail updates and rollback/publication behavior. |

The last two rows are [model arithmetic](vm-row-funded-metadata.md), not measured native storage replacements. The historical full-compiler peak remains 65,481 rows with 55 spare; it is not a new measurement here. Reducing global scans by adding a tail table can increase memory and add failure/write boundaries. No speedup, headroom or system-memory saving is claimed.

Append still admits before owner/raw/display writes and increments count last; Set still writes raw then display with no admission; Copy still resets before sequential append and can leave a prefix. Existing [IR publication guards](../../tests/self_host/test_vm_collection_consumer_contract.py) and [production capacity witnesses](../../tests/self_host/test_vm_publication_capacity.py) remain the evidence for those boundaries. No successful-run trace proves multi-column atomicity or equivalence under every system allocation failure.

## Next safe path

Keep the production representation and existing exhaustion behavior. A future ID-preserving linked slice must retain historical owner identity and counter arithmetic, preserve late name lookup, eager-copy snapshots, scalar/result/frame captures, negative indexing and exact failure publication, and supply an actual backend tail/metadata budget. A row-layout change must prove its own stable reader/index scope; a Text-moving change needs a separate complete root/relocation protocol. Public-dispatch funding is useful evidence, not a waiver for injected/helper histories or a substitute for either proof.

Acceptance requires new and existing focused tests, the full suite, independent frozen-head review, a fresh four-image rebuild, blocked-toolchain smoke, compiler reproduction/272-literal control, and eight successful CI checks on the exact published head. Final results belong in the immutable PR verification receipt, not an ancestor's receipt. Python seeding and Clang/LLVM still block strict independence; #107/#108 remain individually unverified. Keep this and the earlier stack draft/open/unmerged.
