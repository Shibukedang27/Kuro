# Dense presence costs: preserve behavior, measure the whole representation

**Keep this candidate test-only.** Preserving dense logical key presence avoids the exact-summary counterexample found in [the preceding experiment](closure-history-and-presence.md), but fewer fact slots do not automatically make a faster or universally smaller analyzer. This slice expands exact-behavior checks and measures the actual two-container adapter, rather than promoting default omission or changing production analysis.

This work starts directly at [PR #75](https://github.com/Shibukedang27/Kuro/pull/75), exact head `5a13fdcdeac0bda001aa36d7b7851d012de91995`. Before branching, #75 was verified open/unmerged, directly on #74, with all eight final-head checks successful. Keep this slice and the existing stack open/unmerged.

## What changes and why

[`audit_expanded_presence.py`](../../scripts/audit_expanded_presence.py) extends the inherited corpus with fixed summary/RETURN witnesses, generated known/missing/scalar return shapes, and adversarial graphs containing joins, aliases, missing names, multiple backedges, and mutually recursive changing summaries. Each program is compared under LIFO/FIFO worklists and forward/reversed successor orders. The candidate retains every logically present name in a presence set while storing only non-default facts in its dict payload.

The audit requires exact complete assembly or error equality, raw logical dense incoming/outgoing/final states, invocation records and summaries, and the full chronological queue/merge/RETURN stream. It also runs the inherited queue replay and the independently reimplemented per-invocation history simulator on each side. Evidence hashes are recorded only after exact comparisons. Losing even a default key is not acceptable. Deliberately corrupted presence, facts, queues and final summaries must be rejected; comparing two equally unexpected infrastructure exceptions must not count as success.

[`profile_presence_closures.py`](../../scripts/profile_presence_closures.py) separately compares the original production emitter with an uninstrumented production-mode AST clone changing only two map initialization sites. It constructs `PresenceFacts(metrics=None)`: no Timeline, queue tracing, write/copy counters or callbacks execute in the measured emitter. Each sample runs in a fresh Python process. Timing and tracemalloc samples are separate, complete outputs are compared before hashing, and the report records source hashes, interpreter/platform, fixed hash seeds, effective CPU affinity and command arguments.

## Why retaining presence can preserve this analyzer's schedule

Define equivalent maps as having the same logical key domain and the same `(targets, known)` lookup at every name. Empty initial maps agree. Assignment retains the same key and logical fact, including explicit default writes. Copy preserves the complete key domain and read-only target-set aliases. Transfers replace tuples or copy target sets; joins allocate fresh unions rather than mutating shared sets. Both representations therefore enumerate the same merge-key union and calculate the same target union and known-flag conjunction. Logical equality yields the same changed predicate and hence the same successor appends. With the same starting queue and successor order, this gives a conditional step-by-step argument for matching visits, sticky RETURN accumulation and summaries.

That argument depends on the current complete operation contract and immutable use of shared target sets. The experiment does not prove the production analyzer correct for arbitrary IR, and bounded tests are not a proof of general equivalence. AST guards reject operation-shape drift; they do not provide Python's full dict semantics.

## What the measurements include

The timed interval covers the complete emitter call, including dense-presence copies and merges, fact payload containers, name/key hashing, summary construction and queue work. Tracemalloc measures actual Python-managed current/peak traced bytes during the same complete call, including the presence set and dict payload; it is not a conversion of slot counts into bytes. Shared objects are accounted by the tracer, not multiplied by logical references.

Imports, IR construction and candidate AST compilation are excluded from both emit timing and tracing. Peak RSS is a separate whole-process high-water mark that includes those preparation costs, so it is not an emitter-only allocation measure and is not interchangeable with traced peak. Tracemalloc does not cover every native allocation, and final traced bytes are not cumulative allocation traffic. Allocation-traced execution times are not used as ordinary speed measurements. Source setup costs and a full application lifetime are not benchmarked by this isolated emit interval.

## Results: exact histories, but a runtime regression

The completed **100-seed audit covers 439 labeled entries × four orders = 1,756 comparisons, with zero failures**. The entries comprise 29 inherited cases, eight fixed witness/edge/recursive cases, two accepted frontend-source fixtures, and four generated shapes per seed. Some inherited/fixed shapes overlap; these are labeled entries, not 439 distinct CFG topologies. All comparisons reach the analyzer. Per side, **476 complete outcomes are successful assembly and 1,280 are expected native-backend rejections**. Both source fixtures successfully emit assembly under all four schedules after actual analyzer invocations.

Every comparison matches all raw logical states, invocation summaries and chronological events, passes both replay validators and both independent invocation-history validations, and agrees with copy accounting. Observed production-side coverage includes **832 recursive installed-summary changes, 75,897 alias operations with preserved facts, 12,308 missing-name loads, 10,035 unknown RETURN accumulator observations, 2,104 not-all-paths-known invocation summaries, and 10,125 backedge merge events**. These are repeated observations across schedules/invocations, not distinct source constructs. “Unknown RETURN” counts the sticky accumulator's false known flag, not necessarily an unknown value on that individual visit. The [compact summary](closure-presence-expanded-summary.json) and [compressed per-comparison evidence](closure-presence-expanded.json.gz) retain exact-comparison flags, outcome/trace hashes, coverage and accounting. They do not retain every complete raw event stream; rerun with `--full-output` for those.

The balanced timing run uses **five pairs per hash seed, seeds 0 and 42, ten samples per mode/size**, pinned to CPU 1. The separate allocation run uses one pair per size at hash seed 0 on CPU 0. All paired full outputs are byte-identical successful assembly. The fixed sparse workload uses seed 7319 and zero additional random cases, so these resource results do not cover the whole correctness corpus or an end-to-end compiler build.

| Sparse-workload size | Production median emit | Presence median emit | Candidate/production time | Production traced peak | Presence traced peak |
| --- | ---: | ---: | ---: | ---: | ---: |
| 40 | 0.2304 s | 0.5474 s | 2.38× | 3,318,514 bytes | 1,585,265 bytes |
| 100 | 3.3127 s | 5.0126 s | 1.51× | 16,010,768 bytes | 4,926,551 bytes |
| 200 | 14.0292 s | 18.3903 s | 1.31× | 42,029,184 bytes | 17,310,551 bytes |

The measured two-container representation lowers traced peak on these three inputs, while **all ten presence timings are slower than every production timing at each size**. This is not a speedup or a robust overall resource win. Allocation results have only one pair per size/one hash seed; repeated memory distributions, other machines/interpreters and representative compiler inputs remain unmeasured. The [resource report](closure-presence-resources.json) retains all timing ranges, allocation current/peak bytes, process RSS, environment and source hashes. Its initial run also includes two exploratory timing samples per mode/size; those are not pooled into the balanced medians above.

The first allocation run used the initial profiling harness before additional fail-closed guards and a timing-only option were added. Its [compressed exact harness snapshot](closure-presence-initial-profiler.py.gz) matches the recorded hash. The final balanced run uses the final harness. The measured candidate operations and representation are unchanged; preparation-time guards are outside the measured interval. The initial long allocation run finished for all three sizes before publication; no partial run is presented as complete.

## Reproduce and acceptance

```sh
.venv/bin/python -m pytest -q tests/compiler/test_expanded_presence.py tests/compiler/test_profile_presence.py
.venv/bin/python scripts/audit_expanded_presence.py --seed-count 100 --output /tmp/presence-expanded.json
.venv/bin/python scripts/profile_presence_closures.py --output /tmp/presence-timing --sizes 40 100 200 --repeat 5 --hash-seeds 0 42 --random-cases 0 --skip-allocation --cpu 1
.venv/bin/python scripts/profile_presence_closures.py --output /tmp/presence-allocation --sizes 40 100 200 --repeat 1 --hash-seeds 0 42 --random-cases 0 --cpu 0
.venv/bin/python -m pytest -q --durations=20
```

CPU numbers are environment-specific; omit `--cpu` for best-effort selection. Allocation tracing can make the largest sample take several minutes; its duration is not ordinary runtime. Run timing without competing work on the selected CPU. The source/evidence [manifest](closure-presence-resource-manifest.json) records checksums and the exact base. Final-head CI acceptance requires all eight checks; earlier-head green results and pending checks are not acceptance. The final local-suite result and final GitHub head/check status are recorded in the PR description after completion.

## Limits and decision

`PresenceFacts` remains the inherited analyzer-specific dict-subclass adapter. Its presence set does not promise dict insertion order, and base-dict/C-level operations, arbitrary serialization, dict union and unrelated mapping APIs are not supported contracts. Trace freezing depends on its logical `items()` override; this is not a general dict replacement. A future explicit presence/fact abstraction would need its own operation review and measurements, not inherit this adapter's results automatically.

Generated missing-name and unsupported-Invoke programs are analysis stress fixtures, not claims that every fixture is source-valid or executable. Matching backend rejection alone is weak evidence; full analyzed histories and successful-emission cases are tracked separately. Source-to-IR coverage does not constitute executing emitted machine code. Replay/simulation use shared IR definitions and some inherited helpers; they are not independent compiler implementations. Identical four-order traces are bounded evidence, not proof for every graph, hash seed or future analyzer change.

There is no production change or promotion in this PR. Any measured memory reduction must be weighed against total runtime and container overhead; a runtime regression does not meet a robust net-benefit gate. An explicit lower-overhead abstraction, broader representative compiler workloads and repeated cross-environment measurements remain separate follow-ups. Autonomous removal of logical defaults remains blocked by #75's exact-summary counterexample.

This is hosted-bootstrap analysis work, not completion of self-hosting. Clean-checkout Python-free compiler/runtime construction and repository-owned assembler/linker independence remain unfinished; see [the independence roadmap](independence-status.md).
