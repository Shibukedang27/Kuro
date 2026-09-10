"""Kuro IR (spec section 22).

A flat three-address-code IR: each instruction has at most one destination
temporary, control flow is explicit (LABEL/JUMP/JUMPF), and every Action
becomes its own IRFunction with its own instruction list. This is
deliberately *not* SSA — spec section 22 says additional IR layers (HIR/MIR,
true SSA with phi nodes) should only be introduced when they solve a real
compiler problem, and nothing in this codebase yet needs them (no
optimization pass here does anything phi nodes would help with). Temporaries
are named `t0, t1, ...` per function/module and are not reassigned once
written, which is enough for the constant-folding/DCE passes in
optimize.py to be straightforward without full SSA machinery.

Every instruction keeps the source Span it was lowered from, so a runtime
error can still point at real source (spec section 11: no meaningless
crashes).
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .diagnostics import Span


@dataclass
class Instr:
    op: str
    args: tuple = ()
    dest: str | None = None
    span: Span | None = None

    def __str__(self) -> str:
        lhs = f"{self.dest} = " if self.dest else ""
        args = " ".join(_fmt(a) for a in self.args)
        return f"{lhs}{self.op} {args}".rstrip()


def _fmt(a) -> str:
    if isinstance(a, str):
        return a
    return repr(a)


@dataclass
class IRFunction:
    name: str
    params: list[str]
    body: list[Instr] = field(default_factory=list)

    def __str__(self) -> str:
        lines = [f"func {self.name}({', '.join(self.params)}):"]
        lines += [f"  {i:04d}  {instr}" for i, instr in enumerate(self.body)]
        return "\n".join(lines)


@dataclass
class IRProgram:
    main: list[Instr] = field(default_factory=list)
    functions: dict[str, IRFunction] = field(default_factory=dict)

    def __str__(self) -> str:
        parts = []
        for fn in self.functions.values():
            parts.append(str(fn))
        main_lines = [f"{i:04d}  {instr}" for i, instr in enumerate(self.main)]
        parts.append("main:\n" + "\n".join(f"  {l}" for l in main_lines))
        return "\n\n".join(parts)


class IRBuilder:
    """Accumulates instructions for one function (or the module's `main`)."""

    def __init__(self, prefix: str = "t"):
        self._prefix = prefix
        self._tmp = 0
        self._label = 0
        self.instrs: list[Instr] = []

    def fresh_tmp(self) -> str:
        name = f"{self._prefix}{self._tmp}"
        self._tmp += 1
        return name

    def fresh_label(self, hint: str) -> str:
        name = f"{hint}{self._label}"
        self._label += 1
        return name

    def emit(self, op: str, *args, dest: str | None = None, span: Span | None = None) -> str | None:
        self.instrs.append(Instr(op, tuple(args), dest, span))
        return dest

    def emit_value(self, op: str, *args, span: Span | None = None) -> str:
        dest = self.fresh_tmp()
        self.instrs.append(Instr(op, tuple(args), dest, span))
        return dest

    def label(self, name: str):
        self.instrs.append(Instr("LABEL", (), name, None))


def validate(program: IRProgram) -> list[str]:
    """Cheap structural validation: every JUMP/JUMPF target must exist as a
    LABEL in the same instruction list. Returns a list of problems (empty =
    valid). Used by the IR test suite and by `kuro build --emit-ir`."""

    problems: list[str] = []

    def check(instrs: list[Instr], where: str):
        labels = {i.dest for i in instrs if i.op == "LABEL"}
        for instr in instrs:
            if instr.op in ("JUMP", "JUMPF") and instr.args and instr.args[0] not in labels:
                problems.append(f"{where}: jump to undefined label {instr.args[0]!r}")

    check(program.main, "main")
    for fn in program.functions.values():
        check(fn.body, f"func {fn.name}")
    return problems
