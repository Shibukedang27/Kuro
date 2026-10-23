# Backend-aware admission before eager VM row publication

## The production step

This increment starts directly above draft/open [PR #116](https://github.com/Shibukedang27/Kuro/pull/116), exact parent `da63e63c18281c1bf0d48cd6682964bf71db3f5d`. That parent proved a native logical-debit experiment but deliberately did not install its out-of-range Set surrogate. The new private `__KuroAdmitRow` call makes the resource boundary explicit instead of disguising admission as collection access.

The implementation checks one row immediately before `VMAppendCollectionItem` writes its owner, raw value and display columns. It uses `VMCollectionEntryCount`, retains all eager copying and increments the counter only after the same three writes. There is no separate production reservation ledger, sharing, detachment, reclamation or increased ceiling.

## Private contract

`Call __KuroAdmitRow Used;` accepts exactly one nonnegative Integer and returns that Integer unchanged through the ordinary result-register protocol. The name is reserved against top-level Action declarations, private dispatch takes precedence over user functions, and it is not added to the public builtin/standard-library registry. It retains ordinary CALL encoding; neither the artifact version nor a bytecode opcode changes. The existing artifact-suffix intrinsic keeps its separate lowering.

Hosted interpreter and Python-bytecode execution validate the operand but impose **no native row ceiling**. Invalid runtime values must fail even when callers bypass source validation. Native lowering checks against the existing `NATIVE_COLLECTION_CAPACITY` of **65,536** and enters the existing terminal capacity-failure path, not a bounds-access surrogate. `Used = 65,535` admits the last row; `Used = 65,536` rejects the next. Admission itself allocates no collection row and does not increment the caller's counter.

Reference and authored semantic probes agree on top-level reserved-name diagnostics, call arity and the tested statically invalid or unknown operand types. The authored VM also handles the private CALL when executing compiler bytecode: successful calls preserve its stack/result protocol; wrong stack arity and the bounded malformed scalar cases in the tests are rejected. Its scalar kind zero does not preserve full Integer-versus-Text provenance, so these tests do not establish universal forged-bytecode type safety. The full authored semantic passes are still not wired into the production compiler driver; running those passes independently is not evidence that the driver acquired a complete semantic gate. This does not make the standalone authored native generator capable of compiling the complete runtime. Unsupported private calls in that constrained generator remain explicitly rejected rather than producing an unresolved or unsound native call.

The authored bytecode-call handler crosses its type-erased scalar transport through a small `VMAdmitRow Count: Integers` Action. Its explicit parameter ABI supplies the Integer kind required by native admission; the raw word and result are preserved. This does not restore erased provenance or relax native kind checks. The production eager append path still calls the intrinsic directly, so the bridge adds no per-row call to ordinary eager publication.

## What parity means here

The production helper only calls admission after resolving a valid destination owner. Missing names retain `VMFailed`; no row is admitted. Eager copy still admits one matching source row at a time through that helper. Self-copy still returns before source lookup; empty copy, reset, deactivation and Set do not debit or refund row history. The inherited real-capacity and publication-root tests remain the evidence for these paths and for malformed multi-store partial publication.

Native execution remains fail-stop. Direct source output can expose a prefix before termination; the authored VM buffers user output until successful completion, so a launcher failure need not expose the same stdout prefix. Neither observation establishes postmortem column contents or makes partial publication transactional. Hosted allocation failures are not converted into recoverable admission failures.

A separate scalar receipt may call the private operation repeatedly while retaining two actual rows. That proves the operation does not spend physical rows on reservations; it is **not production sharing** or a new VM allocation policy. Production logical and physical historical row counts still coincide.

## Verification record

The exact-parent witness run fails all **seven selected tests**: the parent has no private admission call or eager-helper preflight. The revised new module has **80 cases**, including complete ARM64 runtime/bytecode image emission with assertions on the bridge's signed and capacity guards. The revised focused gate, including the new module, ARM64 provenance/fallback tests and inherited real-capacity/publication-root probes, passes **138 tests in 18.51 seconds**. A separate fresh full compiler-bytecode reproduction and 272-literal initializer control passed **one test in 77.34 seconds** on the first head; fresh immutable-final-head gates remain mandatory. No raised capacity or reduced compiler source is used.

The first published head, `f0f44a1aad10446bc01ed20357958e612cbda6c7`, was **not verified**: despite 134 focused passes and bounded independent review, its full local suite ended **2 failed, 2,511 passed, 20 skipped** and macOS CI failed. ARM64 emitted a generic VMPop result as Text kind and rejected the declared Integer global at the private call. The source-only typed-parameter bridge fixes that transport mismatch without changing `compiler/native.py`, loosening ordinary numeric/collection provenance checks or extending native input parsing. Both initially failing production-image emission cases now pass. Prior green focused reviews do not certify the revised head; its independent review and exact-head CI receipt supersede them.

Full immutable-head suite, fresh four-image rebuild/blocked-toolchain smoke and all eight exact-final-head CI checks are acceptance gates recorded in the PR verification receipt. Until that receipt reports success, this increment is not CI-verified. Parent checks do not certify this change.

The operation has a valid-domain scalar-Integer contract, not a new proof of every frontend inference rule. Existing type/shape metadata can still erase distinctions: Integer collections are not scalars, inferred division need not return an Integer at runtime, and nested lifted declarations are not uniformly reserved by the historical semantic walkers. Python runtime validation rejects non-Integer objects, native lowering requires explicit Integer evidence plus its numeric kind, and private dispatch cannot be overridden by a same-name user Action. This increment does not repair those general frontend/type-provenance boundaries or infer Integer operands from their spelling. Native input parsing is byte-for-byte unchanged.

## Next path and limits

First keep this admission boundary independently reviewable with eager behavior unchanged. A later increment can introduce a separately reviewed logical ledger and stable generation bindings, then migrate every Get/Length/Print, Copy, Set, Append, reset, scalar-overwrite and multi-store path, including in-flight generation protection, before enabling sharing. Do not turn per-row failure into atomic bulk admission or infer rollback from process death.

No new storage census or headroom gain is claimed. The historical complete-compiler peak remains **65,481 rows, 55 spare**. Eager-compatible accounting alone cannot increase that logical success domain. Python-seeded construction and external Clang/LLVM assembly/linking remain strict-independence blockers; PR #107/#108 remain individually unverified. This increment and its ancestors remain draft/open/unmerged.
