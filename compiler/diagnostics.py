"""Structured diagnostics for the Kuro compiler.

Every compiler phase reports problems as `Diagnostic` objects collected by a
`DiagnosticEngine` instead of raising on the first error. This gives the
lexer, parser, and semantic checker error *recovery*: a source file with
three unrelated mistakes can be reported in one pass instead of three runs.

Error code ranges (spec section 18):
    E1xxx  lexer
    E2xxx  parser
    E3xxx  type checking
    E4xxx  name resolution
    E5xxx  module system
    E6xxx  runtime
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Severity(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    HINT = "hint"


@dataclass(frozen=True)
class Span:
    """A half-open source range, both ends inclusive-line/col for display."""

    line: int
    col: int
    end_line: int = -1
    end_col: int = -1

    def __post_init__(self):
        if self.end_line == -1:
            object.__setattr__(self, "end_line", self.line)
        if self.end_col == -1:
            object.__setattr__(self, "end_col", self.col + 1)

    def __str__(self) -> str:
        return f"{self.line}:{self.col}"


@dataclass(frozen=True)
class Diagnostic:
    severity: Severity
    code: str
    message: str
    span: Span
    notes: tuple[str, ...] = field(default_factory=tuple)
    help: str | None = None

    def render(self, filename: str, source_lines: list[str] | None = None) -> str:
        head = f"{self.severity.value}[{self.code}]: {self.message}"
        loc = f"  --> {filename}:{self.span.line}:{self.span.col}"
        out = [head, loc]
        if source_lines and 1 <= self.span.line <= len(source_lines):
            text = source_lines[self.span.line - 1]
            gutter = f"{self.span.line}"
            out.append(f"{' ' * len(gutter)} |")
            out.append(f"{gutter} | {text}")
            width = max(1, self.span.end_col - self.span.col) if self.span.end_line == self.span.line else 1
            caret = " " * (self.span.col - 1) + "^" * width
            out.append(f"{' ' * len(gutter)} | {caret}")
        for note in self.notes:
            out.append(f"  = {note}")
        if self.help:
            out.append(f"  = help: {self.help}")
        return "\n".join(out)


class DiagnosticEngine:
    """Accumulates diagnostics for one compilation unit."""

    def __init__(self, filename: str, source: str | None = None):
        self.filename = filename
        self.source_lines = source.splitlines() if source is not None else None
        self.diagnostics: list[Diagnostic] = []

    def report(
        self,
        severity: Severity,
        code: str,
        message: str,
        span: Span,
        notes: tuple[str, ...] = (),
        help: str | None = None,
    ) -> Diagnostic:
        d = Diagnostic(severity, code, message, span, notes, help)
        self.diagnostics.append(d)
        return d

    def error(self, code: str, message: str, span: Span, **kw) -> Diagnostic:
        return self.report(Severity.ERROR, code, message, span, **kw)

    def warning(self, code: str, message: str, span: Span, **kw) -> Diagnostic:
        return self.report(Severity.WARNING, code, message, span, **kw)

    def has_errors(self) -> bool:
        return any(d.severity == Severity.ERROR for d in self.diagnostics)

    def render_all(self) -> str:
        return "\n\n".join(d.render(self.filename, self.source_lines) for d in self.diagnostics)

    def to_json(self) -> list[dict]:
        return [
            {
                "severity": d.severity.value,
                "code": d.code,
                "message": d.message,
                "line": d.span.line,
                "col": d.span.col,
                "end_line": d.span.end_line,
                "end_col": d.span.end_col,
                "notes": list(d.notes),
                "help": d.help,
            }
            for d in self.diagnostics
        ]


class KuroCompileError(Exception):
    """Raised to unwind a phase once it can no longer usefully recover."""

    def __init__(self, engine: DiagnosticEngine):
        self.engine = engine
        super().__init__(engine.render_all())


# --- Registry -----------------------------------------------------------
# A living table of every diagnostic code this compiler can emit, so codes
# are never reused for unrelated problems. Extend this whenever a new
# .error()/.warning() call site introduces a code that isn't here yet.
REGISTRY: dict[str, str] = {
    "E1001": "unterminated string literal",
    "E1002": "unexpected character",
    # E1003 ("invalid numeric literal") is reserved, not currently emitted:
    # the lexer's dot-requires-a-following-digit rule (see lexer.py
    # _scan_number) means a malformed literal like "3." or "3.4.5" is
    # never produced in the first place — it tokenizes as INTEGER/DECIMAL
    # followed by a separate DOT, which is exactly what a trailing
    # Print-statement terminator needs. Keeping the code reserved (not
    # deleted) in case a future literal form reintroduces a real failure
    # mode here; it must not be reused for something unrelated.
    "E2001": "unexpected token",
    "E2002": "expected a specific token/keyword and did not find it",
    "E2003": "expected a value expression",
    "E2004": "expected a comparison operator",
    "E2005": "duplicate parameter name in Action",
    "E3001": "type mismatch in assignment",
    "E3002": "Add target is not numeric",
    "E3003": "unknown declared type",
    "E3004": "Set on Text requires a single character",
    "E3005": "value is not indexable / has no length",
    "E3006": "incompatible operand types in comparison (ADR-0013)",
    "E3007": "call argument type does not match the parameter's declared type (ADR-0013)",
    "E3008": "Repeat count must be Integers (ADR-0013)",
    "E3009": "Length target must be Text (ADR-0013)",
    "E3010": "Get/Set index must be Integers (ADR-0013)",
    "E3011": "invalid operand types for arithmetic (ADR-0013)",
    "E4001": "undefined variable",
    "E4002": "duplicate declaration",
    "E4003": "unknown action",
    "E4004": "wrong number of arguments to an action call",
    "E4005": "Return used outside of an Action",
    "E6001": "index out of range",
    "E6002": "invalid input conversion",
    "E6003": "division by zero",
    "E6004": "Repeat count is negative",
    "E6005": "maximum recursion depth exceeded",
    "E6006": "While loop exceeded maximum iteration count (ADR-0009)",
}
