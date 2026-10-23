"""Current private ledger consumers, not a counter-free migration proof.

These IR tripwires require a fresh lifetime review when helper edges, effects,
field consumers, or publication order change. They do not prove backend memory
atomicity, allocation failure equivalence, or future callback safety.
"""
from pathlib import Path

import pytest

from compiler.pipeline import compile_source

ROOT = Path(__file__).resolve().parents[2]
EDGES = {
    "VMFindCollectionSlot": set(),
    "VMFindCollection": set(),
    "VMMarkCollection": {"VMFindCollection", "VMFindCollectionSlot"},
    "VMResetCollection": {"VMFindCollectionSlot", "VMMarkCollection"},
    "VMDeactivateCollection": {"VMFindCollectionSlot"},
    "VMAppendCollectionItem": {"VMFindCollection", "__KuroAdmitRow"},
    "VMGetCollectionItem": {"VMFindCollection", "VMLengthCollection"},
    "VMLengthCollection": {"VMFindCollection"},
    "VMSetCollectionItem": {"VMFindCollection"},
    "VMCopyCollection": {"VMFindCollection", "VMResetCollection", "VMAppendCollectionItem"},
}
EFFECTS = {
    "ADD", "AND", "APPEND", "BINOP", "CALL", "CMP", "CONST", "GET",
    "JUMP", "JUMPF", "LABEL", "LOADVAR", "LOOP_GUARD", "RETURN", "SET", "STORE_LIST",
}


@pytest.fixture(scope="module")
def ledger_ir():
    result = compile_source((ROOT / "self_host/vm.kuro").read_text(encoding="utf-8"))
    assert result.ok, result.diags.render_all()
    return result.ir


@pytest.mark.parametrize("root", sorted(EDGES))
def test_collection_borrows_have_closed_nonrecursive_effect_graph(ledger_ir, root):
    visited = set()

    def visit(name, active):
        assert name not in active, f"review collection helper reentry: {active + (name,)}"
        if name == "__KuroAdmitRow":
            assert name not in ledger_ir.functions  # compiler-private leaf
            return
        if name in visited:
            return
        body = ledger_ir.functions[name].body
        calls = {item.args[0] for item in body if item.op == "CALL"}
        assert calls == EDGES[name], f"review new lifetime edges in {name}"
        assert {item.op for item in body} <= EFFECTS
        for callee in calls:
            visit(callee, active + (name,))
        visited.add(name)

    visit(root, ())


def test_private_id_columns_have_only_the_audited_direct_consumers(ledger_ir):
    expected = {
        "VMNextCollectionId": {"VMMarkCollection", "VMResetCollection"},
        "VMCollectionIds": {
            "VMFindCollection", "VMMarkCollection", "VMResetCollection",
            "VMDeactivateCollection", "VMAppendCollectionItem", "VMGetCollectionItem",
            "VMLengthCollection", "VMSetCollectionItem", "VMCopyCollection",
        },
        "VMCollectionOwners": {
            "VMAppendCollectionItem", "VMGetCollectionItem", "VMLengthCollection",
            "VMSetCollectionItem", "VMCopyCollection",
        },
    }
    # LOADVAR matters too: a future alias of an entire column must trigger review.
    for column, consumers in expected.items():
        observed = {
            name for name, function in ledger_ir.functions.items()
            if any(item.op in {"GET", "SET", "APPEND", "LOADVAR", "STORE_LIST", "ADD"}
                   and item.args[0] == column for item in function.body)
        }
        assert observed == consumers


@pytest.mark.parametrize("callee,live_scratch", [
    ("VMLengthCollection", {"VMGetCollectionItem_Id", "VMGetCollectionItem_Wanted"}),
    ("VMResetCollection", {"VMCopyCollection_SourceId"}),
    ("VMAppendCollectionItem", {
        "VMCopyCollection_SourceId", "VMCopyCollection_Pos", "VMCopyCollection_Value",
    }),
])
def test_nested_calls_do_not_clobber_audited_live_scratch(ledger_ir, callee, live_scratch):
    pending = [callee]
    visited = set()
    while pending:
        name = pending.pop()
        if name in visited or name == "__KuroAdmitRow":
            continue
        visited.add(name)
        body = ledger_ir.functions[name].body
        writes = {item.args[0] for item in body
                  if item.op in {"STORE_LIST", "ADD", "SET", "APPEND"}}
        assert not writes & live_scratch, f"{name} clobbers {writes & live_scratch}"
        pending.extend(item.args[0] for item in body if item.op == "CALL")


def _events(ledger_ir, name, selected):
    return [(item.op, item.args[0]) for item in ledger_ir.functions[name].body
            if (item.op, item.args[0] if item.args else None) in selected]


def test_append_admits_before_each_row_column_and_commits_count_last(ledger_ir):
    selected = {("CALL", "__KuroAdmitRow"), ("ADD", "VMCollectionEntryCount")}
    columns = ["VMCollectionOwners", "VMCollectionItems", "VMCollectionItemDisplay"]
    selected |= {(op, column) for op in ("SET", "APPEND") for column in columns}
    # Linear IR contains both mutually exclusive seed-Set and grown-Append arms.
    assert _events(ledger_ir, "VMAppendCollectionItem", selected) == [
        ("CALL", "__KuroAdmitRow"),
        *[("SET", column) for column in columns],
        *[("APPEND", column) for column in columns],
        ("ADD", "VMCollectionEntryCount"),
    ]


def test_copy_captures_id_before_reset_and_scalar_pair_before_append(ledger_ir):
    selected = {
        ("GET", "VMCollectionIds"), ("STORE_LIST", "VMCopyCollection_SourceId"),
        ("CALL", "VMResetCollection"), ("GET", "VMCollectionOwners"),
        ("GET", "VMCollectionItems"), ("STORE_LIST", "VMCopyCollection_Value"),
        ("GET", "VMCollectionItemDisplay"), ("STORE_LIST", "VMAppendCollectionDisplay"),
        ("CALL", "VMAppendCollectionItem"),
    }
    assert _events(ledger_ir, "VMCopyCollection", selected) == [
        ("GET", "VMCollectionIds"), ("STORE_LIST", "VMCopyCollection_SourceId"),
        ("CALL", "VMResetCollection"), ("GET", "VMCollectionOwners"),
        ("GET", "VMCollectionItems"), ("STORE_LIST", "VMCopyCollection_Value"),
        ("GET", "VMCollectionItemDisplay"), ("STORE_LIST", "VMAppendCollectionDisplay"),
        ("CALL", "VMAppendCollectionItem"),
    ]


def test_get_captures_id_across_negative_length_without_mutator_edge(ledger_ir):
    selected = {
        ("STORE_LIST", "VMGetCollectionItem_Id"), ("CALL", "VMLengthCollection"),
        ("GET", "VMCollectionOwners"), ("GET", "VMCollectionItems"),
        ("GET", "VMCollectionItemDisplay"),
    }
    assert _events(ledger_ir, "VMGetCollectionItem", selected) == [
        ("STORE_LIST", "VMGetCollectionItem_Id"),  # inactive fallback
        ("STORE_LIST", "VMGetCollectionItem_Id"),  # successful lookup arm
        ("CALL", "VMLengthCollection"), ("GET", "VMCollectionOwners"),
        ("GET", "VMCollectionItems"), ("GET", "VMCollectionItemDisplay"),
    ]


def test_set_publishes_raw_then_display_without_debit_or_callback(ledger_ir):
    selected = {
        ("SET", "VMCollectionItems"), ("SET", "VMCollectionItemDisplay"),
        ("CALL", "__KuroAdmitRow"), ("ADD", "VMCollectionEntryCount"),
    }
    assert _events(ledger_ir, "VMSetCollectionItem", selected) == [
        ("SET", "VMCollectionItems"), ("SET", "VMCollectionItemDisplay"),
    ]
