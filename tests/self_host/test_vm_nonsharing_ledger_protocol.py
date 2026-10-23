"""Model-only prerequisite: monotonic eager debit, stable metadata, no sharing.

This is not a replacement VM or native storage layout. Immutable scalar cells
exclude marker resolution and moving Text. Reader tokens describe an internal
no-reentry obligation, not a new user-visible lock/failure or an asynchronous
pin. Metadata exhaustion is deliberately a separate rejected design outcome.
"""
from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
from itertools import product

import pytest

from test_vm_publication_reservation_model import (
    Cell, EagerLedgerOracle, Op, TerminalOverflow,
)


class ProtocolViolation(Exception):
    """An excluded helper reentry, never an authored VM failure."""


class MetadataExhausted(Exception):
    """A candidate layout's extra failure, not native row fail-stop."""


@dataclass
class Generation:
    # Row indices are a specification convenience, NOT a proposed native table.
    rows: list[int]


@dataclass(frozen=True)
class Reader:
    serial: int
    generation: int
    length: int


class NonsharingLedger:
    def __init__(self, limit, initial, metadata_limit=None):
        self.limit = limit  # None models hosted admission without a row ceiling.
        self.metadata_limit = metadata_limit
        self.bindings = []
        self.generations = {}
        self.rows = []  # Retained historical (owner generation, scalar cell).
        self.logical_used = 0
        self.next_generation = 0
        self.next_reader = 0
        self.readers = {}
        self.authored_failure = False
        self.terminal = None
        self.reads = []
        for cells in initial:
            if cells is None:
                self.bindings.append(None)
            else:
                generation = self._new_generation()
                self.bindings.append(generation)
                for cell in cells:
                    assert self.limit is None or self.logical_used < self.limit
                    self._commit_row(generation, cell)

    def _new_generation(self):
        if self.metadata_limit is not None and self.next_generation >= self.metadata_limit:
            raise MetadataExhausted("row credit does not fund per-generation metadata")
        generation = self.next_generation
        self.next_generation += 1
        self.generations[generation] = Generation([])
        return generation

    def _commit_row(self, generation, cell):
        # One eager publication point. No bulk reservation and no refund.
        self.generations[generation].rows.append(len(self.rows))
        self.rows.append((generation, cell))
        self.logical_used += 1

    def _append(self, generation, cell, op, prefix=0):
        if self.limit is not None and self.logical_used == self.limit:
            self.terminal = TerminalOverflow(op, prefix)
            return False
        self._commit_row(generation, cell)
        return True

    def snapshot(self, generation):
        return [self.rows[row][1] for row in self.generations[generation].rows]

    def visible(self):
        return [None if generation is None else self.snapshot(generation)
                for generation in self.bindings]

    @contextmanager
    def borrow(self, name):
        if self.terminal is not None:
            raise ProtocolViolation("no operation after terminal overflow")
        generation = self.bindings[name]
        if generation is None:
            raise ProtocolViolation("borrow requires successful late-name lookup")
        token = Reader(self.next_reader, generation, len(self.generations[generation].rows))
        self.next_reader += 1
        self.readers[token.serial] = token
        try:
            yield token
        finally:
            # Model bookkeeping only: no native cleanup after fail-stop is promised.
            del self.readers[token.serial]

    def read(self, token, index):
        if self.terminal is not None:
            raise ProtocolViolation("no read after terminal overflow")
        if self.readers.get(token.serial) is not token:
            raise ProtocolViolation("expired or foreign reader")
        if not 0 <= index < token.length:
            raise IndexError(index)
        row = self.generations[token.generation].rows[index]
        return self.rows[row][1]

    def apply(self, op):
        if self.terminal is not None:
            raise ProtocolViolation("no operation after terminal overflow")
        if self.readers:
            # External entry is excluded, even for another name or a nested copy.
            # Copy's private append/reset path below does not reenter apply().
            raise ProtocolViolation("helper entry while synchronous reader is live")
        if op.kind == "copy":
            if op.dst == op.src:
                return
            if self.bindings[op.src] is None:
                self.authored_failure = True
                return
            with self.borrow(op.src) as reader:
                self.bindings[op.dst] = self._new_generation()
                for index in range(reader.length):
                    cell = self.read(reader, index)
                    if not self._append(self.bindings[op.dst], cell, op, index):
                        return
            return
        if op.kind == "reset":
            self.bindings[op.dst] = self._new_generation()
            return
        if op.kind == "deactivate":
            self.bindings[op.dst] = None
            return
        if op.kind == "replace":
            self.bindings[op.dst] = self._new_generation()
            self._append(self.bindings[op.dst], Cell(op.value, op.display), op)
            return
        generation = self.bindings[op.dst]
        rows = [] if generation is None else self.generations[generation].rows
        if op.kind == "get":
            cell = None
            if generation is None or not 0 <= op.index < len(rows):
                self.authored_failure = True
            else:
                cell = self.rows[rows[op.index]][1]
            self.reads.append((op.dst, op.index, cell))
            return
        if op.kind == "set":
            if generation is None or not 0 <= op.index < len(rows):
                self.authored_failure = True
            else:
                self.rows[rows[op.index]] = (generation, Cell(op.value, op.display))
            return
        if op.kind == "append":
            if generation is None:
                self.authored_failure = True
            else:
                self._append(generation, Cell(op.value, op.display), op)
            return
        raise AssertionError(op)

    def assert_invariants(self):
        assert self.logical_used == len(self.rows)
        assert self.limit is None or self.logical_used <= self.limit
        assert list(self.generations) == list(range(self.next_generation))
        active = [generation for generation in self.bindings if generation is not None]
        assert len(active) == len(set(active))  # No aliases, even for empty copies.
        assert all(generation in self.generations for generation in active)
        indexed = []
        for generation, metadata in self.generations.items():
            assert metadata.rows == sorted(metadata.rows)
            for row in metadata.rows:
                assert self.rows[row][0] == generation
                indexed.append(row)
        assert sorted(indexed) == list(range(len(self.rows)))
        for token in self.readers.values():
            assert token.generation in self.generations
            assert token.length == len(self.generations[token.generation].rows)


def _compare(limit, initial, trace):
    oracle = EagerLedgerOracle(limit, initial)
    model = NonsharingLedger(limit, initial)
    previous = model.logical_used
    for op in trace:
        oracle.apply(op)
        model.apply(op)
        model.assert_invariants()
        assert not model.readers
        assert model.logical_used >= previous
        previous = model.logical_used
        assert oracle.used == model.logical_used
        assert oracle.terminal == model.terminal
        # Unlike the sharing model, even destructive terminal prefixes agree.
        assert oracle.bindings == model.visible()
        assert oracle.reads == model.reads
        assert oracle.authored_failure == model.authored_failure
        if model.terminal is not None:
            return


ALPHABET = (
    Op("copy", dst=0, src=1), Op("copy", dst=1, src=0),
    Op("copy", dst=0, src=0), Op("copy", dst=1, src=1),
    Op("reset", dst=0), Op("reset", dst=1),
    Op("deactivate", dst=0), Op("deactivate", dst=1),
    Op("replace", dst=0, value=30, display="thirty"),
    Op("replace", dst=1, value=40, display="forty"),
    Op("get", dst=0), Op("get", dst=1), Op("get", dst=0, index=99),
    Op("set", dst=0, value=50, display="fifty"),
    Op("set", dst=0, index=99, value=60, display="sixty"),
    Op("append", dst=0, value=70, display="seventy"),
)


def test_exhaustive_nonsharing_traces_match_independent_eager_oracle():
    total = 0
    for limit in (2, 3):
        for trace in product(ALPHABET, repeat=4):
            _compare(limit, ((Cell(10, "ten"),), (Cell(20, "twenty"),)), trace)
            total += 1
    assert total == 131072


@pytest.mark.parametrize("available", [0, 1, 2])
def test_terminal_copy_keeps_exact_destructive_prefix_without_bulk_admission(available):
    initial = ((Cell(1, "01"), Cell(2, "02"), Cell(3, "03")), (Cell(9, "09"),))
    model = NonsharingLedger(4 + available, initial)
    op = Op("copy", dst=1, src=0)
    _compare(4 + available, initial, (op,))
    model.apply(op)
    assert model.terminal == TerminalOverflow(op, available)
    assert model.visible()[1] == list(initial[0][:available])
    assert model.logical_used == 4 + available
    model.assert_invariants()
    with pytest.raises(ProtocolViolation, match="after terminal"):
        model.apply(Op("get"))


@pytest.mark.parametrize("op", [
    Op("set", value=9, display="09"), Op("append", value=9),
    Op("reset"), Op("deactivate"), Op("copy", dst=1, src=0),
])
def test_synchronous_reader_has_no_credit_and_excludes_reentry(op):
    original = Cell(1, "01")
    model = NonsharingLedger(1, ((original,), ()))
    with model.borrow(0) as reader:
        before = (model.visible(), list(model.rows), model.logical_used, model.next_generation)
        with pytest.raises(ProtocolViolation, match="while synchronous reader"):
            model.apply(op)
        assert (model.visible(), model.rows, model.logical_used, model.next_generation) == before
        assert model.read(reader, 0) == original
        model.assert_invariants()
    with pytest.raises(ProtocolViolation, match="expired or foreign"):
        model.read(reader, 0)
    # After release, Set remains legal at a full logical budget; no detachment.
    model.apply(Op("set", value=9, display="09"))
    assert model.visible()[0] == [Cell(9, "09")]
    assert model.logical_used == len(model.rows) == 1


def test_reader_tokens_are_scoped_and_cannot_be_reused_across_models():
    model = NonsharingLedger(1, ((Cell(1, "01"),),))
    other = NonsharingLedger(1, ((Cell(2, "02"),),))
    with model.borrow(0) as token, other.borrow(0) as foreign:
        assert token == foreign  # Coincident fields are not an ownership proof.
        with pytest.raises(ProtocolViolation, match="foreign"):
            model.read(foreign, 0)
    assert not model.readers and not other.readers


def test_empty_generations_exhaust_a_naive_metadata_table_without_row_debits():
    model = NonsharingLedger(1, ((),), metadata_limit=4)
    for _ in range(3):
        model.apply(Op("reset"))
    assert model.logical_used == len(model.rows) == 0
    assert model.next_generation == 4
    with pytest.raises(MetadataExhausted):
        model.apply(Op("reset"))
    assert model.terminal is None and not model.authored_failure
    # An eager logical-row oracle has no such failure: this layout is rejected.
    oracle = EagerLedgerOracle(1, ((),))
    for _ in range(4):
        oracle.apply(Op("reset"))
    assert oracle.used == 0 and oracle.terminal is None
    model.assert_invariants()


def test_hosted_mode_has_no_inherited_native_logical_ceiling():
    model = NonsharingLedger(None, ((),))
    # A deliberately small native control, not the actual native capacity.
    native_control = NonsharingLedger(2, ((),))
    for _ in range(3):
        model.apply(Op("append", value=7, display="007"))
        native_control.apply(Op("append", value=7, display="007"))
    assert model.logical_used == 3 and model.terminal is None
    assert native_control.logical_used == 2 and native_control.terminal is not None
    model.assert_invariants()


def test_retained_names_resolve_late_while_eager_copies_preserve_cells():
    original = Cell(1, "001")
    model = NonsharingLedger(3, ((original,), ()))
    held_name = 0  # A name token, explicitly not a captured generation handle.
    model.apply(Op("copy", dst=1, src=0))
    old_generation = model.bindings[0]
    model.apply(Op("replace", dst=0, value=9, display="009"))
    model.apply(Op("get", dst=held_name))
    assert model.reads[-1] == (0, 0, Cell(9, "009"))
    assert model.visible()[1] == [original]
    assert model.snapshot(old_generation) == [original]
    assert model.logical_used == len(model.rows) == 3
    model.assert_invariants()


def test_inactive_self_copy_and_missing_source_do_not_spend_metadata_or_rows():
    model = NonsharingLedger(1, (None, (Cell(1, "01"),)))
    before = (model.visible(), model.next_generation, model.logical_used)
    model.apply(Op("copy", dst=0, src=0))
    assert not model.authored_failure
    model.apply(Op("copy", dst=1, src=0))
    assert model.authored_failure
    assert (model.visible(), model.next_generation, model.logical_used) == before


def test_multistore_is_sequential_not_atomic_when_later_copy_overflows():
    model = NonsharingLedger(5, ((Cell(1, "01"), Cell(2, "02")), (), ()))
    model.apply(Op("copy", dst=1, src=0))
    first = model.bindings[1]
    model.apply(Op("copy", dst=2, src=0))
    assert model.visible() == [
        [Cell(1, "01"), Cell(2, "02")],
        [Cell(1, "01"), Cell(2, "02")], [Cell(1, "01")],
    ]
    assert model.bindings[1] == first
    assert model.terminal == TerminalOverflow(Op("copy", dst=2, src=0), 1)
    assert model.logical_used == 5
    model.assert_invariants()
