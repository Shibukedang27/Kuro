# A small indexed-state contract before native lowering

Historical PR #89 checkpoint: [PR #90's compatibility correction](collection-index-compatibility.md) and the subsequent [native logical-bounds correction](native-logical-collection-bounds.md) supersede the runtime discrepancy observations below. The actual Kuro-generator collection boundary remains unfinished.

The next safe step is a **test-only contract and boundary proof**, not collection lowering. Small guarded integer-state and Text-name programs can be compared across existing execution paths, while the actual Kuro-authored native generator still rejects their complete compiler-produced bytecode. The full analyzer still does not execute through that generator. Strict independence remains unfinished.

This increment stacks on [PR #88](https://github.com/Shibukedang27/Kuro/pull/88), inspected open and unmerged at `d91aa537d0e572f990b664a24191c6fe4c364506` with eight successful checks. No production compiler, runtime, generator, analyzer, capacity or acceptance rule changes.

## The bounded reference subset

[The new tests](../../tests/self_host/test_native_indexed_state_contract.py) isolate 16 integer mask lanes and 16 × 16 flattened snapshot cells. Two-item literal initialization followed by bounded appends establishes the logical collection sizes without relying on scalar append behavior. Indices are computed at runtime. Explicit guards reject negative and one-past-end slots or frames **before any indexed access**. In-range first, last and interior cases write literal masks `4` and `2`, read them back, and read distinct untouched positions to check noninterference. This is a storage witness, not an analyzer, fixed-point analysis or entry/backedge proof.

A separate Text-name witness declares a collection, appends two names, replaces one complete element, reads both names and checks length. It is not character mutation, arbitrary text processing, Unicode storage or dynamic element-kind coverage.

For these eight programs, tests compare exact expected output with the Python IR interpreter, Kuro-authored compiler/VM stages running in that interpreter, and executables built by the **Python-authored native backend**. Those native executables are hosted-bootstrap evidence, not output from the Kuro-authored generator. Guarded rejection cases are successful executions printing `REJECT`, not traps from an invalid memory access. The constants 16 and 256 are test-local logical bounds, not new native-generator capacities.

The numeric subset deliberately does not use `Length` on variables declared `Integers`: the hosted typechecker rejects that spelling with `E3009`. Initial fixture attempts exposed this restriction; it was not bypassed by weakening the typechecker. Likewise, two-item literals avoid assuming that scalar append behaves identically across runtime paths.

## What the real generator does

A fresh generator image is constructed from the existing artifact loader and Kuro generator through the hosted bootstrap. Each complete witness is compiled with `compile_with_kuro_driver`, framed without truncation, and submitted to that native generator process. Each artifact is below the existing 4,096-token ceiling and asserts its collection opcodes are present. All collection witnesses must reject with exit 1 and empty assembly/stderr. Several unsupported operations coexist; this does not identify a unique first rejection branch or prove native execution of their source-level guards.

A separate scalar program computes `15 * 16 + 15`. The same native generator emits its assembly; the captured assembly is linked with `clang -nostdlib`; the resulting executable must print exactly `255\n` and have no undefined symbols. That demonstrates a live generator and executable scalar indexing arithmetic, **not collection execution**.

Temporary diagnostics retain submitted source/artifacts, captured assembly and a JSON manifest with source/artifact/assembly hashes, compiler-output token counts, generator image hash/exits, and the hash/output of the scalar image actually executed. Collection entries explicitly record `submitted_program_executed: false`. These are local pytest artifacts, not checked-in binaries, CI uploads or reproducible-bootstrap claims.

## Two semantic blockers made explicit

**Negative collection reads differed at PR #89.** The hosted interpreter reads `Items = 10, 20; Get Items -1;` as `20`; the Kuro-authored VM then rejected it. The [compatibility follow-up](collection-index-compatibility.md) identifies the existing authority (README's frozen oracle and ADR-0012), restores logical-end GET offsets in the VM, and converts this observation to a parity regression. Negative SET remains invalid. The guarded storage subset here still excludes negative indices; the native backend discrepancy is not repaired by the VM correction.

**Logical length is not backing capacity.** For a two-element collection, both the hosted interpreter and Kuro VM reject index `2`. The existing Python-authored Linux native backend instead reads a zero-initialized backing cell or continues after a write to that cell, because its GET/SET checks compare with allocated capacity rather than logical length. The tests record both operations and label them nonconforming boundaries, not successful bounds parity. They never infer safe native bounds from that backend. The guarded subset prevents these invalid accesses itself.

These were pre-existing observations, not production fixes in PR #89. That PR's use of “decide” below was a missing authority audit, not permission to choose new semantics: compatibility already specifies GET in `[-length, length)` and SET in `[0, length)`. Neither this historical proof nor its narrow VM follow-up promises complete native memory safety or validates arbitrary invalid bytecode. Initial diagnostic fixture failures are not represented as successful native behavior.

## The next implementation path

1. Preserve the audited compatibility behavior across the interpreter, bytecode VM, Kuro VM and hosted native backend. The VM negative-GET correction is a separate increment; storage-aware native length checks and negative GET normalization remain outstanding. Do not silently copy a nonconforming implementation into the Kuro generator.
2. Design a bounded integer-only collection representation with explicit element kind, logical length and capacity. First prove initialization plus indexed GET/SET and logical bounds; reject every unsupported initialization, alias/copy, parameter, mutation or control-flow form explicitly. Treat the reference witnesses here as candidates, not as an already accepted grammar. The generator's existing GET return-kind inference assumes integer and must not be generalized to Text or Decimal elements without a proof.
3. Add a separately reviewed Text-name/token representation and append/length behavior. Audit identity, copy and Action parameter behavior rather than pretending a scalar slot is a collection handle.
4. Only then address the full analyzer's 16,392-token output, global-slot/storage constraints and generator-compatible decomposition. Require actual analyzer assembly, linking and exact safe/unsafe/malformed/bounds evidence output before claiming integration.

The hosted compiler/generator bootstrap and external assembler/linker remain trusted dependencies throughout this proof.

## Validation and reproduction

The new module passed **20 tests in 6.77 seconds**. The final focused native/analyzer gate passed **755 tests / 18 skipped in 409.42 seconds**. The complete local suite passed **1,507 tests / 20 skipped in 813.64 seconds**. Counts overlap. Python 3.10 syntax parsing and `git diff --check` passed. Linux CI explicitly selects the new module in its fresh-generator native gate; the normal full suite also discovers it. Linux-only execution tests are gated; reference interpreter/Kuro VM parity also runs on other hosts.

The actual generator received 23 tokens for the executable scalar control, 154 tokens for each nonnegative numeric-state witness, 158 tokens for each negative-index numeric-state witness, and 44 tokens for the Text-name witness. Only the scalar control generated an executable. Thus the rejection witnesses isolate this boundary well below 4,096 tokens; they do not solve collection lowering or the full analyzer's size.

An independent soundness reviewer found no blocker and separately ran the 19 non-generator tests successfully. The review specifically confirmed the explicit guards, flattened-index bounds, reference-path labeling and observational treatment of semantic disagreements. Its caveat is preserved above: composite-artifact rejection is not proof that each included opcode was independently reached. Initial fixture failures were corrected before the final focused/full runs; no production behavior was modified.

```sh
.venv/bin/python -m pytest -q tests/self_host/test_native_indexed_state_contract.py --durations=10
.venv/bin/python -m pytest -q tests/self_host/test_native*.py --durations=20
.venv/bin/python -m pytest -q --durations=20
git diff --check
```

Publication requires all eight checks on the exact final documentation-updated head. This PR and its predecessors must remain open and unmerged.
