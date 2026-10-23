"""Model-only bounded ledger comparison; this is not native emulation.

The two independent models use scalar immutable value/display cells (marker
late-name resolution and moving Text are outside this model). The COW model
charges a separate monotonic logical eager debit even when a publication
shares a stable generation, while counting physical cell slots separately.
This is a design proof prerequisite for considering compatibility-preserving
logical admission, not a claim about actual headroom or production equivalence.
A native fail-stop is represented only as a terminal overflow event: after it,
no operation runs and internal post-mortem state is deliberately not compared.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Optional, Sequence

import pytest


@dataclass(frozen=True)
class Cell:
    """An immutable scalar value/display pair; markers and Text are excluded."""

    value: int
    display: str


@dataclass(frozen=True)
class Op:
    kind: str
    dst: int = 0
    src: int = 0
    index: int = 0
    value: int = 0
    display: str = "v"

    def __str__(self) -> str:
        if self.kind == "copy":
            return f"copy({self.dst}<-{self.src})"
        if self.kind in {"reset", "deactivate", "replace"}:
            return f"{self.kind}({self.dst})"
        if self.kind in {"get", "set"}:
            return f"{self.kind}({self.dst},{self.index})"
        if self.kind == "append":
            return f"append({self.dst},{self.value})"
        return self.kind


@dataclass(frozen=True)
class TerminalOverflow:
    operation: Op
    copied_prefix: int


class EagerLedgerOracle:
    """Independent eager-copy ledger oracle, with destructive partial copies."""

    def __init__(self, limit: int, initial: Sequence[Optional[Sequence[Cell]]]):
        self.limit = limit
        self.bindings = [None if cells is None else list(cells) for cells in initial]
        self.used = sum(len(cells) for cells in self.bindings if cells is not None)
        assert self.used <= limit
        self.authored_failure = False
        self.terminal: Optional[TerminalOverflow] = None
        self.reads: list[tuple[int, int, Optional[Cell]]] = []

    def apply(self, op: Op) -> None:
        if self.terminal is not None:
            raise AssertionError("the fail-stop model accepts no post-terminal operations")

        if op.kind == "copy":
            # Identity is tested before source lookup, including an inactive slot.
            if op.dst == op.src:
                return
            source = self.bindings[op.src]
            if source is None:
                self.authored_failure = True
                return
            pinned_source = list(source)
            self.bindings[op.dst] = []
            copied = 0
            for cell in pinned_source:
                if self.used == self.limit:
                    self.terminal = TerminalOverflow(op, copied)
                    return
                self.bindings[op.dst].append(cell)
                self.used += 1
                copied += 1
            return

        if op.kind == "reset":
            self.bindings[op.dst] = []
            return

        if op.kind == "deactivate":
            self.bindings[op.dst] = None
            return

        if op.kind == "replace":
            # Replacement is modeled as reset followed by one eager append.
            self.bindings[op.dst] = []
            if self.used == self.limit:
                self.terminal = TerminalOverflow(op, 0)
                return
            self.bindings[op.dst].append(Cell(op.value, op.display))
            self.used += 1
            return

        if op.kind == "get":
            cells = self.bindings[op.dst]
            if cells is None or not 0 <= op.index < len(cells):
                self.authored_failure = True
                self.reads.append((op.dst, op.index, None))
            else:
                self.reads.append((op.dst, op.index, cells[op.index]))
            return

        if op.kind == "set":
            cells = self.bindings[op.dst]
            if cells is None or not 0 <= op.index < len(cells):
                self.authored_failure = True
                return
            cells[op.index] = Cell(op.value, op.display)
            return

        if op.kind == "append":
            cells = self.bindings[op.dst]
            if cells is None:
                self.authored_failure = True
                return
            if self.used == self.limit:
                self.terminal = TerminalOverflow(op, 0)
                return
            cells.append(Cell(op.value, op.display))
            self.used += 1
            return

        raise AssertionError(f"unknown oracle operation: {op.kind}")


class StableGenerationCowModel:
    """Stable-generation COW model with logical debit and physical slots."""

    def __init__(self, limit: int, initial: Sequence[Optional[Sequence[Cell]]]):
        self.limit = limit
        self.generations: dict[int, list[Cell]] = {}
        self.bindings: list[Optional[int]] = []
        self._next_generation = 0
        for cells in initial:
            if cells is None:
                self.bindings.append(None)
            else:
                generation = self._allocate_generation(cells)
                self.bindings.append(generation)
        self.logical_used = sum(
            len(self.generations[generation])
            for generation in self.bindings
            if generation is not None
        )
        self.physical_cells = self.logical_used
        assert self.logical_used <= limit
        self.authored_failure = False
        self.terminal: Optional[TerminalOverflow] = None
        self.reads: list[tuple[int, int, Optional[Cell]]] = []

    def _allocate_generation(self, cells: Sequence[Cell]) -> int:
        generation = self._next_generation
        self._next_generation += 1
        self.generations[generation] = list(cells)
        return generation

    def _reference_count(self, generation: int) -> int:
        return sum(bound == generation for bound in self.bindings)

    def apply(self, op: Op) -> None:
        if self.terminal is not None:
            raise AssertionError("the fail-stop model accepts no post-terminal operations")

        if op.kind == "copy":
            # Self-copy, even inactive, is a no-lookup no-op.
            if op.dst == op.src:
                return
            source_generation = self.bindings[op.src]
            if source_generation is None:
                self.authored_failure = True
                return
            # Pin the source generation before replacing the destination binding.
            source_cells = self.generations[source_generation]
            needed = len(source_cells)
            available = self.limit - self.logical_used
            if needed > available:
                self.logical_used += available
                self.terminal = TerminalOverflow(op, available)
                return
            self.logical_used += needed
            self.bindings[op.dst] = source_generation
            return

        if op.kind == "reset":
            fresh_empty_generation = self._allocate_generation(())
            self.bindings[op.dst] = fresh_empty_generation
            return

        if op.kind == "deactivate":
            self.bindings[op.dst] = None
            return

        if op.kind == "replace":
            if self.logical_used == self.limit:
                self.terminal = TerminalOverflow(op, 0)
                return
            fresh_generation = self._allocate_generation((Cell(op.value, op.display),))
            self.bindings[op.dst] = fresh_generation
            self.logical_used += 1
            self.physical_cells += 1
            return

        if op.kind == "get":
            generation = self.bindings[op.dst]
            if generation is None or not 0 <= op.index < len(self.generations[generation]):
                self.authored_failure = True
                self.reads.append((op.dst, op.index, None))
            else:
                self.reads.append((op.dst, op.index, self.generations[generation][op.index]))
            return

        if op.kind == "set":
            generation = self.bindings[op.dst]
            if generation is None or not 0 <= op.index < len(self.generations[generation]):
                self.authored_failure = True
                return
            cells = self.generations[generation]
            if self._reference_count(generation) > 1:
                # The logical copy debit was reserved by the earlier publication.
                detached = list(cells)
                detached[op.index] = Cell(op.value, op.display)
                new_generation = self._allocate_generation(detached)
                self.bindings[op.dst] = new_generation
                self.physical_cells += len(detached)
            else:
                # A unique stable generation may replace its immutable cell slot.
                cells[op.index] = Cell(op.value, op.display)
            return

        if op.kind == "append":
            generation = self.bindings[op.dst]
            if generation is None:
                self.authored_failure = True
                return
            if self.logical_used == self.limit:
                self.terminal = TerminalOverflow(op, 0)
                return
            cells = self.generations[generation]
            new_cell = Cell(op.value, op.display)
            if self._reference_count(generation) > 1:
                # Existing cells use the alias's already-debited logical credit;
                # only the appended cell needs new logical admission.
                detached = list(cells)
                detached.append(new_cell)
                new_generation = self._allocate_generation(detached)
                self.bindings[op.dst] = new_generation
                self.physical_cells += len(detached)
            else:
                cells.append(new_cell)
                self.physical_cells += 1
            self.logical_used += 1
            return

        raise AssertionError(f"unknown COW operation: {op.kind}")

    def assert_accounting_invariants(self) -> None:
        assert self.physical_cells == sum(len(cells) for cells in self.generations.values())
        assert tuple(self.generations) == tuple(range(self._next_generation))
        assert self.physical_cells <= self.logical_used <= self.limit
        counts: dict[int, int] = {}
        for generation in self.bindings:
            if generation is not None:
                assert generation in self.generations
                counts[generation] = counts.get(generation, 0) + 1
        alias_credit = sum(
            (binding_count - 1) * len(self.generations[generation])
            for generation, binding_count in counts.items()
        )
        assert self.physical_cells + alias_credit <= self.logical_used


def _initial_state() -> tuple[tuple[Cell, ...], tuple[Cell, ...]]:
    return ((Cell(10, "ten"),), (Cell(20, "twenty"),))


def _assert_models_agree(
    limit: int, initial: Sequence[Optional[Sequence[Cell]]], trace: Sequence[Op]
) -> None:
    eager = EagerLedgerOracle(limit, initial)
    cow = StableGenerationCowModel(limit, initial)
    for op in trace:
        eager.apply(op)
        cow.apply(op)
        if eager.terminal is not None or cow.terminal is not None:
            assert eager.terminal == cow.terminal, _trace_text(trace)
            # A native fail-stop has no continuation: compare only event status,
            # overflowing operation, and number of copied prefix cells.
            assert eager.terminal is not None and cow.terminal is not None
            return
        assert eager.authored_failure == cow.authored_failure, _trace_text(trace)
        assert eager.bindings == [
            None if generation is None else cow.generations[generation]
            for generation in cow.bindings
        ], _trace_text(trace)
        assert eager.reads == cow.reads, _trace_text(trace)
        assert eager.used == cow.logical_used, _trace_text(trace)
        cow.assert_accounting_invariants()


def _trace_text(trace: Sequence[Op]) -> str:
    return " -> ".join(str(op) for op in trace)


# A compact alphabet spans active/inactive source and destination states,
# replacement, no-op identity copies, reads, both Set outcomes, and append.
_EXHAUSTIVE_ALPHABET = (
    Op("copy", dst=0, src=1),
    Op("copy", dst=1, src=0),
    Op("copy", dst=0, src=0),
    Op("copy", dst=1, src=1),
    Op("reset", dst=0),
    Op("reset", dst=1),
    Op("deactivate", dst=0),
    Op("deactivate", dst=1),
    Op("replace", dst=0, value=30, display="thirty"),
    Op("replace", dst=1, value=40, display="forty"),
    Op("get", dst=0, index=0),
    Op("get", dst=1, index=0),
    Op("get", dst=0, index=99),
    Op("set", dst=0, index=0, value=50, display="fifty"),
    Op("set", dst=0, index=99, value=60, display="sixty"),
    Op("append", dst=0, value=70, display="seventy"),
)
_EXHAUSTIVE_DEPTH = 4
_EXHAUSTIVE_TRACES_PER_LIMIT = len(_EXHAUSTIVE_ALPHABET) ** _EXHAUSTIVE_DEPTH


def test_exhaustive_bounded_traces_compare_independent_models():
    """Enumerate all four-step traces at two small limits (model-only)."""
    total = 0
    for limit in (2, 3):
        initial = _initial_state()
        for trace in product(_EXHAUSTIVE_ALPHABET, repeat=_EXHAUSTIVE_DEPTH):
            _assert_models_agree(limit, initial, trace)
            total += 1
    assert total == 2 * _EXHAUSTIVE_TRACES_PER_LIMIT == 131072


def test_long_copy_chain_and_shared_set_at_full_logical_budget():
    """A shared Set uses its earlier logical copy reservation for detachment."""
    initial = _initial_state()
    trace = (
        Op("copy", dst=0, src=1),
        Op("copy", dst=1, src=0),
        Op("copy", dst=0, src=1),
        Op("set", dst=0, index=0, value=99, display="changed"),
        Op("get", dst=0, index=0),
        Op("get", dst=1, index=0),
    )
    _assert_models_agree(5, initial, trace)

    cow = StableGenerationCowModel(3, initial)
    cow.apply(Op("copy", dst=0, src=1))
    assert cow.logical_used == 3  # At the limit before the shared Set.
    cow.apply(Op("set", dst=0, index=0, value=99, display="changed"))
    cow.assert_accounting_invariants()
    assert cow.terminal is None
    assert cow.logical_used == cow.limit == 3
    assert cow.physical_cells == 3


def test_shared_append_fails_at_full_logical_budget_even_with_physical_headroom():
    """Logical admission, not spare physical slots, governs shared append."""
    initial = _initial_state()
    append = Op("append", dst=0, value=71, display="seventy-one")
    eager = EagerLedgerOracle(3, initial)
    cow = StableGenerationCowModel(3, initial)
    eager.apply(Op("copy", dst=0, src=1))
    cow.apply(Op("copy", dst=0, src=1))
    assert cow.physical_cells < cow.limit == cow.logical_used
    eager.apply(append)
    cow.apply(append)
    assert eager.terminal == cow.terminal == TerminalOverflow(append, 0)


def test_reset_deactivate_and_repeated_same_generation_copies_never_refund():
    """Reset/deactivation do not refund monotonic debit; repeated aliases charge."""
    initial = _initial_state()
    trace = (
        Op("copy", dst=0, src=1),
        Op("reset", dst=0),
        Op("copy", dst=0, src=1),
        Op("deactivate", dst=0),
        Op("copy", dst=0, src=1),
        Op("copy", dst=0, src=1),
    )
    _assert_models_agree(5, initial, trace)
    eager = EagerLedgerOracle(5, initial)
    cow = StableGenerationCowModel(5, initial)
    for op in trace[:-1]:
        eager.apply(op)
        cow.apply(op)
    assert eager.used == cow.logical_used == 5
    eager.apply(trace[-1])
    cow.apply(trace[-1])
    assert eager.terminal == cow.terminal == TerminalOverflow(trace[-1], 0)


def test_invalid_mutator_does_not_detach_and_invalid_source_is_sticky_only():
    """Invalid access is authored failure, not a terminal or COW allocation."""
    initial = _initial_state()
    eager = EagerLedgerOracle(3, initial)
    cow = StableGenerationCowModel(3, initial)
    publication = Op("copy", dst=0, src=1)
    eager.apply(publication)
    cow.apply(publication)
    physical_before = cow.physical_cells
    invalid_set = Op("set", dst=0, index=7, value=1, display="bad")
    eager.apply(invalid_set)
    cow.apply(invalid_set)
    assert cow.physical_cells == physical_before
    assert eager.terminal is cow.terminal is None
    assert eager.authored_failure and cow.authored_failure
    assert eager.bindings == [cow.generations[g] for g in cow.bindings]

    inactive_self = Op("copy", dst=0, src=0)
    eager.apply(Op("deactivate", dst=0))
    cow.apply(Op("deactivate", dst=0))
    eager.apply(inactive_self)
    cow.apply(inactive_self)
    # Self-copy does not inspect an inactive source; existing sticky failure stays.
    assert eager.authored_failure and cow.authored_failure
    assert eager.terminal is cow.terminal is None
    _assert_models_agree(
        3,
        initial,
        (publication, invalid_set, Op("deactivate", dst=0), inactive_self),
    )


def test_invalid_source_marks_sticky_authored_failure_without_stopping():
    """Invalid source lookup marks sticky failure; a following valid operation runs."""
    trace = (
        Op("deactivate", dst=1),
        Op("copy", dst=0, src=1),
        Op("replace", dst=1, value=8, display="eight"),
        Op("get", dst=1, index=0),
    )
    _assert_models_agree(5, _initial_state(), trace)


def test_eager_copy_overflow_reports_partial_appended_prefix_only():
    """Terminal comparison includes the overflowing copy and its copied prefix."""
    initial = ((Cell(1, "one"), Cell(2, "two")), None)
    copy = Op("copy", dst=1, src=0)
    eager = EagerLedgerOracle(3, initial)
    cow = StableGenerationCowModel(3, initial)
    eager.apply(copy)
    cow.apply(copy)
    assert eager.terminal == cow.terminal == TerminalOverflow(copy, 1)


def test_shared_append_detaches_len_plus_one_only_after_logical_admission():
    """A successful shared append copies the complete old generation plus cell."""
    initial = ((Cell(1, "one"), Cell(2, "two")), (Cell(3, "three"),))
    # Initial debit is three. Copying the two-cell source into slot 1 reserves
    # two logical slots; appending one cell then fits exactly at limit six.
    trace = (
        Op("copy", dst=1, src=0),
        Op("append", dst=1, value=4, display="four"),
        Op("get", dst=1, index=2),
        Op("get", dst=0, index=1),
    )
    _assert_models_agree(6, initial, trace)
    cow = StableGenerationCowModel(6, initial)
    cow.apply(trace[0])
    before = cow.physical_cells
    cow.apply(trace[1])
    assert cow.logical_used == 6
    assert cow.physical_cells - before == 3  # Existing len=2 plus appended cell.
    cow.assert_accounting_invariants()


def test_three_aliases_detach_reset_and_rebind_without_reclaiming_generations():
    initial = ((Cell(1, "001.50"), Cell(2, "two")), (), ())
    trace = (
        Op("copy", dst=1, src=0),
        Op("copy", dst=2, src=1),
        Op("set", dst=1, index=0, value=9, display="009.00"),
        Op("reset", dst=0),
        Op("append", dst=2, value=3, display="three"),
        Op("get", dst=1, index=0),
        Op("get", dst=2, index=0),
        Op("copy", dst=0, src=2),
        Op("set", dst=2, index=1, value=8, display="eight"),
        Op("deactivate", dst=1),
        Op("get", dst=0, index=1),
    )
    _assert_models_agree(10, initial, trace)
    cow = StableGenerationCowModel(10, initial)
    for op in trace:
        cow.apply(op)
        cow.assert_accounting_invariants()
    assert cow.reads == [(1, 0, Cell(9, "009.00")),
                         (2, 0, Cell(1, "001.50")),
                         (0, 1, Cell(2, "two"))]
    assert cow.logical_used == 10
    assert cow.physical_cells == 8
    # The deactivated writer's generation remains retained, not reclaimed.
    assert any(cells and cells[0] == Cell(9, "009.00")
               for cells in cow.generations.values())


def test_terminal_models_reject_every_continuation():
    initial = _initial_state()
    overflow = Op("append", dst=0, value=7)
    for model in (EagerLedgerOracle(2, initial), StableGenerationCowModel(2, initial)):
        model.apply(overflow)
        assert model.terminal == TerminalOverflow(overflow, 0)
        for op in _EXHAUSTIVE_ALPHABET:
            with pytest.raises(AssertionError, match="no post-terminal operations"):
                model.apply(op)
