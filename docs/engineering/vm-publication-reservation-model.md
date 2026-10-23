# A reservation budget can preserve admission, not create headroom

## The next safe step is still outside production

This increment stacks directly on [PR #114](https://github.com/Shibukedang27/Kuro/pull/114), exact parent `dff82b5a28ee5958c5ddda4feca681d2cbe4d02c`. It makes one proposed resource policy executable in a **test-only bounded model**: keep the eager allocator's logical debit even when publication shares physical storage. Production still eagerly copies, retains its existing limits and exits natively on row overflow. No sharing, detachment, capacity guard or reclamation is installed in the VM.

The [real-limit characterization](vm-publication-capacity-contract.md) established why an unbounded COW model is insufficient. A two-cell copy with one row spare kills the native process. Sharing that copy and letting a later mutation fail would change the admitted instruction prefix. Conversely, an authored `VMFailed` check would replace process death with a different failure protocol. Neither change is authorized by a value-equivalence argument.

The [new executable design model](../../tests/self_host/test_vm_publication_reservation_model.py) addresses the accounting prerequisite, not that native mechanism. Its capacities are small abstract numbers, **not patched native limits or a hosted exhaustion oracle**. The [actual native witnesses](../../tests/self_host/test_vm_publication_capacity.py) remain separate evidence.

## Candidate policy: debit as if publication were eager

Maintain two monotonic counts: `logical`, the number of rows the eager implementation would have allocated, and `physical`, the number of cells retained by the sharing implementation. Reset and deactivation refund neither count. A distinct-name copy charges the source's full length even when the destination already shares that generation; self-copy charges nothing and remains a no-op before source lookup. Append charges one logical row. Set charges no logical rows.

Successful publication resolves the source generation before replacing the destination binding. A valid write to a shared generation first copies its full ordered raw-value/display sequence. A shared append also allocates its new cell. An invalid Set must fail validation without detaching. Empty publication requires no row debit. Old generations are retained; IDs never move or get reused.

A publication that cannot pay the logical debit is a **terminal overflow at the eager operation**, not a successful sharing operation. The model records how many eager copy cells fit before that event, and stops executing. Comparing that arithmetic prefix does not inspect a dead native process or prove its failed destination, column synchronization or rollback. Non-capacity helper errors are separately modeled; they are not used as a substitute for terminal overflow. Malformed multi-store's observable partial publication remains a separate production contract, not an atomic error in this model.

## Why detachment can fit without another logical debit

For each currently bound generation, count its names. Define its outstanding copy obligation as `max(names - 1, 0) * length`. The candidate maintains:

```
physical + total outstanding copy obligations <= logical <= capacity
```

This is stronger than merely checking that physical allocation is below capacity. Sharing an N-cell generation can add at most N to its outstanding obligation; the eager copy debit supplies those N credits. Replacing a destination binding can only release its old obligation before adding the source obligation. Repeated publication between names already sharing a generation still pays the eager debit, even when no extra obligation is created.

Detaching one writer spends N physical cells but removes N outstanding obligation. A subsequent append increases both physical and logical by one. Unique Set changes neither count. Reset, deactivation and scalar-style unbinding cannot increase the obligation and do not reclaim retained cells. Thus an admitted Set can detach even when the logical budget is full; charging it again would incorrectly reject a Set that eager storage permits. An Append still fails at a full logical budget even if sharing left physical space unused.

This transition argument is restricted to the model's sequential flat-cell domain. Exhaustive bounded traces test its implementation; they are not a whole-VM proof or a native allocation receipt. Get uses nonnegative offsets in this restricted domain; production's negative-Get normalization is not modeled. The model has no late-bound stack markers, Text allocator, native metadata allocator, reentry, closure/task heap, bytecode dispatch or multi-store staging. Its retained Python generation lists are not a proposed native layout. Continuing direct helper calls after a sticky modeled error does not claim that normal production bytecode dispatch continues after failure.

## What a production implementation still needs

The accounting policy is a concrete compatibility-preserving candidate, **not an adopted production resource change**. An independent source review confirms that adding a sticky authored guard or sharing IDs alone is unsafe. The next implementation must first provide and test a capacity-admission mechanism that reaches the native fail-stop boundary with the eager instruction prefix. Its logical charges must not accidentally become physical row allocations or a recoverable `VMFailed` path. The native limit must remain 65,536.

Only after that boundary is executable should stable generations and sharing be considered. All Get/Length/Print scans, Copy, Set, Append, reset, scalar overwrite and incremental multi-store paths must obey one reviewed protocol. In-flight source generations, row positions and raw/display values need explicit pinning or a proved no-reentry discipline. Invalid operations must not detach. Preserve late-bound stack names rather than replacing them with frozen generation handles. Preserve scalar/frame/result/output lifetime and existing closure behavior; the authored VM does not gain collection closures from this model. Do not move or reclaim Text.

A real-limit production test matrix must include exact-fit and short-by-one publication, full-budget self-copy, shared Set and invalid Set, shared Append, empty/replacement publication, reset/deactivation without refunds, and malformed multi-store partial publication. Then rerun fresh compiler self-reproduction, the complete 272-literal control, all four bootstrap images, blocked-toolchain smoke, and actual row/Text accounting. Every production mutator and consumer must be migrated before sharing any generation.

## The compiler's blocker is not removed

Preserving eager admission cannot increase the set of programs admitted by the old logical row ceiling. It might save physical cell copies, but the full compiler's historical **65,481 logical rows and 55 spare rows** remain the relevant admission budget. These are parent measurements, not a fresh storage census or a measured saving in this increment. Adopting allocation-on-demand to increase admission headroom would instead be an intentional resource-behavior change requiring a separate explicit decision and failure contract. This model does not silently choose it.

There is therefore no justified production optimization in this increment. No owner is guessed dead, no buffer ceiling is increased, and no blocked semantic pass is integrated. Strict independence remains blocked by Python bootstrap seeding and Clang/LLVM assembly/linking. PR #107 and #108 remain individually unverified; descendant checks do not revise that history. Keep this PR and all ancestors draft/open/unmerged.

## Verification

The new model's focused run passes **10 tests in 1.91 seconds**. It enumerates **131,072 length-four traces** over a 16-operation alphabet at capacities two and three, starting with two single-cell collections. Those capacities are deliberately small; longer explicit witnesses cover three simultaneous aliases, shared two-cell append/detach, full-budget Set, logical rejection despite spare physical slots, invalid mutation, repeated debit, partial-copy terminal events and rejection of every post-terminal continuation. The physical counter is checked against all retained generation-list lengths, not just compared to another counter.

The inherited capacity, COW and production-root witnesses separately pass **39 tests in 5.32 seconds**. A fresh compiler self-reproduction and complete 272-literal initializer gate passes **1 test in 75.04 seconds**, with a separate fresh basetemp. These are successful regression gates for unchanged production, not evidence that the candidate resource policy has been implemented there.

The complete frozen production/test tree passes **2,428 tests, with 20 skipped, in 1,096.50 seconds**, using a fresh basetemp. Independent review approved the increment without blocking findings, independently reran the new tests (**10 passed in 1.94 seconds**) and inherited witnesses (**39 passed in 5.75 seconds**), and challenged the accounting using 200 seeded traces of up to 1,000 operations across varied initial states, name counts and limits. Python 3.10 grammar parsing passed; that review's execution used Python 3.12.3, not Python 3.10. Only this note's evidence was updated after those tests.

The final immutable-head PR receipt will record the focused tests, independent review, full-suite result, separate fresh self-reproduction/initializer gate, production-source identity, fresh four-image rebuild and blocked-toolchain smoke, and all eight exact-final-head CI checks. Pending gates are not successful verification. Only this engineering note and its new model test are intended changes relative to exact #114.
