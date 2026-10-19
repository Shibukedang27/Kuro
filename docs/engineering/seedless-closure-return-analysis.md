# Skip closure-return analysis only when no target can enter it

The hour-long hosted x86 generator build was spending almost all its time analyzing possible returned closures, even though this generator has no recognized closure constructors. The narrow fix skips an Action's closure-return CFG analysis only when neither a constructor nor a call to an Action with currently known returned targets can seed it. The transfer functions, CFG, merge rules, iteration bound, assembly lowering, and test orchestration are unchanged.

## What the profile measured

The baseline is the open, unmerged [PR #69](https://github.com/Shibukedang27/Kuro/pull/69) at `bd1ba3de15bd0883d32fdfdee902ad9e48b015c3`. A fresh Linux/Python 3.12.3 emission compiled `native_codegen_source("x86_64-linux")` with the existing 1 GiB generator Text heap. It has 39 Actions, 9,143 Action-body instructions, and 1,497 main instructions. The largest Action, `EmitStraightIntegerProgram`, has 4,399 instructions; there are no recognized function closure constructors.

| Measurement | Result |
| --- | ---: |
| Baseline hosted x86 emission, sampled at 20 Hz | 3755.969 seconds |
| Samples inside `analyze_action_closure_returns` | 75,155 / 75,240 (99.887%) |
| Sampling errors | 0 |
| Optimized emission, three unprofiled runs | 0.577, 0.572, 0.605 seconds |
| Optimized emission with deterministic cProfile | 1.607 seconds |
| Closure-return analyzer calls in that optimized profile | 0 |
| Complete emitted assembly | 1,896,239 bytes, byte-for-byte identical |

The dominant sampled lines copy the whole incoming state and rebuild/union per-name state at CFG merges. Even empty target sets are stored for many temporaries; repeated propagation through large Action bodies therefore repeatedly allocates and copies facts that cannot contribute a returned closure. This is not Python source compilation, assembler/linker time, or execution of the resulting generator. Baseline compilation took 0.154s; optimized compilation took 0.157–0.167s.

The earlier uninstrumented PR #69 emission was 3776.932s, consistent with the newly sampled run, but not a replacement for it. These are one sampled baseline and three unprofiled after-runs on the same Linux/Python version, with some overlapping test/build activity. They are **not a controlled benchmark**, and profiler overhead is real. No Darwin speedup ratio is inferred. [Machine-readable timings and sample locations](hosted-emitter-profile.json) retain the exact values.

## Why the fast path preserves results

The Action analysis starts with empty target state. Only two operations can introduce a nonempty target set: a constructor found in the existing `function_closure_construction_targets` map, or a destination-bearing `CALL` whose callee has a nonempty entry in the current return-target map. `LOADVAR`, one-value `STORE_LIST`, and `UPDATE` only copy existing targets. Other destination-producing operations clear them; CFG merges only union existing sets.

Without either seed, every reachable target set remains empty. The old analysis might still compute `all_returns_known` and `saw_return`, but its `returned` set is empty, so the caller cannot add that Action to `updated_returns`. Skipping it makes exactly the same contribution: none.

Only immutable constructor-owner and destination-bearing callee-name sets are cached. The intersection with **current** known returns is checked again on every synchronous fixed-point round. Forward and recursive call chains can therefore become eligible on later rounds; no dataflow result is memoized. By induction, every round's updated map, termination decision, and final map are identical to the old algorithm. Unreachable seeds may cause extra work, not incorrect skipping. Mixed known/unknown branches and all seeded Actions still run the untouched analysis.

This proves equivalence to the previous analysis, not completeness of its closure inference or support for new source constructs. It assumes valid, stable IR, as the emitter already does.

## Independent checks and regression protection

A full fresh emission from a separate, unchanged PR #69 worktree was compared with the optimized emission using `cmp`. Both have SHA-256 `715a594ad187ee9ad837ae425a23215f00b5606e09f687c7cf5b267283834c68`. This comparison uses the real baseline emitter, not an expected string produced by the optimized path.

The new differential test also constructs a test-only AST clone of the emitter with only the named seedless guard removed, restoring the unpruned fixed-point path without requiring Git during tests. During development that path was independently checked against the original emitter AST: after removing the unused cached facts, the trees are identical. Tests compare complete assembly or identical `NativeBackendError` diagnostics for direct, forwarded, branch-selected, mixed/unknown, recursive, loop, unreachable, and empty-body cases, plus four deterministic generated call graphs. Main-level `Invoke` consumers make the returned-target summaries affect observable lowering, including the mixed-return rejection.

A separate work-count regression uses `sys.setprofile`, not timing thresholds: 24 seedless Actions with 24 destination-bearing calls each must make **zero** nested closure-return analyzer calls; productive Actions must still enter it. The previous profile hook is restored afterward. No behavioral tests, target coverage, Python versions, or fixture lifetimes are removed or changed.

The final local full suite, including the strengthened new regressions, passed **1035 tests, 20 skipped in 153.75s**. The focused new file passed **2 in 0.32s**. An earlier full run passed **1033, 20 skipped in 153.39s** before collection included that file. The earlier portable selection likewise passed **749 in 75.11s** before those two new cases were included, and the backend/CLI subset passed **12 in 0.31s**. Production images were freshly rebuilt with `make native-hosted-bootstrap`; the existing Python/toolchain-blocked smoke test passed native runtime, compiler, bytecode launcher, generator, and stage-1 full compiler-bytecode reproduction. These counts overlap. Linux does not verify Darwin execution. Exact-head CI results belong in the review PR: all **eight** checks on its final documentation-updated head must succeed; pending, cancelled, and timed-out checks are not green.

## Repeat the experiment

The opt-in script writes assembly, JSON metadata, and optionally cProfile statistics. It does not build or link an executable, modify production compiler APIs, or add a runtime dependency:

```sh
python scripts/profile_hosted_emitter.py --root /path/to/baseline --output /tmp/before
python scripts/profile_hosted_emitter.py --root /path/to/after --output /tmp/after
cmp /tmp/before.s /tmp/after.s
python scripts/profile_hosted_emitter.py --output /tmp/after-profile --profile
```

For sampling, wrap the first command with `py-spy record --rate 20 --format raw --output /tmp/stacks.txt --`. Use the same interpreter and host; separate profiling from timing runs. `--output-target` chooses the ABI emitted by the compiled generator, not the x86 Linux ABI of the hosted image being measured. The baseline may remain CPU-busy for about an hour; periodic stack traces are progress evidence, not a timeout.

## Limits and the next path

This eliminates demonstrably unproductive analysis; it does not optimize seeded closure-return analysis, the main static-target propagation, numeric-alias inference, or ARM64 lowering. The next bounded performance experiment is to profile a genuinely closure-producing large Action and count body visits, copied names, and merge updates; compare cached immutable CFG construction and ordered prefiltered numeric constraints against the unchanged reference before considering a worklist change. Do not cache transfer results across changing return-kind, parameter, or capture facts.

The follow-up is stacked directly on PR #69; all PRs remain open and unmerged. Faster hosted construction is **not toolchain independence**. A clean checkout still needs Python-hosted bootstrap construction and external assembly/linking. Broader compiler/runtime lowering, chunked/indexed full-source native generation, nested/loop Decimal first-initialization joins, Action-shared storage analysis, repository-owned assembler/linker work, and genuine target release validation remain unfinished. See the [independence roadmap](independence-status.md).
