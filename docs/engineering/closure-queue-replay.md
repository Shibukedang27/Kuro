# Production queue replay: matching shadows, different schedules

The normalized fact representation matches every checked state and RETURN accumulator when it follows the **production queue**. It still does not follow the same queue when allowed to schedule itself. This is stronger evidence about the representation, not proof that deleting dense worklist events is safe. **No production compiler, analyzer, runtime, queue, or summary-installation code changes in this slice. Sparse and normalized facts remain test-only.**

This review branch starts at [PR #73](https://github.com/Shibukedang27/Kuro/pull/73), exact head `c2e989cd80ff4052eb21765339dd3811f3aee0b5`. Before branching, #73 was open/unmerged, directly based on #72's `experiment/sparse-closure-return-facts`, with all eight final-head checks successful. Keep this slice and the existing stack open and unmerged.

## What the replay establishes

[`scripts/replay_closure_queue.py`](../../scripts/replay_closure_queue.py) builds the existing fail-closed AST instrumentation clone of the real hosted emitter. It records a **single chronological timeline** across analyzer entry, queue seed, dequeue, instruction transfer, merge, append, analyzer exit and outer summary round. Production instructions and scheduling are unchanged; FIFO and successor reversal are explicitly test-only perturbations.

An independent model reconstructs each recorded event from the IR body. Its dense maps decide whether to append; separate normalized shadow maps perform their own transfers and joins but follow that dense schedule. It checks exact dense incoming/outgoing states, normalized shadow states, both accumulators, edge order, duplicate queue entries, queue contents and exhaustion, final states, exact invocation triples, summary inputs, installation under the correct function identity, and outer-round convergence. It does not stop comparing after autonomous schedules diverge.

The autonomous normalized trace is independently replayed too, using normalized writes and joins for its own changed-state decisions. This checks its actual queue rather than treating its correctness as a consequence of the dense shadow run.

The finite audit covers **29 labeled workloads × four orders = 116 comparisons**: LIFO/FIFO crossed with forward/reversed successors. It carries forward the previous 22 cases, adds the compact witness and physically swapped predecessor layout, and includes five named adversarial replay entries. Some entries intentionally reuse existing fixtures; **29 is a label count, not 29 distinct graph shapes**. Coverage includes three backedges, absent-name joins, alternate/overwritten/unreachable returns, closure-or-scalar returns, and recursive CALL results whose summaries actually change. There is no production predecessor-list iteration to reverse: predecessor arrival is varied by queue/successor order and physical branch layout instead.

The retained results are:

| Check | Result |
| --- | --- |
| Production queue replay with normalized shadows | 116/116 valid |
| Autonomous normalized queue replay | 116/116 valid |
| Exact complete emitter assembly or error outcomes, same order | 116/116 equal |
| Exact final invocation triples and normalized final states, same order | 116/116 equal |
| Outer summary transitions, same order | 116/116 equal |
| Production analyzer invocations | 272 |
| Production instruction visits checked, including after divergence | 11,496 |
| Production RETURN steps checked | 622 |
| Production queue events checked | 22,992 |
| Production merge events checked | 6,166 |
| Representation-only dense appends | 1,200 |
| Case/order runs with autonomous control divergence | 20 |
| Per-invocation RETURN sequence differences | 44 |
| Unmatched chronological events under occurrence matching | 4,928 |

Queue events include seeds, pops and appends; merge events exclude first-reach copies. Invocation sequence differences are not a count of distinct programs or individual RETURN events. Every state/summary comparison is exact before outcomes are represented by digests.

## What differs after the first divergence

The report records all unmatched queue/visit/merge events and every matched normalized transition difference, not only a zipped common prefix. It also retains every RETURN observation on both sides, including unmatched visits and before/after production/shadow accumulators.

The correspondence key is `(function, known_returns, invocation ordinal, event site, occurrence)`. For append events, the site is the destination; for merges it includes source and destination. **Matching occurrences do not establish matching causal histories.** Different visits to a loop header can be paired by occurrence despite observing different earlier paths. Those input and accumulator differences remain explicit evidence, not silently normalized away.

Across the corpus, 518 paired RETURN observations have equal normalized inputs and accumulators, 40 paired observations differ, and 64 production RETURN observations have no autonomous counterpart. There are no candidate-only RETURN observations under this matching rule. Thus the old sequence differences are not all merely identical duplicate returns.

For example, in `multibackedge_0`, LIFO/forward order, the first divergence occurs at timeline offset 74. Dense analysis appends header 12 after edge `26 → 12`, with queue `[6,17,22,12]`; the autonomous normalized run instead pops 22, leaving `[6,17]`. The dense join has added explicit empty/unknown facts for `loop_cond`, `ra` and `rb`, without changing any normalized fact. On the corresponding invocation, dense RETURN accumulators progress `A → A → {A,B} → {A,B}`, whereas autonomous observations progress `A → {A,B}`. Both eventually install `{A,B}`, but their second RETURN observations have different normalized inputs and accumulated targets. Dense replay checks all four observations and their shadow states, not just the final union.

## A compact explanation of the existing order witness

[`scripts/closure_queue_cases.py`](../../scripts/closure_queue_cases.py) reduces the earlier generated witness to this nine-instruction analyzer body:

```text
0 CONST "QueueTarget" -> name
1 CALL MakeClosure(name) -> c
2 CONST 1 -> cond
3 JUMPF unknown, cond
4 JUMP join
5 LABEL unknown
6 LOADVAR absent -> c
7 LABEL join
8 RETURN c
```

This is a compact handcrafted reduction, **not a claim of global minimality**. The analyzer explores both CFG successors even though this fixture uses a constant condition. It is an analysis workload, not an execution-based demonstration of the absent variable.

Production LIFO scheduling visits the unknown arm first. Its two RETURN observations are `(empty, False, True)` and `(empty, False, True)`, and its final exact triple is `(empty, False, True)`. Reversing successors reaches the known arm first: its RETURN observations are `({QueueTarget}, True, True)` then `({QueueTarget}, False, True)`. The final triple retains the target despite `all_known=False`.

This follows directly from the existing implementation: `returned.update(targets)` only adds targets from currently known, nonempty return facts; observing an unknown return makes `all_returns_known=False` without retracting earlier targets. A known/unknown join also ANDs the known flag. Therefore **when** RETURN is visited is observable in the exact triple. A ten-instruction physical-layout-swapped fixture gets the known-first result under unmodified production scheduling. Both versions still reject installation because `all_known` is false; unchanged emitted output does not erase the exact-summary difference.

## Evidence and verification

The readable [summary JSON](closure-queue-replay.json) contains counts, first witnesses, source hashes and hashes of complete evidence lists. The [compressed JSON evidence](closure-queue-replay-evidence.json.gz) retains every representation-only append, every production and autonomous RETURN step, every occurrence-matched RETURN pair, every unmatched event and every matched transition difference. The CLI can additionally emit both full chronological timelines with `--full-output`; those much larger raw timelines are reproducible rather than checked into the repository.

```sh
.venv/bin/python -m pytest -q tests/compiler/test_closure_queue_replay.py tests/compiler/test_closure_queue_cases.py
.venv/bin/python scripts/replay_closure_queue.py \
  --output /tmp/closure-queue-replay.json \
  --evidence-output /tmp/closure-queue-replay-evidence.json.gz \
  --full-output /tmp/closure-queue-timelines.json
.venv/bin/python -m pytest -q --durations=20
```

Regression controls deliberately corrupt queue appends, dequeue contents, incoming facts, RETURN accumulators, installed summary maps, analyzer inputs, function identity, invocation ids, negative/out-of-range indices and final summaries; they also omit a merge and the final round. The validator rejects those corruptions. Compact-report tests ensure list hashes and counts retain their connection to full evidence without mutating it. Existing AST shape assertions remain in force, and no platform, Python-version, or test coverage is removed.

The final complete local suite passes **1,080 tests, 20 skipped in 351.10s**. The 29 new tests are included in that complete run; the targeted corruption/witness run separately passed 27 tests with two bounded-corpus tests deselected. No performance samples are taken in this slice, and these regression runtimes are not benchmark claims. Final-head CI results are recorded in this PR's review description. All eight CI checks must be successful on the final committed head; pending checks or earlier-head green runs are not acceptance evidence.

## Limits and next path

The independent transfer model takes constructor targets captured from the existing emitter's prepass as trusted inputs. It checks the instruction and installed CALL-summary inputs, but **does not independently prove constructor discovery**. It also shares the existing instrumented-clone builder and its fail-closed AST assertions. The dense replay is a proof for these captured runs, not a proof for all IR, targets, compiler configurations or future analyzer changes.

The experiment explains how representation-only appends disappear and how later semantic propagation coalesces, but does not establish a causal simulation relation between arbitrary independent dense and normalized schedules. The sticky accumulator makes an appeal to final monotone state unions insufficient. The existing order witness is not a dense-versus-normalized same-order counterexample; no such final-summary counterexample was found in this corpus. Nor does that absence establish semantic equivalence.

**Production promotion remains blocked.** A next bounded slice can either develop a history-aware simulation argument/counterexample search around sticky RETURN observations, or test a representation optimization that explicitly preserves dense scheduling (for example, retaining separate presence information). Any eventual production proposal must be a separate PR with its own evidence; do not bundle accumulator/worklist redesign, numeric inference, CFG caching or stale-summary reuse into normalization.

This slice investigates a hosted-bootstrap bottleneck. Clean-checkout Python-free compiler/runtime construction and repository-owned assembler/linker independence remain unfinished; see the [independence status](independence-status.md).
