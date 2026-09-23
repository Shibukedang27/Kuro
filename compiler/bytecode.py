"""Kuro bytecode container and execution boundary.

The instruction payload is deliberately JSON-safe and contains no Python
objects or source spans. This is the stable boundary used by executable
artifacts while the Kuro-authored VM is being brought to feature parity.
"""
from __future__ import annotations

from dataclasses import dataclass

import sys

from .interpreter import KuroRuntimeException
from .ir import IRFunction, IRProgram, Instr
from .memory import MemoryManager
from .values import ClosureValue, TaskValue, builtin_call
from .concurrency import Scheduler


@dataclass(frozen=True)
class BytecodeInstruction:
    op: str
    args: tuple = ()
    dest: str | None = None

    def to_data(self) -> dict:
        return {"op": self.op, "args": list(self.args), "dest": self.dest}

    @classmethod
    def from_data(cls, data: object) -> "BytecodeInstruction":
        if not isinstance(data, dict) or not isinstance(data.get("op"), str):
            raise ValueError("invalid Kuro bytecode instruction")
        args = data.get("args", [])
        if not isinstance(args, list):
            raise ValueError("bytecode instruction arguments must be a list")
        dest = data.get("dest")
        if dest is not None and not isinstance(dest, str):
            raise ValueError("bytecode instruction destination must be text or null")
        return cls(data["op"], tuple(args), dest)


@dataclass(frozen=True)
class BytecodeProgram:
    main: tuple[BytecodeInstruction, ...]
    functions: dict[str, tuple[BytecodeInstruction, ...]]

    def to_data(self) -> dict:
        return {
            "main": [item.to_data() for item in self.main],
            "functions": {
                name: {"params": list(params), "body": [item.to_data() for item in body]}
                for name, (params, body) in self.functions.items()
            },
        }

    @classmethod
    def from_data(cls, data: object) -> "BytecodeProgram":
        if not isinstance(data, dict) or not isinstance(data.get("main"), list):
            raise ValueError("invalid Kuro bytecode program")
        main = tuple(BytecodeInstruction.from_data(item) for item in data["main"])
        raw_functions = data.get("functions", {})
        if not isinstance(raw_functions, dict):
            raise ValueError("invalid Kuro bytecode functions")
        functions = {}
        for name, value in raw_functions.items():
            if not isinstance(name, str) or not isinstance(value, dict):
                raise ValueError("invalid Kuro bytecode function")
            params = value.get("params", [])
            body = value.get("body", [])
            if not isinstance(params, list) or not all(isinstance(item, str) for item in params):
                raise ValueError("invalid Kuro bytecode parameters")
            if not isinstance(body, list):
                raise ValueError("invalid Kuro bytecode function body")
            functions[name] = (tuple(params), tuple(BytecodeInstruction.from_data(item) for item in body))
        return cls(main, functions)


def encode_ir(program: IRProgram) -> BytecodeProgram:
    def encode(items):
        return tuple(BytecodeInstruction(item.op, item.args, item.dest) for item in items)

    return BytecodeProgram(
        encode(program.main),
        {name: (tuple(fn.params), encode(fn.body)) for name, fn in program.functions.items()},
    )


def decode_to_ir(program: BytecodeProgram) -> IRProgram:
    def decode(items):
        return [Instr(item.op, item.args, item.dest) for item in items]

    return IRProgram(
        decode(program.main),
        {name: IRFunction(name, list(params), decode(body)) for name, (params, body) in program.functions.items()},
    )


class BytecodeVM:
    """Execute a validated Kuro bytecode program."""

    def __init__(self, program: BytecodeProgram, input_fn=input, output=None, max_while_iterations: int = 10_000_000):
        self.program = program
        self.env: dict[str, object] = {}
        self.frames: list[dict[str, object]] = []
        self._input_fn = input_fn
        self._out = output if output is not None else sys.stdout
        self._max_while_iterations = max_while_iterations
        self.memory = MemoryManager()
        self.scheduler = Scheduler()

    def _read(self, name):
        if self.frames and name in self.frames[-1]:
            return self.frames[-1][name]
        if name in self.env:
            return self.env[name]
        if name == "_":
            return None
        raise KuroRuntimeException("E4001", f"undefined value {name!r}")

    def _write(self, name, value):
        self.memory.track(value)
        self.env[name] = value

    def run(self):
        self._execute(self.program.main)
        # Queued and completed tasks are runtime-owned roots until the
        # scheduler itself is discarded; closures may retain captured heaps.
        self.memory.collect([self.env, self.frames, self.scheduler.tasks])

    def _call(self, name, args):
        if name == "Spawn" and len(args) >= 1 and isinstance(args[0], ClosureValue):
            return TaskValue(self.scheduler.spawn(args[0], args[1:]))
        if name == "Await" and len(args) == 1 and isinstance(args[0], TaskValue):
            try:
                return self.scheduler.await_task(args[0].task, lambda closure, values: self._call("Invoke", [closure, *values]))
            except KuroRuntimeException:
                raise
            except BaseException as error:
                raise KuroRuntimeException("E6007", f"task failed: {error}") from error
        if name == "MakeClosure" and len(args) == 1 and isinstance(args[0], str):
            if name not in self.program.functions and args[0] not in self.program.functions:
                raise KuroRuntimeException("E4003", f"unknown action {args[0]!r}")
            captured = dict(self.env)
            for frame in self.frames:
                captured.update(frame)
            return ClosureValue(args[0], captured)
        if name == "Invoke" and args and isinstance(args[0], ClosureValue):
            closure, call_args = args[0], args[1:]
            function = self.program.functions.get(closure.action)
            if function is None or len(call_args) != len(function[0]):
                raise KuroRuntimeException("E4004", "closure invocation has the wrong arity")
            self.frames.append({**closure.captured, **dict(zip(function[0], call_args))})
            try:
                self._execute(function[1])
            except _Return as returned:
                return returned.value
            finally:
                self.frames.pop()
            return None
        if name in {"Some", "None", "Ok", "Err", "IsSome", "IsNone", "IsOk", "IsErr", "Unwrap", "UnwrapErr", "MakeRecord", "RecordSet", "RecordGet", "MakeEnum", "EnumIs", "MakeMap", "MapSet", "MapGet", "MapHas", "ReadFile", "WriteFile", "FileExists", "ListDirectory", "Now", "MakeChannel", "Send", "Receive", "ChannelHas"}:
            try:
                return builtin_call(name, args)
            except ValueError as error:
                raise KuroRuntimeException("E3001", str(error)) from error
        function = self.program.functions.get(name)
        if function is None:
            raise KuroRuntimeException("E4003", f"unknown action {name!r}")
        if len(self.frames) >= 200:
            raise KuroRuntimeException("E6005", "maximum recursion depth exceeded")
        params, body = function
        self.frames.append(dict(zip(params, args)))
        try:
            self._execute(body)
        except _Return as returned:
            return returned.value
        finally:
            self.frames.pop()
        return None

    def _execute(self, instructions):
        labels = {item.dest: index for index, item in enumerate(instructions) if item.op == "LABEL"}
        temps: dict[str, object] = {}
        loop_counts: dict[object, int] = {}
        pc = 0
        while pc < len(instructions):
            item = instructions[pc]
            op = item.op
            if op == "LABEL" or op == "DECLTYPE":
                pc += 1
                continue
            if op == "CONST":
                temps[item.dest] = item.args[0]
            elif op == "LOADVAR":
                temps[item.dest] = self._read(item.args[0])
            elif op == "STORE_LIST":
                name, values = item.args
                resolved = [temps[value] for value in values]
                self._write(name, resolved[0] if len(resolved) == 1 else resolved)
            elif op == "CHECK_NONNEG":
                if temps[item.args[0]] < 0:
                    raise KuroRuntimeException("E6004", "Repeat count cannot be negative")
            elif op == "LOOP_GUARD":
                guard = item.args[0]
                loop_counts[guard] = loop_counts.get(guard, 0) + 1
                if loop_counts[guard] > self._max_while_iterations:
                    raise KuroRuntimeException("E6006", "While loop exceeded maximum iteration count")
            elif op == "INPUT":
                name, typ = item.args
                raw = self._input_fn(f"{name} ({typ}): ")
                try:
                    value = int(raw) if typ == "Integers" else float(raw) if typ == "Decimals" else raw
                except ValueError as error:
                    raise KuroRuntimeException("E6002", f"invalid {typ} input for {name!r}") from error
                self._write(name, value)
            elif op == "ADD":
                name, temp = item.args
                current = self._read(name) if name in self.env or (self.frames and name in self.frames[-1]) else 0
                self._write(name, current + temps[temp])
            elif op == "UPDATE":
                self._write(item.args[0], temps[item.args[1]])
            elif op == "APPEND":
                name, temp = item.args
                current = self._read(name) if (name in self.env or (self.frames and name in self.frames[-1])) else None
                if current is None:
                    self._write(name, [temps[temp]])
                elif isinstance(current, list):
                    current.append(temps[temp])
                else:
                    self._write(name, [current, temps[temp]])
            elif op == "PRINT":
                value = temps[item.args[0]]
                for output in value if isinstance(value, list) else [value]:
                    print(output, file=self._out)
            elif op == "GET":
                name, index_temp = item.args
                value = self._read(name)
                if index_temp is None:
                    temps[item.dest] = value
                else:
                    index = int(temps[index_temp])
                    try:
                        temps[item.dest] = value[index]
                    except (IndexError, TypeError) as error:
                        raise KuroRuntimeException("E6001", f"index {index} out of range for {name!r}") from error
            elif op == "LENGTH":
                name = item.args[0]
                try:
                    temps[item.dest] = len(self._read(name))
                except TypeError as error:
                    raise KuroRuntimeException("E3005", f"{name!r} has no length") from error
            elif op == "SET":
                name, index_temp, value_temp = item.args
                target = self._read(name)
                index = int(temps[index_temp])
                value = temps[value_temp]
                if isinstance(target, str):
                    if not isinstance(value, str) or len(value) != 1:
                        raise KuroRuntimeException("E3004", "Set on Text requires one character")
                    if not 0 <= index < len(target):
                        raise KuroRuntimeException("E6001", "Text index out of range")
                    self.env[name] = target[:index] + value + target[index + 1:]
                elif isinstance(target, list) and 0 <= index < len(target):
                    target[index] = value
                else:
                    raise KuroRuntimeException("E6001", "collection index out of range")
            elif op == "BINOP":
                operator, left, right = item.args
                a, b = temps[left], temps[right]
                if operator == "+" and isinstance(a, str) and isinstance(b, str):
                    temps[item.dest] = a + b
                else:
                    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
                        raise KuroRuntimeException("E3001", f"cannot apply {operator!r} to non-numeric values")
                    if operator == "+": temps[item.dest] = a + b
                    elif operator == "-": temps[item.dest] = a - b
                    elif operator == "*": temps[item.dest] = a * b
                    elif operator == "/":
                        if b == 0: raise KuroRuntimeException("E6003", "division by zero")
                        temps[item.dest] = a // b if isinstance(a, int) and isinstance(b, int) and a % b == 0 else a / b
                    else: raise KuroRuntimeException("E3001", f"unknown operator {operator!r}")
            elif op == "CMP":
                operator, left, right = item.args
                a, b = temps[left], temps[right]
                temps[item.dest] = {"gt": a > b, "lt": a < b, "eq": a == b, "ne": a != b, "ge": a >= b, "le": a <= b}[operator]
            elif op == "AND" or op == "OR":
                left, right = item.args
                temps[item.dest] = (bool(temps[left]) and bool(temps[right])) if op == "AND" else (bool(temps[left]) or bool(temps[right]))
            elif op == "ISCLASS":
                value, cls = temps[item.args[0]], item.args[1]
                temps[item.dest] = isinstance(value, str) and len(value) == 1 and {"digit": value.isdigit(), "alpha": value.isalpha(), "space": value.isspace(), "alnum": value.isalnum(), "quote": value == '"'}[cls]
            elif op == "CALL":
                name, *arguments = item.args
                temps[item.dest] = self._call(name, [temps[arg] for arg in arguments])
            elif op == "RETURN":
                raise _Return(temps[item.args[0]])
            elif op == "JUMP":
                pc = labels[item.args[0]]
                continue
            elif op == "JUMPF":
                label, condition = item.args
                if not temps[condition]:
                    pc = labels[label]
                    continue
            else:
                raise KuroRuntimeException("E8004", f"unsupported bytecode operation {op!r}")
            pc += 1


class _Return(Exception):
    def __init__(self, value):
        self.value = value
