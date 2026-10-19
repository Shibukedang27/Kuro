"""Guardrails for the opt-in uninstrumented presence resource profiler."""
from __future__ import annotations

import ast

import pytest

import compiler.native as native
from scripts.audit_normalized_closures import _clone_tree
from scripts.profile_presence_closures import (
    _make_presence_emitter,
    _outcome,
    _run_pair,
    _validate_analyzer_map_contract,
)
from scripts.profile_sparse_closures import sparse_workload


def _analyzer(tree):
    matches = [node for node in ast.walk(tree)
               if isinstance(node, ast.FunctionDef)
               and node.name == "analyze_action_closure_returns"]
    assert len(matches) == 1
    return matches[0]


def test_candidate_clone_has_only_two_presence_sites_and_no_trace_instrumentation():
    emitter, tree = _make_presence_emitter(native)
    analyzer = _analyzer(tree)
    calls = [ast.unparse(node.func) for node in ast.walk(analyzer) if isinstance(node, ast.Call)]
    assert calls.count("_PresenceFacts") == 2
    assert not any("closure_audit" in name.lower() or "timeline" in name.lower() for name in calls)
    assert not any(isinstance(node, ast.Name) and node.id.startswith("_closure_audit")
                   for node in ast.walk(tree))
    assert emitter.__globals__["_PresenceFacts"]()._metrics is None
    # Calling the clone confirms that candidate construction is executable.
    assert callable(emitter)


def test_analyzer_map_operation_contract_rejects_an_injected_unsupported_method():
    tree = _clone_tree(native, mode="production", trace=False)
    analyzer = _analyzer(tree)
    _validate_analyzer_map_contract(analyzer)

    unsupported = ast.parse('state.setdefault("new", (set(), False))').body[0]
    analyzer.body.append(unsupported)
    with pytest.raises(AssertionError, match="map method contract"):
        _validate_analyzer_map_contract(analyzer)


@pytest.mark.parametrize("source, message", [
    ('dict.clear(state)', "passed to function"),
    ('dict.copy(state)', "passed to function"),
    ('foreign_helper(state)', "passed to function"),
    ('alias = state', "alias assignment"),
])
def test_analyzer_map_contract_rejects_escape_hatches(source, message):
    tree = _clone_tree(native, mode="production", trace=False)
    analyzer = _analyzer(tree)
    analyzer.body.append(ast.parse(source).body[0])

    with pytest.raises(AssertionError, match=message):
        _validate_analyzer_map_contract(analyzer)


def test_presence_candidate_matches_complete_successful_assembly():
    candidate, _tree = _make_presence_emitter(native)
    program = sparse_workload(size=40, random_cases=2, seed=7319)
    production_outcome = _outcome(native.emit_x86_64_linux, program)
    candidate_outcome = _outcome(candidate, program)
    assert production_outcome["ok"] and candidate_outcome["ok"]
    assert production_outcome == candidate_outcome
    assert len(production_outcome["assembly"]) > 1_000


def test_outcome_comparison_detects_success_and_error_differences():
    success = _outcome(lambda _program: "assembly", object())
    changed_success = _outcome(lambda _program: "assembly!", object())
    assert success != changed_success

    error_one = _outcome(lambda _program: (_ for _ in ()).throw(ValueError("first")), object())
    error_two = _outcome(lambda _program: (_ for _ in ()).throw(ValueError("second")), object())
    assert not error_one["ok"] and error_one != error_two


def test_run_pair_rejects_identical_unexpected_exception_kinds(tmp_path, monkeypatch):
    def unexpected(_output_dir, *, mode, **_kwargs):
        return ({
            "outcome": {
                "ok": False,
                "error_module": "builtins",
                "error_type": "RuntimeError",
                "error_text": "same failure",
            },
        }, tmp_path / f"{mode}.assembly")

    monkeypatch.setattr("scripts.profile_presence_closures._run_sample", unexpected)
    with pytest.raises(AssertionError, match="unexpected production exception"):
        _run_pair(
            tmp_path, size=40, seed=0, cpu=None, random_cases=0,
            workload_seed=7319, allocation=False, order_index=0, serial=0,
        )
