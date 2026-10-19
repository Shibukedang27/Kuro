"""Test-only sparse representation experiment for closure-return analysis.

The sparse clone removes only the default fact ``(set(), False)``. In
particular, an explicit empty-known fact is retained, and joining an absent
mapping key uses the production default rather than an empty-known identity.
"""
from __future__ import annotations

import compiler.native as native
from scripts.profile_sparse_closures import (
    SparseFacts,
    _outcome,
    closure_edge_workloads,
    generated_graph_workload,
    make_emitter,
    negative_workload,
    sparse_workload,
)


def test_sparse_fact_map_elides_only_the_default_unknown_fact():
    facts = SparseFacts()
    facts["default"] = (set(), False)
    assert "default" not in facts

    facts["empty_known"] = (set(), True)
    assert "empty_known" in facts
    assert facts["empty_known"] == (set(), True)

    targets = {"TargetA"}
    facts["known"] = (targets, True)
    targets.add("TargetB")
    assert facts["known"] == ({"TargetA"}, True), "stored target sets must not alias transfer operands"

    facts["nonempty_unknown"] = ({"TargetA"}, False)
    assert facts["nonempty_unknown"] == ({"TargetA"}, False)
    facts["nonempty_unknown"] = (set(), False)
    assert "nonempty_unknown" not in facts


def test_sparse_fact_copy_has_fresh_mapping_and_read_only_shared_target_sets():
    facts = SparseFacts()
    facts["closure"] = ({"TargetA", "TargetB"}, True)
    copied = facts.copy()

    assert copied is not facts
    assert copied == facts
    assert copied["closure"][0] is facts["closure"][0], "copy shares target sets, which transfers must treat as read-only"
    copied["extra"] = ({"TargetC"}, True)
    assert "extra" not in facts, "copy must own an independent mapping"
    assert copied["closure"][0] == facts["closure"][0] == {"TargetA", "TargetB"}


def test_sparse_clone_matches_production_and_unpruned_reference_exactly():
    # The size is large enough to make facts wide but small enough for normal CI.
    cases = {
        "seeded_cfg": sparse_workload(size=24, random_cases=1, seed=8821),
        "mixed_known_scalar_error": negative_workload(),
    }
    cases.update(closure_edge_workloads())
    # Eight small, deterministic graph seeds vary branch depth, optional loop
    # structure, and known / missing / scalar return shapes for Invoke.
    cases.update({f"generated_seed_{seed}": generated_graph_workload(seed) for seed in range(8)})
    production_instrumented, prod_metrics = make_emitter(native, mode="production", instrument=True)
    legacy_instrumented, legacy_metrics = make_emitter(native, mode="legacy", instrument=True)
    sparse_instrumented, sparse_metrics = make_emitter(native, mode="sparse", instrument=True)
    legacy, legacy_uninstrumented_metrics = make_emitter(native, mode="legacy")
    sparse, sparse_uninstrumented_metrics = make_emitter(native, mode="sparse")
    assert legacy_uninstrumented_metrics["copy_calls"] == 0
    assert sparse_uninstrumented_metrics["copy_calls"] == 0

    for name, program in cases.items():
        expected = _outcome(native.emit_x86_64_linux, program)
        assert expected == _outcome(legacy, program), f"legacy reference differed for {name}"
        assert expected == _outcome(sparse, program), f"sparse clone differed for {name}"
        assert expected == _outcome(production_instrumented, program)
        assert expected == _outcome(legacy_instrumented, program)
        assert expected == _outcome(sparse_instrumented, program)
        known_generated = name.startswith("generated_seed_") and int(name.rsplit("_", 1)[1]) % 3 == 0
        if name in {"seeded_cfg", "unreachable_scalar_return"} or known_generated:
            assert expected["kind"] == "assembly" and expected["assembly"]
        else:
            assert expected["kind"] == "native-error"
            assert expected["type"] == f"{native.NativeBackendError.__module__}.{native.NativeBackendError.__qualname__}"
            assert expected["text"] == "x86_64-linux Invoke requires closures with statically known targets"

    # Large positive case has live locals, absent-key joins, and target-bearing
    # unknown facts. Sparse storage removes default unknowns without erasing the
    # nonempty/unknown lattice element or changing the emitted assembly.
    prod_empty = prod_metrics["empty_unknown_entries"]
    sparse_empty = sparse_metrics["empty_unknown_entries"]
    assert prod_empty > 0
    assert sparse_empty == 0
    assert sparse_metrics["one_sided_join_names"] > 0
    assert sparse_metrics["nonempty_unknown_entries"] > 0
    assert sparse_metrics["union_candidate_names"] < prod_metrics["union_candidate_names"]
    assert sparse_metrics["merge_attempts"] < prod_metrics["merge_attempts"]
    assert sparse_metrics["body_visits"] < prod_metrics["body_visits"]
    assert sparse_metrics["mapping_entries"] < prod_metrics["mapping_entries"]
    assert sparse_metrics["max_mapping_size"] < prod_metrics["max_mapping_size"]
    assert sparse_metrics["copy_entries"] < prod_metrics["copy_entries"]
    assert legacy_metrics["deep_target_copy_entries"] > 0
    assert prod_metrics["deep_target_copy_entries"] == 0
    assert sparse_metrics["deep_target_copy_entries"] == 0
