# Publication at the real collection-row limit

## What this increment establishes

This test-only increment stacks on open, unmerged [PR #113](https://github.com/Shibukedang27/Kuro/pull/113), exact parent `0e7519cade61e092767baf641de2664f3bace95c`. It makes the current Linux x86-64 publication capacity boundary executable before any production snapshot sharing or detach implementation. **Production source, eager copies, storage limits and failure handling are unchanged.** This is a prerequisite characterization, not a row-saving implementation or a completed capacity-aware COW contract.

The [new probes](../../tests/self_host/test_vm_publication_capacity.py) execute the complete, unchanged authored VM and call its actual collection helpers. They do not replace helpers, shrink the native limit, patch emitted assembly, or model exhaustion with a Python exception. The standalone demo remains present and allocates no interpreted collection rows. A freshly built native image receives one exact mode string per process, without a newline: native `Take user` retains every stdin byte.

## The current boundary is native fail-stop

All three interpreted row columns are ordinary native fixed-capacity buffers, each limited to 65,536 entries. Their first two slots are seeds reused by the first two logical rows. `VMCollectionEntryCount` measures append-only allocation, not the sum of active collection lengths. Reset and deactivation do not reclaim old rows. The capacity is aggregate across interpreted owners, not a separate 65,536 allowance per interpreted name.

The probe starts with two Source cells, including raw value `raw-one` and independent display spelling `001.50`, then fills a second interpreted owner. The mode selects the operation and the remaining physical capacity. Exact stdout, exit status and empty stderr are asserted:

| Operation | Rows before | Current Linux x86-64 outcome |
| --- | ---: | --- |
| Copy two Source cells to Published | 65,534 | Succeeds at exactly 65,536; Published length is two and its first raw value/display is retained. The second cell's content is not separately read by this probe. |
| Copy the same two cells | 65,535 | Process exits 1 after the pre-operation checkpoint; no normal completion output. |
| Copy the same two cells | 65,536 | Same fail-stop boundary. |
| Self-copy Source | 65,536 | Succeeds without allocating or resetting Source. |
| Set Source's first cell | 65,536 | Succeeds without allocating rows; raw value and display both change. |
| Reset Source, then append | 65,536 | Reset succeeds and Source length is zero; the append exits 1. |
| Deactivate Source, then append to Filler | 65,536 | Name lookup reports -1; the append still exits 1. |
| Copy an empty collection over Source | 65,536 | Succeeds without allocating rows; Source becomes empty. |

On completed native probes, the logical row count and both measurable Text-column lengths agree. The Integer owner column cannot be measured using source `Length` under the existing Text-only contract; this test does not broaden that contract. Small hosted controls additionally inspect all three actual backing-list lengths through the interpreter environment.

The failure path matters: [VMAppendCollectionItem](../../self_host/vm.kuro) has no authored row-limit guard. Native `Append` branches to the emitter's process-exit overflow label. This is **not** evidence of `VMFailed = 1`, `RuntimeExitCode = 1`, a recoverable VM exception, or a normal runtime epilogue at row exhaustion. The process status is the observed failure contract. No statement following the overflowing append runs.

A failed copy with one spare row is expected from source order to append a prefix, because [VMCopyCollection](../../self_host/vm.kuro) resets its destination and appends one row at a time. These tests deliberately **do not inspect memory after process death** and do not claim an exact failed destination snapshot, synchronized failure-state columns, rollback, or atomicity. Existing [malformed multi-store witnesses](vm-publication-cow-model.md#existing-runtime-observations-a-replacement-must-preserve) cover a different, authored-VM failure path with observable partial publication; that evidence is not substituted for native exhaustion.

## Hosted behavior is not a reduced-limit oracle

Eight portable controls exercise the same operation branches with a small ledger. They check logical transitions, retained raw/display values, row accounting and all three backing-list lengths. They intentionally continue beyond their small starting allocation: the hosted interpreter uses Python lists, not native 65,536-entry buffers. These runs are neither exhaustion tests nor proof that resource failures match across runtimes. Native executable probes are skipped outside Linux x86-64; no Darwin or ARM64 execution claim follows.

These are helper-boundary probes. Existing production-root tests separately exercise artifact framing, bytecode dispatch, snapshot isolation, late-bound stack names, frames and results. Neither suite alone proves whole-VM representation refinement, arbitrary reentry safety, Text lifetime or capacity-aware detachment.

## Compatibility decision for the next implementation

Keep eager publication and native fail-stop behavior in production until a separately reviewed implementation defines its new resource policy. A shared snapshot cannot be called a behavior-preserving replacement merely because ordinary values agree. With one spare row, current eager publication stops immediately; sharing can instead let subsequent instructions run, and a later write can fail during detachment.

There are two explicit choices, neither implemented here:

1. Preserve eager admission timing using a separate logical reservation/debit budget, including replacement and self-copy rules. Physical rows may be saved, but the existing logical limit would still reject the same publication; this alone does not create semantic-admission headroom.
2. Deliberately adopt allocation-on-demand admission: publication can share, and mutation may fail later while separating a snapshot. This requires a defined failure boundary, destination state on an unsuccessful detach, helper-scan rooting, every mutator's write barrier, and new real-limit witnesses. It is an intentional resource-behavior change, not exhaustion parity.

Do not silently select the second policy in an optimization PR or describe the first as increasing the admissible program budget. An authored pre-append guard would also change observable native exhaustion from immediate process exit to sticky VM failure; such a guard needs its own reviewed propagation and partial-publication tests, plus full self-reproduction under the existing limits. This increment adds no guard and does not assume the current 55 spare rows can absorb one.

## Verification and remaining blockers

The focused run passes **16 tests**: eight small hosted transitions and eight fresh native real-capacity probes. Independent review approved this bounded characterization and independently reran all 16 tests. Its only low-priority suggestion was to assert the second copied cell or narrow the table wording; the table now states the exact first-cell/length coverage without implying the extra content assertion.

The frozen production/test tree passes the **complete suite: 2,418 passed, 20 skipped in 1,030.33 seconds**, using a fresh basetemp. A separate fresh full compiler self-reproduction and complete 272-literal initializer passes **1 test in 75.57 seconds**. Only this note's evidence and wording changed afterward. The final verification receipt will identify the immutable head, exact-head review, separate four-image bootstrap/blocked smoke and final-head CI results; pending gates are not approval.

Only this test module and this engineering note are intended changes. Production compiler/runtime, bootstrap, wrapper, native emitter and Makefile files must match the exact parent byte-for-byte. Because production is unchanged, the previous 65,481-row full-self census and its **55 spare rows** remain historical parent evidence, not a new measured optimization. No fresh allocation-reduction claim is made.

The existing full-suite self-reproduction and complete 272-literal control remain regression gates. Linux CI separately builds the four hosted-seeded production images and executes the Python/toolchain-blocked smoke test. Final-head CI must finish before this increment is called verified. Earlier unverified PR #107 and #108 heads remain unverified drafts; descendant test results do not rewrite their histories.

Strict independence remains blocked by Python seeding and Clang/LLVM assembly/linking. Snapshot sharing, safe detach, row/Text reclamation and blocked semantic integration remain unimplemented. Keep this PR and its ancestors open and unmerged.
