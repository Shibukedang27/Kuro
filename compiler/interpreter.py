"""The Kuro IR interpreter — Stage 4's runtime (spec section 4/22).

Executes `IRProgram` (compiler/ir.py) directly; nothing here looks at the
AST. Ordinary bindings retain the global-write/parameter-overlay model.
The result binding `_` is different: main and each Action invocation own
one writable slot, whose absence is distinct from a present None. Direct
calls copy the caller's slot; Invoke copies the closure snapshot. A `_`
parameter initializes that slot, rather than permanently shadowing it.
Source producers and explicit writes replace only the current owner's slot.
This is not general lexical scoping; the frozen bootstrap oracle is unchanged.

Unlike the bootstrap engine, uncontrolled Python exceptions are not allowed
to reach the caller: deep recursion, division by zero, and out-of-range
indexing all become structured `KuroRuntimeException`s with an E6xxx code
(spec section 11 — "runtime errors must never produce meaningless crashes").

`While` (ADR-0009) is the first construct that can fail to terminate by
construction, so its lowered IR includes one `LOOP_GUARD` instruction per
loop (compiler/lower.py); this interpreter counts how many times each one
fires and raises `E6006` past `max_while_iterations` instead of hanging —
the same "no indefinite hangs" principle that already motivated `E6005`
for recursion depth.
"""
from __future__ import annotations

import re
import sys

from .diagnostics import Span
from .ir import IRFunction, IRProgram
from .values import ClosureValue, _artifact_suffix, _kuro_admit_row, builtin_call
from .concurrency import Scheduler
from .values import TaskValue

_MAX_CALL_DEPTH = 200
_DEFAULT_MAX_WHILE_ITERATIONS = 10_000_000


class _Unset:
    def __repr__(self):
        return "<unset>"


UNSET = _Unset()


class KuroRuntimeException(Exception):
    def __init__(self, code: str, message: str, span: Span | None = None):
        self.code = code
        self.message = message
        self.span = span
        loc = f"{span}: " if span else ""
        super().__init__(f"{loc}{message}")


class _Return(Exception):
    def __init__(self, value):
        self.value = value


class Interpreter:
    def __init__(
        self,
        ir: IRProgram,
        input_fn=input,
        output=None,
        max_while_iterations: int = _DEFAULT_MAX_WHILE_ITERATIONS,
        trace=None,
    ):
        self.ir = ir
        self.env: dict[str, object] = {}
        self.frames: list[dict[str, object]] = []
        self._input_fn = input_fn
        self._out = output if output is not None else sys.stdout
        self._max_while_iterations = max_while_iterations
        self.scheduler = Scheduler()
        self._trace = trace
        self.instruction_count = 0
        self.call_count = 0
        self.max_call_depth = 0

    # --- variable access --------------------------------------------
    def _result_owner(self):
        return self.frames[-1] if self.frames else self.env

    def _has_value(self, name):
        if name == "_":
            return name in self._result_owner()
        return name in self.env or (self.frames and name in self.frames[-1])

    def _read(self, name: str, span: Span | None):
        if name == "_":
            return self._result_owner().get(name)
        if self.frames and name in self.frames[-1]:
            return self.frames[-1][name]
        if name in self.env:
            return self.env[name]
        raise KuroRuntimeException("E4001", f"undefined value {name!r}", span)

    def _write(self, name: str, value):
        owner = self._result_owner() if name == "_" else self.env
        owner[name] = value

    # --- program entry -------------------------------------------------
    def run(self):
        self._execute(self.ir.main)

    def runtime_stats(self) -> dict[str, object]:
        states: dict[str, int] = {}
        for task in self.scheduler.tasks.values():
            states[task.state] = states.get(task.state, 0) + 1
        return {
            "instruction_count": self.instruction_count,
            "action_call_count": self.call_count,
            "max_call_depth": self.max_call_depth,
            "task_count": len(self.scheduler.tasks),
            "task_states": states,
        }

    def call(self, name: str, args: list):
        self.call_count += 1
        if name == "__KuroAdmitRow":
            if len(args) != 1:
                raise KuroRuntimeException("E3001", "__KuroAdmitRow requires exactly one argument", None)
            try:
                return _kuro_admit_row(args[0])
            except ValueError as error:
                raise KuroRuntimeException("E3001", str(error), None) from error
        if name == "Spawn" and len(args) >= 1 and isinstance(args[0], ClosureValue):
            return TaskValue(self.scheduler.spawn(args[0], args[1:]))
        if name == "Await" and len(args) == 1 and isinstance(args[0], TaskValue):
            try:
                return self.scheduler.await_task(args[0].task, lambda closure, values: self.call("Invoke", [closure, *values]))
            except KuroRuntimeException:
                raise
            except BaseException as error:
                raise KuroRuntimeException("E6007", f"task failed: {error}", None) from error
        if name == "MakeClosure" and len(args) == 1 and isinstance(args[0], str):
            if args[0] not in self.ir.functions:
                raise KuroRuntimeException("E4003", f"unknown action {args[0]!r}", None)
            captured = dict(self.env)
            for frame in self.frames:
                captured.update(frame)
            # Absence in the current owner must not resurrect an older slot.
            captured.pop("_", None)
            owner = self._result_owner()
            if "_" in owner:
                captured["_"] = owner["_"]
            # lower.py's hygienic counters are invocation bookkeeping, not
            # source-visible captures. An immutable Invoke overlay would hide
            # subsequent loop writes to env and can freeze a live counter.
            # Keep Index and all user bindings under the existing policy.
            captured = {
                name: value for name, value in captured.items()
                if re.fullmatch(r"__repeat_i[1-9][0-9]*\$", name) is None
            }
            return ClosureValue(args[0], captured)
        if name == "Invoke" and len(args) >= 1 and isinstance(args[0], ClosureValue):
            fn = self.ir.functions.get(args[0].action)
            if fn is None or len(args) - 1 != len(fn.params):
                raise KuroRuntimeException("E4004", "closure invocation has the wrong arity", None)
            frame = dict(args[0].captured)
            frame.update(zip(fn.params, args[1:]))
            self.frames.append(frame)
            self.max_call_depth = max(self.max_call_depth, len(self.frames))
            try:
                self._execute(fn.body)
            except _Return as returned:
                return returned.value
            finally:
                self.frames.pop()
            return None
        if name in {"Some", "None", "Ok", "Err", "IsSome", "IsNone", "IsOk", "IsErr", "Unwrap", "UnwrapErr", "MakeRecord", "RecordSet", "RecordGet", "MakeEnum", "EnumIs", "MakeMap", "MapSet", "MapGet", "MapHas", "ReadFile", "WriteFile", "FileExists", "ListDirectory", "Now", "MakeChannel", "Send", "Receive", "ChannelHas"}:
            try:
                return builtin_call(name, args)
            except ValueError as error:
                raise KuroRuntimeException("E3001", str(error), None) from error
        fn = self.ir.functions.get(name)
        if fn is None:
            raise KuroRuntimeException("E4003", f"unknown action {name!r}", None)
        if len(self.frames) >= _MAX_CALL_DEPTH:
            raise KuroRuntimeException("E6005", "maximum recursion depth exceeded", None)
        # Copy before pushing: direct entry inherits the effective caller slot.
        owner = self._result_owner()
        frame = {"_": owner["_"]} if "_" in owner else {}
        frame.update(zip(fn.params, args))
        self.frames.append(frame)
        self.max_call_depth = max(self.max_call_depth, len(self.frames))
        try:
            self._execute(fn.body)
            return None
        except _Return as r:
            return r.value
        finally:
            self.frames.pop()

    # --- the instruction loop -------------------------------------------
    def _execute(self, instrs):
        labels = {instr.dest: i for i, instr in enumerate(instrs) if instr.op == "LABEL"}
        temps: dict[str, object] = {}
        loop_counts: dict[str, int] = {}
        pc = 0
        n = len(instrs)
        while pc < n:
            instr = instrs[pc]
            self.instruction_count += 1
            if self._trace is not None:
                self._trace(instr, dict(self.env), len(self.frames), pc)
            op = instr.op
            span = instr.span

            if op == "LABEL":
                pc += 1
                continue
            if op == "CONST":
                temps[instr.dest] = instr.args[0]
            elif op == "LOADVAR":
                temps[instr.dest] = self._read(instr.args[0], span)
            elif op == "STORE_LIST":
                name, tmp_names = instr.args
                vals = [temps[t] for t in tmp_names]
                self._write(name, vals[0] if len(vals) == 1 else vals)
            elif op == "DECLTYPE":
                pass
            elif op == "CHECK_NONNEG":
                val = temps[instr.args[0]]
                if isinstance(val, (int, float)) and val < 0:
                    raise KuroRuntimeException("E6004", "Repeat count cannot be negative", span)
            elif op == "LOOP_GUARD":
                guard_id = instr.args[0]
                count = loop_counts.get(guard_id, 0) + 1
                loop_counts[guard_id] = count
                if count > self._max_while_iterations:
                    raise KuroRuntimeException(
                        "E6006",
                        f"While loop exceeded maximum iteration count ({self._max_while_iterations})",
                        span,
                    )
            elif op == "INPUT":
                name, typ = instr.args
                raw = self._input_fn(f"{name} ({typ}): ")
                try:
                    if typ == "Integers":
                        value = int(raw)
                    elif typ == "Decimals":
                        value = float(raw)
                    else:
                        value = raw
                except ValueError:
                    raise KuroRuntimeException("E6002", f"invalid {typ} input for {name!r}", span)
                self._write(name, value)
            elif op == "ADD":
                target, tmp = instr.args
                current = self._read(target, span) if self._has_value(target) else 0
                self._write(target, current + temps[tmp])
            elif op == "UPDATE":
                name, tmp = instr.args
                self._write(name, temps[tmp])
            elif op == "APPEND":
                name, tmp = instr.args
                current = self._read(name, span) if self._has_value(name) else None
                if current is None:
                    self._write(name, [temps[tmp]])
                elif isinstance(current, list):
                    current.append(temps[tmp])
                else:
                    self._write(name, [current, temps[tmp]])
            elif op == "PRINT":
                value = temps[instr.args[0]]
                if isinstance(value, list):
                    for item in value:
                        print(item, file=self._out)
                else:
                    print(value, file=self._out)
            elif op == "GET":
                name, idx_tmp = instr.args
                value = self._read(name, span)
                if idx_tmp is None:
                    temps[instr.dest] = value
                else:
                    idx = int(temps[idx_tmp])
                    try:
                        temps[instr.dest] = value[idx]
                    except (IndexError, TypeError):
                        raise KuroRuntimeException("E6001", f"index {idx} out of range for {name!r}", span)
            elif op == "LENGTH":
                name = instr.args[0]
                value = self._read(name, span)
                try:
                    temps[instr.dest] = len(value)
                except TypeError:
                    raise KuroRuntimeException("E3005", f"{name!r} has no length", span)
            elif op == "SET":
                name, idx_tmp, val_tmp = instr.args
                target = self._read(name, span)
                idx = int(temps[idx_tmp])
                val = temps[val_tmp]
                if isinstance(target, str):
                    if not isinstance(val, str) or len(val) != 1:
                        raise KuroRuntimeException("E3004", "Set on Text requires one character", span)
                    if not 0 <= idx < len(target):
                        raise KuroRuntimeException("E6001", "Text index out of range", span)
                    self._write(name, target[:idx] + val + target[idx + 1 :])
                elif isinstance(target, list):
                    if not 0 <= idx < len(target):
                        raise KuroRuntimeException("E6001", "collection index out of range", span)
                    target[idx] = val
                else:
                    raise KuroRuntimeException("E3005", "Set target is not indexable", span)
            elif op == "BINOP":
                bop, lt, rt = instr.args
                temps[instr.dest] = self._binop(bop, temps[lt], temps[rt], span)
            elif op == "CMP":
                cop, lt, rt = instr.args
                temps[instr.dest] = self._cmp(cop, temps[lt], temps[rt])
            elif op == "AND":
                lt, rt = instr.args
                temps[instr.dest] = bool(temps[lt]) and bool(temps[rt])
            elif op == "OR":
                lt, rt = instr.args
                temps[instr.dest] = bool(temps[lt]) or bool(temps[rt])
            elif op == "ISCLASS":
                operand_tmp, cls = instr.args
                temps[instr.dest] = self._isclass(temps[operand_tmp], cls)
            elif op == "SAVEVAR":
                name = instr.args[0]
                temps[instr.dest] = self.env.get(name, UNSET)
            elif op == "RESTOREVAR":
                name, tmp = instr.args
                val = temps[tmp]
                if val is UNSET:
                    self.env.pop(name, None)
                else:
                    self.env[name] = val
            elif op == "ARTIFACT_SUFFIX":
                source_tmp, offset_tmp = instr.args
                try:
                    temps[instr.dest] = _artifact_suffix(temps[source_tmp], temps[offset_tmp])
                except (IndexError, TypeError) as error:
                    raise KuroRuntimeException("E6001", str(error), span) from error
            elif op == "CALL":
                name, *arg_tmps = instr.args
                args = [temps[t] for t in arg_tmps]
                try:
                    temps[instr.dest] = self.call(name, args)
                except RecursionError:
                    raise KuroRuntimeException("E6005", "maximum recursion depth exceeded", span)
            elif op == "RETURN":
                raise _Return(temps[instr.args[0]])
            elif op == "JUMP":
                pc = labels[instr.args[0]]
                continue
            elif op == "JUMPF":
                label, cond_tmp = instr.args
                if not temps[cond_tmp]:
                    pc = labels[label]
                    continue
            else:
                raise AssertionError(f"unhandled IR op {op!r}")
            pc += 1

    def _binop(self, op: str, a, b, span):
        if op == "+" and isinstance(a, str) and isinstance(b, str):
            return a + b
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise KuroRuntimeException("E3001", f"cannot apply {op!r} to non-numeric values", span)
        if op == "+":
            return a + b
        if op == "-":
            return a - b
        if op == "*":
            return a * b
        if op == "/":
            if b == 0:
                raise KuroRuntimeException("E6003", "division by zero", span)
            if isinstance(a, int) and isinstance(b, int) and a % b == 0:
                return a // b
            return a / b
        raise AssertionError(f"unhandled binop {op!r}")

    def _cmp(self, op: str, a, b) -> bool:
        if op == "eq":
            return a == b
        if op == "ne":
            return a != b
        if op == "gt":
            return a > b
        if op == "lt":
            return a < b
        if op == "ge":
            return a >= b
        if op == "le":
            return a <= b
        raise AssertionError(f"unhandled comparison {op!r}")

    def _isclass(self, value, cls: str) -> bool:
        if not isinstance(value, str) or len(value) != 1:
            return False
        return {
            "digit": value.isdigit(),
            "alpha": value.isalpha(),
            "space": value.isspace(),
            "alnum": value.isalnum(),
            "quote": value == '"',
        }[cls]


def run(ir: IRProgram, input_fn=input, output=None) -> Interpreter:
    interp = Interpreter(ir, input_fn=input_fn, output=output)
    interp.run()
    return interp
