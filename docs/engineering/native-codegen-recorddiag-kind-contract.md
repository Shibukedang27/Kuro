# `RecordDiag.Code` Text parameter contract

This follow-up is stacked directly above draft/open PR #129 at exact parent head `9829a0bf0bbfd11b2a3f34ec15c19f4c64eb3ff3`. It declares only the fixed compiler parser's `RecordDiag.Code` formal as `Text`. It does not add general inference for untyped (`NONE`) action parameters or change native codegen's fail-closed policy.

## Complete fixed-composition call set

The production composer, `compiler.self_host.native_compiler_source()`, combines the fixed lexer, parser, length checker, lowerer, bytecode encoder, compiler driver, and native-compiler entry point. The only six calls to `RecordDiag` in that complete composition are in `self_host/parser.kuro`:

| Caller | Source line | `Code` argument | IR producer |
| --- | ---: | --- | --- |
| `ExpectKind` | 233 | `"E2002"` | Text constant |
| `ExpectWord` | 246 | `"E2002"` | Text constant |
| `ExpectIdent` | 269 | `"E2001"` | Text constant |
| `ParseAtom` | 345 | `"E2003"` | Text constant |
| `ParseComparisonOp` | 515 | `"E2004"` | Text constant |
| `ParseStatement` | 1071 | `"E2001"` | Text constant |

The compiler source may parse arbitrary user input at runtime, but that input is data in `Source`; it cannot add callers to the fixed parser's own `RecordDiag` action. Compiling the exact composed source and inspecting its main/function IR confirms those six static callsites, with an immediate string `CONST` for each `Code` argument. There is no caller that forwards a `Code` alias, reads a shared scalar as the code, or supplies an input-dependent value. `RecordDiag` only reads its frame-local `Code` parameter to append to `DiagCodes`; no composed IR instruction writes a variable named `Code`.

All calls in the composed IR are static action calls. The composition has no `MakeClosure`, `Invoke`, `Spawn`, or `Await` call route that can invoke `RecordDiag` dynamically. The shell bootstrap composer was also verified to match the Python fixed-source composer byte for byte. The code remains narrowly tied to this exact fixed composition, not to arbitrary Kuro programs or future parser edits.

## Fail-closed type checks

The regression compiles the full fixed composition and asserts that `RecordDiag.Code` is `Text`, that the exact six callers and four string code values remain, and that the argument is not routed through shared aliases or mutable writes. Native-codegen tests accept Text calls to the explicit `Text` parameter and reject Integer, Decimal, and mixed Text-plus-numeric call sets with no assembly. The existing generic untyped-parameter regression still rejects both Text and Decimal arguments; no generic inference was added.

## Full artifact replay and next boundary

The complete composition was run through its Kuro-authored compiler stages in the hosted interpreter with the complete source supplied as runtime input. It emitted **9,118 bytecode tokens**, **73 function blocks**, and **294 call blocks**. A fresh Linux x86-64 native codegen image was built through the existing hosted `compile_source`/`build_native` path, then given the complete framed artifact. Its `RecordDiag` signature is `BC_PARAM Code Text; BC_PARAM Message NONE`. The actual generator exited **1**, with empty stdout and stderr and no assembly.

`RecordDiag.Message` is the next remaining untyped formal in the artifact. A separate source audit found its fixed callers produce Text: some messages are literals, while `ExpectKind_Msg`, `ExpectWord_Msg`, and `ParseStatement_Msg` are assembled into shared scalar scratch variables from Text operands. That source-level conclusion does not establish that the current generator can pass them as Text. Its call check requires kind `T` for a Text formal, but its shared-global load path defaults non-Decimal scalar globals to Integer; Text recognition is available for explicitly typed action parameters, not these shared globals (`native_codegen.kuro`, `NativeEmitCallArgument` and the `BC_LOADVAR` kind path). Thus `Message` remains untyped and is not annotated here: treating it as a simple next signature edit could still fail at shared-scalar Text-kind propagation. The full artifact replay also does not instrument a unique rejection branch or prove `Message` is the sole remaining incompatibility.

## Verification

The full repository suite passed **2,683 tests, with 20 skipped**. The focused contract, parser-diagnostic, and compiler-composer selection passed **33 tests**. An independent review approved the narrow type contract and caller-provenance tests.

Fresh Linux images were rebuilt from this branch through the hosted bootstrap path. With Python and compiler tools blocked from `PATH`, the native smoke verified runtime, compiler, bytecode launcher, codegen, and full stage-1 compiler reproduction; the audit also verified arithmetic codegen and confirmed the full compiler still exits 1 with empty output and no partial assembly. The audit counted 9,119 framed lines (including the artifact header), 73 function blocks, and 294 call blocks. These gates confirm the existing bootstrap boundary; they do not establish independent image construction.

Generated images and replay artifacts are temporary and are not committed. Python-hosted bootstrap seeding and Clang/LLVM assembly/linking remain required; strict toolchain independence is not claimed. Any next step must separately address the shared Text-kind path and continue to fail closed for unsupported or mixed kinds; do not widen generic codegen behavior.
