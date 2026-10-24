# Native self-hosting: verified Text gates

## Current result

The verified baseline is draft/open PR [#135](https://github.com/Shibukedang27/Kuro/pull/135), exact head `d8cfd9b0c8ec7b8eaa525ca538af66e2fa309a6d`, directly above PR #134 at `f58a87c4d93a23a2f27113260c3dce78479a22e6`. All eight exact-head CI checks passed. The exact compiler self-bytecode artifact contains **9,118 tokens** (about 88 KB); the source composition audit reports **9,119 lines**, 73 functions, and 294 calls. These are different artifacts. The native loader ceiling is 65,536 tokens; the 4,096-token checks are work bounds, not the first blocker.

This follow-up gives four closed parser helpers explicit `Text` parameter contracts: `RecordDiag.Message`, `IsWord.ExpectedWord`, `ExpectKind.ExpectedKind`, and `ExpectWord.ExpectedWord`. It is a language-level contract for this fixed compiler composition, not general `NONE` inference, a global Text tag, or a backend-lowering claim. The exact source/IR regression pins all six `RecordDiag` callers, all 28 `ExpectKind` calls, all 18 `ExpectWord` calls, and all 38 `IsWord` calls by scope and argument: 37 `IsWord` calls pass Text literals, and the remaining one forwards `ExpectWord.ExpectedWord`. A separate boundary test confirms that an explicitly Text-typed diagnostic Action containing `BC_APPEND` still fails with empty assembly; generic untyped Action parameters remain rejected.

Fresh x86-64 Linux native images rebuilt from this source. The Python/toolchain-blocked smoke passed, including stage-1 compilation and byte-for-byte reproduction of the full 9,118-token compiler bytecode. Feeding that exact artifact to the fresh native code generator still exits 1 and emits zero assembly bytes. Kuro is not yet self-hosting its native code generator, and this increment does not claim otherwise.

## Why these contracts are safe and narrow

The six fixed `RecordDiag` callers are three immediate Text literals, two dynamic messages built from the explicitly Text-typed `ExpectedKind` and `ExpectedWord` formals, and one token-dependent message. The latter flows from `CurValue`/`PeekValue` through `TokenValues`, which is declared `Text`; end-of-input returns the empty Text value. Every fixed call to `ExpectKind` and `ExpectWord` supplies a quoted token or word. Every direct `IsWord` call supplies a Text literal except the single forwarding call from the now-typed `ExpectWord` parameter. The composed source has no closure, invoke, spawn, or await route that can add an indirect caller.

The normal Kuro type checker enforces these explicit parameter contracts at call sites. The general rule for an untyped parameter is unchanged: it accepts dynamically typed values, so the native generator continues to reject generic `NONE` rather than guess. The contract change does not make Action-local concatenation or collection mutation safe by itself.

## Remaining blockers

1. **Native collection append:** `RecordDiag` appends codes, line/column values, and messages to diagnostic collections. Native `BC_APPEND` has no lowering/storage path. A correct implementation must preserve the language's collection semantics, align related diagnostic columns, and define capacity, allocation, and failure behavior; accepting Text pointers alone would not suffice.
2. **Action-local dynamic Text concatenation:** `ExpectKind`, `ExpectWord`, and `ParseStatement` construct messages with `+` inside Actions. The existing native concatenation path admits bounded literal chains in top-level straight-line code, not these dynamic Action expressions. Any extension needs explicit bounds, reentrant allocation, aliasing, lifetime, and failure guarantees; a shared static scratch buffer would be unsafe under recursion or nested calls.
3. **Resource envelope:** a valid 9,216-token stress input exhausted the 1 GiB arena at about 1.05 GiB peak RSS; the accepted 4,096-token case used about 786 MiB. Do not raise work or memory limits without separate evidence.
4. **Strict toolchain independence:** Python-seeded native image construction and Clang/LLVM assembly/linking are still required.

The next useful backend step should address diagnostic collection append semantics before assuming that typed signatures or the existing scoped shared-Text argument proof enable native full-compiler generation. Exact compiler-bytecode reproduction is bootstrap continuity after hosted image seeding, not proof of a Python-free clean-checkout toolchain.
