# Closure histories: a counterexample, not a normalization promotion

**Deleting default facts can change an exact final analyzer summary even with the same worklist and successor order.** The earlier 116 comparisons did not find this; the expanded bounded search now does. The emitted result in the reduced witness is still the same backend rejection, so this is an exact-summary counterexample, **not evidence of a user-visible miscompilation**. Production compiler/runtime code remains unchanged.

This review slice starts directly at [PR #74](https://github.com/Shibukedang27/Kuro/pull/74), exact head `cb35b2216cf998f44b0f386a876e68265ed5df9d`. Before branching, #74 was open/unmerged, directly on #73's `c2e989cd80ff4052eb21765339dd3811f3aee0b5`, with all eight checks successful. Keep this slice and the existing stack open/unmerged.

## The new same-order counterexample

[`minimal_final_summary_counterexample()`](../../scripts/search_closure_schedules.py) contains this reduced 13-instruction `SummaryWitness` body:

```text
 0 CONST "SummaryTarget" -> target_a
 1 CALL MakeClosure(target_a) -> closure_a
 2 LOADVAR closure_a -> selected
 3 LABEL head
 4 JUMPF loop_exit, loop_condition
 5 CONST 0 -> pick_a
 6 JUMPF arm_b, pick_a
 7 JUMP head
 8 LABEL arm_b
 9 LOADVAR missing_loop -> selected
10 LABEL loop_exit
11 LOADVAR selected -> result
12 RETURN result
```

This is a handcrafted reduction, not a global-minimality claim. Its complete fixture retains a target Action and mutually recursive seeded Actions. The analyzer explores both branch edges; the missing names make this an adversarial IR-analysis fixture, not an execution-valid program claim.

With **LIFO and reversed successors on both sides**, production first observes `({SummaryTarget}, True, True)` at RETURN, then `({SummaryTarget}, False, True)`. The normalized candidate observes only `(empty, False, True)`. Their first final invocation triples therefore differ:

| Analyzer | Exact final triple |
| --- | --- |
| Production | `({SummaryTarget}, False, True)` |
| Normalized | `(empty, False, True)` |

The first representation-only dense join is `7 → 3`: `pick_a` has become explicitly present as empty/unknown. Dense requeues propagate this presence through the header, producing an additional pending exit visit ahead of the missing-name arm. That early exit reaches RETURN while `selected` remains known. Normalization suppresses the header append; it instead visits the missing-name arm before RETURN. Once production has accumulated the target, the later unknown observation clears `all_known` without retracting it. The [retained exact histories](closure-summary-counterexample.json) contain the independent reconstruction, queue events, facts and RETURN ancestry for both sides.

Both complete emitter outcomes are exactly `compiler.native.NativeBackendError: x86_64-linux Invoke requires closures with statically known targets`. Both final triples have `all_known=False`, so neither summary is installed. Matching rejection does not satisfy the requested exact-summary contract. This counterexample blocks normalization promotion even without a demonstrated difference in installed summaries or emitted code.

The completed [100-seed search](closure-schedule-search.json) checks eight fixed fixtures plus 400 generated graph entries, each under four orders: **1,632 case/order comparisons**. It finds **28 comparisons with exact final invocation-summary sequence differences**, **207 with RETURN accumulator-sequence differences**, and **zero complete output/error differences**. The aligned occurrence diagnostic finds 415 unequal accumulator observations; this is not causal pairing. Counts are per comparison, not distinct programs or differing individual summaries. The report retains aggregate totals, the first ten mismatch records and first ten summary witnesses, plus a digest over every comparison; it does not retain every generated event trace. These seeded templates are a bounded corpus, not arbitrary-graph coverage.

## What the history simulation establishes

[`scripts/simulate_closure_history.py`](../../scripts/simulate_closure_history.py) reimplements transfer, join, constructor call-site discovery, successor construction and pending scheduling from IR. It reconstructs each invocation independently and checks its complete queue/visit/merge stream, final dense or normalized states, and exact final accumulator against the instrumented real emitter. The existing replay separately checks outer installations and invocation inputs. This is more than matching event-site occurrence numbers.

Across the inherited **29 labeled workloads × four orders = 116 comparisons**, both reconstructions validate every complete invocation stream. The simulation retains all **44 differing invocation RETURN sequences**, **40 occurrence-paired differing RETURN observations**, **64 production-only RETURN observations**, and **1,200 representation-only dense appends**. It records queue tokens with producer visits and edge updates, and exact incoming/outgoing facts and sticky accumulator values at RETURN. Counts and per-comparison digests are in [the history summary](closure-history.json); [compressed evidence](closure-history-evidence.json.gz) retains reconstructed RETURN histories and diagnostic ancestry.

**This is not a causal simulation relation between independent schedules.** Queue-token ancestry explains how each reconstructed visit was scheduled, not every dependency contributing to its current state or prior sticky accumulator. Candidate suppression witnesses are selected by CFG reachability, bounded to four witnesses, and ancestry paths to 24 nodes. They can include an update elsewhere in the same invocation rather than the unique earlier cause of a particular RETURN. They must not be read as temporal counterfactual attribution. Invocation pairing still uses function, installed known-return map and ordinal. The full histories reproduce all 44 differences, but the diagnostic associations do not prove that deleting any particular append is harmless. The new concrete witness demonstrates that a general exact-summary equivalence claim is false.

Constructor discovery is independently reimplemented to match the existing linear prepass, not independently proven to be semantically correct on arbitrary IR. AST instrumentation and inherited replay still share helpers; their guarded shape assumptions remain explicit.

## A different representation: preserve presence and scheduling

[`scripts/audit_presence_closures.py`](../../scripts/audit_presence_closures.py) tests a separate approach: retain every dense logical key in a presence set, but store a fact tuple only when it is not `(empty, False)`. Reads, keys, joins and equality still see explicit default presence; every copy owns a fresh presence index. Shared non-default target sets remain read-only under the existing shallow-copy/fresh-union contract.

All **116 inherited case/order pairs** match production's complete outcomes/errors, raw dense incoming/outgoing/final states, exact invocation records, complete chronological queue/merge/RETURN timelines and independently replayed summary installations. A separate regression checks the new summary counterexample under all four orders against production and the independent history simulator. This representation does **not** remove any dense queue event.

The [storage accounting](closure-presence-storage.json) records:

| Logical copy/storage work | Count |
| --- | ---: |
| Mapping copies | 17,328 |
| Dense logical presence slots copied | 234,700 |
| Non-default fact slots copied | 110,874 |
| Default fact slots omitted from payload copies | 123,826 |
| Final-state logical presence slots | 74,956 |
| Final-state non-default stored facts | 36,856 |
| Final-state default fact slots omitted | 38,100 |

These are aggregate slots over repeated snapshots/copies, **not simultaneously live objects, measured bytes, peak allocation, or speedup**. The presence index is still copied densely, merges still enumerate dense names, and a second container adds overhead. There is no timing or memory-benefit claim.

`PresenceFacts` is an analyzer-specific test adapter, not a general replacement for Python dictionaries: its presence set does not promise insertion order, `popitem` is not dict LIFO, and arbitrary inherited C-level dict operations may bypass its logical payload. The exercised analyzer only uses the guarded operations. Do not promote this adapter unchanged or infer safety for future unguarded operations. Mutation controls check fresh mapping ownership and fresh set unions, not isolation from arbitrary in-place mutation of shared target sets.

## Reproduce and review

```sh
.venv/bin/python -m pytest -q \
  tests/compiler/test_closure_history.py \
  tests/compiler/test_closure_schedule_search.py \
  tests/compiler/test_presence_closures.py
.venv/bin/python scripts/simulate_closure_history.py \
  --output /tmp/closure-history.json \
  --evidence-output /tmp/closure-history-evidence.json.gz
.venv/bin/python scripts/audit_presence_closures.py \
  --output /tmp/closure-presence-storage.json
.venv/bin/python scripts/search_closure_schedules.py \
  --seeds 100 --start-seed 0 --output /tmp/closure-schedule-search.json
.venv/bin/python -m pytest -q --durations=20
```

The search resets each closed-over trace collector before each program; a regression prevents cumulative invocation histories and misleading mismatch totals. Comparisons use exact values before recording outcome/sequence digests. Deliberate omitted append, forged state, queue, constructor fact, accumulator and final-summary controls reject. No CI platform, Python-version or existing test is removed. Final documentation-updated-head acceptance requires all eight checks; the PR description records those results, not earlier-head or pending checks.

The final complete local suite passed **1,094 tests, 20 skipped in 443.03s**, including all 14 new regression tests. The earlier focused run passed 11 tests before the last three controls were added; the complete run includes those final controls. `py_compile`, JSON/gzip payload validation, source/evidence checksums in [the manifest](closure-history-manifest.json), and `git diff --check` also pass. Regression durations are not performance measurements of the candidate representation.

## Decision and next experiment

Keep all changes test/instrumentation/documentation-only. Default omission with autonomous scheduling is **not exact-summary equivalent** on this bounded corpus, so do not promote it. No accumulator redesign is bundled into this finding.

A next separate experiment should replace the dict-subclass adapter with an explicit presence/fact abstraction whose complete operation contract is guarded, then extend exact full-timeline comparisons to the expanded generated graphs and changing recursive summaries. Measure total live/peak allocation and uninstrumented runtime including dense presence-copy overhead before claiming an optimization. General reasoning about presence, reads, joins, equality and queue induction must accompany any separate production proposal; bounded equality alone is not proof.

This slice investigates hosted-bootstrap analysis, not completion of self-hosting. Clean-checkout Python-free compiler/runtime construction and repository-owned assembler/linker independence remain unfinished; see [the independence roadmap](independence-status.md).
