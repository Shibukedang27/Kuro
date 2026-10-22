# Reconcile the semantic frontend with the verified bootstrap stack

## What is verified, and where

The verified cumulative tip is open, draft [PR #109](https://github.com/Shibukedang27/Kuro/pull/109), exact final code-and-documentation head `5af148a8272dfa40fb6445ba5f5b305c68672dcf`. Its [push run](https://github.com/Shibukedang27/Kuro/actions/runs/39842850702) and [pull-request run](https://github.com/Shibukedang27/Kuro/actions/runs/39842858299) each passed macOS Python 3.10/3.11/3.12 and Linux portability: **eight successful checks in total**. Live PR inspection confirms the following unchanged stack; none is merged or promoted here.

| PR | Exact head | Actual base branch | Exact-head status |
| --- | --- | --- | --- |
| [#107](https://github.com/Shibukedang27/Kuro/pull/107) | `1dc7eebadd042175eb9bd54eba824ead545601df` | `fix/length-reference-parity` (#106) | Open/draft, unverified; rollup contains 12 failed checks across repeated workflows |
| [#108](https://github.com/Shibukedang27/Kuro/pull/108) | `a97687859e9669745c39e7ddf1eeb2f8938f741b` | `fix/compiler-length-frontend` (#107) | Open/draft, unverified; six macOS failures and two Linux successes |
| [#109](https://github.com/Shibukedang27/Kuro/pull/109) | `5af148a8272dfa40fb6445ba5f5b305c68672dcf` | `fix/vm-single-character-decode` (#108) | Open/draft, verified cumulative increment; eight successes |

Draft status and verification are different properties. #109 deliberately remains draft above draft ancestors. Its green checks certify its cumulative tree, **not the unchanged exact heads of #107 or #108**. #106 remains the last independently verified ancestor before those two failed heads; it is no longer the latest verified cumulative tip.

## Which changes clear which blockers

The [#107 frontend record](compiler-length-frontend.md) describes a real historical failure of its own tree: full compiler-bytecode reproduction exhausted the unchanged character arena after aggregate collection pressure had been reduced. Its selective frontend tests were not full reproduction evidence.

The [#108 decoder prerequisite](vm-single-character-decode.md) avoids redundant one-character extraction without changing decoded values, flags or spelling. It clears the whole-source reproduction failure locally, including the unchanged 272-literal initializer, without enlarging either arena. However, its exact tree still fails ARM64 complete-compiler assembly generation: `LCFrameAction` loses its Integer kind and a downstream cursor ADD rejects. Thus decoder-local success was not whole-branch eight-check acceptance.

The [#109 ARM64 prerequisite](arm64-integer-collection-kind.md) admits numeric initial collection kinds only when conservative write provenance proves them. It preserves the numeric ADD guard and the previous fallback for unproven owners. The cumulative tree passes full reproduction and the eight-check gate. ARM64 source generation, object cross-assembly and byte-identical unaffected assemblies are **not ARM64 executable runtime parity**.

A fresh reproduction test at exact #109 rebuilt both compiler and launcher and passed the complete self case **and** the 272-literal initializer: **1 passed in 69.45s**. This is a new cumulative baseline, not a rerun of #107's head or a retroactive correction of its history.

## The next smallest semantic candidate

[ADR-0013](ADR-0013-type-system-stage7.md) already requires `Repeat` counts to be Integers (E3008). Both reference and standalone authored typechecker implement that rule. The integrated authored source compiler still bypasses the full resolver/typechecker; its bounded parsed-token stage currently enforces only known non-Text Length admission.

Independent inspection selected an intentionally smaller slice: **bare Text or Decimal literal Repeat counts**, with a following semicolon. `Repeat "x"; Print 0. Done.` and `Repeat 1.5; Print 0. Done.` are rejected by the reference but accepted by the exact cumulative parent compiler. Integer counts remain accepted. This is implementation of an existing rule, not a new language rule. Aliases, computed expressions, parameter inference and general Repeat type analysis are excluded.

A detached scratch worktree tests adding that check to the existing phase-three scanner, reusing scalar scratch names and diagnostic storage, with no new retained symbol/frame collections. The diagnostic points to the count token and prevents lowering/bytecode publication. Neither full semantic pass, storage ceiling nor runtime operation is changed. The proposal must pass fresh complete compiler-bytecode reproduction and the full initializer before any production change is retained.

## Acceptance and next prerequisite

**The semantic probe is not retained.** Hosted and freshly built native probe results reject both bare noninteger literals with E3008 at line 1, column 8, with no bytecode, while accepting `Repeat 1` and `Repeat 1 + 1`. But the unchanged fresh full-reproduction test fails its first, complete-self case: exit 1, empty stdout/stderr, **1 failed in 47.41s**. The 272-literal second control is not reached and is not counted as passed for this candidate. Complete compiler bytecode grows from **9,118 to 9,212 tokens**; composed source grows from **83,192 to 84,103 bytes**. Identical explicit hosted/native admission tests give **4 failed / 4 passed on exact #109**, and **8 passed on the scratch candidate**. These are parent-failing semantic witnesses, not whole-pipeline acceptance. This is a rejected feasibility experiment, not an implemented parity increment.

A focused semantic success alone is insufficient: the parent's aggregate-store estimate leaves only **55 spare entries** under 65,536, and scanner code itself enlarges the compiler's tokens, AST, IR and bytecode. Character-arena relief does not provide aggregate-store headroom. Exit 1 alone was not treated as a resource diagnosis. A separate scratch-only debugger run, exposing assembly labels without changing instructions or ceilings, stops at the launcher's original overflow guard. `VMCollectionOwners`, `VMCollectionItems` and `VMCollectionItemDisplay` each contain **65,536 entries**; the character cursor is **720,108 bytes** and the text-join cursor **1,549,420 bytes**. The same instrumented launcher reaches normal completion on the parent self input with **65,481 entries in each backing-store column**, character cursor **870,724**, and text-join cursor **2,192,152**. Parent and probe launcher assembly are byte-identical before this symbol-only instrumentation. Thus the observed candidate blocker is aggregate backing-store exhaustion, not a repeated character-arena overflow. The measured parent spare count is **55**, not just a prediction. Debugger observations diagnose the rejected probe; they do not replace the normal fresh test or certify any changed executable.

**Next concrete prerequisite:** obtain a per-owner/lifetime breakdown of the now-measured complete-self aggregate allocation, then reduce retained compiler metadata or redundant copies while proving exact-parent artifact/output/diagnostic parity. Start with the encoder/output boundary (`BytecodeOut`, the final `CompilerOutput = BytecodeOut` copy and the VM's collection-store implementation): investigate duplication, but do not assume an alias or ownership change preserves publication semantics. Budget the full token/AST/IR/bytecode/output composition, not just the scanner's added collections. Preserve the 65,536-entry store, character/text arenas, full source and 272-literal controls. Require measured positive headroom and fresh complete reproduction before retrying this exact bare-literal E3008 slice. Do not enable both full semantic passes, broaden alias/shape inference or silently change scope semantics as a substitute.

This PR changes documentation only. All tracked production, test and bootstrap files remain byte-identical to verified #109; the scratch checker patch is neither committed nor included in its branch.

This follow-up is open, draft [PR #110](https://github.com/Shibukedang27/Kuro/pull/110), stacked directly above the exact verified #109 head. Its own final documentation-updated head requires independent review, a full fresh suite, fresh four-image hosted bootstrap, Python/toolchain-blocked smoke including full reproduction, and **all eight CI checks** before it is called verified. The immutable final SHA and workflow receipts belong in the PR verification record rather than a subsequent documentation commit that would invalidate that receipt. Keep this PR and every ancestor open/unmerged.

## Fresh local verification of the retained documentation branch

- **Full suite:** 2,372 passed, 20 skipped in 847.39s, with production/test source frozen. This includes complete compiler-bytecode reproduction and the full 272-literal initializer.
- **Separate fresh detached checkout:** all four old production executables removed, then compiler, runtime, bytecode launcher and code generator rebuilt with the hosted bootstrap. Production doctor reports the complete 9,118-value compiler artifact.
- **Python/toolchain-blocked smoke:** passed using those fresh images, including full compiler-bytecode self-reproduction, stage-zero/stage-one output comparison, and known non-Text Length rejection/Text acceptance. The separate baseline reproduction test also passed both self and initializer before the rejected experiment.
- **Independent review:** approved the decision not to retain the semantic patch and the distinction between descendant green and ancestor status; requested removal of a dangling instrumentation cross-reference, addressed by the explicit guard measurements above. Final independent follow-up review approved the explicit measurements and reconciliation wording with no content blocker; its own exact-head CI remains a separate requirement.
- **Source identity and whitespace:** final checks compare all tracked non-documentation files to exact #109 and compiler/authored/bootstrap files to the fresh bootstrap checkout. No semantic experiment, new test or debug executable is part of this PR.
- **CI:** eight successes on this follow-up's exact final documentation head remain mandatory; the PR records the immutable head and both workflow receipts after completion. Local evidence and ancestor successes alone do not meet this gate.

Reproduce retained-tree checks with fresh output directories:

```sh
python -m pytest -q --basetemp=/absolute/fresh/test-output --durations=20
# In a separate source-identical checkout:
rm -f dist/kuro-compiler dist/kuro-runtime dist/kuro-bytecode dist/kuro-codegen
make native-hosted-bootstrap PYTHON=/absolute/path/to/python NATIVE_TARGET=x86_64-linux
sh tests/self_host/python_free_native_smoke.sh
```

The rejected scratch probe is not the retained tree. Its test failure must not be described as a failure of this documentation-only branch, nor its eight admission successes as a passing whole-source gate.

Strict independence remains unfinished: **Python seeds production images; Clang/LLVM assemble and link them.** Successful blocked-toolchain execution after seeding does not demonstrate Python-free image construction from a clean checkout.
