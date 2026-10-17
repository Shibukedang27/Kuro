# Freestanding x86 Decimal printing in Kuro codegen

The Kuro-authored native generator can now lower Decimal `BC_PRINT` on `x86_64-linux` and `x86_64-macos`. This closes the computed-value and typed Action-parameter/return printing gap on the x86 target family without introducing libc or a Python dependency into the generated programs.

## What changed and why

`BC_PRINT` inspects the operand's tracked stack kind. Decimal values call an emitted `_kuro_print_float`; Integer and Text printing retain their existing paths. A program containing Decimal print instructions gets one shared formatter, including when the instruction occurs inside an Action.

The formatter is a snapshot of the repository's existing freestanding x86 backend implementation in `compiler/native.py`. Its binary80 power-of-ten table is frozen as 3,420 bytes in Kuro Text literals, so producing assembly does not need a Python-generated table at runtime. Linux and Darwin use their respective direct write syscalls. Bounded Text chunks avoid hundreds of extra compiler IR operations and repeated output concatenations.

The Action regression also exposed a pre-existing macOS x86 section bug: Action bodies emitted `.section .text`. They now select `.section __TEXT,__text` for that target, matching its main program and printer sections.

## Verification

Final local gates on Linux x86-64, Python 3.12:

- `python -m pytest -q tests/self_host/test_native_codegen.py --durations=10`: **158 passed, 18 skipped**, in **2728.24 seconds (45m28s)**. This includes a fresh compiled Kuro generator, both x86 targets' cross-assembly, ARM64 backend emission, the 4096/4097 token boundary, and existing ABI/control-flow regressions. Generator fixture setup took **2679.19 seconds**; hosted build performance remains an open engineering cost.
- `python -m pytest -q tests/self_host/test_vm_cross.py`: **22 passed**, in **7.86 seconds**.
- `git diff --check`: passed before publication.

The compiled Linux generator consumes framed bytecode, emits assembly, and produces an executable linked with `clang -nostdlib`. The new runtime regression checks Decimal printing inside an Action and after its return, fixed-form values, an integral Decimal retaining `.0`, `0.1 + 0.2`, small/large scientific notation, a negative value, signed zero, positive/negative infinity, and NaN. Stdout is checked exactly and stderr must be empty.

A macOS-only executable regression covers Decimal Action-parameter and return printing through a native generator image. Linux locally validates the Mach-O assembly, not its execution; GitHub's macOS jobs provide that execution evidence. The Linux portability workflow now explicitly runs the new compiled-generator regression using its existing shared fixture. Final-head GitHub results are attached to the stacked review PR; a passing older head is not a substitute.

An early unchunked prototype's test session was terminated at the background wait limit and is not counted as a passed gate. Its completed image passed a subsequent direct probe; after compacting the Text appends, the full fresh-build gate above completed successfully. An independent review confirmed that the formatter instructions and frozen table match the hosted implementation except for the intended target-specific syscall substitution, and its requested Action-parameter/return coverage was added.

## Limits and next path

This is parity with the existing x86 formatter, not proof of universal shortest-decimal parity. It inherits the known high-precision fallback that can print longer, numerically equivalent decimal strings for some values. The unchanged literal-only fast path can preserve source spelling; this slice does not redefine that behavior.

Apple ARM64 computed/parameter Decimal printing remains explicitly rejected rather than silently treated as Integer output or delegated to libc. Its literal-only direct-output fast path is unchanged. Non-parameter Decimal mutation, broader native bytecode lowering, and full hosted-versus-self-hosted conformance also remain unfinished.

The next bounded slice is a freestanding Apple ARM64 Decimal formatter with the same explicit display contract and real target execution coverage. Then broaden Decimal differential cases and general compiler/runtime lowering. The generator is still built through the hosted bootstrap and generated assembly still requires a host assembler/linker. Clean-checkout Python-free production-image rebuilding and a repository-owned native image construction path remain open; the independence goal is not complete.
