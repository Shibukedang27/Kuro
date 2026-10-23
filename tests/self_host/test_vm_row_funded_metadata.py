"""Candidate layout only: fixed binding descriptors and one link per paid row.

No production metadata or consumer is migrated. Python objects/integers are
specification devices; the native ID-boundary test is a separate obligation.
"""
from dataclasses import dataclass
from itertools import product

import pytest

from test_vm_nonsharing_ledger_protocol import ALPHABET
from test_vm_publication_reservation_model import Cell, EagerLedgerOracle, Op, TerminalOverflow


@dataclass
class Binding:
    generation: int
    head: int = -1
    tail: int = -1
    length: int = 0


@dataclass
class Row:
    generation: int
    cell: Cell
    following: int = -1


class RowFundedLedger:
    """No table indexed by generation ID; historical rows never disappear."""

    def __init__(self, limit, initial):
        self.limit = limit
        self.bindings = [None] * len(initial)
        self.rows = []
        self.logical_used = 0
        self.next_generation = 0
        self.authored_failure = False
        self.terminal = None
        self.reads = []
        for name, cells in enumerate(initial):
            if cells is not None:
                self._reset(name)
                for cell in cells:
                    assert self._append(name, cell, None)

    def _reset(self, name):
        self.bindings[name] = Binding(self.next_generation)
        self.next_generation += 1

    def _append(self, name, cell, op, prefix=0):
        if self.limit is not None and self.logical_used == self.limit:
            self.terminal = TerminalOverflow(op, prefix)
            return False
        binding = self.bindings[name]
        index = len(self.rows)
        self.rows.append(Row(binding.generation, cell))
        if binding.tail == -1:
            binding.head = index
        else:
            self.rows[binding.tail].following = index
        binding.tail = index
        binding.length += 1
        self.logical_used += 1
        return True

    def _indices(self, binding):
        if binding is None:
            return []
        indices = []
        index = binding.head
        for _ in range(binding.length):
            assert index != -1
            indices.append(index)
            index = self.rows[index].following
        assert index == -1
        return indices

    def visible(self):
        return [None if binding is None else
                [self.rows[index].cell for index in self._indices(binding)]
                for binding in self.bindings]

    def apply(self, op):
        assert self.terminal is None
        if op.kind == "copy":
            if op.dst == op.src:
                return
            source = self.bindings[op.src]
            if source is None:
                self.authored_failure = True
                return
            # Local synchronous reader: capture before destructive destination reset.
            # No callback/reentry API is offered or certified by this layout model.
            index, remaining = source.head, source.length
            self._reset(op.dst)
            for prefix in range(remaining):
                row = self.rows[index]
                cell, following = row.cell, row.following
                if not self._append(op.dst, cell, op, prefix):
                    return
                index = following
            return
        if op.kind == "reset":
            self._reset(op.dst)
            return
        if op.kind == "deactivate":
            self.bindings[op.dst] = None
            return
        if op.kind == "replace":
            self._reset(op.dst)
            self._append(op.dst, Cell(op.value, op.display), op)
            return
        binding = self.bindings[op.dst]
        if op.kind == "append":
            if binding is None:
                self.authored_failure = True
            else:
                self._append(op.dst, Cell(op.value, op.display), op)
            return
        indices = self._indices(binding)
        if op.kind == "get":
            cell = None
            if binding is None or not 0 <= op.index < len(indices):
                self.authored_failure = True
            else:
                cell = self.rows[indices[op.index]].cell
            self.reads.append((op.dst, op.index, cell))
            return
        if op.kind == "set":
            if binding is None or not 0 <= op.index < len(indices):
                self.authored_failure = True
            else:
                self.rows[indices[op.index]].cell = Cell(op.value, op.display)
            return
        raise AssertionError(op)

    def assert_invariants(self):
        assert len(self.rows) == self.logical_used
        assert self.limit is None or self.logical_used <= self.limit
        active = [binding for binding in self.bindings if binding is not None]
        assert len({binding.generation for binding in active}) == len(active)
        for binding in active:
            indices = self._indices(binding)
            assert all(self.rows[index].generation == binding.generation for index in indices)
            assert binding.tail == (indices[-1] if indices else -1)
        # Historical chains remain intact even after their descriptor is overwritten.
        by_generation = {}
        for index, row in enumerate(self.rows):
            assert 0 <= row.generation < self.next_generation
            by_generation.setdefault(row.generation, []).append(index)
        for indices in by_generation.values():
            for offset, index in enumerate(indices):
                expected = indices[offset + 1] if offset + 1 < len(indices) else -1
                assert self.rows[index].following == expected
        # by_generation is temporary proof bookkeeping, NOT retained layout metadata.


def _compare(limit, initial, trace):
    oracle = EagerLedgerOracle(limit, initial)
    model = RowFundedLedger(limit, initial)
    previous = model.logical_used
    for op in trace:
        oracle.apply(op)
        model.apply(op)
        model.assert_invariants()
        assert model.logical_used >= previous
        previous = model.logical_used
        assert model.logical_used == oracle.used
        assert model.visible() == oracle.bindings
        assert model.reads == oracle.reads
        assert model.authored_failure == oracle.authored_failure
        assert model.terminal == oracle.terminal
        if model.terminal is not None:
            return model
    return model


def test_exhaustive_row_funded_layout_matches_independent_eager_oracle():
    total = 0
    for limit in (2, 3):
        for trace in product(ALPHABET, repeat=4):
            _compare(limit, ((Cell(10, "ten"),), (Cell(20, "twenty"),)), trace)
            total += 1
    assert total == 131072


def test_empty_churn_allocates_no_row_metadata_then_preserves_historical_chains():
    model = RowFundedLedger(4, ((), (), ()))
    for _ in range(65537):
        model.apply(Op("reset"))
        model.apply(Op("copy", dst=1, src=0))
    assert model.next_generation == 131077
    assert len(model.bindings) == 3
    assert model.logical_used == len(model.rows) == 0
    model.apply(Op("append", value=7, display="0007"))
    model.apply(Op("copy", dst=1, src=0))
    old_rows = [(row.generation, row.cell, row.following) for row in model.rows]
    model.apply(Op("reset"))
    model.apply(Op("append", value=8, display="0008"))
    model.apply(Op("copy", dst=2, src=0))
    assert [(row.generation, row.cell, row.following) for row in model.rows[:2]] == old_rows
    assert model.visible() == [[Cell(8, "0008")], [Cell(7, "0007")], [Cell(8, "0008")]]
    assert model.logical_used == len(model.rows) == 4
    model.assert_invariants()


@pytest.mark.parametrize("available", [0, 1, 2])
def test_copy_partial_prefix_and_source_chain_survive_terminal_admission(available):
    initial = ((Cell(1, "01"), Cell(2, "02"), Cell(3, "03")), (Cell(9, "09"),))
    op = Op("copy", dst=1, src=0)
    model = _compare(4 + available, initial, (op,))
    assert model.visible()[1] == list(initial[0][:available])
    assert model.terminal == TerminalOverflow(op, available)
    assert [model.rows[index].following for index in (0, 1, 2)] == [1, 2, -1]


def test_interleaved_appends_link_only_same_generation_and_set_spends_no_row():
    trace = (Op("append", value=1, display="01"),
             Op("append", dst=1, value=2, display="02"),
             Op("append", value=3, display="03"),
             Op("set", value=9, display="09"),
             Op("copy", dst=2, src=0))
    model = _compare(5, ((), (), ()), trace)
    assert [row.following for row in model.rows] == [2, -1, -1, 4, -1]
    assert model.visible() == [[Cell(9, "09"), Cell(3, "03")], [Cell(2, "02")],
                               [Cell(9, "09"), Cell(3, "03")]]


def test_hosted_layout_does_not_inherit_native_row_ceiling():
    model = RowFundedLedger(None, ((),))
    control = RowFundedLedger(2, ((),))
    for value in range(5):
        op = Op("append", value=value)
        model.apply(op)
        if control.terminal is None:
            control.apply(op)
    assert model.logical_used == 5 and model.terminal is None
    assert control.logical_used == 2 and control.terminal is not None
    model.assert_invariants()


def test_sequential_multistore_preserves_first_destination_and_later_prefix():
    initial = ((Cell(1, "01"), Cell(2, "02")), (), ())
    first = Op("copy", dst=1, src=0)
    second = Op("copy", dst=2, src=0)
    model = _compare(5, initial, (first, second))
    assert model.visible() == [list(initial[0]), list(initial[0]), [Cell(1, "01")]]
    assert model.terminal == TerminalOverflow(second, 1)


def test_real_sized_row_index_range_and_full_budget_empty_copy():
    # Model boundary only, not native allocator or fail-stop evidence.
    capacity = 65536
    model = RowFundedLedger(capacity, ((), (), ()))
    for index in range(capacity):
        model.apply(Op("append", value=index))
    assert model.bindings[0].head == 0
    assert model.bindings[0].tail == capacity - 1
    assert model.bindings[0].length == capacity
    assert model.rows[-1].following == -1
    model.apply(Op("set", index=capacity - 1, value=7, display="007"))
    model.apply(Op("copy", dst=2, src=1))
    assert model.logical_used == capacity and model.terminal is None
    model.assert_invariants()
    op = Op("append", dst=2, value=8)
    model.apply(op)
    assert model.terminal == TerminalOverflow(op, 0)
    assert model.bindings[2].length == 0
    assert len(model.rows) == capacity
    model.assert_invariants()
