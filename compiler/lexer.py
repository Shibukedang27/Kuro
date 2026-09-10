"""Lexer for Kuro source text.

Design decisions (see docs/engineering/ADR-0003-lexer-and-unicode.md):

* Line-oriented, like the bootstrap lexer: strings and comments cannot span
  lines. This is a real limitation, kept deliberately rather than silently
  changed, because changing it would be a grammar change, not a cleanup.
* Comments: `# ...` and `// ...` to end of line, respecting `"..."` string
  boundaries so a `#` inside a string literal is not treated as a comment.
  No block comments exist.
* Identifiers: `(alpha|_) (alnum|_)*` using Python's Unicode-aware
  `str.isalpha()`/`str.isalnum()`, so non-ASCII identifiers (e.g. Devanagari,
  accented Latin) lex correctly. Keywords are not reserved (see tokens.py).
* Error recovery: unlike the bootstrap lexer (which raised on the first
  problem), this lexer records a diagnostic and keeps going — an unexpected
  character is skipped and lexing resumes after it; an unterminated string
  consumes the rest of the line as its content and resumes on the next line.
  This lets one run report every lexical problem in a file, not just the
  first (spec section 33: the compiler must not abort a whole pass over a
  recoverable local error).
"""
from __future__ import annotations

import unicodedata

from .diagnostics import DiagnosticEngine, Span
from .tokens import PUNCTUATION, Token, TokKind

_ESCAPES = {"n": "\n", "t": "\t", "r": "\r", '"': '"', "\\": "\\", "0": "\0"}

# Identifier continuation follows a simplified Unicode ID_Continue: letters,
# digits, underscore, and combining marks (category Mn/Mc — e.g. Devanagari
# matras) so a composed identifier like "नाम" lexes as one token instead of
# stopping at the first combining vowel sign.
def _is_ident_continue(c: str) -> bool:
    return c.isalnum() or c == "_" or unicodedata.category(c) in ("Mn", "Mc")


class Lexer:
    def __init__(self, source: str, diags: DiagnosticEngine):
        self.source = source
        self.diags = diags

    def tokenize(self) -> list[Token]:
        tokens: list[Token] = []
        lines = self.source.splitlines()
        last_line = 1
        for lineno, raw in enumerate(lines, start=1):
            last_line = lineno
            tokens.extend(self._lex_line(raw, lineno))
        tokens.append(Token(TokKind.EOF, "", last_line + 1, 1, last_line + 1, 1))
        return tokens

    def _lex_line(self, line: str, lineno: int) -> list[Token]:
        stripped = _strip_comment(line)
        out: list[Token] = []
        i = 0
        n = len(stripped)
        while i < n:
            c = stripped[i]
            if c.isspace():
                i += 1
                continue
            start_col = i + 1

            if c == '"':
                value, i, ok = self._lex_string(stripped, i, lineno)
                out.append(Token(TokKind.STRING, value, lineno, start_col, lineno, i + 1))
                if not ok:
                    self.diags.error(
                        "E1001",
                        "unterminated string literal",
                        Span(lineno, start_col, lineno, i + 1),
                        help='add a closing " before the end of the line',
                    )
                continue

            if c.isdigit():
                j, is_decimal = self._scan_number(stripped, i)
                text = stripped[i:j]
                kind = TokKind.DECIMAL if is_decimal else TokKind.INTEGER
                out.append(Token(kind, text, lineno, start_col, lineno, j + 1))
                i = j
                continue

            if c.isalpha() or c == "_":
                j = i + 1
                while j < n and _is_ident_continue(stripped[j]):
                    j += 1
                out.append(Token(TokKind.IDENT, stripped[i:j], lineno, start_col, lineno, j + 1))
                i = j
                continue

            if c in PUNCTUATION:
                out.append(Token(PUNCTUATION[c], c, lineno, start_col, lineno, start_col + 1))
                i += 1
                continue

            self.diags.error(
                "E1002",
                f"unexpected character {c!r}",
                Span(lineno, start_col, lineno, start_col + 1),
            )
            i += 1
        return out

    def _lex_string(self, s: str, i: int, lineno: int) -> tuple[str, int, bool]:
        assert s[i] == '"'
        i += 1
        buf: list[str] = []
        n = len(s)
        while i < n:
            if s[i] == '"':
                return "".join(buf), i + 1, True
            if s[i] == "\\" and i + 1 < n:
                buf.append(_ESCAPES.get(s[i + 1], s[i + 1]))
                i += 2
                continue
            buf.append(s[i])
            i += 1
        return "".join(buf), i, False

    def _scan_number(self, s: str, i: int) -> tuple[int, bool]:
        # A '.' only belongs to the number if a digit follows it. This
        # matters because '.' is *also* the `Print`-statement terminator
        # (`Print 10 / 2.`) — without this lookahead, `2.` would be
        # swallowed whole as a decimal literal and the statement would
        # never find its terminator. A digit run with no following-digit
        # dot (e.g. plain "3.") is just the integer "3" followed by a
        # separate DOT token, not a malformed literal.
        n = len(s)
        start = i
        while i < n and s[i].isdigit():
            i += 1
        is_decimal = False
        if i < n and s[i] == "." and i + 1 < n and s[i + 1].isdigit():
            is_decimal = True
            i += 1
            while i < n and s[i].isdigit():
                i += 1
        return i, is_decimal


def _strip_comment(line: str) -> str:
    out = []
    i = 0
    quoted = False
    n = len(line)
    while i < n:
        c = line[i]
        if c == '"':
            quoted = not quoted
            out.append(c)
            i += 1
            continue
        if not quoted and c == "#":
            break
        if not quoted and c == "/" and i + 1 < n and line[i + 1] == "/":
            break
        out.append(c)
        i += 1
    return "".join(out)


def tokenize(source: str, filename: str = "<source>") -> tuple[list[Token], DiagnosticEngine]:
    diags = DiagnosticEngine(filename, source)
    toks = Lexer(source, diags).tokenize()
    return toks, diags
