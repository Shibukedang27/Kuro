# Native metadata has a real reservation cost

## Why this proof comes next

This test/design increment starts directly above draft/open [PR #124](https://github.com/Shibukedang27/Kuro/pull/124), exact parent `a8dab8a3f73ddf12405f494378708549815c448c`. It leaves compiler, runtime, authored helpers, bootstrap, distribution images, wrappers, workflows, native resource ceilings and hosted semantics unchanged. It does not install a replacement ledger or authorize merging the stack.

The [row-funded descriptor proposal](vm-row-funded-metadata.md) adds three integer columns per retained name (head, tail and logical length) and one next-link column per retained historical row, while retaining current generation IDs and owner/raw/display columns. Its earlier 2,097,152-byte estimate counted only four full-capacity 64-bit payload buffers. The next useful proof is to ask the unchanged backend what it actually emits and links, rather than treating that arithmetic as a complete storage budget.

The [new tests](../../tests/self_host/test_vm_native_metadata_budget.py) are isolated allocation and boundary probes, not a collection implementation. Their arrays exercise the real compiler and backend; they do not replace VM helpers or change production admission.

## What is measured

**The current backend needs 4,194,336 extra zero-fill bytes for these four integer arrays, not just the 2,097,152 payload bytes previously estimated.** Each native integer collection gets a 524,288-byte value buffer, a separate 524,288-byte per-element Text-length sidecar, and an 8-byte logical-length cell. The sidecar is emitted for every collection, even these integer-only metadata columns. This is current backend behavior, not an intrinsic lower bound for a specialized metadata layout. Removing the sidecars would itself be a separate production compiler change requiring proof.

The portable emission control compiles the actual artifact-launcher source, then compiles that same source with four two-integer metadata declarations appended. It counts the emitted BSS directives, including alignment, and verifies four additional value buffers, four additional sidecars and four additional logical-length cells with no additional scalar-global cells. The VM's original helper source is untouched; these declarations are an allocation probe, not integrated descriptors or a new tail algorithm.

The linked Linux x86-64 control builds both full launcher images through the unchanged backend. A standard-library ELF64 parser independently reads section headers and load segments. The [measurement snapshot](vm-native-metadata-budget.json) records this sandbox's results:

| Linked-image quantity | Baseline | Four extra arrays | Increase |
| --- | ---: | ---: | ---: |
| BSS section / load-segment zero-fill bytes | 48,385,584 | 52,579,920 | 4,194,336 |
| Load-segment file-backed bytes | 96,492 | 96,860 | 368 |
| Load-segment memory bytes | 48,482,076 | 52,676,780 | 4,194,704 |
| Complete ELF file bytes | 104,432 | 104,432 | 0 |

Both BSS sections are `SHT_NOBITS`: zero-fill does not occupy equivalent bytes in the file. Equal final file sizes here reflect linker/file padding, not zero added executable code or zero memory cost. Absolute file and segment sizes can vary with the toolchain; the tests gate the structural reservation delta and BSS/zero-fill agreement, not these incidental absolute sizes. No Linux ELF result is claimed for Darwin, ARM execution or the authored code generator.

The native execution control dynamically fills one of the four probe arrays to the real 65,536-slot capacity. Reads of its first and last valid slots return `0` and `65535`. A separate one-past Set prints the pre-access `777` marker, exits with status 1 and never reaches the later marker or subsequent tail-array Set. This establishes ordinary backend bounds/fail-stop behavior for the isolated array, not VM multi-column failure equivalence or inspection of a partially published ledger. A small hosted control grows from one value to 65 values and reads the last value, without treating the native ceiling as a hosted ceiling. The four new checks run with `python -m pytest -q tests/self_host/test_vm_native_metadata_budget.py`.

## What this does not prove

An ELF zero-fill reservation is not resident-set size, physical memory commitment, a deployment limit, an allocation-failure equivalence proof or a speed measurement. Headers, segment/page alignment and executable code/data have different costs from array payload. The probes do not measure a complete tail implementation, tail traversal speed, compiler headroom or any reduction in historical rows.

The logical native row ceiling remains 65,536. Extra metadata columns do not create more logical admission credit, and an isolated array successfully reaching its last slot is not proof that all four arrays can be published transactionally. Native failure remains terminal; hosted storage must remain dynamically growing rather than inherit a native bound. No production storage, performance, capacity or independence gain is claimed.

The broader [history compatibility gate](vm-generation-history-compatibility.md) remains binding. The [public-dispatch row-funding argument](vm-generation-reachability-lifetimes.md) does not waive direct-helper histories, native counter behavior, historical owner collisions, hosted nonwrapping arithmetic or compatibility at partial publication boundaries. A descriptor indexed only by a name's current generation still needs to preserve all backend-observable historical aliases; an isolated integer column does not establish that.

## Next safe implementation gate

Retain production storage. An ID/history-preserving backend slice must still prove stable synchronous reader/index scopes; late name resolution; captured raw/display pairs; eager snapshots; scalar, result, frame and closure captures; negative Get offsets and Set's different indexing rule; reset/deactivation history; and exact sequential admission and partial-publication behavior. Tail/link writes need an explicit ordering and failure argument on the actual backend, including how retained owner aliases select historical rows. Moving Text requires its own complete root/relocation proof, not just stable integer links.

A full deployment budget must include real compiled metadata code and scalars, executable file and segment padding, the existing Text arena, retained names and rows, and host resource behavior. Preallocated columns have a cost even when the logical ledger is empty. A more compact or lazy layout needs a separate measured implementation and failure-compatibility proof; it cannot borrow these measurements as certification.

## Acceptance and limits

Acceptance requires the new and existing focused contracts, the complete suite, independent review of the frozen candidate, a fresh four-image rebuild, blocked-toolchain smoke, compiler self-reproduction/272-literal control, and all eight CI checks on the exact published head. Immutable results belong in the PR verification receipt, not in an ancestor's receipt.

Python bootstrap seeding and Clang/LLVM assembly/linking still block strict independence. PRs #107/#108 remain individually unverified. Keep this PR and the earlier stack draft/open/unmerged.
