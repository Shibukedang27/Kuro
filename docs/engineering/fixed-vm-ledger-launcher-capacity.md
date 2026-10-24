# Fixed VM-ledger headroom for the native artifact launcher

## What this change permits

This source-derived increment gives only the native bytecode artifact launcher a fixed **65,600-row** limit for its three VM ledger columns: `VMCollectionOwners`, `VMCollectionItems`, and `VMCollectionItemDisplay`. Ordinary native collections and ordinary `__KuroAdmitRow` calls remain fixed at **65,536**. There is no configurable backend ceiling and no general capacity increase.

The launcher profile is derived from the VM append helper's IR, not from a counter spelling or an Action name at each guard. It is accepted only when the helper still loads `VMCollectionEntryCount`, admits that exact callsite, appends the owner/raw/display columns in the reviewed order, and increments the count after those writes. A changed or aliased protocol fails the build closed. The one bounded profile supplies the same metadata to each of the three backing buffers, the x86-64 per-item text-length sidecars, every static initializer/append guard, and the ARM64 buffers and compare-immediate guards.

Only the public `self_host.build_native_artifact_launcher` wrapper selects this profile, and it compiles the canonical artifact-loader + VM + runtime source internally; callers cannot supply arbitrary IR or a capacity. Profile creation also compares the complete IR against a fresh compilation of that exact source, so a lookalike with the same helper/counter/columns is rejected. The profile is bound to the exact IR object that created it, and every internal builder/emitter entry rejects transfer to another IR object, even one with structurally equal contents. The ARM64 Action emitter derives capacities from that profile rather than accepting a separate capacity map. The generic native builder accepts IR but has no profile parameter, and the native module exposes no IR-taking launcher builder. Generic public builders and emitters therefore remain at 65,536 even when an unrelated program uses the same helper, counter, and column names.

## Why this narrow allowance exists

The exact PR #137 baseline reproduces its 9,118-token stage-2 artifact at 65,529 physical rows. The one-tail-return `IsWord` normalization is a source-derived reconstruction: it retains the `IsWord_V` scratch update, replaces early returns with a single final return, and emits **9,124 tokens**. A fresh stage-2 run reproduces the complete bytecode without truncation; its shared VM ledger count reaches **65,573 rows**, 37 above the ordinary limit and 27 below the fixed 65,600 ceiling. The VM append protocol writes all three columns before advancing that shared count. The missing discarded source diff/hash is not represented as recovered history: the reconstruction itself is the new intended and tested source change.

The static-storage delta is bounded: x86-64 adds 3,072 BSS bytes for three buffers and their three text-length sidecars; ARM64 adds 1,536 BSS bytes for its three buffers. The scratch measurement observed about 52–60 KiB additional high-water/private-dirty memory for the candidate workload; that result is workload evidence, not a universal memory ceiling or a reason to widen other backends.

## Publication and exhaustion behavior

Admission still happens before writes. The helper writes the owner, raw value, and display spelling in that order, then increments `VMCollectionEntryCount` last. The 65,600th row is readable from all three columns. A 65,601st append takes the existing terminal native overflow path before the next marker executes.

The three column writes are separate operations. If an unexpected failure occurs after one or two writes, the process fail-stops; the change does **not** make the columns transactional, add rollback, or claim an atomic failed append. No postmortem state after native termination is used as a correctness assertion.

## Verification and limits

The regression module checks seeded rows 0–2, the 65,600th row's numeric owner/raw/display reads, fail-stop at 65,601, a generic 65,536/65,537 control, same-name/action collisions, unsupported aliases and protocol-shape changes, cross-IR profile transfer rejection at every backend entry, public API rejection of arbitrary capacity values, exact static allocations, and ARM64 cross-assembly. Fresh x86-64 Linux images of the native compiler, runtime, ARM64-output code generator, and artifact launcher all rebuilt outside `dist/`. Under a restricted environment with no Python/toolchain on `PATH`, the compiler emitted 9,124 tokens and the artifact launcher reproduced both its own full bytecode and a 272-value initializer byte-for-byte. The fresh census reached 65,573 rows in the shared VM ledger. The x86-64 image has six 65,600-row buffers/sidecars and the matching three column guards plus one pre-write admission guard; generic 65,536 guards remain present. ARM64 emitted storage and compare guards cross-assembled successfully, but ARM64 runtime execution is not claimed.

The complete local suite passed (**2,761 passed, 23 skipped**); the focused launcher/parser/Stage-2 set passed (**98 passed**), and the previously failing closure-audit set passed (**74 passed**). A separate read-only review found no blocking findings. Tracked `dist/` outputs remain untouched. The eight exact-head GitHub checks have not run because this local candidate is unpushed; local tests are not represented as CI results.

Full stage-2 bytecode reproduction is a separate claim from native code generation. The native generator still does not lower the full compiler because Text-versus-Text `BC_CMP` and dynamic Text/`BC_APPEND` remain unsupported. This increment does not claim native compiler image generation, full native self-hosting, or a broader compiler/backend capacity increase. Python-seeded construction and the host assembler/linker remain separate independence gaps.

The local candidate is based directly on the current head of open/draft/unmerged PR #137 (`9d6887eaba68c3b4ea8485aeed475e5a7081af5e`). It has not been pushed and no follow-up PR has been created; the required eight exact-head checks therefore remain pending. No merge is authorized by this note.
