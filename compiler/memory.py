"""Kuro-owned heap accounting and tracing collector boundary."""
from __future__ import annotations

from dataclasses import dataclass

from .values import ChannelValue, ClosureValue, RecordValue, TaggedValue, TaskValue


@dataclass
class HeapObject:
    value: object
    marked: bool = False


class MemoryManager:
    """Deterministic mark/sweep bookkeeping for runtime-managed Kuro values."""

    def __init__(self) -> None:
        self._heap: dict[int, HeapObject] = {}
        self.collections = 0
        self.freed = 0

    def track(self, value: object) -> object:
        if isinstance(value, (list, dict, tuple, set, RecordValue, ClosureValue, TaggedValue, TaskValue, ChannelValue)) or (hasattr(value, "closure") and hasattr(value, "args")) or (hasattr(value, "values") and not callable(value.values)):
            if id(value) in self._heap:
                return value
            self._heap[id(value)] = HeapObject(value)
            # Register descendants immediately. This keeps the collector's
            # graph complete even when a value was created in a temporary or
            # inside a closure before it became a named environment root.
            for child in self._children(value):
                self.track(child)
        return value

    @property
    def allocated(self) -> int:
        return len(self._heap)

    def _children(self, value: object):
        if isinstance(value, RecordValue):
            yield from value.fields.values()
        elif isinstance(value, ClosureValue):
            yield value.captured
        elif isinstance(value, TaggedValue):
            if value.value is not None:
                yield value.value
        elif isinstance(value, TaskValue):
            yield value.task
        elif isinstance(value, ChannelValue):
            yield value.channel
        elif hasattr(value, "values") and not callable(value.values):
            yield from value.values
        elif hasattr(value, "closure") and hasattr(value, "args"):
            yield value.closure
            yield from value.args
            if getattr(value, "result", None) is not None:
                yield value.result
        elif isinstance(value, dict):
            yield from value.keys()
            yield from value.values()
        elif isinstance(value, (list, tuple, set)):
            yield from value

    def _mark(self, value: object) -> None:
        record = self._heap.get(id(value))
        if record is None or record.marked:
            return
        record.marked = True
        for child in self._children(record.value):
            self._mark(child)

    def collect(self, roots) -> int:
        for record in self._heap.values():
            record.marked = False
        for root in roots:
            self._mark(root)
        dead = [key for key, record in self._heap.items() if not record.marked]
        for key in dead:
            del self._heap[key]
        self.collections += 1
        self.freed += len(dead)
        return len(dead)

    def stats(self) -> dict[str, int]:
        return {"allocated": self.allocated, "collections": self.collections, "freed": self.freed}
