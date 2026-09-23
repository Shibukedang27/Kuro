"""Wires the compiler phases together: source -> diagnostics | IR -> result.

This is the one place that knows the full phase order, so both the CLI and
the test suite call through here instead of re-assembling lexer/parser/
resolver/typecheck/lower by hand.
"""
from __future__ import annotations

from dataclasses import dataclass

from .ast_nodes import Program
from .diagnostics import DiagnosticEngine
from .interpreter import Interpreter, KuroRuntimeException
from .ir import IRProgram
from .lexer import tokenize
from .lower import lower
from .modules import load_modules
from .parser import parse
from .resolver import SymbolTable, resolve
from .typecheck import typecheck


@dataclass
class CompileResult:
    diags: DiagnosticEngine
    program: Program | None = None
    symbols: SymbolTable | None = None
    ir: IRProgram | None = None

    @property
    def ok(self) -> bool:
        return not self.diags.has_errors()


def compile_source(source: str, filename: str = "<source>") -> CompileResult:
    diags = DiagnosticEngine(filename, source)
    source = load_modules(source, filename, diags)
    if diags.has_errors():
        return CompileResult(diags)
    tokens, lex_diags = tokenize(source, filename)
    diags.diagnostics.extend(lex_diags.diagnostics)
    if diags.has_errors():
        return CompileResult(diags)

    program = parse(tokens, diags)
    if diags.has_errors():
        return CompileResult(diags, program)

    symbols = resolve(program, diags)
    if diags.has_errors():
        return CompileResult(diags, program, symbols)

    typecheck(program, symbols, diags)
    if diags.has_errors():
        return CompileResult(diags, program, symbols)

    ir = lower(program, symbols)
    return CompileResult(diags, program, symbols, ir)


@dataclass
class RunResult:
    compile: CompileResult
    stdout: str | None = None
    runtime_error: KuroRuntimeException | None = None
    interpreter: Interpreter | None = None

    @property
    def ok(self) -> bool:
        return self.compile.ok and self.runtime_error is None


def run_source(source: str, filename: str = "<source>", input_fn=input, **interp_kwargs) -> RunResult:
    import io

    result = compile_source(source, filename)
    if not result.ok:
        return RunResult(result)

    buf = io.StringIO()
    interp = Interpreter(result.ir, input_fn=input_fn, output=buf, **interp_kwargs)
    try:
        interp.run()
    except KuroRuntimeException as e:
        return RunResult(result, buf.getvalue(), e, interp)
    return RunResult(result, buf.getvalue(), None, interp)
