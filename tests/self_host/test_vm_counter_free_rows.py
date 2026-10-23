"""Counter-free specification alternative; no production consumer is migrated.

Only immutable scalar cells are modeled. Inactive and
active-empty names have distinct sentinels. No IDs, owner labels, tail table,
sharing, reclamation, borrowed-reader API, or overflow policy is installed.
"""
from dataclasses import dataclass
from itertools import product

import pytest

from test_vm_nonsharing_ledger_protocol import ALPHABET
from test_vm_publication_reservation_model import Cell, EagerLedgerOracle, Op, TerminalOverflow

INACTIVE = -1
EMPTY = -2


@dataclass
class LinkedCell:
    cell: Cell
    following: int = -1


class CounterFreeRows:
    """One head per name; one scalar pair and next index per paid historical row."""

    def __init__(self, limit, initial):
        self.limit = limit
        self.heads = []
        self.rows = []
        self.logical_used = 0
        self.authored_failure = False
        self.terminal = None
        self.reads = []
        # Instrumentation only, not candidate retained metadata.
        self.tail_link_reads = 0
        for name, cells in enumerate(initial):
            self.heads.append(INACTIVE if cells is None else EMPTY)
            if cells is not None:
                for cell in cells:
                    assert self._append(name, cell, None)

    def _indices(self, head):
        # Sentinels MUST be checked before indexing; Python negative indexing
        # would otherwise turn an empty binding into a historical-row alias.
        if head in (INACTIVE, EMPTY):
            return []
        indices = []
        while head != -1:
            assert 0 <= head < len(self.rows)
            indices.append(head)
            head = self.rows[head].following
        return indices

    def visible(self):
        return [None if head == INACTIVE else
                [self.rows[index].cell for index in self._indices(head)]
                for head in self.heads]

    def _append(self, name, cell, op, prefix=0):
        if self.limit is not None and self.logical_used == self.limit:
            self.terminal = TerminalOverflow(op, prefix)
            return False
        head = self.heads[name]
        assert head != INACTIVE
        tail = None
        if head != EMPTY:
            tail = head
            while True:
                self.tail_link_reads += 1
                following = self.rows[tail].following
                if following == -1:
                    break
                tail = following
        index = len(self.rows)
        self.rows.append(LinkedCell(cell))
        if tail is None:
            self.heads[name] = index
        else:
            self.rows[tail].following = index
        self.logical_used += 1
        return True

    def apply(self, op):
        assert self.terminal is None
        if op.kind == "copy":
            if op.dst == op.src:
                return
            head = self.heads[op.src]  # Late source lookup, before destination reset.
            if head == INACTIVE:
                self.authored_failure = True
                return
            self.heads[op.dst] = EMPTY
            index = head
            prefix = 0
            while index not in (EMPTY, -1):
                row = self.rows[index]
                cell, following = row.cell, row.following
                if not self._append(op.dst, cell, op, prefix):
                    return
                index = following
                prefix += 1
            return
        if op.kind == "reset":
            self.heads[op.dst] = EMPTY
            return
        if op.kind == "deactivate":
            self.heads[op.dst] = INACTIVE
            return
        if op.kind == "replace":
            self.heads[op.dst] = EMPTY
            self._append(op.dst, Cell(op.value, op.display), op)
            return
        head = self.heads[op.dst]
        if op.kind == "append":
            if head == INACTIVE:
                self.authored_failure = True
            else:
                self._append(op.dst, Cell(op.value, op.display), op)
            return
        indices = self._indices(head)
        if op.kind in ("get", "set"):
            wanted = op.index
            if op.kind == "get" and wanted < 0:
                wanted += len(indices)
            valid = head != INACTIVE and 0 <= wanted < len(indices)
            if not valid:
                self.authored_failure = True
            if op.kind == "get":
                self.reads.append((op.dst, op.index,
                                   self.rows[indices[wanted]].cell if valid else None))
            elif valid:
                self.rows[indices[wanted]].cell = Cell(op.value, op.display)
            return
        raise AssertionError(op)

    def assert_invariants(self):
        assert len(self.rows) == self.logical_used
        assert self.limit is None or self.logical_used <= self.limit
        # Strictly increasing links give acyclicity even in abandoned chains.
        incoming = set()
        for index, row in enumerate(self.rows):
            following = row.following
            assert following == -1 or index < following < len(self.rows)
            if following != -1:
                assert following not in incoming
                incoming.add(following)
        active_rows = set()
        for head in self.heads:
            assert head in (INACTIVE, EMPTY) or 0 <= head < len(self.rows)
            if head >= 0:
                assert head not in incoming
            indices = self._indices(head)
            assert active_rows.isdisjoint(indices)
            active_rows.update(indices)
        # Sets above are transient proof bookkeeping, not retained layout fields.


def _compare(limit, initial, trace):
    oracle = EagerLedgerOracle(limit, initial)
    model = CounterFreeRows(limit, initial)
    for op in trace:
        oracle.apply(op)
        model.apply(op)
        model.assert_invariants()
        assert model.visible() == oracle.bindings
        assert model.logical_used == oracle.used
        assert model.reads == oracle.reads
        assert model.authored_failure == oracle.authored_failure
        assert model.terminal == oracle.terminal
        if model.terminal is not None:
            break
    return model


def test_exhaustive_counter_free_layout_matches_eager_oracle_in_scalar_domain():
    total = 0
    for limit in (2, 3):
        for trace in product(ALPHABET, repeat=4):
            _compare(limit, ((Cell(10, "ten"),), (Cell(20, "twenty"),)), trace)
            total += 1
    assert total == 131072


def test_empty_churn_retains_only_heads_and_no_generation_counter():
    model = CounterFreeRows(0, ((), (), None))
    for _ in range(65537):
        model.apply(Op("reset"))
        model.apply(Op("copy", dst=1, src=0))
    assert model.heads == [EMPTY, EMPTY, INACTIVE]
    assert model.rows == [] and model.logical_used == 0
    assert not hasattr(model, "next_generation")
    model.assert_invariants()


def test_sentinels_do_not_alias_retained_historical_rows():
    model = _compare(3, ((Cell(7, "007"), Cell(8, "008")), (), None),
                     (Op("reset"), Op("get"), Op("get", dst=2),
                      Op("set", value=9), Op("append", value=4, display="004")))
    assert model.heads == [2, EMPTY, INACTIVE]
    assert model.rows[0].cell == Cell(7, "007")
    assert model.rows[1].cell == Cell(8, "008")
    assert model.reads == [(0, 0, None), (2, 0, None)]


@pytest.mark.parametrize("available", [0, 1, 2])
def test_copy_keeps_exact_destructive_paid_prefix(available):
    initial = ((Cell(1, "01"), Cell(2, "02"), Cell(3, "03")), (Cell(9, "09"),))
    op = Op("copy", dst=1, src=0)
    model = _compare(4 + available, initial, (op,))
    assert model.visible()[1] == list(initial[0][:available])
    assert model.terminal == TerminalOverflow(op, available)
    assert [model.rows[i].following for i in (0, 1, 2)] == [1, 2, -1]


def test_copy_is_not_aliasing_and_reset_keeps_old_chains():
    model = _compare(6, ((), (), ()),
                     (Op("append", value=1, display="01"),
                      Op("append", dst=1, value=2, display="02"),
                      Op("append", value=3, display="03"),
                      Op("copy", dst=2, src=0),
                      Op("set", dst=2, value=9, display="09"),
                      Op("reset"), Op("append", value=4, display="04")))
    assert model.visible() == [[Cell(4, "04")], [Cell(2, "02")],
                               [Cell(9, "09"), Cell(3, "03")]]
    assert [row.following for row in model.rows] == [2, -1, -1, 4, -1, -1]
    assert model.rows[0].cell == Cell(1, "01")


def test_sequential_multistore_keeps_completed_and_partial_destinations():
    initial = ((Cell(1, "01"), Cell(2, "02")), (), ())
    first, second = Op("copy", dst=1, src=0), Op("copy", dst=2, src=0)
    model = _compare(5, initial, (first, second))
    assert model.visible() == [list(initial[0]), list(initial[0]), [Cell(1, "01")]]
    assert model.terminal == TerminalOverflow(second, 1)


def test_full_budget_empty_copy_self_copy_and_missing_source_precedence():
    model = _compare(1, ((Cell(7, "007"),), (), None),
                     (Op("copy", dst=2, src=2), Op("copy", src=2),
                      Op("set", value=8, display="008"), Op("copy", dst=2, src=1)))
    assert model.heads == [0, EMPTY, EMPTY]
    assert model.logical_used == 1 and model.terminal is None
    assert model.rows[0].cell == Cell(8, "008")
    assert model.authored_failure


def test_tail_scan_cost_is_quadratic_not_a_free_memory_optimization():
    count = 256
    model = CounterFreeRows(count, ((),))
    for value in range(count):
        model.apply(Op("append", value=value))
    assert model.tail_link_reads == count * (count - 1) // 2 == 32640
    model.assert_invariants()


@pytest.mark.parametrize("name,index,expected", [
    (0, -1, Cell(8, "008")), (0, -2, Cell(7, "007")),
    (0, -3, None), (0, 2, None), (1, -1, None), (2, -1, None),
])
def test_get_negative_offsets_are_not_head_sentinels(name, index, expected):
    # Directed production-helper semantics; the independent eager oracle only
    # defines nonnegative Get, so do not use it to certify this extension.
    model = CounterFreeRows(2, ((Cell(7, "007"), Cell(8, "008")), (), None))
    model.apply(Op("get", dst=name, index=index))
    assert model.reads == [(name, index, expected)]
    assert model.authored_failure == (expected is None)
    model.assert_invariants()


def test_set_does_not_normalize_negative_indices_or_spend_rows():
    model = _compare(1, ((Cell(7, "007"),),),
                     (Op("set", index=-1, value=8, display="008"),))
    assert model.visible() == [[Cell(7, "007")]]
    assert model.authored_failure and model.logical_used == 1


def test_real_sized_indices_without_quadratic_fixture_construction():
    # Publish one row into each pre-existing empty name: linear fixture setup.
    # Name and row ceilings coincide today; no native memory behavior is claimed.
    count = 65536
    model = CounterFreeRows(count, ((),) * count)
    for name in range(count):
        model.apply(Op("append", dst=name, value=name))
    assert model.heads[0] == 0 and model.heads[-1] == count - 1
    model.apply(Op("set", dst=count - 1, value=7, display="007"))
    model.apply(Op("reset", dst=0))
    op = Op("append", dst=0, value=9)
    model.apply(op)
    assert model.heads[0] == EMPTY
    assert model.terminal == TerminalOverflow(op, 0)
    assert model.rows[-1].cell == Cell(7, "007")
    model.assert_invariants()


def test_hosted_candidate_has_no_native_row_ceiling():
    model = CounterFreeRows(None, ((),))
    for value in range(5):
        model.apply(Op("append", value=value))
    assert model.logical_used == 5 and model.terminal is None
    model.assert_invariants()
