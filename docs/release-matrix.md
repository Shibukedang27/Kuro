# Kuro support and verification matrix

This matrix separates implementation claims from verified release guarantees.
A target is not considered supported merely because its binary can be cross-built.

## Runtime and compiler paths

| Path / target | Repository evidence | Release status |
|---|---|---|
| Hosted compiler and IR interpreter | Full pytest suite configured on macOS with Python 3.10, 3.11, and 3.12 | Development path; latest CI result must be checked on GitHub |
| Kuro-authored compiler and bytecode VM | Self-hosted lexer, parser, lowering, bytecode encoder, VM, and runtime with cross-tests; append-built and literal multi-value-assignment collections are covered | Experimental; bootstrap still uses the hosted implementation as its execution harness, and collection aliasing and nested elements remain incomplete |
| Python-free compiler and bytecode launcher images | Checked-in `dist/` images and `Makefile` release-check/doctor flow | Experimental; clean rebuild from source is not yet established as a release guarantee |
| macOS arm64 native backend | In-tree native lowering and native-codegen tests | Supported subset only; not every Kuro construct has native lowering |
| macOS x86-64 under Rosetta | Architecture audit records a full compiler self-compile and second-stage execution path | Documented milestone; rerun the release gate before each release |
| Linux x86-64 native output | Ubuntu CI assembles dynamic IR, links and runs Kuro-generated arithmetic/loop programs, and runs the native artifact launcher with multi-value reassignment | Bounded runtime smoke gate; keep experimental until exact-commit CI is green and broader compiler/runtime coverage is established |
| Windows | No Windows execution target is established in the current architecture audit | Unsupported / unverified |

## Required release evidence

Before describing a target as release-supported, CI should demonstrate all of the following on that target or a genuine runner for it:

1. Install dependencies from a clean checkout.
2. Run the applicable compiler and runtime conformance suite.
3. Build the target's native images from source.
4. Execute generated programs and verify stdout, stderr, and exit status.
5. Run self-compilation and second-stage execution where the target supports the bootstrap.
6. Upload build logs and checksums for release artifacts.

Cross-compilation is useful evidence that a backend can emit and link an image. It is not evidence that the image executes correctly on the target operating system.

## Current verification limitation

This matrix describes the checked-in workflow and architecture documentation. It does not assert that the latest CI run is green. Check the GitHub Actions run for the exact commit being released and retain its logs as release evidence.

The Kuro-authored VM's `BC_STORE_MULTI` now preserves the values in a
multi-value assignment such as `Items = 1, 2, 3;`. The cross-runtime corpus
checks output order, length, indexing, and replacement on reassignment for
scalar collection items. Nested collection elements remain unsupported, and
assigning an existing collection still copies its items rather than preserving
aliasing. This closes the previously documented assignment gap, not complete
collection parity; it also does not remove the hosted bootstrap harness from
the current test path.

Update this document whenever CI adds or removes a tested target, or when a documented milestone becomes an automated release gate.
