# Scoped Text provenance for shared Action arguments

## What this increment admits

The native generator now accepts one deliberately small shared-scalar Text shape: a direct `BC_STORE_LIST` of a value already known as `T`, followed later in the same emitted Action by a load of that exact global slot as an argument to a formal explicitly declared `Text`.

The proof is transient and slot-identity-based. It resets at each Action entry. Only literal constants, Text constants, variable loads, and `BC_CALL_BEGIN` framing can leave it alive; `BC_CALL_BEGIN` does not execute the callee. Any other opcode clears it, including actual call completion, stores, mutations, control-flow boundaries, and unknown instructions. A Text write inside an If/Repeat/While does not create an eligible proof. Parameter/local lookup happens before the global-slot check, so a same-named Action parameter cannot borrow the global fact. Within that same Action, once any shared Text store is observed, a later shared-global read without the matching uninterrupted proof is rejected rather than guessed as Text. The fact is never established by caller expectations or persisted as a global Text kind.

At the read, the generator resolves the top call frame and the next argument position and confirms that the corresponding formal is explicitly `Text`. The stack value receives `T` only for that checked argument. Tests pin a non-first argument and a nested call frame. The return-kind prepass is not taught to infer shared Text: a direct shared-global return after a Text store in that same Action is rejected by the seen-store guard.

## Why the bounded case is safe

The native representation is one pointer-sized word, not an owned mutable buffer. Existing Text producers admitted to this path are immutable literals, typed Text parameters, and Text results whose current backing storage has process lifetime. Passing the pointer does not copy or mutate the string. The slot is written before it is loaded, and the proof cannot cross a completed Action call that might overwrite the slot. The native generator admits only direct synchronous Action calls in this path; unsupported closure/task/private calls remain rejected. No allocator, arena, capacity, failure, reclamation, or resource-bound behavior is added.

## What remains unsupported

This does not infer Text across Action boundaries, branches, loops, aliases without an explicit same-slot store, or unknown/mixed writes. A cross-Action read passed to a `Text` formal remains Integer-kind and is rejected by existing typed-call checking. However, other untyped cross-Action reads or returns may retain the pre-existing Integer-default behavior; this is a separate limitation and this bounded increment does not fix it. Do not treat the implementation as universal shared-global type safety.

It does not add dynamic Text concatenation, Text `BC_APPEND`, collection storage, or generic `NONE` inference. In particular, the full compiler artifact still encounters the independently verified `RecordDiag.Message: NONE` preparation gate; the parser's Action-local dynamic messages and diagnostic append remain separate blockers. This increment does not raise the 4,096 work bounds, claim the 9,118-token artifact fits the memory envelope, or remove Python-seeded image construction and external Clang/LLVM assembly/linking.

## Verification and review

Independent review approved the bounded implementation and requested the cross-Action qualification above; that correction is reflected here and in the independence index.

On the candidate above PR #134, the native codegen module passed **247 tests, 21 skipped**, and the full repository suite passed **2,744 tests, 23 skipped**. Focused provenance/indexing tests passed **34 tests**. Fresh x86-64 Linux compiler, runtime, bytecode-launcher, and codegen images rebuilt with `make PYTHON=python3 NATIVE_TARGET=x86_64-linux native-hosted-bootstrap`. The default `aarch64-macos` target is not linkable by this Linux runner's Clang, so the host-target rebuild is the applicable image gate.

The Python/toolchain-blocked native smoke passed, including stage-1 compilation and exact full compiler-bytecode reproduction. The restricted bootstrap audit passed its guardrails (9,119 artifact lines, 73 function markers, 294 call markers) and confirmed the full artifact still receives the expected normal codegen rejection (status 1, empty stdout/stderr, no partial assembly) at the `RecordDiag.Message: NONE` gate. The newly built tracked `dist/` files were restored after these checks.

These local gates prove only this scoped lowering contract and the existing baseline checks. The new draft PR's exact-head CI receipt must be verified separately; no merge is authorized.
