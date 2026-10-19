# Copy closure-analysis mappings, not read-only target sets

The seeded closure-return path was repeatedly cloning every target set in every instruction's state, even when those sets were empty. This follow-up to [PR #70](https://github.com/Shibukedang27/Kuro/pull/70) changes only two whole-state copies: each now copies the dictionary while sharing its read-only `(target set, known-on-every-path)` values. Transfers, merge unions, CFG construction, processing order, fixed-point rounds and bounds, seedless pruning, and lowering are unchanged. No analysis result is cached.

## A workload that actually returns and uses closures

`scripts/profile_seeded_closures.py` generates valid Kuro source, rather than adding a constructor to an otherwise seedless compiler image. `MakeAdder` constructs an `AddBase` closure capturing `Base`, keeps it live across many numeric local initializations, and returns it. Main constructs two independent instances for 10 and 20, invokes both with 7, and prints 17 and 27. At size 200 the maker has **807 IR instructions**, and the captured target has four. This is a synthetic stress workload, not evidence of application-corpus or whole-build speedups; its straight-line body intentionally isolates state copying. Reconverging branches, loops and changing call summaries are separate differential regressions.

The reference is a separate clean worktree at PR #70's final head `6043938e2e14fd97ad4f2b430573945deabce1dd`, still open/unmerged and based directly on #69. The benchmark script can import either checkout with `--root`. Timings exclude parsing/IR construction, assembly/linking, and executable startup. All runs here use Linux x86-64 / Python 3.12.3, with instrumentation separated from ordinary timing runs.

| Size-200 measurement | PR #70 | Mapping-copy follow-up |
| --- | ---: | ---: |
| Three uninstrumented emissions | 1.901, 1.914, 1.970 seconds | 0.02745, 0.02703, 0.02751 seconds |
| Analyzer calls / CFG builds | 2 / 2 | 2 / 2 |
| Body-index visits | 1,614 | 1,614 |
| Names copied across the two whole-state mapping clones | 1,300,884 | 1,300,884 |
| Target-set clones at those two sites | 1,300,884 | 0 |
| Merge attempts / successful merge updates | 0 / 0 | 0 / 0 |
| Complete assembly | 104,608 bytes | byte-identical |

The assembly SHA-256 is `196b658c231a28e7d50fceea30157754652bbdb3a9e3b487ccada0b7a5041263`. An additional independent worktree emission took 1.880s and matched it with `cmp`. A combined instrumented/cProfile run spent 2.132 of 2.248 profiled seconds inside the original analyzer, versus 0.034 of 0.075 profiled seconds afterward. Instrumented numbers include counter/profiler overhead and are not timing baselines. The counter called `deep_target_copies` counts set allocations only at the two whole-state clone sites, not transfer or merge set allocations; `copied_names` counts mapping entries, not distinct variable names or set members. `merge_updates` counts successful successor-state replacements, not changed names.

At size 400, `MakeAdder` has **1,607 instructions**. Three clean-reference emissions took **11.254, 10.498, 10.056s**, versus **0.12799, 0.12960, 0.13020s** afterward. All **173,608 assembly bytes** match, SHA-256 `044b63c270bc54650ce54eee342c4280cd55683658c3cddb444a390dc43ccbd0`. These are sequential local observations, not randomized controlled measurements; some build verification overlapped the larger run. No portable speedup factor is claimed.

## Why not cache the CFG first?

The harness includes an opt-in, test-only `--cfg-cache` experiment. It retains the exact original edge builder, caches only an immutable successor tuple per Action for one emission, and recomputes all states and summaries. On the same size-200 input it reduced CFG builds **2 to 1**, while visits and all 1,300,884 target-set clones remained unchanged. Three uninstrumented experimental emissions took **2.066, 2.134, 2.000s**, with identical assembly. This does not establish a regression or a speedup: it shows no supported benefit in this copying-dominated workload. The production patch therefore does not add a CFG cache. Ordered numeric-constraint prefiltering is also not bundled into this change; the profile does not justify changing another algorithm.

## Why sharing cannot change analysis values

At entry to each visit, the old and new dictionaries contain equal values. The new dictionary remains a fresh dictionary, so overwriting or adding a destination cannot affect its predecessor. The only newly shared objects are tuples, booleans, and target sets already present in those values.

Within this analyzer, target sets stored in states are never mutated in place. `LOADVAR`, single-value `STORE_LIST` and `UPDATE` allocate a new set and replace the destination tuple. `CALL` allocates a new singleton or copies the current callee summary; it never stores that mutable external summary directly. Other destinations get a new empty set. A merge builds a new dictionary and new union sets for every name; it does not update either predecessor's set. `RETURN` updates the distinct `returned` accumulator, never its source set. There is no callback or escape that can mutate a stored target set while the analyzer runs.

Thus every transfer, merge comparison and returned value is unchanged, including empty/unknown facts and all-path-known booleans. The pending list and successor ordering are unchanged, so visits and successful merge updates are identical, not just the final assembly. By induction over visits and then synchronous outer rounds, the same return map, termination decision and bounded iteration count result. All state maps and the accumulator are still fresh for each analyzer call. The safety argument depends on this explicit read-only-set invariant; any future in-place mutation of a stored target set must first restore isolation or introduce an enforced immutable representation. It assumes stable valid IR, like the existing emitter.

## Independent regression and build checks

The new differential reference restores **exactly two** deep-copy sites and removes **exactly one** seedless guard. It therefore does not inherit either optimization. It compares complete assembly and identical `NativeBackendError` type/message for aliasing through `LOADVAR`/`STORE_LIST`/`UPDATE`, distinct-target reconverging diamonds, seeded loops, mixed known/scalar returns, reverse dependency call chains, and seeded recursion. The size-200 source also compares all assembly bytes with that reference, counts zero whole-state target clones, and has a Linux x86-64 executable test asserting `17\n27\n`. The two existing seedless/reference tests are retained; together the focused files passed **5 tests**.

On the branch/loop fixture, the actual clean PR #70 emitter and this follow-up emitted identical **40,874 bytes** and had identical non-copy counters: **29 analyzer calls/CFG builds, 262 body visits, 1,410 copied names, 52 merge attempts over 276 names, and 44 successful merge updates**. Only whole-state target-set clones changed, **1,410 to zero**. This verifies that convergence work was not accidentally pruned. Restoring the two copy expressions in the modified `native.py` also produced a whole-file AST identical to the separate clean PR #70 checkout.

The original hosted generator still emits **1,896,239 byte-identical bytes**, SHA-256 `715a594ad187ee9ad837ae425a23215f00b5606e09f687c7cf5b267283834c68`. A fresh `make native-hosted-bootstrap NATIVE_TARGET=x86_64-linux` and `sh tests/self_host/python_free_native_smoke.sh` passed: runtime, compiler, bytecode launcher, generator, stage-1 probe and full compiler-bytecode reproduction. This is execution with Python/toolchains blocked **after hosted construction**, not a clean-checkout Python-free rebuild. Generated `dist` artifacts are not part of this source-only PR.

The complete local suite, including all three new regressions and the retained existing tests, passed **1,038 tests, 20 skipped in 161.75s** with `.venv/bin/python -m pytest -q --durations=20`. Counts overlap the focused/build checks above; Linux execution does not establish Darwin behavior. Review acceptance requires all **eight** checks on the final documentation-updated head (push and pull-request workflows, including all macOS Python versions and Linux portability). The review PR records that exact head and its observed results; pending, cancelled, timed-out or earlier-head checks do not count as green.

## Repeat the comparison

```sh
python scripts/profile_seeded_closures.py --root /path/to/pr70 --size 200 --repeat 3 --output /tmp/before
python scripts/profile_seeded_closures.py --size 200 --repeat 3 --output /tmp/after
cmp /tmp/before.s /tmp/after.s
python scripts/profile_seeded_closures.py --root /path/to/pr70 --size 200 --instrument --profile --output /tmp/counts-before
python scripts/profile_seeded_closures.py --size 200 --instrument --profile --output /tmp/counts-after
python scripts/profile_seeded_closures.py --root /path/to/pr70 --size 200 --cfg-cache --output /tmp/cfg-experiment
```

The script writes source, complete assembly, metadata and optionally cProfile data. Counters use an AST-only clone and assert that all expected instrumentation sites exist, rather than adding overhead to production. Use separate fresh processes and the same interpreter/host; compare full bytes before interpreting timings. The retained [machine-readable measurements](seeded-closure-profile.json) distinguish a clean original compiler from the modified working tree.

## Limits and next experiment

This removes repeated set allocations, not the quadratic number of mapping entries carried through a large body. It does not prune unknown facts, change the worklist, cache dataflow across changing return/kind/capture facts, or optimize numeric alias inference or ARM64 lowering. The next bounded experiment should measure mapping sizes and merge-name work on a large **branching/looping** seeded corpus. Compare a test-only sparse representation of exactly empty/unknown facts against the independent unpruned/deep-copy reference, including missing-name joins, before considering production or a worklist redesign.

An initial workload forwarded a captured parameter through an extra Action and hit the existing capture-kind consistency rejection. The retained workload uses supported direct maker calls; this patch deliberately does not broaden capture-kind inference. Timings are observations on a synthetic local workload, not Darwin or end-to-end toolchain claims. No tests, targets, Python versions or CI jobs are removed. A full clean-checkout Python-free build and replacement of external assemblers/linkers remain unfinished; see the [independence roadmap](independence-status.md). All stacked PRs remain open and unmerged.
