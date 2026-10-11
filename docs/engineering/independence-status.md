# Kuro independence status and roadmap

**Updated:** 2026-10-11  
**Status:** In progress; Kuro is not yet entirely independent.

This is the running index for the independence work. Each implementation batch is published as a reviewable GitHub pull request with its own change summary, rationale, verification results, and known limits. Keep this page current as follow-up work is pushed.

## Goal and completion criteria

The goal is to make Kuro build, compile, run, test, and package itself from a clean checkout without requiring the Python-hosted compiler or reference runtime. The strict interpretation also removes reliance on a host-provided assembler and linker for native image construction. Python may remain as an optional development tool or compatibility oracle, but must not be required to build or use Kuro.

Completion also requires honest language/runtime parity, a useful standard library and developer toolchain, and verified execution on every target Kuro claims to support. A successful cross-compile alone is not evidence of runtime support.

The earlier planning estimate was approximately **7–10 months full-time-equivalent** for the strict goal, or **5–8 months** if the host assembler/linker are explicitly accepted. These are planning estimates, not delivery dates; scope and actual remaining work should be recalibrated as the roadmap is completed.

## Current state

- **All PRs #2–#28 are open and unmerged.** `main` is unchanged; these branches are submitted for inspection and review, not silently integrated.
- **GitHub CI:** PRs #2–#27 have 8/8 successful checks; PR #28's current check state is available on its linked pull-request page.
- **Local Linux x86-64 full suite on the current stacked branch:** 649 passed, 19 skipped, 0 failed.
- Linux CI now builds native production images with Python, then blocks Python and host compiler tools from `PATH` while testing `doctor`, source run/compile, bytecode execution, and codegen. This proves the built images' use path only; clean-checkout image bootstrap remains Python-hosted, and native image construction still invokes the system assembler/linker.
- Linux x86-64 native support remains experimental and incomplete. Closures dispatch at runtime among compile-time-known targets; straight-line action-created closures now carry per-instance environments in a fixed pool of 128 objects. Integer captures are supported and non-integer captures are rejected; pool exhaustion exits with status 1, and reclamation, branch-merged closure returns, and dynamically created targets remain open. Record fields support runtime selection among statically known literal names when selected values have one known kind; arbitrary runtime field names remain unsupported. Tasks remain statically bounded and are not a parallel scheduler.

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
| [#28](https://github.com/Shibukedang27/Kuro/pull/28) | Give Linux native captured closures per-instance environments | Open; check state on the PR page |

The PR descriptions contain the detailed intent, implementation, test outcomes, and explicit limits for each batch. The dependency chain is deliberate: review and merge in dependency order if accepting the changes.

## Remaining roadmap

### 1. Close the native/runtime parity gaps

- PR #20 preserves an unchanged decimal constant's value and spelling; PR #21 carries it through scalar assignment/reload and action arguments; PR #22 carries it through collection operations and action returns. PR #23 adds freestanding computed-float formatting for ordinary finite values, including a 16/17-digit round-trip selection path, scalar/action output, and float collections. Scientific notation, extreme magnitudes, and complete shortest-decimal parity still need coverage.
- Continue differential conformance testing across the hosted compiler, Kuro-authored bytecode compiler/VM, launcher, and native backends; each mismatch should become a minimal regression test and a focused PR.
- Replace bounded per-callsite task storage with semantics that remain correct under loops and multiple task instances; determine and implement the intended scheduler behavior.
- Broaden per-instance capture beyond integers and straight-line closure returns; add safe reclamation or make the fixed 128-object allocation limit configurable.
- Expand record field selection beyond finite, compile-time-known literal sets; audit fixed-capacity collections, maps, and records for overflow, aliasing, nested elements, and error handling.
- Track unsupported IR/native operations explicitly so the compiler either lowers them correctly or reports a deliberate capability error.

### 2. Remove Python from the required build and use path

- Inventory every Python dependency in bootstrap, compiler, packaging, tests, release scripts, and developer commands.
- Establish a clean-checkout bootstrap sequence that starts from checked-in Kuro source and reproducible seed artifacts, then builds the compiler/runtime using Kuro itself.
- Extend the Python-blocked runtime gate from prebuilt-image use to a clean-checkout bootstrap that does not invoke Python at all.
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

Continue closure parity with branch-sensitive closure returns, broader captured value kinds, and reclamation or configurable heap limits; record parity by supporting arbitrary runtime field names. Establish a clean-checkout bootstrap that does not require Python; scientific notation/extreme binary64 formatting and the strict assembler/linker-independence decision also remain open. The current PR stack is not completion of the independence goal.
