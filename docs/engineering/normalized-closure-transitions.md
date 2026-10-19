# Normalized closure facts: faster, but still a test-only experiment

Explicit plain-dictionary normalization preserves the exact final analyzer summaries in this bounded audit, and uses much less temporary memory. It does **not** preserve the queue or intermediate return-summary event sequences. The analyzer also has a reproducible, pre-existing order-sensitive accumulator. This follow-up therefore makes **no production compiler, runtime, or worklist change**.

The branch is stacked directly on [PR #72](https://github.com/Shibukedang27/Kuro/pull/72), verified open/unmerged at `bdbfe1b2e7599b3d29a52929459e8c3d68f402ab`, based on PR #71's `perf/share-closure-return-target-sets`. All eight #72 checks were successful before this work started. Keep the stack open and unmerged.

## What the comparison actually checks

`scripts/audit_normalized_closures.py` clones the actual hosted emitter with fail-closed AST assertions. The three variants are unchanged production; an unpruned reference restoring the two whole-state deep-copy sites and removing only the seedless guard; and a candidate that explicitly writes or pops facts in ordinary dictionaries. The candidate does not use `SparseFacts` or inherited dictionary-mutator behavior. It elides only `(empty targets, False)`: empty-known and nonempty-unknown facts remain explicit. Every read and join keeps production's missing-name default, union, and all-paths-known AND.

The corpus contains 22 deterministic cases, each checked in four test-only orders: LIFO/FIFO crossed with forward/reversed successor order. It includes 12 generated branch/loop graphs, three reachable three-backedge fixtures, absent-name joins, mixed/overwritten/unreachable returns, and recursive returned CALL results. In the latter, `RecursiveA` has an unused constructor to ensure it is analyzed before `RecursiveB` becomes known; its actual return triple changes from `(empty, False, True)` to `({RecursiveSeedTarget}, True, True)`. This tests changing results, not just a changing global input map. The fixtures are analysis workloads, not claims about executing or terminating these loops.

All **88 case/order comparisons** compare full assembly strings or exact error class and text before retaining digests. There are 40 assembly outcomes and 48 intentional errors across those comparisons. Each variant is compared under the **same** order; the audit does not assume that different orders are interchangeable.

For production versus unpruned deep-copy, shared invocations match on exact known-return inputs, return triples, every visit/transfer/merge/queue event, final states, and outer summary transitions. Invocation IDs are remapped out before comparison. The reference's additional seedless invocations cannot install return summaries.

For production versus normalized dictionaries, every invocation's exact `(targets, all_known, saw_return)`, final normalized instruction states, and every outer summary transition match. An independent validator checks every recorded transfer, union/AND merge, and sticky return-accumulator step, even after schedules diverge. Cross-run prefix comparisons cover 7,905 aligned visits and 3,553 aligned merges. Their 40 recorded differences are **changed/not-changed queue controls**, not unequal normalized operands, transfer results, or return triples. First-divergence witnesses remain visible rather than treating unmatched later visits as equivalent. Negative controls reject corrupted transfers, merges, and return summaries.

## The scheduling boundary is real

The retained [audit evidence](normalized-closure-audit.json) classifies every changed production merge, with normalized-state fingerprints and matching append evidence. The compact file retains classifications and divergence witnesses; `--full-output` retains expanded maps. Matching append evidence is a local observation, not a complete one-to-one simulation between independently scheduled runs.

| Across the 88 comparisons | Production | Unpruned deep-copy | Normalized dict |
| --- | ---: | ---: | ---: |
| Analyzer invocations | 236 | 540 | 236 |
| Body visits | 10,513 | 11,121 | 9,449 |
| Merge attempts | 5,641 | 5,641 | 4,491 |
| Changed merges with equal normalized state | 1,058 | 1,058 | 0 |
| Changed merges with different normalized state | 3,895 | 3,895 | 3,889 |

The 1,058 representation-only dense updates add explicit default entries without changing any local's semantic fact. Normalization makes that equality test unchanged, so the corresponding local requeue is unnecessary for fact propagation. But **not every scheduling difference is accounted for simply by subtracting those events**: the independently scheduled candidate also coalesces six semantic updates and changes 36 invocations' exact return-summary event sequences. Equal final states and triples do not prove that arbitrary queues preserve the sticky accumulator's observation history.

There is a concrete warning against assuming order independence. On `generated_graph_workload(1, "missing")`, production with ordinary successor order returns `(empty, False, True)` for `GeneratedGraph` at empty known-return input. Reversing successors returns `({GraphTargetA}, False, True)`. In the reversed run, the first RETURN observes a known target before the missing predecessor weakens knownness; the accumulated target is never removed. Both complete emissions reject with exactly `compiler.native.NativeBackendError: x86_64-linux Invoke requires closures with statically known targets`. This is an existing scheduling property, **not a demonstrated normalized-versus-production final-triple mismatch under the same order**. The regression deliberately preserves it; the candidate does not repair it.

## Fresh-process time and memory

The [measurement record](normalized-closure-profile.json) retains all raw samples, interpreter/platform, source hashes, CPU affinity, hash seed, assembly digests, and peak memory. Each sample runs in a fresh Python process pinned to CPU 0 with `PYTHONHASHSEED=0`; three clean repetitions rotate variant order. Tracemalloc is enabled only in a separate fresh allocation sample per variant/size. Timing excludes clone setup and IR construction. Every full assembly output is checked byte-for-byte against production before recording its digest.

| Seeded workload | Production | Unpruned deep-copy | Normalized dict |
| --- | ---: | ---: | ---: |
| Size 80 clean emission, three runs | 1.6523–1.7229s | 2.0545–2.0715s | 0.1768–0.1835s |
| Size 80 peak traced bytes | 11,076,472 | 14,829,112 | 1,387,808 |
| Size 160 clean emission, three runs | 9.9642–11.3718s | 18.7384–21.2998s | 0.8030–0.8762s |
| Size 160 peak traced bytes | 34,476,028 | 48,921,020 | 3,522,764 |

Assembly remains exactly **85,510 bytes** at size 80 and **106,824 bytes** at size 160, with the same digests as #72. Peak traced bytes are simultaneous traced Python allocations during emission, **not total allocated bytes or allocation-event counts**. Process peak RSS includes interpreter, IR, and AST-clone setup; at size 80 the candidate's clean-process RSS is actually higher than production despite lower traced emission memory. Both measurements are retained to avoid conflating them.

These are Linux/Python 3.12.3 observations, not Darwin, whole-build, or runtime speed claims. CPU affinity is not a reserved CPU; background audit development/focused checks were not machine-isolated, no CPU-frequency control was applied, and three repetitions plus one traced sample do not establish a statistical performance guarantee. No local full suite ran during sampling. The recorded measured audit-module hash predates trace/comparator, fixture, and preflight-assertion strengthening; those changes do not change the untraced normalized-emitter transformation. The final audit-source hash is recorded separately rather than relabeling the old measurements.

## Verification and next path

The final focused module passes **10 tests**. The final complete suite passes **1,051 tests, 20 skipped in 255.91s**. An earlier 1,050-pass collection began before the last negative-control test was added; it is not substituted for this final run. No existing checks, cases, platforms, or Python versions are removed. All eight CI checks must pass on the final documentation-updated PR head before acceptance; earlier-head or pending checks are not green evidence.

```sh
.venv/bin/python -m pytest -q tests/compiler/test_normalized_closure_analysis.py
.venv/bin/python scripts/record_normalized_audit.py --output /tmp/normalized-audit.json --full-output /tmp/normalized-expanded.json
.venv/bin/python scripts/profile_normalized_closures.py --output /tmp/normalized-profile --sizes 80 160 --repeat 3
.venv/bin/python -m pytest -q --durations=20
```

The next bounded experiment should replay the production queue with normalized shadow states and explicit event correspondence, then investigate each absent candidate append and return observation after the first divergence. Extend the adversarial CFG corpus and changing recursive summaries without assuming monotonic final-state reasoning settles the sticky accumulator. Either demonstrate the required exact-triple/scheduling relation, or separately evaluate a representation optimization that preserves dense scheduling. Do not bundle a worklist or accumulator redesign, numeric inference, or CFG caching into a production normalization proposal. The present evidence supports further experiments, not promotion.

Clean-checkout Python-free compiler/runtime construction and host assembler/linker replacement remain unfinished. This PR improves evidence about a hosted-bootstrap bottleneck; it does not complete [toolchain independence](independence-status.md).
