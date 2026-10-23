# Keep `RecordDiag.Message` untyped until Text paths are sound

This follow-up is stacked directly above draft/open PR [#130](https://github.com/Shibukedang27/Kuro/pull/130), at parent head `fb58bf404aae61f9ceb1600b262a483a033b01c2`. It audits the next untyped formal, `RecordDiag.Message`, and deliberately does not annotate it or widen general kind inference.

## Every fixed message caller produces Text

The exact composed source from `compiler.self_host.native_compiler_source()` compiles to 73 functions and 294 static call blocks. Its only six `RecordDiag` calls are in `self_host/parser.kuro`:

| Caller | Source line | Message producer |
| --- | ---: | --- |
| `ExpectKind` | 233 | `"expected " + ExpectedKind`, stored in `ExpectKind_Msg` |
| `ExpectWord` | 246 | `"expected '" + ExpectedWord`, stored in `ExpectWord_Msg` |
| `ExpectIdent` | 269 | Text literal `"expected an identifier"` |
| `ParseAtom` | 345 | Text literal `"expected a value"` |
| `ParseComparisonOp` | 515 | Text literal `"expected a comparison operator"` |
| `ParseStatement` | 1071 | `"unknown statement starting with " + ParseStatement_BadV`, stored in `ParseStatement_Msg` |

This is a fixed caller set, not an inference from the formal's name. Every composed call to `ExpectKind` and `ExpectWord` passes a quoted text constant. `ParseStatement_BadV` comes from `CurValue` → `PeekValue` → `Get TokenValues`; `TokenValues` is declared `Text` in `self_host/lexer.kuro:62–63`, and the end-of-input branch returns `""` in `self_host/parser.kuro:188–196`. Runtime input can change the token text, but cannot add a new caller to the parser's compiled IR.

The composed IR has no closure, invoke, spawn, or await operation that can add an indirect route to `RecordDiag`. Its message uses are exactly three immediate text constants and three loads of the named scratch scalars. Each scratch has one IR `STORE_LIST` fed by a `BINOP +`. In `RecordDiag` itself, `Message` is only loaded from its parameter, appended to `DiagMessages`, and followed by `ParseFailed = 1` (`self_host/parser.kuro:164–173`). The parallel diagnostic collections are declared `Text` (`:104–115`). The parser's failure latch stops further block parsing; `self_host/compiler.kuro:13–30` withholds bytecode on failure, while `self_host/native_compiler_entry.kuro:61–63` emits the generic `kuro.compile-error/1` rather than displaying the accumulated diagnostic message.

## Why a Text annotation is still unsafe for native codegen

Two independent missing paths block a signature-only change:

1. **Text concatenation is rejected.** `native_codegen.kuro`'s `BC_BINOP` path only marks Integer/Decimal operands valid (`:1851–1876`); Text operands set `NativeFailed`, and the failed program publishes no assembly. This is the operation used to build all three scratch messages.
2. **Shared Text scalar loads are erased to Integer.** `NativeEmitCallArgument` requires actual kind `T` for a `Text` formal (`:661–719`). The `BC_LOADVAR` path initializes the kind to `I`; inside functions it recognizes typed parameters, but not shared globals (`:2537–2550`). Main-scope global loads only upgrade the kind for `D`; a shared `T` load remains `I` (`:2551–2575`). Thus a typed `RecordDiag.Message` would fail closed on the scratch arguments even if their Text-producing expression were supported.

Targeted bytecode probes confirm both gates independently: `BC_CONST_TEXT + BC_CONST_TEXT` fails with `NativeOut == ""`, and a known Text stored in a shared scalar then passed to a typed Text parameter also fails with empty output. By contrast, a Text constant passed directly to the same typed parameter succeeds. The regression tests preserve these distinctions on x86-64 Linux and ARM64 macOS targets.

The source-to-IR regression connects each scratch `BINOP` result to its `STORE_LIST`, traces the runtime `ParseStatement_BadV` value through `CurValue` and `PeekValue` into Text-typed `TokenValues`, and verifies that the same `TokPos + Offset` scalar feeds both the bounds check and the `GET` index. It pins the EOF empty-Text return to the `JUMPF` false-target label and confirms `Message` is read only in `RecordDiag`, with no writes.

## Regression boundary and next step

`tests/self_host/test_native_codegen.py` asserts the six exact message sources and keeps `RecordDiag.Message` untyped. It checks text-constant arguments to `ExpectKind`/`ExpectWord`, the absence of dynamic-call opcodes, and no-output fail-closed behavior for unsupported Text concatenation and shared Text global loads on both targets. Existing generic `NONE` behavior is unchanged.

The safe next implementation step is not to annotate this formal. It must separately add a sound text-concatenation path and preserve/check Text kind across shared-scalar writes, aliases, and loads, with positive and mixed-kind regressions. Until both are proven, this complete-composition compiler artifact remains fail-closed with no assembly. Python-seeded image construction and Clang/LLVM assembly/linking also remain; strict toolchain independence is not claimed.
