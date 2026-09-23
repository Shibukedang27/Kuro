"""Runtime values owned by Kuro's algebraic-result surface."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import time


@dataclass(frozen=True)
class TaggedValue:
    tag: str
    value: object = None

    def __str__(self) -> str:
        return "None" if self.tag == "None" else f"{self.tag}({self.value})"


@dataclass(frozen=True)
class ClosureValue:
    action: str
    captured: dict[str, object]

    def __str__(self) -> str:
        return f"<closure {self.action}>"


@dataclass
class TaskValue:
    task: object

    def __str__(self) -> str:
        return f"<task {self.task.id}:{self.task.state}>"


@dataclass
class ChannelValue:
    channel: object

    def __str__(self) -> str:
        return "<channel>"


@dataclass
class RecordValue:
    type_name: str
    fields: dict[str, object]

    def __str__(self) -> str:
        values = ", ".join(f"{key}={value}" for key, value in self.fields.items())
        return f"{self.type_name}{{{values}}}"


@dataclass(frozen=True)
class EnumValue:
    type_name: str
    variant: str

    def __str__(self) -> str:
        return f"{self.type_name}.{self.variant}"


def builtin_call(name: str, args: list[object]):
    if name == "MakeChannel" and not args:
        from .concurrency import Channel
        return ChannelValue(Channel())
    if name == "Send" and len(args) == 2 and isinstance(args[0], ChannelValue):
        return args[0].channel.send(args[1])
    if name == "Receive" and len(args) == 1 and isinstance(args[0], ChannelValue):
        try:
            return args[0].channel.receive()
        except RuntimeError as error:
            raise ValueError(str(error)) from error
    if name == "ChannelHas" and len(args) == 1 and isinstance(args[0], ChannelValue):
        return args[0].channel.has_value()
    if name == "ReadFile" and len(args) == 1 and isinstance(args[0], str):
        try:
            return Path(args[0]).read_text(encoding="utf-8")
        except OSError as error:
            raise ValueError(f"cannot read file {args[0]!r}: {error.strerror or error}") from error
    if name == "WriteFile" and len(args) == 2 and all(isinstance(item, str) for item in args):
        try:
            Path(args[0]).write_text(args[1], encoding="utf-8")
            return len(args[1])
        except OSError as error:
            raise ValueError(f"cannot write file {args[0]!r}: {error.strerror or error}") from error
    if name == "FileExists" and len(args) == 1 and isinstance(args[0], str):
        return Path(args[0]).is_file()
    if name == "ListDirectory" and len(args) == 1 and isinstance(args[0], str):
        try:
            return sorted(item.name for item in Path(args[0]).iterdir())
        except OSError as error:
            raise ValueError(f"cannot list directory {args[0]!r}: {error.strerror or error}") from error
    if name == "Now" and not args:
        return time.time()
    if name == "MakeMap" and not args:
        return {}
    if name == "MapSet" and len(args) == 3 and isinstance(args[0], dict):
        args[0][args[1]] = args[2]
        return args[0]
    if name == "MapGet" and len(args) == 2 and isinstance(args[0], dict):
        if args[1] not in args[0]:
            raise ValueError(f"map key {args[1]!r} is not defined")
        return args[0][args[1]]
    if name == "MapHas" and len(args) == 2 and isinstance(args[0], dict):
        return args[1] in args[0]
    if name == "MakeRecord" and len(args) == 1 and isinstance(args[0], str):
        return RecordValue(args[0], {})
    if name == "RecordSet" and len(args) == 3 and isinstance(args[0], RecordValue) and isinstance(args[1], str):
        args[0].fields[args[1]] = args[2]
        return args[0]
    if name == "RecordGet" and len(args) == 2 and isinstance(args[0], RecordValue) and isinstance(args[1], str):
        if args[1] not in args[0].fields:
            raise ValueError(f"record field {args[1]!r} is not defined")
        return args[0].fields[args[1]]
    if name == "MakeEnum" and len(args) == 2 and all(isinstance(item, str) for item in args):
        return EnumValue(args[0], args[1])
    if name == "EnumIs" and len(args) == 2 and isinstance(args[0], EnumValue) and isinstance(args[1], str):
        return args[0].variant == args[1]
    if name in {"Some", "Ok", "Err"} and len(args) == 1:
        return TaggedValue(name, args[0])
    if name == "None" and not args:
        return TaggedValue("None")
    expected = {"IsSome": "Some", "IsNone": "None", "IsOk": "Ok", "IsErr": "Err"}.get(name)
    if expected is not None and len(args) == 1:
        return isinstance(args[0], TaggedValue) and args[0].tag == expected
    if name in {"Unwrap", "UnwrapErr"} and len(args) == 1 and isinstance(args[0], TaggedValue):
        expected = "Err" if name == "UnwrapErr" else "Ok" if args[0].tag == "Ok" else "Some"
        if args[0].tag == expected:
            return args[0].value
    raise ValueError(f"invalid builtin {name} arguments")
