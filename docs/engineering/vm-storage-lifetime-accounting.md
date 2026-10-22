# Account for VM storage before changing compiler semantics

## Decision: measure first; do not replace copies with aliases

This increment is stacked directly above [PR #110](https://github.com/Shibukedang27/Kuro/pull/110), exact parent `0b2a3fdfc1ffcafff519f69265ab85d30eee9d52`. It retains **no production compaction, reference reuse, semantic integration, or capacity increase**. The immediate prerequisite is an explicit collection ownership/publication model, not an assumption that compiler intermediates or old strings are dead. The [reconciliation](semantic-bootstrap-reconciliation.md) records why the rejected Text/Decimal Repeat check cannot advance on only 55 spare aggregate rows.

The new [accounting command](../../scripts/account_vm_storage.py) builds the unchanged production-composed Linux launcher, exposes assembler-local symbols by a reversible spelling substitution, and reads its final storage using GDB. It changes no instruction, data, VM operation, or ceiling. Its census is allocation/retention evidence, **not a garbage-collection root proof or an ARM64 runtime measurement**.

## Where the 65,481 rows go

The complete-self census resolves every row to a currently named owner:

| Interpreted owner | Retained rows |
| --- | ---: |
| `TokenKinds` | 8,771 |
| `TokenStarts` | 8,771 |
| `TokenValues` | 8,771 |
| `AstOut` | 11,654 |
| `LCNames` / `LCTypes` | 61 each |
| `LCFrameAction` / `LCFrameRepeat` | 19 each |
| `IROut` | 9,118 |
| `BytecodeOut` | 9,118 |
| `CompilerOutput` | 9,118 |
| **Total / unnamed rows** | **65,481 / 0** |

There is therefore **no stale-owner row saving available in this complete-self run**. This is a stronger and narrower observation than the general fact that reset can leave obsolete generations. Named token/AST/IR arrays might be dead to a particular later compiler phase, but that needs a separate observability/ownership proof.

| Complete-self peak retained allocation | #110 measured baseline | This unchanged production tree |
| --- | ---: | ---: |
| Rows in **each** ledger column | 65,481 | 65,481 |
| Spare rows under 65,536 | 55 | 55 |
| Character cursor / 2 MiB capacity | 870,724 bytes | 870,724 bytes |
| Text-join cursor / 16 MiB capacity | 2,192,152 bytes | 2,192,152 bytes |

The three columns together contain 1,571,544 bytes of occupied 8-byte cells at that peak. This excludes the emitter's reserved buffers, auxiliary metadata and arenas; it is **not RSS**. No reduction is claimed. The exact 272-literal compiler control retains 4,189 rows, with character cursor 347,354 and text-join cursor 1,188,633 bytes, also with zero unnamed rows. Its interpreted token columns contain 555 rows each, AST 837, Length name/type columns two each, and IR/bytecode/output 561 each; it has no frame-owner rows.

The [machine-readable receipts](vm-storage-census.json) bind source, assembly, diagnostic image, snapshotted input and output hashes. Success requires the explicit normal-epilogue breakpoint, zero VM/runtime/inferior failure status, empty stderr, synchronized column lengths and a complete owner histogram. A generic overflow-handler stop is not accepted as a successful census or a diagnosis of a particular capacity. The ordinary fresh-parent launcher assembly and the script's original assembly match byte-for-byte, and both ordinary and symbolized runs reproduce the same output bytes. Symbol metadata itself is not claimed byte-identical.

## What owns storage

There are two different collection layers. The native emitter reserves a fixed 65,536-cell buffer for each authored collection. Inside the authored VM, all *interpreted* collection owners share the three parallel native collections `VMCollectionOwners`, `VMCollectionItems`, and `VMCollectionItemDisplay` ([VM declarations](../../self_host/vm.kuro)). A VM append adds one row to each column. The 65,536 limit is consequently a shared logical row limit for these interpreted owners, not a process-wide count of every native buffer or a resident-memory measurement.

`VMCollectionEntryCount` starts at zero and only increases in `VMAppendCollectionItem`. Neither reset nor deactivation reduces it. Thus, on a normally completed run, the final row count is also its peak retained row count. Native character and text-join cursors are likewise monotonic in the unchanged launcher; their final positions measure cumulative arena consumption, not the number of live strings.

| Operation | Ownership and lifetime consequence |
| --- | --- |
| `VMResetCollection` | Assigns a fresh monotonically increasing owner ID; old rows remain allocated. |
| `VMDeactivateCollection` | Sets a name's current ID to -1; it does not reclaim rows or Text bytes. |
| `VMAppendCollectionItem` | Stores owner, raw value and display in lockstep, then increments the shared row count. |
| `VMGetCollectionItem` / `VMSetCollectionItem` | Scan rows of the current owner ID; order within an owner determines indexing. |
| `VMCopyCollection` | Resets the destination to a distinct owner and copies values **and display spellings** row by row. Self-copy is a no-op. |
| `VMPushCollection` | Carries a collection **name** with a kind marker, not a reference-counted generation handle. |

These rules are visible in [VM ownership/copy actions](../../self_host/vm.kuro), especially `VMMarkCollection` through `VMCopyCollection`. A collection assignment is a snapshot of its cells, not a mutable alias. Changing the destination must not mutate the source; resetting the source must not destroy the destination. Copying cells does not deep-copy the immutable Text bytes they point to.

## Decoding, validation and self-reproduction retain different things

The [artifact loader](../../self_host/artifact_loader.kuro) retains the complete input buffer, decodes framed tokens into its outer `BytecodeOut`, and exposes program input through `__KuroArtifactSuffix`. The native suffix implementation copies the suffix into the text-join arena; it is not an ownership transfer of the input buffer. Decoded token strings are accumulated from character extractions and immutable joins, so earlier allocations remain in their monotonic arenas.

`VMDecodeConstant` returns numeric values or the original malformed Text; Decimal display retains original spelling. The one-character optimization already in the parent reuses a valid input Text, without introducing any reclaimable lifetime boundary. Empty input inherits the existing numeric flag, repeated dots retain the inherited acceptance, and native UTF-8 length is byte-based. The existing [decoder parity tests](../../tests/self_host/test_vm_decode_allocation.py) pin those behaviors; none is corrected or broadened here.

During bytecode-stage compiler self-reproduction, interpreted `TokenKinds`, `TokenValues`, `TokenStarts`, `AstOut`, Length-checker metadata, `IROut`, `BytecodeOut`, and `CompilerOutput` live in the shared ledger. They are distinct from the outer launcher's bytecode and output collections. The [encoder](../../self_host/bytecode.kuro) copies operands from `IROut` and constructs opcode Text. The [compiler publication](../../self_host/compiler.kuro) then executes `CompilerOutput = BytecodeOut`, which the VM implements as another owner/cell copy. The runtime's outer `RuntimeOutput = VMOutput` is a separate native collection copy; it does not account for another interpreted compiler owner in the shared ledger.

## Why no compaction is retained

An owner census tells us which IDs remain named, not when a named intermediate becomes semantically unobservable. Even a currently unnamed owner does not prove its Text allocations can be reclaimed: the same bytes may remain referenced by another owner's cell, a scalar, decimal display, operand stack, result slot, frame, or saved native temporary. Collection row compaction and arena/string reclamation are separate problems.

A blanket alias substitution for `CompilerOutput = BytecodeOut` breaks the existing copy contract when either name is subsequently changed. Reclaiming token/AST/IR arrays based only on the current pipeline order assumes no later diagnostics, inspection, nested action or consumer can observe them. Neither proof is supplied by this increment, so neither optimization is shipped.

The narrowest next candidate is **publication-specific copy elision with an explicit contract**, not general assignment aliasing. Before implementation, specify and prove:

1. Whether publication produces an immutable snapshot, transfers unique ownership, or creates a shared copy-on-write object. Preserve the existing public `CompilerOutput` value, failure gates and bytecode framing; do not merely remove its assignment.
2. The complete root set: name-to-generation bindings, stack collection-name markers, values/displays, frame slots, return/result slots, action parameters/captures and any native temporaries that survive a call. State how reset, self-copy, overwrite, append and deactivation interact with those roots.
3. For shared storage, detach on every mutating path and preserve per-owner indexing, original cell/display pairs, bounds failures and malformed artifact/compiler behavior. For moving storage, update every root or use stable handles. Raw Text pointers currently have no moving-GC relocation protocol.
4. For row-only compaction, retain rows in stable per-owner order and keep all three columns synchronized. Prove no captured scan index or in-progress copy can be invalidated. Do not infer Text death from row death or rewind either arena.
5. Demonstrate exact-parent output bytes, artifacts, flags and errors across repeated decode/copy/reset, actions and malformed input; then measure positive headroom on full compiler self-reproduction and the exact 272-literal control under unchanged limits.

Eliminating one 9,118-cell publication copy would *arithmetically* reduce 65,481 rows to 56,363 and yield 9,173 spare rows. This is a **counterfactual budget, not a measured optimization or permission to integrate semantics**. No before/after reduction is claimed for this unchanged production tree.

## Verification record

Completed local gates on the retained production-identical tree:

- **Fresh full compiler self-reproduction and exact 272-literal control:** the unchanged reproduction test passed both cases, **1 passed in 76.98s**. It freshly built the native compiler and launcher; there is no truncated compiler or reduced initializer.
- **Fresh four-image bootstrap:** in a separate detached exact-parent checkout, removed the compiler, runtime, bytecode launcher and generator executables, then rebuilt all four with `make native-hosted-bootstrap`. Current production/compiler/bootstrap sources are byte-identical to that checkout.
- **Python/toolchain-blocked smoke:** passed on those fresh images, including the complete 9,118-value compiler self-reproduction, stage-zero/stage-one probe comparison, known non-Text Length rejection and Text acceptance.
- **New lifetime contracts:** [four tests](../../tests/self_host/test_vm_storage_lifetime.py), **4 passed in 1.72s**, compare repeated decoding against an embedded, SHA-pinned decoder from exact #110 (only its terminal source newline is omitted; statements are unchanged). Hosted/native checks retain malformed Text and Decimal spelling across later decodes, compare final flags and unchanged original framed input, and pin complete native `(exit, stdout bytes, stderr)`. The copy witnesses preserve destination cells/display and a stacked destination-name reference across source mutation, reset and deactivation. They characterize the existing contract; they are not evidence that a proposed collector is safe. Native execution is Linux x86-64 only.
- **Final accounting script:** both self and 272-control runs reach the explicit normal epilogue, pass all ledger invariants and exit/status checks, have empty stderr and match the ordinary fresh reproduction output bytes. The committed JSON contains their exact receipts.

The full fresh suite is run with a new `--basetemp` and frozen production/test sources. Independent review, its disposition, the final whole-suite result, the immutable final documentation-updated head and the two workflow receipts are published in this PR's verification comment after completion. Acceptance requires **eight successful checks on that exact head**, spanning push and pull-request macOS Python 3.10/3.11/3.12 and Linux workflows. Pending gates, local results and ancestor checks alone are not verification; do not change the tree after the receipt without revalidating its new head.

Reproduce the bounded accounting after the fresh reproduction test has produced its framed inputs (choose new output directories):

```sh
.venv/bin/python -m pytest -q \
  tests/self_host/test_native_integer_storage_capacity.py::test_fresh_bytecode_stage_compiler_reproduces_self_and_large_initializer \
  --basetemp=/absolute/fresh/reproduction
python scripts/account_vm_storage.py \
  /absolute/fresh/reproduction/test_fresh_bytecode_stage_comp0/self-stage-input.kurobc \
  /absolute/fresh/self-census
python scripts/account_vm_storage.py \
  /absolute/fresh/reproduction/test_fresh_bytecode_stage_comp0/initializer-stage-input.kurobc \
  /absolute/fresh/initializer-census
```

The accounting command requires Linux x86-64, Python, Clang and GDB as development instrumentation; it is not part of the blocked-toolchain production route. It snapshots input before execution, disables ambient GDB initialization/auto-loading, and fails closed on an overflow stop or inconsistent ledger. It executes the supplied bytecode workload: use trusted local test inputs. Its symbol-only assembly round-trip and original assembly identity do not assert byte identity of debug symbols or diagnostic images.

This PR and its ancestors remain open/unmerged. #107/#108 remain draft/unverified at their unchanged heads; descendant green checks do not retrospectively verify them.

Strict independence remains unfinished: **Python seeds the images; Clang/LLVM assemble and link them.** Running the seeded images with those tools blocked demonstrates execution continuity, not clean-checkout independent construction.
