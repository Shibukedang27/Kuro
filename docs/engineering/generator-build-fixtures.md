# Reuse the macOS x86 generator, not its process state

The macOS x86-64 integration test rebuilt the same native Kuro generator for each of six parameterized inputs. A module-scoped fixture now builds that executable once from the current checkout. All six cases still start a separate generator process, assemble/link its output, run the resulting image, and assert the same stdout. Their `tmp_path` workspaces remain separate.

This is test orchestration only: no compiler, Kuro source, generated-code semantics, runtime, dependency, target matrix, or production-image build path changes. No prebuilt image or persistent cache is introduced. The fixture explicitly retains both `target="x86_64-macos"` and `output_target="x86_64-macos"`; these are not interchangeable with the ARM64-hosted Linux-output fixture.

## What the profiling found

The verified starting checkout was PR #68 head `3edffb52d35d168dc7791cb74f827dc4c1e3a600`, clean, open, and unmerged. Its [completed macOS Python 3.10 run](https://github.com/Shibukedang27/Kuro/actions/runs/39144085916/job/117805685104) passed **975 tests, 77 skipped in 18,703.27 seconds (5h11m43s)**. Python 3.12 hit GitHub's six-hour job limit twice; that is timeout/incomplete evidence, not a test assertion failure or a green gate. At the start of this optimization, four of eight final-head checks had succeeded; subsequent macOS reruns were still in progress.

A full local Linux/Python 3.12.3 suite, instrumented with lightweight `perf_counter` wrappers around the existing build/emission entry points, isolated the remaining cost:

| Stage | Measured seconds |
| --- | ---: |
| Fresh Linux-output generator build | 3777.579 |
| Its `build_native` stage | 3777.408 |
| Its `emit_x86_64_linux` stage | 3776.932 |
| Entire local suite | 3946.43 |

These are nested, **not additive**, timings. More than 99.98% of that generator build was spent inside hosted x86 emission; source compilation and host assembly/linking were not the dominant stages. The fixture setup accounts for about 95.72% of the local suite's elapsed time. The macOS x86 emitter delegates lowering to the same x86 Linux emitter before adapting Darwin assembly. These Linux measurements identify an avoidable repeated operation; they are not a measurement of Darwin execution or a promise of identical host timings.

## Before and after

| Work per macOS pytest process | PR #68 | This change |
| --- | ---: | ---: |
| x86-macOS generator images built for the six cases | 6 | 1 |
| All successful full generator image builds | 8 | 3 |
| x86-macOS behavioral cases executed | 6 | 6 |
| Fresh processes for those cases | 6 | 6 |

The total includes one ARM64 artifact-consumption generator and one ARM64-hosted/Linux-output generator. The unsupported-target rejection does not construct an image. There is also a separate ARM64 source-emission/assembly test, which remains unchanged and is not counted as a linked generator build.

The x86-macOS build count falls by **83.33%**, and total generator-image construction by **62.5%** per macOS process. With Python 3.10/3.11/3.12 and both push/PR workflows unchanged, that removes five builds per process, thirty across the six macOS jobs. These are build-count reductions, **not a claimed wall-clock speedup**. Actual hosted before/after wall times must be read from the final-head CI logs; scheduling, Python version, host variation, and the three remaining builds still matter.

The new `test_codegen_fixtures.py` uses pytest's built-in `pytester` plugin and a cheap build spy in isolated pytest subprocesses. It consumes the real fixture and actual six-case parameter list, checks the integration signature requests that fixture, verifies exactly one build with the exact host/output target pair, then repeats in a second pytest session and requires a fresh image path. The spy is confined to the child process; the native integration suite still performs real builds. This guards fixture lifetime and stale-image reuse without adding another costly generator build. macOS CI adds `--durations=20` for setup/call visibility; no tests or assertions are removed.

## Local verification

- Full suite with fresh native generator and stage timing: **1033 passed, 20 skipped in 3946.43s (1h05m46s)**.
- Exact Linux portable-suite selection: **749 passed in 78.88s**.
- Linux backend/CLI selection: **12 passed, 69 deselected in 0.32s**.
- Final fixture regression rerun: **1 passed in 1.45s**, including two child pytest sessions with six consumers each.
- Native-codegen collection remains **178 tests**. The six Darwin x86 cases remain skipped on Linux, as before; Linux success does not verify Rosetta/Darwin execution.
- `git diff --check`: clean. Counts overlap; do not add the gates together.

The full-suite run began before the final regression-only strengthening to consume the integration's actual parameter list; that strengthened regression was rerun successfully afterward. Production and native integration sources were unchanged during the run.

## CI acceptance and the next path

[PR #69](https://github.com/Shibukedang27/Kuro/pull/69) is stacked directly on PR #68; keep both open and unmerged. All **eight** checks on the final documentation-updated head are required: six macOS matrix checks across push/PR workflows and both Linux portability checks. Until those finish successfully, the optimization is locally verified but **not complete**. Exact-head conclusions and measured hosted runtimes belong in the PR verification record; an earlier commit's green result is not transferable. A timeout, cancellation, queued job, or running job is never reported as green.

This change removes duplicate builds; it does not accelerate a single hosted x86 emission. Next profile inside `emit_x86_64_linux` (including its fixed-point dataflow analyses) before attempting any algorithmic change, retaining closure/kind/control-flow conformance. Other repeated launcher/compiler builds and separate Linux pytest/production-build invocations are left intact; sharing across those boundaries requires its own freshness and lifecycle design. Preserve genuine ARM64 macOS execution, x86-macOS execution, and Linux generated-code coverage rather than pruning the Python matrix to fit a timeout.

Overall independence remains unfinished: a clean checkout still needs Python-hosted bootstrap construction and host assembler/linker tools. Nested/loop Decimal first-initialization joins, Action-shared kind analysis, broader runtime lowering, and repository-owned native image construction remain separate work. See the [independence roadmap](independence-status.md).
