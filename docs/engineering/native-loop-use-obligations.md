# A Kuro-written ledger for loop-read obligations

This test-only increment follows [PR #82](https://github.com/Shibukedang27/Kuro/pull/82), inspected open/unmerged with all eight predecessor/baseline checks successful at `aec515c9c93ab8cf6414aca1907f5a43b22c78aa`. Those checks validate the predecessor, not this new increment. This slice moves the obligation bookkeeping into Kuro without claiming that Kuro now computes loop-flow facts. Production compiler sources, acceptance rules, runtime and CI configuration remain unchanged. Strict compiler/runtime/toolchain independence is not complete.

## Why slot snapshots are not enough

A branch can read an unknown slot before a later store makes every exit Decimal. Restoring the branch-entry slot snapshot, or examining only the eventual exit, must not erase that early read. Integer entry followed by Decimal backedges is also conflicting evidence, not a Decimal-only read.

The [preceding boundary-origin oracle](native-loop-per-use-evidence.md) records this evidence in Python. The new [Kuro prototype](../../tests/self_host/loop_use_obligations.kuro) tests the next representation boundary: read obligations have their own identity and lifetime, independent of mutable slot snapshots. Its companion [tests](../../tests/self_host/test_native_loop_obligations.py) supply facts, exercise malformed/incomplete evidence and compare the resulting obligation decisions with the oracle.

## What this does—and does not—prove

A read is identified by its containing loop, original load-token PC and slot name. Entry-origin and backedge-origin coverage remain separate. Every required origin must have evidence, and every observed kind must be Decimal before that obligation can discharge. Unknown or conflicting evidence must remain bad even after later Decimal observations. An unreachable origin is not an unknown kind.

This is a streaming reducer, not a retained map of all reads: one active row holds the identity, declared required origins and two observed-coverage bits. A run-wide sticky failure bit accumulates the result of every row. Any non-Decimal observation immediately poisons the run. Duplicate Decimal observations are idempotent. Begin/Observe/Finish/Seal protocol checks prevent a new row from erasing an unfinished obligation; missing coverage, observations with a mismatched identity, invalid origins/requirements and calls after sealing fail closed. Only a trusted explicit Reset starts a new independent run; Reset is never part of branch snapshot restoration.

Capacity is an integer from zero through 64 rows. The counter stops advancing at the bound, overflow poisons the run, and the prototype does not accumulate an unbounded textual event log. Caller-owned input strings and the number of supplied calls are not independently bounded by this reducer. It retains only the current identity and constant-size decision state, not origin kind masks or diagnostic history. Identities are trusted canonical Text values; it checks equality, not whether a PC actually points to a load in the program.

It is test-only and has no connection to the production generator's permission flags. In particular, discharging the reads after a complete multitrip two-arm initializer does **not** authorize that initializer in production; the existing native gate still rejects it.

The caller remains responsible for one initial Reset, declaring the complete set of read identities, required reachable origins and all relevant kind evidence. The reducer cannot discover an omitted read, an omitted possible kind, duplicate declared rows or a falsely declared unreachable origin. Python still constructs the CFG and solves loop facts. This is neither a certificate checker for arbitrary bytecode nor a Kuro-owned fixed-point solver, and it is not a proof that all stores, joins or representation transitions are safe.

The oracle's earlier limitations still apply: boundary-origin seeds are globally converged, nested entry is not first-ever iteration, arithmetic is nonrelational, and positive literal loops are overapproximated rather than exactly unrolled. No universal equality between locally partitioned and globally merged arithmetic facts is assumed.

## Validation

The new module passes **27 tests**. Its oracle comparison covers **34 named programs and 52 per-use obligations**. Separate cases exercise missing origin evidence, all three identity components, reachable unknown versus unreachable origins, conflicting and malformed kinds, duplicate/order invariance, sticky failures across rows, malformed lifecycle calls, and exact 64-row/overflow/zero-capacity boundaries. The branch/overwrite witnesses demonstrate that eventual Decimal exits do not rescue earlier unknown reads. A safe complete-arm multitrip read discharges the reducer while production still rejects that initializer on all three native targets.

The focused/fresh-generator gate passed **259 tests in 169.99 seconds**. The complete suite passed **1,315 tests / 20 skipped in 644.37 seconds**. `git diff --check` passed. The focused gate includes the previous per-use/positive Repeat/loop-flow/branch-join suites, the freshly built native generator's Decimal storage gate, depth/slot/token limits and ARM64 source emission. Existing fresh-generator rejection probes require exit 1 with empty stdout/stderr; accepted controls link and execute with exact output.

Native execution of a prototype bootstrapped by the Python native backend is useful evidence about the Kuro implementation and runtime, but is not a clean-checkout Python-free bootstrap or a new Kuro-owned solver. The separate fresh Kuro-generator gate checks that existing production acceptance remains intact.

The prototype's four Linux x86-64 native probes cover safe D/D, unknown followed by Decimal, Integer entry and missing backedge coverage. They do not establish native lifecycle/capacity coverage on every target. The oracle differential checks compare the aggregate discharge decision, not a retained Kuro history of every kind set.

Independent design review found no blocker for a test-only bookkeeping slice and emphasized that a sticky side ledger cannot derive entry/backedge states from the current one-pass emitter. Initial implementation inspection found that beginning a row before finishing the previous one could erase pending observations, and an unused textual log could keep growing after overflow. The final protocol and immediate run-wide poison remove those defects, with raw-call and capacity regressions. Independent re-review of the hardened code found no blocker within its explicitly documented trusted-caller contract. It highlighted the intentional Reset boundary: calling Reset after failure creates a new run and can succeed, so arbitrary untrusted call streams are not validated. Additional direct native malformed-lifecycle and missing-entry-only probes remain possible test extensions, not claimed coverage.

```sh
.venv/bin/python -m pytest -q \
  tests/self_host/test_native_loop_obligations.py \
  tests/self_host/test_native_loop_use_evidence.py \
  tests/self_host/test_native_positive_repeat.py \
  tests/self_host/test_native_loop_flow_facts.py \
  tests/self_host/test_native_repeat_branch_joins.py \
  tests/self_host/test_native_loop_init.py \
  tests/self_host/test_native_branch_joins.py \
  tests/self_host/test_native_codegen.py::test_kuro_owned_x86_linux_codegen_runs_decimal_storage \
  tests/self_host/test_native_codegen.py::test_kuro_native_codegen_keeps_if_depth_limit_at_sixteen \
  tests/self_host/test_native_codegen.py::test_kuro_native_codegen_keeps_global_slot_limit_at_sixty_four \
  tests/self_host/test_native_codegen.py::test_kuro_native_codegen_enforces_exact_4096_token_boundary \
  tests/self_host/test_native_codegen.py::test_native_codegen_source_emits_with_macos_arm64_backend \
  --durations=10
.venv/bin/python -m pytest -q --durations=20
```

## Next bounded path

Before production multitrip branch initialization, replace the trusted Python fact producer with a Kuro-owned, independently reviewed analysis that preserves complete read identities and boundary-origin evidence. Prove how it handles both branch arms, nested regions, entry/backedge coverage and bounded-resource failure without restoring away ledger state. Then check it against the adversarial corpus before considering any narrow permission change. Read obligations alone do not prove store compatibility, exit joins, stack shape or Action/result-slot semantics; those need their own invariants. Keep all existing exclusions until those proofs exist.

Publication is verified only after all eight CI checks pass on the exact final documentation-updated head. The stacked PR must remain open/unmerged, with the immutable checked head recorded in its metadata.
