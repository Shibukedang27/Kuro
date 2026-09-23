"""Deterministic cooperative task scheduler for Kuro runtimes."""
from __future__ import annotations

from dataclasses import dataclass
from collections import deque


@dataclass
class Task:
    id: int
    closure: object
    args: list[object]
    state: str = "queued"
    result: object = None
    error: BaseException | None = None


@dataclass
class Channel:
    """FIFO communication endpoint for cooperative Kuro tasks."""
    values: deque = None

    def __post_init__(self):
        if self.values is None:
            self.values = deque()

    def send(self, value):
        self.values.append(value)
        return value

    def receive(self):
        if not self.values:
            raise RuntimeError("receive would block: Kuro channel is empty")
        return self.values.popleft()

    def has_value(self) -> bool:
        return bool(self.values)


class Scheduler:
    """FIFO scheduler; tasks run only at an explicit Await safe point."""

    def __init__(self) -> None:
        self._next_id = 1
        self.tasks: dict[int, Task] = {}

    def spawn(self, closure: object, args: list[object] | None = None) -> Task:
        task = Task(self._next_id, closure, list(args or []))
        self._next_id += 1
        self.tasks[task.id] = task
        return task

    def await_task(self, task: Task, runner):
        if task.state == "done":
            return task.result
        if task.state == "failed":
            assert task.error is not None
            raise task.error
        if task.state != "queued":
            raise RuntimeError("invalid Kuro task state")
        task.state = "running"
        try:
            task.result = runner(task.closure, task.args)
            task.state = "done"
            return task.result
        except BaseException as error:
            task.error = error
            task.state = "failed"
            raise
