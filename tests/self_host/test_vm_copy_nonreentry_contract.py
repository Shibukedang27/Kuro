"""Test-only guardrail: stable IDs alone do not protect an in-flight reader.

The reservation model deliberately excludes reentry. These counterexamples are
not production failures: the closed current eager-copy call graph has no user
callback or bytecode-dispatch edge. New edges/effects require a fresh review.
"""
from pathlib import Path

import pytest

from compiler.pipeline import compile_source
from test_vm_publication_reservation_model import Cell, Op, StableGenerationCowModel


ROOT = Path(__file__).resolve().parents[2]


def test_eager_copy_has_a_closed_nonrecursive_helper_call_graph():
    compiled = compile_source((ROOT / "self_host/vm.kuro").read_text(encoding="utf-8"))
    assert compiled.ok, compiled.diags.render_all()
    # Deliberately closed: even a new apparently harmless edge needs review of
    # source-ID, row-position and raw/display scratch lifetimes before acceptance.
    expected = {
        "VMCopyCollection": {"VMFindCollection", "VMResetCollection", "VMAppendCollectionItem"},
        "VMFindCollection": set(),
        "VMFindCollectionSlot": set(),
        "VMResetCollection": {"VMFindCollectionSlot", "VMMarkCollection"},
        "VMMarkCollection": {"VMFindCollection", "VMFindCollectionSlot"},
        "VMAppendCollectionItem": {"VMFindCollection", "__KuroAdmitRow"},
    }
    # CALL is checked separately. INPUT/PRINT, dynamic invocation and VM dispatch
    # are not admitted by this whitelist. This is a source/IR regression tripwire,
    # not a concurrency theorem or a proof about arbitrary future runtime opcodes.
    effects = {
        "ADD", "AND", "APPEND", "BINOP", "CALL", "CMP", "CONST", "GET",
        "JUMP", "JUMPF", "LABEL", "LOADVAR", "LOOP_GUARD", "RETURN", "SET", "STORE_LIST",
    }
    visited = set()

    def visit(name, active):
        assert name not in active, f"copy helper reentry: {active + (name,)}"
        if name == "__KuroAdmitRow":
            assert name not in compiled.ir.functions  # reserved private leaf
            return
        if name in visited:
            return
        body = compiled.ir.functions[name].body
        calls = {instruction.args[0] for instruction in body if instruction.op == "CALL"}
        assert calls == expected[name], f"review new copy-helper edges in {name}"
        assert {instruction.op for instruction in body} <= effects
        for callee in calls:
            visit(callee, active + (name,))
        visited.add(name)

    visit("VMCopyCollection", ())
    assert visited == set(expected)


@pytest.mark.parametrize("mutation", [
    Op("set", dst=0, index=0, value=99, display="changed"),
    Op("append", dst=0, value=99, display="changed"),
], ids=["set", "append"])
def test_a_borrowed_stable_id_is_not_an_immutable_snapshot(mutation):
    model = StableGenerationCowModel(3, ((Cell(10, "original"),),))
    borrowed_id = model.bindings[0]
    captured_cells = tuple(model.generations[borrowed_id])
    # An uncounted in-flight reader is outside this sequential model's contract.
    # Holding its ID in a local variable does not make _reference_count see it.
    model.apply(mutation)
    assert model.bindings[0] == borrowed_id
    assert tuple(model.generations[borrowed_id]) != captured_cells
    model.assert_accounting_invariants()


def test_a_debited_second_binding_supplies_snapshot_detachment_credit():
    model = StableGenerationCowModel(2, ((Cell(10, "original"),), ()))
    model.apply(Op("copy", dst=1, src=0))
    snapshot_id = model.bindings[1]
    assert model.logical_used == model.limit == 2
    assert model.physical_cells == 1
    model.apply(Op("set", dst=0, index=0, value=99, display="changed"))
    assert model.bindings[0] != snapshot_id
    assert model.generations[snapshot_id] == [Cell(10, "original")]
    assert model.generations[model.bindings[0]] == [Cell(99, "changed")]
    assert model.logical_used == model.physical_cells == 2
    model.assert_accounting_invariants()
