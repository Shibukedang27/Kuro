# Preserve exhaustion behavior before replacing collection storage

## The migration gate is now explicit

This bounded test/documentation increment starts above draft/open [PR #122](https://github.com/Shibukedang27/Kuro/pull/122), parent `274151dd58a4244f5f8f905da5906cdbea0a06b9`. It changes no production implementation, generated distribution artifact, resource ceiling, or language operation.

**Acceptance policy for the next representation change: preserve the existing backend's observable collection behavior, including exhaustion/history effects. Do not silently exclude long histories or install a new overflow failure.** This is a conservative engineering gate, not a claim that signed native wrap is a portable language guarantee, and not a promise that every conceivable history has already been certified. A proposal that narrows supported histories or replaces exhaustion behavior needs a separate explicit contract decision before implementation. Private ID/owner fields may change; their downstream activity, contents, failures, and publication effects may not be discarded merely because the fields are private.

This settles which rule to apply while the language-level exhaustion policy remains undecided: keep the current behavior rather than choose a pre-exhaustion domain by default. The [consumer contract](vm-collection-consumer-contract.md) and [counter-free model](vm-counter-free-row-identity.md) remain valid evidence, but the purely counter-free layout is **not eligible for production under this gate**. Empty resets retain neither rows nor a distinct head in that layout, so it cannot distinguish the history-dependent activity transitions of today's native counter. An added history counter or epoch is a different design requiring its own proof.

The gate is intentionally restrictive. It does not itself deliver a storage improvement, migration, or independence gain. If preserving this behavior makes a proposed optimization impractical, stop that proposal; do not weaken the contract by implication.

The follow-up [reachability and row-lifetime evidence](vm-generation-reachability-lifetimes.md) distinguishes row-free outer-helper histories from row-funded normal public dispatch, and tests actual in-place overwrite versus retained reset history. Its bounded public-dispatch argument does not waive this broader preservation gate or demonstrate a natural full native cycle.

## What unchanged helpers actually do

The [new helper witnesses](../../tests/self_host/test_vm_generation_history_contract.py) run the complete unchanged authored VM on hosted execution and Linux x86-64 native execution. Seven scenarios run on both paths, with literal backend-specific expected traces rather than a replacement model's expected transitions.

| Scenario | Observed behavior and its consequence |
| --- | --- |
| Eight empty resets | One name, zero logical rows, counter eight, Length zero. Row capacity cannot bound generation history. |
| Mark active; deactivate; reset at the boundary | Mark and deactivation leave the counter unchanged. Reset reuses the name slot but consumes the next ID. Hosted remains active; native becomes inactive without setting `VMFailed`. |
| Reset an existing name with a historical row | The row and display remain physically present. Hosted selects a new active empty generation; native becomes inactive. Length returns zero on both but sets failure only on native. |
| Mark an already negative generation again | Native retries consume another ID without adding a name slot; hosted Mark sees an active generation and does nothing. Slot count alone cannot encode this history. |
| Copy an empty source across the boundary | Destination reset publishes an inactive native name, but no Append runs and `VMFailed` stays zero. Hosted publishes an active empty destination. A generic “overflow always fails” guard would change this distinction. |
| Copy a nonempty source across the boundary | Native resets the destination, then Append fails: one historical row remains, no copy row is added, append-display scratch is cleared, and failure remains sticky even after a successful source Get. Hosted copies the row with its raw/display pair intact. Reset and failure cannot be collapsed into one new atomic step. |
| Synthetic `-1` to `0` reuse | With an existing owner-zero row, injected `-1` makes one new name inactive; the next reset assigns zero to another name. That name sees the old row; Set through it changes the original name's contents/display. Deactivating the original does not hide the row from the reused name. This is a deliberately seeded alias witness, not a naturally executed full cycle. |

The signed crossing is computed from small runtime literals, as in the [earlier boundary witness](../../tests/self_host/test_vm_generation_id_bounds.py). No helper body is patched, no buffer limit is reduced, and no natural execution of `2**63` resets is claimed. The reuse scenario separately assigns `-1` in both hosted and native execution. It does **not** show hosted integers wrapping, establish that such a hosted state is reachable through ordinary operations, or prove an entire native cycle reachable under actual system limits. The alias witness identifies an obligation for a claim covering injected/reused IDs; natural full-history compatibility still requires an explicit reachability argument, not this shortcut.

No Copy is attempted when its new destination ID equals its captured source ID. The current Copy scans a growing global row count; such an injected collision could make it follow its own appended rows. We do not execute that potentially unbounded case or claim its termination behavior is characterized. A future history-preserving replacement must separately analyze collisions and copy traversal, rather than infer safety from the bounded alias control.

## Diagnostic limits

An initial version printed the empty append-display scratch directly. Four native scenarios rendered six NUL bytes where hosted rendered an empty string; the other observations matched. The corrected probe compares scratch with the empty string and prints an explicit nonempty tag for either outcome. This narrows the claim to scratch equality on these paths; it does not fix or certify native empty-Text rendering, attribute its cause, or establish raw/display ABI parity. The nonempty source raw/display pair is still printed and checked after failed native Copy, and no failed Get fallback is rendered as Text.

These are helper-level witnesses, not a complete public-bytecode execution through exhaustion, authored-generator boundary parity, natural full-cycle execution, Darwin/ARM overflow contract, moving-Text lifetime proof, metadata/tail cost measurement, or complete publication proof. The prior normal-dispatch failure guard remains separate evidence. Test success does not turn a backend-specific arithmetic result into a new language specification.

## The next production path

First choose a representation compatible with this gate, or obtain an explicit supported-history/exhaustion contract before pursuing a counter-free replacement. A history-preserving design needs an actual backend implementation and evidence for counter arithmetic, active/empty state, historical owner identity, collision effects, and sequential publication/failure precedence. Do not assume a new epoch, remapping, row link, or tail table is free.

Then prove replacement lifetimes, raw/display capture, source identity and traversal bounds, name-marker late binding, scalar/result/Action-frame behavior, native row admission, hosted dynamic growth, and metadata/tail cost. Preserve existing admission boundaries and fail-stop behavior. The [consumer table](vm-collection-consumer-contract.md#what-each-consumer-borrows) remains the review checklist; synchronous helpers alone do not prove every backend lifetime.

Acceptance for this increment requires focused and full tests, independent review on the frozen candidate, a fresh four-image rebuild, blocked-toolchain smoke, compiler reproduction/272-literal control, and all eight exact-head CI checks. Actual results belong in the PR's verification receipt, not this prospective checklist. Python seeding and Clang/LLVM still block strict independence; PRs #107/#108 remain individually unverified. Keep this and the earlier stack draft/open/unmerged.
