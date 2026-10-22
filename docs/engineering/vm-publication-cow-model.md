# Publication snapshots need more than shared owner IDs

## Decision: retain production copies

This increment stacks directly on [PR #111](https://github.com/Shibukedang27/Kuro/pull/111), exact parent `39e33043a33c331b69e74b805aeac1f5fd3561b1`. It adds a **test-only stable-generation/copy-on-write model and production-VM adversarial witnesses**. No production collection representation, assignment semantics, storage limit, assembler, or runtime instruction changes. No row or Text reclamation is implemented.

The central distinction is observable: **assignment copies a snapshot, but a collection marker on the operand stack is a late-bound name**. Replacing both with a shared mutable owner breaks assignment isolation; replacing both with a frozen handle changes stack behavior. A failed multi-store can also leave a partially published destination. A model that silently improves failures into transactions is not equivalent to this VM.

The current [allocation census](vm-storage-lifetime-accounting.md) remains the baseline, not permission to compact. Strict independence is still unfinished: Python seeds production images and Clang/LLVM assemble and link them.

## What the candidate means

The [executable model](../../tests/self_host/test_vm_publication_cow_model.py) is deliberately separate from production. A cell consists of an immutable raw value and its immutable original display spelling. A name maps to a stable, never-reused generation ID; a generation contains an ordered sequence of cells. Distinct names may share one generation after assignment. The model neither moves cells nor rewinds Text arenas nor collects unbound generations.

The abstract operation contract is:

| Operation | Required effect |
| --- | --- |
| Assign `B = A` | Bind B to A's current contents, with snapshot isolation on future writes. Resolve source before replacing destination. |
| Self-assign | No-op, including no destination reset. |
| Set or append | If another name shares the generation, allocate an ordered copy of every value/display pair before mutating; otherwise mutate the unique sequence. |
| Reset | Bind only the selected name to a fresh empty generation; preserve every other binding. |
| Deactivate / scalar overwrite | Remove the collection binding for that name; do not destroy another name's snapshot. |
| Push collection | Save a **name**, not its current generation. Resolve that name when consumed. |
| Read a cell into a scalar/result | Retain its raw value and display independently of later collection writes or reset. |

For this sequential, flat-cell model, the refinement invariant is: for every active name, the ordered cell sequence equals that in an independent eager-copy oracle; saved cell values/displays and late-resolved stack observations agree. Assignment preserves the invariant by binding to an equal sequence. A write preserves it by separating the writer from all other bindings before modification. Reset/deactivation alter only the selected binding; stack markers retain name lookup. Induction over these abstract transitions establishes the invariant **only inside this model's operation domain**. Bounded exhaustive traces are executable checks of that implementation, not a proof that production bytecode refines the model.

Monotonic allocation accounting is distinct from live-length summation: a detach allocates copied rows, and unreachable generations remain allocated. Synthetic model savings, if recorded by its test, are not measured VM savings, native memory savings, or permission to change production failure behavior.

## Existing runtime observations a replacement must preserve

The [concrete production-VM witnesses](../../tests/self_host/test_vm_publication_roots.py) run unchanged launcher source through both the hosted interpreter and fresh Linux x86-64 native images. They pin complete stdout, native exit status and empty stderr, not merely successful values:

- Push A, copy A into B, reset A, then consume the earlier marker: the marker sees **new A**, while B retains the original cells and Decimal spelling.
- Copy A to B to C, self-copy B, then Set and Append to B and replace A with a scalar: C remains unchanged; B has independent order and original display cells.
- Read a Decimal cell, pass it into an Action, mutate its source collection, and return it: the frame, returned value and caller result slot retain `001.50`.
- Push A, overwrite A with a scalar, then print the earlier collection marker: collection resolution fails. The old generation is not revived; runtime failure and native exit status are one.
- A multi-store containing a scalar followed by a collection marker resets B and appends its first cell before failing on the marker. B contains the partial cell even though normal RuntimeOutput is suppressed. A transactional model does **not** cover this behavior.
- Pass collection A to an Action's differently named parameter and return it: the collection kind is erased, so the result is scalar Text `A`, not A's cells.
- Give an Action a scalar parameter named A while a global collection A exists: `BC_LOADVAR A` selects the global collection before checking the scalar frame. A new handle representation must not silently repair this lookup precedence.

These characterize the existing contract, including its awkward edges. They do not add language capabilities or change failures. The model excludes capacity exhaustion, partial bytecode failure, nested/reentrant calls, native temporary roots, closure/task objects, and Text allocation. Its synthetic abstract error handling is not a replacement specification for production VMFailed/RuntimeExitCode.

## Root and consumer boundary

The ledger is shared only by interpreted collections. Native collections in the composed launcher, including its outer BytecodeOut, are a separate storage layer. The VM's name/ID bindings and row scans are in [vm.kuro](../../self_host/vm.kuro); [compiler.kuro](../../self_host/compiler.kuro) publishes interpreted `CompilerOutput = BytecodeOut`, while [runtime.kuro](../../self_host/runtime.kuro) separately copies outer `VMOutput` into native `RuntimeOutput`. Removing either publication without auditing its consumers would conflate those layers.

The independent source audit covers the following roots and transfers. Line ranges refer to the unchanged exact-parent files, not hypothetical implementation sites.

| Root or consumer | Existing representation / consequence |
| --- | --- |
| Active name bindings | `vm.kuro:27–40,157–217`: current name/ID table plus append-only owner/value/display ledger. Reset gives a fresh ID; deactivation writes -1. Bindings are the model's only generation-sharing owners; no reclamation follows from that restricted model. |
| Operand and multi-store staging | `374–414,971–974,1104–1129`: live prefix below VMTop carries value/kind/display; popped backing slots are not cleared. Kind-1 payloads are names. Multi-store rejects kind-1 cells after any earlier scalar publication. A future tracer must distinguish logical live slots from stale backing cells. |
| Copy and scan temporaries | `241–361,1405–1428`: Get/Set/Length/copy/print retain owner IDs, logical indices, physical row positions, values and displays across helper calls. Copy holds source ID while resetting destination and scans a ledger whose count grows. No moving/reclaiming operation is safe merely because a binding changed. |
| Scalar environment and frame entries | `416–536,772–847`: values/displays outlive collection mutation; frame ranges and VMFrameEntryCount define live slots. VMInvoke discards argument kind when publishing parameters. Scalar frame stores do not deactivate same-spelled global collections. |
| Result, return and caller publication | `363–372,784–800,833–844,1033–1039,1057–1087,1309–1339`: `_`, per-depth frame return slots and VMReturnValue preserve raw value/display, not a collection kind. Collection handle returns are not encoded. Collection lookup precedes ordinary frame lookup in BC_LOADVAR. |
| Output | `1405–1428` plus `runtime.kuro:15–28`: print resolves collection names now and appends each value/display to outer VMOutput/VMOutputDisplay; RuntimeOutput subsequently copies that native buffer. Output cells remain Text roots independently of their input collection. |
| Input and decoded artifacts | `artifact_loader.kuro:11–95,141–247`: full ArtifactSource, decoded outer BytecodeOut and suffix input remain distinct roots. Validation checks structure and arity of opcode operands, not stack kinds, collection lifetimes or atomicity. Suffix copying allocates Text; it does not transfer ownership of the source. |
| Authored captures | The loader's opcode list (`154–167`) and VM call path (`735–847,1019–1039`) admit static named Actions, not MakeClosure/Invoke/capture opcodes. There is no authored collection capture root to enumerate today. Supporting one would expand the representation and proof, not complete an existing hidden transfer. |
| Hosted captures and tasks | [interpreter.py](../../compiler/interpreter.py):131–165 and [bytecode.py](../../compiler/bytecode.py):133–173 snapshot environment/frame mappings shallowly; captured lists remain reference objects. BytecodeVM's end-of-main collector roots env, frames and scheduler tasks. These are not authored VM eager-copy semantics or evidence of per-instruction temporary rooting. |
| Native buffers, temporaries and captures | [native.py](../../compiler/native.py):37–93,1205–1255,1979–1999,2143–2155,3950–4035,4463–4469: direct collections have static buffers/length metadata; temporaries and Action locals use stack-frame slots. Provenance rejection is not a dynamic owner protocol. Collection operations through unknown aliases/parameters/captures are conservatively rejected or lack length metadata; scalar closure capture slots are not a collection COW heap. |

This is a source-level inventory and a boundary for a future proof, **not a verified complete tracing/root implementation**. A name marker is not a generation root, while its Text spelling and any scalar/display pointers still matter for Text lifetime. If a future implementation caches a generation inside an in-flight operation, that temporary needs an explicit pin until the operation ends. A current-name census does not cover those pins, dead backing slots, captured heaps or native stack registers.

## Why production promotion is blocked

1. **Failure refinement:** preserve malformed artifact validation, sticky failure state, native exit/stderr, partial stores and old rows. The candidate's transactional abstract errors and unbounded allocation cannot establish compatibility at the 65,536-row boundary. Deferring a copy also changes *when* capacity can fail; that needs an explicit, separately reviewed contract rather than an accidental semantic change.
2. **Representation refinement:** all collection accesses must dereference name-to-generation bindings consistently. Row owner IDs currently imply distinct copy generations; simply giving two names one ID does not install write barriers. Every Set, Append, reset, multi-store, scalar overwrite and assignment path needs a reviewed transition, including partial failures.
3. **In-flight lifetime:** current copy/get/set/length/print scans retain owner IDs, row positions, raw values and display pointers across authored helper calls. Preserve them through detach, or prove a safepoint/no-reentry discipline. Do not compact rows under an active scan.
4. **Cross-runtime scope:** native collection buffers, authored VM names, hosted environment/frames and captured heaps do not share one ownership contract. Native closure captures and scheduler/task roots require their own target-specific proof. Do not infer support from a Python model or a successful Action scalar test.
5. **Text lifetime:** values/displays can survive in scalar environments, stack slots, frames, results, returns, output, input/artifact buffers and native temporaries. Retaining immutable pointers is allowed; moving or reclaiming their bytes is not proved. No Text allocator change belongs to this prototype.
6. **Actual benefit:** after those obligations, compare exact-parent output and failures, full compiler self-reproduction and the complete 272-literal control under unchanged limits. Measure actual monotonic retained peak and metadata costs. Do not report the arithmetic removal of a 9,118-cell copy as a measured optimization.

Until those obligations are discharged, keep production copies and the evidence that current-owner compaction is insufficient. Do not integrate blocked semantic passes, increase ceilings or claim a completed independent toolchain.

## Measured production peak: no reduction

The [fresh machine-readable receipts](vm-publication-cow-census.json) bind the unchanged source, snapshotted inputs, ordinary/symbolized assembly, diagnostic image and stdout hashes. Both runs reach the explicit normal epilogue with VM/runtime/inferior statuses zero, empty stderr, synchronized columns and complete owner accounting. Their stdout matches ordinary fresh reproduction byte-for-byte. Ordinary launcher assembly matches the separate four-image bootstrap checkout byte-for-byte; all 71 tracked production/compiler/bootstrap/wrapper/Makefile files compared are identical to exact #111 and that checkout.

| Monotonic retained allocation | Full compiler reproduction | Complete 272-literal control |
| --- | ---: | ---: |
| Rows per ledger column | 65,481 | 4,189 |
| Character cursor bytes | 870,724 | 347,354 |
| Text-join cursor bytes | 2,192,152 | 1,188,633 |
| Rows with no currently named owner | 0 | 0 |

These equal #111's measurements. The full run still has only **55 spare rows**. Row count and arena cursors only increase in this production implementation, so successful final retained positions are their peaks. This is not RSS, a live-Text count, or an ARM64 measurement. Interpreted BytecodeOut and CompilerOutput still retain 9,118 cells each. The experiment has **not** reduced actual peak storage; current-owner reclamation has zero unnamed rows to reclaim in this workload.

The focused gate passes **23 tests**: nine model tests plus seven concrete programs run hosted and native. The model exhausts all **52,060 traces of length zero through three over a 37-operation alphabet**, with separate longer copy/mutation/reset/marker witnesses and exact synthetic allocation assertions. Shared transition dispatch and bounded coverage limit independence of the oracle: these are representation checks, not a formal or whole-VM equivalence proof. Fresh full compiler reproduction and the complete initializer control pass in **75.06 seconds**. The separate checkout removed all four old images before rebuilding; its blocked-toolchain smoke reproduces all 9,118 compiler values and passes stage-zero/stage-one probe and known Length rejection/acceptance checks.

## Verification contract

Run the new model and concrete witnesses, the full suite with a new basetemp, separate fresh full compiler reproduction plus 272-literal control, a four-image bootstrap with all old images removed, Python/toolchain-blocked smoke, and fresh self/control storage accounting. The source-identical detached bootstrap checkout and assembly/output hashes bind those runs to the retained production tree. Independent review and all eight CI checks must be successful on the final documentation-updated commit; pending or ancestor checks do not count.

The final PR verification comment records the immutable head, exact local results, source identity, accounting receipts, independent-review disposition and push/PR workflow URLs without creating another documentation commit. This PR and its ancestors must remain open/unmerged. Earlier unverified ancestor heads are not retroactively verified by this increment.
