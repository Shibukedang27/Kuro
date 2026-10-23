# `ComputeLineCol` integer parameter contract

This follow-up is stacked directly above draft/open PR #128, exact parent head `47d8a44edd8d35ec52555becdd997eee4dd17ba1`. It gives the fixed bootstrap compiler's `ComputeLineCol.TargetPos` parameter an explicit `Integers` type. It does **not** add general inference for untyped (`NONE`) parameters, and does not change the native generator's fail-closed policy for them.

## The complete fixed-composition call set

The bootstrap composer includes the lexer, filtered parser, length checker, filtered lowerer and bytecode encoder, compiler driver, and native-compiler entry point. Its shell output is byte-for-byte equal to `compiler.self_host.native_compiler_source()`. The exact composed program has two direct calls to `ComputeLineCol`:

| Caller | Argument alias | Producer |
| --- | --- | --- |
| `RecordDiag` | `RecordDiag_Pos` | `CurDiagPos` returns either `Get TokenStarts TokPos` or `Length Source`. |
| Length-check main flow | `LCOffset` | `Get TokenStarts LCPos`. |

The integer provenance is bounded to this fixed program. In the lexer, `Pos` starts at `0`, `TokStartPos` copies `Pos`, and every `TokenStarts` append uses `TokStartPos`; the lexer advances `Pos` arithmetically. `Length Source` is also an integer. Neither caller passes a token value or a source string to `ComputeLineCol`.

The two forwarding names are ordinary globals because Kuro action parameters are frame-local while other variable assignments are shared. The composed IR has exactly one write to `RecordDiag_Pos` and one to `LCOffset`; each is loaded immediately for the corresponding direct call. The `TargetPos` formal itself is in the action frame. `ComputeLineCol` has no action calls in its body, so its shared scratch variables cannot be interleaved by a callback or re-entrant call while it scans the source.

The composed program contains no `MakeClosure`, `Invoke`, `Spawn`, or `Await` call route. Calls to `ComputeLineCol` are static action calls, not function-valued aliases. Parser recursion can reach diagnostic recording, but there is no recursive route into `ComputeLineCol` while its body is running.

There is one additional source-tree call outside the production composer: `self_host/resolver.kuro` calls `ComputeLineCol` with `RecordSemDiag_Off`, returned by `StartAt`. `StartAt` returns either a `TokenStarts` offset or `Length Source`, also integer. The resolver is not part of the fixed compiler composition.

## Why this is not general `NONE` inference

An untyped Kuro action parameter remains dynamically polymorphic. A Kuro-authored VM regression calls the same untyped `Echo Value` action with an integer, text, and decimal and preserves all three values. The native code generator therefore still rejects generic untyped formals rather than guessing a kind from a subset of callers.

Only this internal fixed action is now declared as `Integers`. The native emitter accepts only an integer stack value for that parameter; Text, Decimal, and mixed integer-plus-incompatible call sets fail with empty assembly. This explicit contract is supported by the complete fixed callsite/write-set analysis above, not by a new general-purpose alias, effect, dynamic-dispatch, or type-inference analysis. Do not treat it as a guarantee for arbitrary Kuro programs or future call paths.

## What remains blocked

The Kuro-authored compiler processed its complete composed source and emitted 9,118 bytecode tokens, 73 function blocks, and 294 call blocks. The target formal is emitted as `Integers`; the first remaining untyped formal is `RecordDiag.Code`. A temporary native codegen image, built through the existing hosted toolchain path, rejected that full artifact with status 1 and empty stdout/stderr. This confirms no partial assembly was emitted, but is not evidence of independent image construction.

The full compiler artifact therefore remains unable to produce a native compiler image. The existing Python-hosted bootstrap seed and Clang/LLVM assembly/linking dependencies remain; strict toolchain independence is not claimed. No generated image or temporary audit artifact is checked into the repository.
