# Kuro independence status and roadmap

**Updated:** 2026-10-12
**Status:** In progress; Kuro is not yet entirely independent.

This is the running index for the independence work. Each implementation batch is published as a reviewable GitHub pull request with its own change summary, rationale, verification results, and known limits. Keep this page current as follow-up work is pushed.

## Goal and completion criteria

The goal is to make Kuro build, compile, run, test, and package itself from a clean checkout without requiring the Python-hosted compiler or reference runtime. The strict interpretation also removes reliance on a host-provided assembler and linker for native image construction. Python may remain as an optional development tool or compatibility oracle, but must not be required to build or use Kuro.

Completion also requires honest language/runtime parity, a useful standard library and developer toolchain, and verified execution on every target Kuro claims to support. A successful cross-compile alone is not evidence of runtime support.

The earlier planning estimate was approximately **7–10 months full-time-equivalent** for the strict goal, or **5–8 months** if the host assembler/linker are explicitly accepted. These are planning estimates, not delivery dates; scope and actual remaining work should be recalibrated as the roadmap is completed.

## Current state

- **All PRs #2–#39 are open and unmerged.** `main` is unchanged; the stack is submitted for inspection and review, not silently integrated.
- **GitHub CI:** PRs #2–#38 have 8/8 successful checks. PR #39’s first matrix exposed a stale-image probe; commit `0133449` fixed it, but commit `7571fc7` still crashes on the 70,008-character framed-input case across all six macOS jobs (both Linux checks pass). Replacing ARM64 suffix copying with a bounds-checked zero-copy Text view did not fix it. On `b691b66`, the same large payload passes an outer-loader-only program but fails when the VM consumes it; LLDB stops in `_platform_strlen` with `EXC_BAD_ACCESS` at `0x11170` (70,000). The next probe loads and prints the large VM input before measuring it, to isolate storage/load from `BC_LENGTH`.
- **Full-suite checkpoint:** 685 passed, 19 skipped, 0 failed on the source state published as `0133449` (2026-10-12). The zero-copy backend candidate had 5 focused tests passing and ARM64 Mach-O assembly validation; outer-loader/LLDB isolation and the new direct VMInput-read regression both pass locally on Linux. Full-suite and current-Mac revalidation remain pending.
- Linux CI builds static native production images, then blocks Python and host toolchains from `PATH` while testing `doctor`, source run/compile, bytecode execution, and codegen. PR #38 adds the stage-1 compiler bootstrap probe; PR #39 extends this to a stage-2 full-source rebuild whose bytecode matches stage 1 exactly. Clean-checkout image bootstrap remains Python-hosted, and native image construction still invokes the system assembler/linker.
- Linux x86-64 native support remains experimental and incomplete. Closures dispatch at runtime among compile-time-known targets; action-created closures carry per-instance environments allocated from a syscall-grown `brk` heap in 4 KiB pages, with no fixed 128-object cap. Integer, float, NUL-terminated text, record-reference, map-reference, and collection-reference captures are supported; indexed captured-collection reads and same-kind writes are covered, while closure values and other capture kinds remain unsupported. Closure actions can read and update record fields using literal names when the field kind was established earlier; text-field writes remain rejected because variable display lengths are not tracked. Map actions support `MapHas`, `MapGet`, and same-kind `MapSet` with literal keys whose kinds are known; text-value writes remain rejected because variable display lengths are not tracked. Arbitrary runtime field names and map keys remain unsupported inside closure actions. Action returns may merge statically known closure targets across branches when every return path is known; mixed closure/scalar paths are rejected. Allocated pages remain live until process exit; reclamation, broader control-flow cases, and dynamically created targets remain open. Main-program record fields support runtime selection among statically known literal names when selected values have one known kind. Tasks remain statically bounded and are not a parallel scheduler.

## Published work

| PR | Change | GitHub status |
|---|---|---|
| [#2](https://github.com/Shibukedang27/Kuro/pull/2) | Add cross-runtime conformance gate and release matrix | Open; 8/8 checks passing |
| [#3](https://github.com/Shibukedang27/Kuro/pull/3) | Fix multi-value assignments in the self-hosted VM | Open; 8/8 checks passing |
| [#4](https://github.com/Shibukedang27/Kuro/pull/4) | Reject malformed lockfile entries and digests | Open; 8/8 checks passing |
| [#5](https://github.com/Shibukedang27/Kuro/pull/5) | Add Linux x86-64 native execution smoke gates | Open; 8/8 checks passing |
| [#6](https://github.com/Shibukedang27/Kuro/pull/6) | Refresh the checked-in native compiler source seed | Open; 8/8 checks passing |
| [#7](https://github.com/Shibukedang27/Kuro/pull/7) | Reject negative Repeat counts in the self-hosted VM | Open; 8/8 checks passing |
| [#8](https://github.com/Shibukedang27/Kuro/pull/8) | Reject mismatched local package dependency names | Open; 8/8 checks passing |
| [#9](https://github.com/Shibukedang27/Kuro/pull/9) | Support multi-line input in the Kuro REPL | Open; 8/8 checks passing |
| [#10](https://github.com/Shibukedang27/Kuro/pull/10) | Keep generated-file cleanup from deleting tracked assembly | Open; 8/8 checks passing |
| [#11](https://github.com/Shibukedang27/Kuro/pull/11) | Broaden Linux self-hosted native codegen execution coverage | Open; 8/8 checks passing |
| [#12](https://github.com/Shibukedang27/Kuro/pull/12) | Fix Linux native text collection output | Open; 8/8 checks passing |
| [#13](https://github.com/Shibukedang27/Kuro/pull/13) | Gate native tests by host target | Open; 8/8 checks passing |
| [#14](https://github.com/Shibukedang27/Kuro/pull/14) | Fix Linux native MapHas result | Open; 8/8 checks passing |
| [#15](https://github.com/Shibukedang27/Kuro/pull/15) | Fix empty-token output in native compiler image | Open; 8/8 checks passing |
| [#16](https://github.com/Shibukedang27/Kuro/pull/16) | Lower known enums in the Linux native backend | Open; 8/8 checks passing |
| [#17](https://github.com/Shibukedang27/Kuro/pull/17) | Lower bounded records in the Linux native backend | Open; 8/8 checks passing |
| [#18](https://github.com/Shibukedang27/Kuro/pull/18) | Support known closures in the Linux native backend | Open; 8/8 checks passing |
| [#19](https://github.com/Shibukedang27/Kuro/pull/19) | Support deterministic tasks in the Linux native backend | Open; 8/8 checks passing |
| [#20](https://github.com/Shibukedang27/Kuro/pull/20) | Preserve decimal constants in Linux native runtime output | Open; 8/8 checks passing |
| [#21](https://github.com/Shibukedang27/Kuro/pull/21) | Preserve decimal spelling through VM assignments | Open; 8/8 checks passing |
| [#22](https://github.com/Shibukedang27/Kuro/pull/22) | Preserve decimal spelling in VM collections and returns | Open; 8/8 checks passing |
| [#23](https://github.com/Shibukedang27/Kuro/pull/23) | Format computed floats in the Linux x86-64 native backend | Open; 8/8 checks passing |
| [#24](https://github.com/Shibukedang27/Kuro/pull/24) | Dispatch Linux native closure calls at runtime | Open; 8/8 checks passing |
| [#25](https://github.com/Shibukedang27/Kuro/pull/25) | Add Linux Python-free native runtime CI gate | Open; 8/8 checks passing |
| [#26](https://github.com/Shibukedang27/Kuro/pull/26) | Dispatch Linux native record fields at runtime | Open; 8/8 checks passing |
| [#27](https://github.com/Shibukedang27/Kuro/pull/27) | Capture a numeric value in an escaping Linux native closure | Open; 8/8 checks passing |
| [#28](https://github.com/Shibukedang27/Kuro/pull/28) | Give Linux native captured closures per-instance environments | Open; 8/8 checks passing |
| [#29](https://github.com/Shibukedang27/Kuro/pull/29) | Support float captures in Linux native closures | Open; 8/8 checks passing |
| [#30](https://github.com/Shibukedang27/Kuro/pull/30) | Track closure targets through branch returns in Linux native actions | Open; 8/8 checks passing |
| [#31](https://github.com/Shibukedang27/Kuro/pull/31) | Grow Linux captured-closure storage with a syscall-backed allocator | Open; 8/8 checks passing |
| [#32](https://github.com/Shibukedang27/Kuro/pull/32) | Capture NUL-terminated text in Linux native closures | Open; 8/8 checks passing |
| [#33](https://github.com/Shibukedang27/Kuro/pull/33) | Capture record references and access typed fields in Linux closures | Open; 8/8 checks passing |
| [#34](https://github.com/Shibukedang27/Kuro/pull/34) | Capture maps and access typed literal keys in Linux closures | Open; 8/8 checks passing |
| [#35](https://github.com/Shibukedang27/Kuro/pull/35) | Capture collections in Linux native closures | Open; 8/8 checks passing |
| [#36](https://github.com/Shibukedang27/Kuro/pull/36) | Compose native compiler source without Python | Open; 8/8 checks passing |
| [#37](https://github.com/Shibukedang27/Kuro/pull/37) | Link Linux native images without a dynamic loader | Open; 8/8 checks passing |
| [#38](https://github.com/Shibukedang27/Kuro/pull/38) | Verify Python-free stage-one compiler bootstrap | Open; 8/8 checks passing |
| [#39](https://github.com/Shibukedang27/Kuro/pull/39) | Prove exact Python-free stage-two compiler self-rebuild | Open; outer loader passes on Mac, VMInput/BC_LENGTH crashes at `_platform_strlen`; direct-load probe pending CI |

The PR descriptions contain the detailed intent, implementation, test outcomes, and explicit limits for each batch. The dependency chain is deliberate: review and merge in dependency order if accepting the changes.

## Remaining roadmap

### 1. Close the native/runtime parity gaps

- PR #20 preserves an unchanged decimal constant's value and spelling; PR #21 carries it through scalar assignment/reload and action arguments; PR #22 carries it through collection operations and action returns. PR #23 adds freestanding computed-float formatting for ordinary finite values, including a 16/17-digit round-trip selection path, scalar/action output, and float collections. Scientific notation, extreme magnitudes, and complete shortest-decimal parity still need coverage.
- Continue differential conformance testing across the hosted compiler, Kuro-authored bytecode compiler/VM, launcher, and native backends; each mismatch should become a minimal regression test and a focused PR.
- Replace bounded per-callsite task storage with semantics that remain correct under loops and multiple task instances; determine and implement the intended scheduler behavior.
- Broaden per-instance capture beyond numeric/text scalars and record/map references; test closure-return propagation through loops and nested action calls, and add safe reclamation or resource accounting for process-lifetime heap pages.
- Expand record field selection beyond finite, compile-time-known literal sets; audit fixed-capacity collections, maps, and records for overflow, aliasing, nested elements, and error handling.
- Track unsupported IR/native operations explicitly so the compiler either lowers them correctly or reports a deliberate capability error.

### 2. Remove Python from the required build and use path

- Inventory every Python dependency in bootstrap, compiler, packaging, tests, release scripts, and developer commands.
- PR #36 adds a POSIX shell/awk compiler-source composer. PR #38 verifies the stage-1 bootstrap probe. PR #39 extends the restricted-PATH smoke gate through a stage-2 recompile of the full compiler source, requiring byte-for-byte equality with stage 1.
- The full-source input bottleneck is removed with a private `__KuroArtifactSuffix` operation that extracts the framed input suffix in linear time while preserving `BC_INPUT`'s Text semantics; the ARM64 dynamic backend now returns a bounds-checked view into immutable text rather than materializing a large copy. Stack-balance fixes in the self-hosted lowerer, explicit `BC_CONST_TEXT` tagging, and correct reserved-marker escaping are also required for exact stage-2 reproduction.
- Establish a clean-checkout bootstrap sequence that starts from checked-in Kuro source and reproducible seed artifacts, then builds the compiler/runtime using Kuro itself. Extend the Python-blocked gate from prebuilt-image use to seed construction that does not invoke Python.
- Keep the frozen reference interpreter as an optional oracle if desired; it must not be a required build dependency.

### 3. Decide and implement the native toolchain boundary

- The strict goal is to remove the required system assembler/linker dependency. Evaluate an in-house object/executable writer or another repository-owned path and document the chosen design before broad implementation.
- If host assembler/linker tools are intentionally accepted instead, narrow the independence claim and update release requirements; do not describe that configuration as fully toolchain-independent.
- Verify native artifact construction from a clean environment and record exact tool and version requirements until the strict path is complete.

### 4. Complete the standard library and developer toolchain

- Inventory the promised runtime and standard-library surface, identify missing modules and host-backed operations, and add language-level conformance tests.
- Finish package, build, test, debug, profile, and release workflows so they can operate through the self-hosted toolchain.
- Ensure diagnostics, exit statuses, artifact validation, and generated-file safety remain consistent across hosted and self-hosted paths.

### 5. Verify target platforms and releases

- The current [release matrix](../release-matrix.md) records macOS arm64, macOS x86-64 under Rosetta, Linux x86-64, and Windows as unsupported/unverified. Keep these distinctions explicit.
- Add genuine target execution and self-host gates before promoting any target from experimental to supported; cross-compilation alone is insufficient.
- For each supported target, require clean dependency installation, compiler/runtime conformance, native image construction from source, stdout/stderr/exit-status checks, self-compilation where applicable, and retained artifact checksums/logs.

## Next concrete step

Next, move seed-image construction out of Python and verify a clean-checkout bootstrap from reproducible, repository-owned seeds; the current smoke test still starts from prebuilt native images. Then remove the remaining host assembler/linker dependency. In parallel, continue closure parity for loop/nested-action returns, reclamation/accounting, closure-valued captures, and non-literal record/map access; scientific notation and extreme binary64 formatting also remain open. The current PR stack is not completion of the independence goal.
