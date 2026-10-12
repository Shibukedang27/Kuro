# Kuro independence status and roadmap

**Updated:** 2026-10-12
**Status:** In progress; Kuro is not yet entirely independent.

This is the running index for the independence work. Each implementation batch is published as a reviewable GitHub pull request with its own change summary, rationale, verification results, and known limits. Keep this page current as follow-up work is pushed.

## Goal and completion criteria

The goal is to make Kuro build, compile, run, test, and package itself from a clean checkout without requiring the Python-hosted compiler or reference runtime. The strict interpretation also removes reliance on a host-provided assembler and linker for native image construction. Python may remain as an optional development tool or compatibility oracle, but must not be required to build or use Kuro.

Completion also requires honest language/runtime parity, a useful standard library and developer toolchain, and verified execution on every target Kuro claims to support. A successful cross-compile alone is not evidence of runtime support.

The earlier planning estimate was approximately **7–10 months full-time-equivalent** for the strict goal, or **5–8 months** if the host assembler/linker are explicitly accepted. These are planning estimates, not delivery dates; scope and actual remaining work should be recalibrated as the roadmap is completed.

## Current state

- **All PRs #2–#49 are open and unmerged.** `main` is unchanged; the stack is submitted for inspection and review, not silently integrated.
- **GitHub CI:** PRs #2–#43 have 8/8 successful checks. PR #39’s macOS crash was narrowed to ARM64 dynamic output: the 4 KiB scalar/pointer cutoff misclassified ordinary large integer output as a Text pointer, while Linux uses native memory-range checks. Commit `6e4b564` uses Darwin’s 4 GiB user-pointer floor and 48-bit user-address ceiling; regression coverage prints integer `70000` and verifies the 70,008-character `BC_LENGTH` result. PR #39’s final head `0113a86` is verified green across all six macOS jobs and both Linux portability jobs. PR #40’s head `bc11142`, PR #41’s head `0de3768`, and PR #42’s head `c53c5fe` are verified green across all eight checks. PR #43’s head `54fbe2b` is verified 8/8 green; PR #44’s implementation commit `8e9affc` also passed all eight checks. PR #45’s final head `9134b5b`, PR #46’s implementation commit `0ae6cb6`, PR #47’s implementation commit `38decef`, PR #48’s final head `56ad510`, and PR #49’s implementation commit `bd51ea0` each passed 8/8 checks.
- **Full-suite checkpoint:** 729 passed, 19 skipped, 0 failed on the PR #49 local candidate (2026-10-12); focused native-codegen module 58 passed, 17 skipped. The PR #48 baseline was 727 passed, 19 skipped with 56 native-codegen passes and 17 skips; PR #47 previously passed 725/19.
- Linux CI builds static native production images, then blocks Python and host toolchains from `PATH` while testing `doctor`, source run/compile, bytecode execution, and codegen. PR #38 adds the stage-1 compiler bootstrap probe; PR #39 extends this to a stage-2 full-source rebuild whose bytecode matches stage 1 exactly. PR #40 adds POSIX shell source composition with byte-for-byte parity tests against the canonical Python helpers. PR #41 adds direct calls to Actions with one `Integers` parameter; PR #42 adds zero-parameter Actions; PR #43 adds one supported integer `If`/`Else` with one returning arm per branch; PRs #45–#46 extend direct integer calls to two and three parameters; PR #47 adds one integer local per Action; PR #48 adds writeback to existing integer parameter slots; PR #49 supports multiple distinct integer locals with per-function name ranges. A full Python-free native image rebuild remains deferred: the Kuro-owned codegen still cannot lower the compiler/runtime’s general bytecode. `make native` therefore remains on the hosted builder rather than exposing a failing path.
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
| [#39](https://github.com/Shibukedang27/Kuro/pull/39) | Prove exact Python-free stage-two compiler self-rebuild | Open; 8/8 checks passing |
| [#40](https://github.com/Shibukedang27/Kuro/pull/40) | Add POSIX shell source-composition parity for native bootstrap inputs | Open; 8/8 checks passing |
| [#41](https://github.com/Shibukedang27/Kuro/pull/41) | Lower direct calls to one-parameter integer Actions in Kuro native codegen | Open; 697 passed, 19 skipped; 28 focused tests pass; 8/8 checks passing |
| [#42](https://github.com/Shibukedang27/Kuro/pull/42) | Add zero-argument integer-returning Actions to Kuro native codegen | Open; hosted tests, ARM64 cross-assembly, compiled Linux execution; 8/8 checks passing |
| [#43](https://github.com/Shibukedang27/Kuro/pull/43) | Support fully returning If/Else branches in integer Actions in Kuro native codegen | Open; 9 hosted tests, ARM64 cross-assembly, compiled Linux integration, and 8/8 checks passing |
| [#44](https://github.com/Shibukedang27/Kuro/pull/44) | Add scientific notation and binary64 round-trip formatting to Linux native output | Open; 707 passed, 19 skipped; native tests 78 passed, 1 skipped; implementation commit `8e9affc` passed 8/8 checks |
| [#45](https://github.com/Shibukedang27/Kuro/pull/45) | Support two-integer-parameter Actions in Kuro native codegen | Open; 714 passed, 19 skipped; native-codegen tests 43 passed, 17 skipped; 8/8 checks passing |
| [#46](https://github.com/Shibukedang27/Kuro/pull/46) | Support three-integer-parameter Actions in Kuro native codegen | Open; 719 passed, 19 skipped; native-codegen tests 48 passed, 17 skipped; 8/8 checks passing |
| [#47](https://github.com/Shibukedang27/Kuro/pull/47) | Lower one integer local variable per Action in Kuro native codegen | Open; 725 passed, 19 skipped; native-codegen tests 54 passed, 17 skipped; 8/8 checks passing |
| [#48](https://github.com/Shibukedang27/Kuro/pull/48) | Support assignments back to integer Action parameters in Kuro native codegen | Open; 727 passed, 19 skipped; native-codegen tests 56 passed, 17 skipped; 8/8 checks passing |
| [#49](https://github.com/Shibukedang27/Kuro/pull/49) | Support multiple integer locals per Action in Kuro native codegen | Open; 729 passed, 19 skipped; native-codegen tests 58 passed, 17 skipped; 8/8 checks passing |

The PR descriptions contain the detailed intent, implementation, test outcomes, and explicit limits for each batch. The dependency chain is deliberate: review and merge in dependency order if accepting the changes.

## Remaining roadmap

### 1. Close the native/runtime parity gaps

- PR #20 preserves an unchanged decimal constant's value and spelling; PR #21 carries it through scalar assignment/reload and action arguments; PR #22 carries it through collection operations and action returns. PR #23 adds freestanding computed-float formatting for ordinary finite values, including scalar/action output and float collections. PR #44 adds Linux x86-64 scientific notation using an x87 binary80 scale table, checks candidate decimals for binary64 round-trip, and searches shorter significands before using a high-precision fallback. Regressions cover small and large exponent output, computed division, subnormals, maximum finite, infinity, and NaN. A deterministic 15-value exponent probe round-tripped all 15 values and matched hosted text exactly for 13; two values and some extreme inputs still use longer equivalent decimals. Complete shortest-decimal parity and broader edge coverage remain open.
- Continue differential conformance testing across the hosted compiler, Kuro-authored bytecode compiler/VM, launcher, and native backends; each mismatch should become a minimal regression test and a focused PR.
- Replace bounded per-callsite task storage with semantics that remain correct under loops and multiple task instances; determine and implement the intended scheduler behavior.
- Broaden per-instance capture beyond numeric/text scalars and record/map references; test closure-return propagation through loops and nested action calls, and add safe reclamation or resource accounting for process-lifetime heap pages.
- Expand record field selection beyond finite, compile-time-known literal sets; audit fixed-capacity collections, maps, and records for overflow, aliasing, nested elements, and error handling.
- Track unsupported IR/native operations explicitly so the compiler either lowers them correctly or reports a deliberate capability error.
- The Kuro-authored native codegen handles literal-text output, a limited integer/control-flow subset, direct calls to integer-returning Actions with zero parameters or exactly one, two, or three `Integers` parameters, writeback to those existing parameter slots through `BC_STORE_LIST`, and multiple distinct integer locals per Action via `BC_STORE_LIST`/`BC_LOADVAR` (32 local slots maximum, with names isolated per function). It supports a simple `If`/`Else` in an Action when both arms return one integer. Mixed parameter types, four or more parameters, Action-local `BC_UPDATE`/`BC_ADD`, declared local types, indirect/closure calls, and the general function/action bytecode needed by the compiler/runtime remain unsupported. Expand it under hosted-versus-Kuro differential tests before relying on it to rebuild production images.

### 2. Remove Python from the required build and use path

- Inventory every Python dependency in bootstrap, compiler, packaging, tests, release scripts, and developer commands.
- PR #36 adds a POSIX shell/awk compiler-source composer. PR #38 verifies the stage-1 bootstrap probe. PR #39 extends the restricted-PATH smoke gate through a stage-2 recompile of the full compiler source, requiring byte-for-byte equality with stage 1.
- The full-source input bottleneck is removed with a private `__KuroArtifactSuffix` operation that extracts the framed input suffix in linear time while preserving `BC_INPUT`'s Text semantics; the ARM64 dynamic backend now returns a bounds-checked view into immutable text rather than materializing a large copy. Stack-balance fixes in the self-hosted lowerer, explicit `BC_CONST_TEXT` tagging, and correct reserved-marker escaping are also required for exact stage-2 reproduction.
- Establish a clean-checkout bootstrap sequence that starts from checked-in Kuro source and reproducible seed artifacts, then builds the compiler/runtime using Kuro itself. PR #40 establishes shell-based source composition; PRs #41–#43 and #45–#49 add only narrow integer Action/call/control-flow/local subsets. Building native compiler/runtime images remains blocked until Kuro-owned codegen can lower their general bytecode. Linux currently retains the Python-hosted image bootstrap.
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

PR #43’s eight-check gate is now green. Next, extend Kuro-owned codegen beyond direct zero/one-parameter calls and one simple conditional return to the functions, closures, records/maps, and runtime constructs required by the compiler. PR #44 advances freestanding scientific formatting and binary64 round-trip behavior; shortest-decimal parity remains open. Then prove a full image rebuild from committed native seeds with Python blocked. After that, provision a runnable Linux x86-64 stage-0 seed and design a repository-owned assembler/linker path. Continue closure parity for loop/nested-action returns, reclamation/accounting, closure-valued captures, and non-literal record/map access. The current PR stack is not completion of the independence goal.
