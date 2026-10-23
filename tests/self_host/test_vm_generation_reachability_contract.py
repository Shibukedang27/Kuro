"""Frozen-source audit tripwires, not an automatic reachability theorem.

The public row-funding argument additionally depends on branch predicates,
normal initialization, fail-stop dispatch and the absence of public deletion.
A new caller/mutation requires re-auditing that argument, not updating a list
without reviewing its semantics.
"""
from pathlib import Path

import pytest

from compiler.pipeline import compile_source

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def vm_ir():
    result = compile_source((ROOT / "self_host/vm.kuro").read_text(encoding="utf-8"))
    assert result.ok, result.diags.render_all()
    return result.ir


def _bodies(program):
    yield "<main>", program.main
    for name, function in program.functions.items():
        yield name, function.body


def test_generation_creating_helpers_have_only_audited_callers(vm_ir):
    expected = {
        "VMMarkCollection": ["VMResetCollection", "VMStep"],
        "VMResetCollection": ["VMCopyCollection", "VMStep"],
        "VMCopyCollection": ["VMStep"],
    }
    for callee, callers in expected.items():
        observed = [name for name, body in _bodies(vm_ir) for item in body
                    if item.op == "CALL" and item.args[0] == callee]
        assert sorted(observed) == sorted(callers)


def test_counter_is_initialized_once_and_incremented_only_by_mark_reset(vm_ir):
    writes = [(name, item.op) for name, body in _bodies(vm_ir) for item in body
              if item.op in {"STORE_LIST", "ADD", "SET", "APPEND"}
              and item.args[0] == "VMNextCollectionId"]
    assert writes == [("<main>", "STORE_LIST"), ("VMMarkCollection", "ADD"),
                      ("VMResetCollection", "ADD")]


def test_row_debit_is_initialized_once_and_never_refunded(vm_ir):
    writes = [(name, item.op) for name, body in _bodies(vm_ir) for item in body
              if item.op in {"STORE_LIST", "ADD", "SET", "APPEND"}
              and item.args[0] == "VMCollectionEntryCount"]
    assert writes == [("<main>", "STORE_LIST"), ("VMAppendCollectionItem", "ADD")]
    append = vm_ir.functions["VMAppendCollectionItem"].body
    debit = [item for item in append if item.op == "ADD" and item.args[0] == "VMCollectionEntryCount"]
    constants = {item.dest: item.args[0] for item in append if item.op == "CONST"}
    assert constants[debit[0].args[1]] == 1
