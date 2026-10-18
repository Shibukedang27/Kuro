# First Decimal initialization in both branch arms

This increment is stacked on [PR #67](https://github.com/Shibukedang27/Kuro/pull/67), whose checkout and remote head were verified as `eab3eae360aea5e38f6b1f652db38a9c3df49fb9`, open and unmerged, based on `feat/native-decimal-global-storage`. All eight checks on that base head succeeded. This is a bounded Kuro-authored native-generator improvement, not completion of toolchain independence.

## What changed and why

A previously untouched named slot may first acquire a Decimal representation when **both explicit arms of a top-level, function-free `If/Else` initialize it as Decimal**. Each arm can then load and mutate that slot after its own initialization, and subsequent statements, branches, and loops reuse the joined Decimal kind. Both taken and untaken branch outcomes are tested.

The generator snapshots the kinds of its preregistered global slots at eligible `If` entry. At `Else`, it saves the first arm's kinds and restores the entry snapshot before emitting the second arm. At `Done`, it compares the arms for slots that were untouched on entry. A new Decimal kind is accepted only when both arms establish Decimal; Decimal/Integer and Decimal/Text mismatches reject regardless of arm order. Newly established, conflicting non-Decimal kinds also reject at this join. This avoids mistaking the last emitted arm for the arm that executes.

The entry and first-arm snapshots use two existing-style global Text collections, indexed like the global-kind collection, not Text-character indexing or arrays of snapshot strings. Only one eligible top-level join is active at a time. There is no new allocator implementation, libc dependency, Python lowering, or generated-program dependency. Snapshot lengths are bounded by the existing 64 shared slots and existing control-flow limits.

## Boundaries kept deliberately narrow

- First Decimal initialization must occur directly in each eligible arm. First initialization inside nested branches or loops remains rejected, even if a broader analysis could prove it safe. Once established within an arm, Decimal-preserving nested regions remain allowed.
- A missing `Else`, an empty opposite arm, or one-sided Decimal initialization rejects. Constant conditions do not bypass these rules.
- Reading an untouched slot directly in an eligible arm rejects instead of supplying an inferred Integer zero. Reads after that arm's initialization are supported. Outside this bounded join, existing conservative unknown-read behavior remains.
- Legacy one-sided Integer/Text assignment behavior is not converted into a general definite-assignment requirement. Its preexisting zero-initialized storage semantics are not a new guarantee of Text-value safety or general non-Decimal type joins.
- Existing Decimal/Integer/Text representation-conflict checks remain. Action-shared Decimal storage remains unsupported, including unused Actions.
- The special `_` result slot is not part of the new join; its existing entry-kind guards remain. Operand stacks still must be empty at statement-region joins. No general operand-stack dataflow or result-slot inference is claimed.
- The existing 64-slot, 4096-token, and per-construct nesting bounds are unchanged. Declared types, multi-value storage, loop fixed points, and nested definite-assignment joins are not generalized.

Failure sets `NativeFailed` and clears assembly output. There is no fallback to the hosted compiler.

## Verification

- Final fresh-generator/native/VM gate: **372 passed, 18 skipped in 3797.66s (1h03m17s)**. Fresh compiled Linux generator setup took **3708.36s**. This includes generated Linux execution with no undefined executable symbols, three-target cross-assembly, ARM64 instruction emulation, compiled-generator positive/negative branch joins, and hosted-versus-Kuro VM conformance.
- Final exact Linux portable-suite command: **748 passed in 77.41s**. Linux backend/CLI subset: **12 passed**, 69 deselected, in 0.32s. Counts overlap and must not be added together.
- Final branch-join/ARM64-emission focus: **49 passed in 10.59s**; whitespace checks pass. Independent review found no actionable defect after the corrections below.
- Genuine macOS ARM64 compiled-generator execution remains an exact-head CI gate, not a local Linux execution claim. Emulation and cross-assembly are not Darwin execution. Completion requires all eight GitHub checks on the final documentation-updated head; the PR's exact-head status is authoritative.

The shared positive source initializes two different Decimal slots using opposite branch outcomes, performs post-join arithmetic, then uses `Repeat` and `While` with those established slots. A same-kind Integer join is also retained and executed. The fixture prints `2.5`, `5.5`, `-0.0`, and `3`, one per line. Raw-bytecode regressions reject missing/one-sided arms, mixed representations in both orders, early reads, unsupported nested/loop initialization, Action sharing, and residual operand-stack joins. The same positive fixture and representative invalid joins run through the compiled Kuro generator.

An early prototype unnecessarily propagated global Text kinds into pointer-based printing. That unrelated expansion was removed before final verification: a skipped Text assignment could otherwise leave zero storage treated as a pointer. The subsequent first full fresh-generator gate was **370 passed, 18 skipped, 2 failed in 3902.61s**: the compiled generator crashed on invariant control flow, and the ARM64 bootstrap emitter rejected a multi-value snapshot assignment inside an Action. Replacing string snapshots and arrays of snapshot strings with the bounded global collections corrected the unsupported representation. The next gate passed **371 tests, skipped 18, and failed 1 in 3845.89s**: invariant control flow now passed, but first-initialization joins still crashed. A native debugger isolated an inherited hosted-bootstrap inference limitation: a newly introduced numeric eligibility collection read inside an Action was lowered as Text comparison, sending integer `1` to `strlen`. The redundant collection was removed; eligibility is now expressed directly using function mode and the existing control-flow/If depths. A diagnostic-only assembly correction made the entire compiled storage/control-flow/branch helper pass, confirming the fault, but is not fresh-source verification and is not shipped. Focused branch tests plus ARM64 source emission then passed **49 tests in 10.68s**. Prototype or interrupted build results are not final-implementation evidence.

## Next path

Extend the bounded join only after adding explicit nested-region definite-assignment analysis and loop-entry/backedge rules. Analyze Action-shared slots and initialization across calls separately; do not relax the Action guard as a shortcut. General result-slot and value-stack joins remain separate work.

Clean-checkout rebuilding still requires Python, and generated production images still use host assemblers/linkers. Repository-owned object/executable construction, wider runtime and standard-library parity, formatter parity, bootstrap performance, and genuine target validation remain unfinished. Keep this PR and the dependency stack open and unmerged.

### Exact local commands

```sh
.venv/bin/python -m pytest -q tests/self_host/test_native_codegen.py tests/self_host/test_native_decimal_storage.py tests/self_host/test_native_decimal_control_flow.py tests/self_host/test_native_branch_joins.py tests/self_host/test_vm_cross.py --durations=10
.venv/bin/python -m pytest -q --ignore=tests/compiler/test_native.py --ignore=tests/compiler/test_self_host.py --ignore=tests/self_host/test_artifact_launcher.py --ignore=tests/self_host/test_native_codegen.py
.venv/bin/python -m pytest -q tests/compiler/test_native.py -k 'linux_backend or x86_64_backend or native_cli'
```
