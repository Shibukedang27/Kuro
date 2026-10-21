# Loop-flow facts before multitrip Decimal initialization

This is an analysis and regression-test increment, not a new native-codegen feature. It is stacked on [PR #79](https://github.com/Shibukedang27/Kuro/pull/79), whose open/unmerged head `9b6904665c5ce524661def2c93eff97e5116a8cb` was confirmed with eight successful checks before editing. Production compiler sources and the set of accepted programs are unchanged. Strict independence remains unfinished.

## Why stop at a test scaffold?

The current emitter learns named-slot kinds during one traversal of the bytecode. That traversal is not execution order once a loop has a backedge. A kind learned near the end of a body cannot justify an earlier read on the first iteration, and a body store cannot justify a post-loop read when the body may be skipped. The existing literal `Repeat 1` permission deliberately avoids a second body entry.

The next plausible feature is direct, unconditional initialization in a function-free top-level positive-literal multitrip Repeat. Before granting it, we need inspectable entry, backedge, exit and use-site facts rather than a wider literal-provenance flag. Independent design review recommended establishing these facts separately first. This PR therefore keeps the current fail-closed production boundary, including rejection of the otherwise promising `Repeat 2` direct-store candidate.

## The facts that matter

- **Entry:** what representations can reach a slot before the loop starts?
- **Backedge:** what representations can reach another iteration after the body?
- **Normal exit:** what representations can reach statements after the loop, including the zero-trip path when possible?
- **Use site:** what representations can reach each read, including the first iteration rather than only later iterations?

A fresh named Decimal needs a dominating store on every relevant path before each read. Existing Decimal storage must retain its representation on every repeated path. A union containing both unknown and Decimal is not definite Decimal initialization. Likewise, an Integer/Decimal union at an early body read exposes a representation conflict even if a later body store overwrites that slot.

The [test-only reference model](../../tests/self_host/loop_flow_facts.py) computes a worklist fixed point over a deliberately restricted bytecode control-flow graph. It is an analysis aid, not a production pass, a new runtime, or a substitute for the Kuro-owned implementation. It does not decide native acceptance.

## What the model does—and does not prove

The decoder supports numeric `BC_CONST`, `BC_LOADVAR`, scalar `BC_STORE_LIST`, `BC_PRINT`, `BC_BINOP +`, and structured If/Else, Repeat and While markers. Store facts come from an abstract operand stack, not from guessing the preceding literal. Each slot and stack position carries a set of possible kinds: unknown `?`, Integer `I`, or Decimal `D`. Stores strongly replace a slot's current fact; graph joins union the incoming possibilities. Re-enqueuing changed nodes propagates backedge facts to a fixed point. Incompatible reachable stack heights and unsupported instructions fail explicitly; crossed, duplicate and missing region delimiters are rejected by structured parsing.

Adjacent canonical Integer literals `0`, `1` and `2`–`9` classify a Repeat as zero-trip, exact-once or definitely entered/multitrip. Other counts are conservatively unknown: this deliberately does not constant-fold expressions or recover runtime-variable values. Positive multitrip loops may take arbitrarily many abstract backedges; the model does not claim exact iteration counts. Both If arms are considered even for constant conditions. While always includes a possible zero-trip exit and sends the backedge through the condition again. No path feasibility, correlations between slots, termination proof, Action/call semantics, result-slot rules, mutation opcodes, collection storage, bounds policy or abrupt-exit support is implemented. It is a kind-flow witness for these fixtures, not a bytecode validator for production.

Unknown `?` means no established kind in this model, not a fourth runtime representation. Unlike the emitter's legacy fallback, the model leaves a raw unknown read unknown rather than implicitly choosing Integer zero. This distinction is intentional: a union such as `{?, D}` exposes the uninitialized first-entry possibility. Neither a singleton `{D}` nor any other fact is sufficient on its own to grant production support.

Opcode arities, supported operators and region structure are checked across the decoded stream, but literal validity and abstract operand-stack checks run only at reachable nodes. For example, an underflowing `BC_PRINT` or unsupported `BC_CONST nan` inside a literal-zero Repeat body is not checked by transfer. Independent review identified this limit; it is documented rather than advertised as whole-stream fail-closed validation. Production validation is not delegated to this helper.

## Regression witnesses

The [fixture module](../../tests/self_host/test_native_loop_flow_facts.py) distinguishes the promising direct `Repeat 2` store-before-use case from an early read that has `{?, D}` across first entry and backedges. A separate Integer-entry/Decimal-backedge witness has `{I, D}` at its early read even though a later overwrite makes its exit `{D}`. Missing Else paths retain unknown facts; complete arms establish Decimal facts in the model but remain outside production multitrip support.

Zero, runtime and computed counts retain conservative exit paths. Nested skipped initializers do not establish an outer-loop slot, and nested skippable-body reads retain first-entry uncertainty. While condition reads include both initial entry and the repeated condition path. An exact-once control has no reachable backedge. The established-Decimal multitrip control remains accepted by production and prints `1.5` twice inside the loop and once afterward.

The raw witness corpus is checked against all three hosted generator targets without widening acceptance. The same corpus is integrated into the [freshly compiled Kuro generator gate](../../tests/self_host/test_native_codegen.py): candidate programs must still fail with exit status 1 and no assembly or diagnostics, while the established control must generate, link and execute with the expected output and no undefined symbols. Linux execution is local; genuine Darwin execution belongs to macOS CI, not cross-assembly.

## Next bounded implementation

Use the fact witnesses to design a Kuro-owned proof for direct body stores in a top-level positive-literal Repeat. Keep skippable/runtime-count loops, nested initialization, While initialization, Action-shared storage, result-slot joins and mixed representations outside that first feature. Require valid literal provenance, first-entry domination, compatible repeated-entry use sites and all normal exits. Do not automatically extend the existing If-join permission to multitrip bodies.

Negative-count semantics and the interpreter-only While guard remain separate discrepancies documented in [the exact-once analysis](native-exact-once-repeat.md#actual-loop-behavior). Full clean-checkout Python-free compiler/runtime rebuilding and repository-owned assembly/linking remain open work.

## Verification and review

The full local suite passed **1,268 tests, with 20 skipped, in 524.93s (8m44s)**. That run includes the corrected use-site assertion: an initial focused run had accidentally inspected the nested loop's count-variable read rather than the `Fresh` read. Selecting the named use fixes the test, not the model or production behavior. Subsequent module edits clarify validation scope in its docstring only.

The corrected focused reference-model/fresh-generator/bounds/inherited-regression gate passed **212 tests in 112.41s**. These runs overlap; their counts must not be added. Independent design, model and final-diff reviews found no remaining actionable issue after the validation-scope clarification. `git diff --check` is clean. All changed executable logic is confined to tests; `self_host/` and `compiler/` are unchanged.

```sh
.venv/bin/python -m pytest -q tests/self_host/test_native_loop_flow_facts.py tests/self_host/test_native_repeat_branch_joins.py tests/self_host/test_native_loop_init.py tests/self_host/test_native_branch_joins.py tests/self_host/test_native_codegen.py::test_kuro_owned_x86_linux_codegen_runs_decimal_storage tests/self_host/test_native_codegen.py::test_kuro_native_codegen_keeps_if_depth_limit_at_sixteen tests/self_host/test_native_codegen.py::test_kuro_native_codegen_keeps_global_slot_limit_at_sixty_four tests/self_host/test_native_codegen.py::test_kuro_native_codegen_enforces_exact_4096_token_boundary tests/self_host/test_native_codegen.py::test_native_codegen_source_emits_with_macos_arm64_backend --durations=10
.venv/bin/python -m pytest -q --durations=20
```

Acceptance requires the focused reference-model and fresh-generator regression gates, the full local suite, independent soundness review, and all eight CI checks on the final documentation-updated head. Earlier-head, pending, cancelled or failed checks do not count. The review PR stays open/unmerged and directly stacked on #79. No CI result is claimed in advance.
