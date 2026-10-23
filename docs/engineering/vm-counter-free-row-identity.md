# Counter-free row identity is a different compatibility choice

## Decision: keep production IDs until the supported history is explicit

This test/design increment starts directly above draft/open [PR #120](https://github.com/Shibukedang27/Kuro/pull/120), exact parent `492cabd85287be395be2c116fc57617d373cc995`. It changes no production source, distribution artifact, admission point, resource ceiling, or consumer. It installs neither a maximum-ID guard nor counter-free storage. Production performance, row usage, peak, and headroom are unchanged by this patch.

The counter-free alternative avoids the generation-overflow problem by removing the counter, not by preserving its behavior. Therefore it is **not an unconditional compatibility-preserving migration**. Retain today's production representation while the owner-supported history and helper/internal observability contract remain undecided. Neither this note nor a passing model silently declares native wrap to be a language guarantee or authorizes a changed overflow policy.

The [existing seeded witness](../../tests/self_host/test_vm_generation_id_bounds.py) already distinguishes hosted execution from Linux x86-64 native helpers: the first post-boundary reset remains active when hosted, but publishes a negative/inactive native ID. Appending then succeeds hosted and fails native. No natural execution of `2**63` resets, portable wrap rule, or new production failure is claimed.

There is a simple incompatibility argument for a truly counter-free layout. Repeated empty resets leave exactly the same active-empty head and zero rows; there is no retained history to distinguish one reset count from another. Today's native counter state, however, can distinguish a pre-wrap empty reset from a post-wrap inactive reset. A counter-free implementation cannot produce both outcomes from identical retained state. A hidden reset count, epoch, or poison flag driven by that count would be additional history metadata, not the counter-free candidate tested here. Restricting supported histories or deliberately changing exhaustion behavior requires an explicit compatibility decision.

## What the alternative stores

The [separate specification model](../../tests/self_host/test_vm_counter_free_rows.py) retains one head per existing name slot: `-1` means inactive, `-2` means active empty, and a nonnegative value is a row index. Each historical row holds an immutable scalar raw/display cell and a mutable next-row index, ending at `-1`. There are no generation IDs, owner labels, historical-generation descriptors, tail tables, row reuse, sharing, or reclamation.

Conceptually, heads could reuse the current ID column and next links could reuse the owner column. That is a field-count observation, **not** an implemented native memory reduction: Python objects and proof sets are not native buffers. Seeds, sentinels, dynamic hosted growth, allocation failures, multi-array publication, and consumer changes still need implementation evidence. It makes no new-buffer or allocation-failure-equivalence claim.

Every published link moves to a strictly later paid row. Each row has at most one predecessor and active chains are disjoint. Reset/deactivation abandons a head without deleting historical rows. Set changes only a scalar pair, spending no row. Append keeps the existing eager row-admission point before publication. Copy does its self-copy check first, resolves its source late, captures source traversal before resetting the destination, and publishes one paid row at a time. No bulk reservation changes a terminal partial prefix.

This argument assumes synchronous unique ownership with no callback/reentry. A row index is not an asynchronous pin or public reusable handle. Historical chain retention alone proves neither a consumer lifetime nor permission to share/reclaim.

## Bounded evidence, including the runtime cost

The independent eager-list oracle and the counter-free candidate are compared after every operation over **131,072 depth-four traces**, two existing names, and row budgets two and three. The inherited alphabet exercises reset, deactivate, replacement, append, nonnegative Get, valid/invalid Set, and eager copy. Comparison includes visible raw/display cells, sticky authored failures, logical debit, read observations, terminal operation, and exact paid copy prefix. This is finite evidence, not induction or complete language equivalence.

Directed controls cover 65,537 empty reset/copy pairs with three retained heads and zero rows; distinct inactive/empty sentinels in the presence of old rows; interleaved chains; Set and copied-cell isolation; historical chain retention; missing-source and inactive self-copy precedence; full-budget empty copy; sequential multi-store's completed and partial destinations; and row indices `0..65,535`. The real-sized fixture appends one row per name to keep setup linear; it does not test a 65,536-row single-chain append workload. A separate no-ceiling control avoids importing native capacity into the hosted candidate.

Get's negative offset uses `length + requested_index`, unlike Set. Six directed Get cases cover last/first elements, too-negative, positive-at-length, active-empty, and inactive names. They assert chosen production-helper semantics separately because the independent eager oracle defines only nonnegative Get. They do not certify the production fallback result register/display behavior or all Print/Length consumers.

Without a tail table, Append walks the destination chain. Instrumentation counts **32,640 next-link reads for 256 consecutive appends**, exactly `n*(n-1)/2`. The measurement counts algorithmic work, not wall-clock performance. Instrumentation and transient invariant sets are not candidate metadata. This quadratic cumulative cost is a real tradeoff, not a free memory improvement; current owner scanning is also not assumed constant-time. A tail table would be another representation with its own resource proof. No speedup is claimed.

## What can and cannot be called compatible

A possible future claim would be **public collection semantics for a specified finite, pre-exhaustion scalar-history domain**, subject to the existing logical row budget, supported indexing semantics, and sufficient system resources. Even that claim is not established for every production consumer by this model. It does not include marker/name indirection, moving Text, result registers, frame/closure snapshots, or internal/helper observations. Hosted execution must retain its own growth behavior rather than inherit a native ceiling.

Current tests directly inspect `VMNextCollectionId`, `VMCollectionIds`, and `VMCollectionOwners`. Their contents necessarily change or disappear in a counter-free implementation. `VMFindCollection` also currently recognizes activity through `id >= 0`; that predicate cannot be copied onto heads because `-2` must be active. Internal observability must be explicitly classified rather than silently discarded. A model/oracle agreement cannot resolve that API decision.

| Path | Required before any migration |
| --- | --- |
| Find/Mark/Reset/Deactivate | Distinguish unseen/inactive, active empty, and nonempty; preserve name slots and failure precedence; decide ID/helper observability and exhaustion. |
| Append | Preserve admission before publication and multi-array write order; prove tail traversal, sentinel handling, and failure boundaries on each backend. |
| Get/Length/Set/Print | Walk only the selected chain; preserve Get-only negative normalization, raw/display pairing, sticky failure and fallback behavior. |
| Copy/list store/sequential multi-store | Capture source before destructive reset; preserve eager copies, late name lookup, self-copy/missing-source precedence, exact partial prefixes. |
| Marker/Text/result/frame/closure consumers | Audit every borrowing scope, snapshot and scalar capture; prove no reentry, moving-reference alias, sharing or reclamation is introduced. |
| Native and hosted storage | Prove row-index bounds, seed treatment, hosted dynamic growth, allocation/write boundaries and practical runtime, not just field counts. |

## Acceptance and next step

Focused and full tests, independent frozen-head review, a fresh four-image hosted-bootstrap rebuild, blocked-toolchain smoke, fresh compiler reproduction/272-literal control, and all eight CI checks on the exact documented final head are acceptance gates. The PR verification receipt records results and the immutable head; a parent's successful checks are not inherited certification.

The next safe production step is still conditional: select the supported-history and internal-observation contract, then prove all consumer lifetimes and native write/admission order before choosing a representation. Strict preservation of today's full native boundary behavior rules out this purely counter-free design. Choosing a pre-exhaustion domain or a changed overflow policy would permit further evaluation, not automatically authorize migration.

Historical full-compiler peak remains 65,481 rows with 55 spare, not a new peak measurement. Python seeding and Clang/LLVM assembly/linking still block strict independence. PR #107/#108 remain individually unverified. This PR and the existing stack remain draft/open/unmerged.
