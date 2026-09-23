"""Token model for the Kuro lexer.

Keywords are NOT reserved words at the token level (matches the bootstrap
implementation and spec's "recognize positionally" style): every alphabetic
identifier lexes as IDENT, and the parser decides whether a given IDENT is
acting as a keyword based on grammar position. This keeps `Name`, `Age`, etc.
usable as ordinary identifiers even though words like `Print` or `If` are
meaningful elsewhere.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto


class TokKind(Enum):
    STRING = auto()
    INTEGER = auto()
    DECIMAL = auto()
    IDENT = auto()

    EQUAL = auto()      # =
    COMMA = auto()       # ,
    SEMI = auto()         # ;
    DOT = auto()          # .
    LPAREN = auto()      # (
    RPAREN = auto()      # )
    AT = auto()            # @
    PLUS = auto()        # +
    MINUS = auto()       # -
    STAR = auto()        # *
    SLASH = auto()       # /
    COLON = auto()       # :
    LT = auto()          # <
    GT = auto()          # >

    EOF = auto()


# Single-character punctuation this lexer recognizes directly.
PUNCTUATION: dict[str, TokKind] = {
    "=": TokKind.EQUAL,
    ",": TokKind.COMMA,
    ";": TokKind.SEMI,
    ".": TokKind.DOT,
    "(": TokKind.LPAREN,
    ")": TokKind.RPAREN,
    "@": TokKind.AT,
    "+": TokKind.PLUS,
    "-": TokKind.MINUS,
    "*": TokKind.STAR,
    "/": TokKind.SLASH,
    ":": TokKind.COLON,
    "<": TokKind.LT,
    ">": TokKind.GT,
}


@dataclass(frozen=True)
class Token:
    kind: TokKind
    value: str
    line: int
    col: int
    end_line: int
    end_col: int

    def is_word(self, *words: str) -> bool:
        return self.kind is TokKind.IDENT and self.value in words

    def __repr__(self) -> str:
        return f"Token({self.kind.name}, {self.value!r}, {self.line}:{self.col})"
