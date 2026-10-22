"""Executable DESIGN model for publication-time VM collection copying.

This is deliberately an abstract comparison, not a production implementation and
not proof that the complete VM is safe. Cells and their value/display strings are
immutable; this model has no text reclamation, row collector, capacity limits, or
claims about production allocation reduction. Synthetic cell counts are model-only.
Failures here are transactional; partial production failures and the production VM
flag model are outside this model and its proof boundary.
"""

from dataclasses import dataclass
from itertools import product


NAMES = ("a", "b", "c")


@dataclass(frozen=True)
class Cell:
    value: str
    display: str


@dataclass(frozen=True)
class NameMarker:
    """A stack marker names a variable; it does not retain a row/generation."""

    name: str


class ModelFailure(Exception):
    def __init__(self, kind):
        self.kind = kind


class Engine:
    """Shared abstract API; subclasses differ only in storage representation."""

    def __init__(self):
        self.markers = []
        self.history = []
        self.allocated_cells = 0

    def _read_cells(self, name):
        raise NotImplementedError

    def _write_cells(self, name, cells):
        raise NotImplementedError

    def _snapshot(self):
        return (self.logical_state(), tuple(self.markers), self.allocated_cells,
                self._storage_snapshot())

    def _storage_snapshot(self):
        return None

    def _assert_invariants(self):
        pass

    def logical_state(self):
        raise NotImplementedError

    def _name_view(self, name):
        """Resolve a name now, rather than when its marker was pushed."""
        binding = self.bindings.get(name)
        if binding is None:
            return ("failure", "inactive-name")
        if binding[0] != "collection":
            return ("failure", "not-collection")
        return self.logical_state()[name]

    def step(self, op):
        """Execute a named abstract operation, recording values/displays by value."""
        before = self._snapshot()
        try:
            tag = op[0]
            if tag == "append":
                _, name, value, display = op
                old = self._read_cells(name)
                self._write_cells(name, tuple(old) + (Cell(value, display),))
                result = ("ok",)
            elif tag == "set":
                _, name, index, value, display = op
                old = self._read_cells(name)
                if index < 0:
                    # Abstract logical-end bounds behavior, never Python from-end indexing.
                    raise ModelFailure("bounds-logical-end")
                if index >= len(old):
                    raise ModelFailure("bounds-past-end")
                new = list(old)
                new[index] = Cell(value, display)
                self._write_cells(name, tuple(new))
                result = ("ok",)
            elif tag == "get":
                _, name, index = op
                cells = self._read_cells(name)
                if index < 0:
                    index += len(cells)
                    if index < 0:
                        raise ModelFailure("bounds-logical-end")
                if index >= len(cells):
                    raise ModelFailure("bounds-past-end")
                cell = cells[index]
                # Return and retain an immutable value/display pair.
                result = ("value", cell.value, cell.display)
            elif tag == "display":
                _, name = op
                result = ("displays", tuple(cell.display for cell in self._read_cells(name)))
            elif tag == "empty":
                _, name = op
                result = ("empty", len(self._read_cells(name)) == 0)
            elif tag == "copy":
                _, target, source = op
                self.copy_name(target, source)
                result = ("ok",)
            elif tag == "reset":
                _, name = op
                self.reset_name(name)
                result = ("ok",)
            elif tag == "deactivate":
                _, name = op
                self.deactivate_name(name)
                result = ("ok",)
            elif tag == "scalar":
                _, name, value, display = op
                self.overwrite_scalar(name, Cell(value, display))
                result = ("ok",)
            elif tag == "push-marker":
                _, name = op
                self.markers.append(NameMarker(name))
                result = ("ok",)
            elif tag == "resolve-markers":
                result = ("markers", tuple(self._name_view(m.name) for m in self.markers))
            else:
                raise AssertionError(f"unknown operation {op!r}")
        except ModelFailure as failure:
            result = ("failure", failure.kind)
            # The model specifies atomic failures. This says nothing about production.
            assert self._snapshot() == before
        self._assert_invariants()
        self.history.append(result)
        return result

    def copy_name(self, target, source):
        raise NotImplementedError

    def reset_name(self, name):
        raise NotImplementedError

    def deactivate_name(self, name):
        raise NotImplementedError

    def overwrite_scalar(self, name, cell):
        raise NotImplementedError


class EagerCopy(Engine):
    """Oracle: copies cells on collection copy; mutation allocates only appends."""

    def __init__(self):
        super().__init__()
        self.bindings = {name: ("collection", tuple()) for name in NAMES}

    def _read_cells(self, name):
        binding = self.bindings.get(name)
        if binding is None:
            raise ModelFailure("inactive-name")
        if binding[0] != "collection":
            raise ModelFailure("not-collection")
        return binding[1]

    def _write_cells(self, name, cells):
        if len(cells) > len(self._read_cells(name)):
            self.allocated_cells += 1
        self.bindings[name] = ("collection", tuple(cells))

    def copy_name(self, target, source):
        if target == source:
            return
        source_binding = self.bindings.get(source)
        if source_binding is None:
            raise ModelFailure("inactive-name")
        if source_binding[0] == "collection":
            cells = tuple(Cell(cell.value, cell.display) for cell in source_binding[1])
            self.allocated_cells += len(cells)
            self.bindings[target] = ("collection", cells)
        else:
            self.bindings[target] = ("scalar", Cell(source_binding[1].value, source_binding[1].display))

    def reset_name(self, name):
        self.bindings[name] = ("collection", tuple())

    def deactivate_name(self, name):
        self.bindings.pop(name, None)

    def overwrite_scalar(self, name, cell):
        self.bindings[name] = ("scalar", Cell(cell.value, cell.display))

    def logical_state(self):
        result = {}
        for name, binding in self.bindings.items():
            if binding[0] == "collection":
                result[name] = ("collection", tuple((c.value, c.display) for c in binding[1]))
            else:
                result[name] = ("scalar", binding[1].value, binding[1].display)
        return result


class GenerationCow(Engine):
    """Stable IDs over mutable per-generation lists, detached only when shared."""

    def __init__(self):
        super().__init__()
        self.generations = {}
        self.next_generation = 0
        self.bindings = {}
        for name in NAMES:
            self.bindings[name] = ("collection", self._new_generation(tuple()))

    def _new_generation(self, cells):
        generation = self.next_generation
        self.next_generation += 1
        self.generations[generation] = list(cells)
        return generation

    def _read_cells(self, name):
        binding = self.bindings.get(name)
        if binding is None:
            raise ModelFailure("inactive-name")
        if binding[0] != "collection":
            raise ModelFailure("not-collection")
        return self.generations[binding[1]]

    def _write_cells(self, name, cells):
        binding = self.bindings.get(name)
        if binding is None:
            raise ModelFailure("inactive-name")
        if binding[0] != "collection":
            raise ModelFailure("not-collection")
        generation = binding[1]
        current = self.generations[generation]
        sharing = sum(1 for kind, gen in self.bindings.values()
                      if kind == "collection" and gen == generation)
        if sharing >= 2:
            # Retain old generations forever; the mutating name receives a new ID.
            self.allocated_cells += len(current)
            generation = self._new_generation(current)
            self.bindings[name] = ("collection", generation)
            current = self.generations[generation]
        if len(cells) > len(current):
            self.allocated_cells += 1
        current[:] = cells

    def copy_name(self, target, source):
        if target == source:
            return
        source_binding = self.bindings.get(source)
        if source_binding is None:
            raise ModelFailure("inactive-name")
        if source_binding[0] == "collection":
            # Copy only the binding; the next write detaches iff still shared.
            self.bindings[target] = ("collection", source_binding[1])
        else:
            self.bindings[target] = ("scalar", Cell(source_binding[1].value, source_binding[1].display))

    def reset_name(self, name):
        self.bindings[name] = ("collection", self._new_generation(tuple()))

    def deactivate_name(self, name):
        self.bindings.pop(name, None)

    def overwrite_scalar(self, name, cell):
        self.bindings[name] = ("scalar", Cell(cell.value, cell.display))

    def logical_state(self):
        result = {}
        for name, binding in self.bindings.items():
            if binding[0] == "collection":
                cells = self.generations[binding[1]]
                result[name] = ("collection", tuple((c.value, c.display) for c in cells))
            else:
                result[name] = ("scalar", binding[1].value, binding[1].display)
        return result

    def _storage_snapshot(self):
        return (self.next_generation,
                tuple((generation, tuple((cell.value, cell.display) for cell in cells))
                      for generation, cells in sorted(self.generations.items())))

    def _assert_invariants(self):
        assert self.next_generation >= 0
        assert tuple(sorted(self.generations)) == tuple(range(self.next_generation))
        for binding in self.bindings.values():
            if binding[0] == "collection":
                assert binding[1] in self.generations
        for cells in self.generations.values():
            assert isinstance(cells, list)
            assert all(isinstance(cell, Cell) and isinstance(cell.value, str)
                       and isinstance(cell.display, str) for cell in cells)


def compare_trace(ops):
    eager, cow = EagerCopy(), GenerationCow()
    previous_eager_cells = previous_cow_cells = 0
    for op in ops:
        eager_result = eager.step(op)
        cow_result = cow.step(op)
        assert eager_result == cow_result, (ops, op, eager_result, cow_result)
        assert eager.logical_state() == cow.logical_state(), (ops, op)
        assert eager.history == cow.history
        assert eager.markers == cow.markers
        assert eager.allocated_cells >= previous_eager_cells
        assert cow.allocated_cells >= previous_cow_cells
        previous_eager_cells, previous_cow_cells = eager.allocated_cells, cow.allocated_cells
    return eager, cow


def operation_alphabet():
    ops = []
    for name in NAMES:
        ops.extend((
            ("append", name, "v", "<v>"),
            ("set", name, 0, "s", "<s>"),
            ("get", name, 0),
            ("display", name),
            ("empty", name),
            ("reset", name),
            ("deactivate", name),
            ("scalar", name, "q", "<q>"),
            ("push-marker", name),
        ))
    for target in NAMES:
        for source in NAMES:
            ops.append(("copy", target, source))
    ops.append(("resolve-markers",))
    return tuple(ops)


def test_exhaustive_bounded_named_operation_traces_match_after_every_operation():
    """Exhaust all 3-op traces over three names (no sampling or random seed)."""
    alphabet = operation_alphabet()
    for length in range(4):
        for ops in product(alphabet, repeat=length):
            compare_trace(ops)


def test_assignment_chain_mutation_reset_deactivate_and_late_name_marker():
    ops = (
        ("append", "c", "old", "OLD"),
        ("copy", "b", "c"),
        ("copy", "a", "b"),
        ("push-marker", "a"),
        ("get", "a", 0),
        ("display", "a"),
        ("set", "c", 0, "new", "NEW"),
        ("append", "a", "tail", "TAIL"),
        ("resolve-markers",),
        ("reset", "b"),
        ("deactivate", "c"),
        ("resolve-markers",),
        ("copy", "a", "a"),
    )
    eager, cow = compare_trace(ops)
    # The saved result/display from before mutations stay value snapshots.
    assert eager.history[4] == ("value", "old", "OLD")
    assert eager.history[5] == ("displays", ("OLD",))
    assert eager.history[8] == ("markers", (("collection", (("old", "OLD"), ("tail", "TAIL"))),))
    assert eager.history[11] == ("markers", (("collection", (("old", "OLD"), ("tail", "TAIL"))),))
    assert eager.logical_state() == cow.logical_state()


def test_get_negative_indices_normalize_but_set_negative_and_oob_fail_transactionally():
    eager, cow = compare_trace((
        ("append", "a", "one", "ONE"),
        ("append", "a", "two", "TWO"),
        ("get", "a", -1),
        ("set", "a", -1, "bad", "BAD"),
        ("get", "a", -2),
        ("get", "a", -3),
        ("get", "a", 2),
        ("set", "a", 2, "bad", "BAD"),
        ("get", "a", 0),
    ))
    assert eager.history[2] == ("value", "two", "TWO")
    assert eager.history[3] == ("failure", "bounds-logical-end")
    assert eager.history[4] == ("value", "one", "ONE")
    assert eager.history[5] == ("failure", "bounds-logical-end")
    assert eager.history[6] == ("failure", "bounds-past-end")
    assert eager.history[7] == ("failure", "bounds-past-end")
    assert eager.history[8] == ("value", "one", "ONE")
    assert eager.logical_state() == cow.logical_state()


def test_collection_marker_reports_failure_for_scalar_or_inactive_name():
    eager, cow = compare_trace((
        ("push-marker", "a"),
        ("scalar", "a", "value", "<value>"),
        ("resolve-markers",),
        ("deactivate", "a"),
        ("resolve-markers",),
    ))
    assert eager.history[2] == ("markers", (("failure", "not-collection"),))
    assert eager.history[4] == ("markers", (("failure", "inactive-name"),))
    assert eager.logical_state() == cow.logical_state()


def test_naive_mutable_aliasing_has_a_counterexample():
    """A deliberately wrong aliasing model diverges on the shortest useful case."""
    naive = {"a": [Cell("before", "BEFORE")], "b": []}
    naive["b"] = naive["a"]  # Wrong: assignment shares mutable list without COW.
    naive["b"].append(Cell("after", "AFTER"))
    assert tuple((c.value, c.display) for c in naive["a"]) == (
        ("before", "BEFORE"), ("after", "AFTER"))
    expected, _ = compare_trace((
        ("append", "a", "before", "BEFORE"),
        ("copy", "b", "a"),
        ("append", "b", "after", "AFTER"),
    ))
    assert expected.logical_state()["a"] == ("collection", (("before", "BEFORE"),))
    assert naive["a"] != [Cell("before", "BEFORE")]


def test_naive_eager_stack_handle_has_a_counterexample_to_late_name_resolution():
    """A saved row handle is not equivalent to a marker that stores only a name."""
    generation_rows = {7: (Cell("old", "OLD"),)}
    name_binding = {"a": 7}
    naive_saved_handle = name_binding["a"]
    marker = NameMarker("a")
    # Reset gives the name a fresh empty generation; old handle wrongly sees old data.
    generation_rows[8] = tuple()
    name_binding["a"] = 8
    wrong = tuple((c.value, c.display) for c in generation_rows[naive_saved_handle])
    late = ("collection", tuple((c.value, c.display) for c in generation_rows[name_binding[marker.name]]))
    assert wrong == (("old", "OLD"),)
    assert late == ("collection", tuple())
    eager, cow = compare_trace((
        ("append", "a", "old", "OLD"),
        ("push-marker", "a"),
        ("reset", "a"),
        ("resolve-markers",),
    ))
    assert eager.history[-1] == ("markers", (("collection", ()),))
    assert cow.history[-1] == eager.history[-1]


def test_synthetic_publication_cell_counts_are_exact_and_model_only():
    """Exact synthetic cell counts; these are not production savings claims."""
    eager, cow = EagerCopy(), GenerationCow()
    for index in range(80):
        eager.step(("append", "a", f"v{index}", f"<{index}>"))
        cow.step(("append", "a", f"v{index}", f"<{index}>"))
    for name in ("b", "c"):
        eager.step(("copy", name, "a"))
        cow.step(("copy", name, "a"))
    # Repeated publication-style snapshots, including assignment chains.
    for _ in range(12):
        eager.step(("copy", "b", "a"))
        cow.step(("copy", "b", "a"))
        eager.step(("copy", "c", "b"))
        cow.step(("copy", "c", "b"))
    assert eager.logical_state() == cow.logical_state()
    # Eager: 80 append cells + 2 initial 80-cell copies + 24 more 80-cell copies.
    # COW: 80 append cells; publication copies only share bindings.
    assert eager.allocated_cells == 80 + 2 * 80 + 24 * 80 == 2160
    assert cow.allocated_cells == 80
    assert len(cow.generations) == 3  # Separate generation-metadata count.


def test_exact_cell_allocations_for_reset_append_set_and_shared_detach():
    eager, cow = EagerCopy(), GenerationCow()
    assert eager.allocated_cells == cow.allocated_cells == 0
    for engine in (eager, cow):
        engine.step(("reset", "a"))
        assert engine.allocated_cells == 0
        engine.step(("append", "a", "one", "ONE"))
        assert engine.allocated_cells == 1
        engine.step(("copy", "b", "a"))
        assert engine.allocated_cells == (2 if engine is eager else 1)
        engine.step(("set", "a", 0, "ONE!", "ONE!"))
        assert engine.allocated_cells == 2
    # Eager allocated a one-cell copy for b; COW allocated a one-cell detach
    # when a was set while shared.
    cow.step(("copy", "c", "a"))
    cow.step(("append", "a", "two", "TWO"))
    assert cow.allocated_cells == 4  # detach one cell + append one cell
    assert cow.logical_state()["c"] == ("collection", (("ONE!", "ONE!"),))
    eager.step(("copy", "c", "a"))
    eager.step(("append", "a", "two", "TWO"))
    assert eager.allocated_cells == 4  # copy one cell + append one cell


def test_long_adversarial_alias_detach_reset_and_rebind_chain():
    ops = [("append", "a", "seed", "<seed>"),
           ("append", "a", "second", "<second>"),
           ("copy", "b", "a"), ("copy", "c", "b")]
    for index in range(60):
        ops.extend((
            ("copy", "a", "b"),
            ("append", "a", f"tail-{index}", f"<tail-{index}>"),
            ("set", "b", 0, f"b-{index}", f"<b-{index}>"),
            ("copy", "c", "a"),
            ("reset", "a"),
            ("append", "c", f"c-{index}", f"<c-{index}>"),
            ("deactivate", "b"),
            ("copy", "b", "c"),
            ("get", "b", -1),
        ))
    eager, cow = compare_trace(tuple(ops))
    assert eager.logical_state() == cow.logical_state()
    assert tuple(sorted(cow.generations)) == tuple(range(cow.next_generation))
    assert len(cow.generations) > 3
    assert all(isinstance(cell, Cell) and cell.display.startswith("<")
               for row in cow.generations.values() for cell in row)
