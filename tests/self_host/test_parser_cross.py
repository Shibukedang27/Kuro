"""Stage 6 differential test (spec section 61, ADR-0010): the Kuro-in-Kuro
parser (self_host/parser.kuro) must build the same AST — compared via the
canonical flat encoding in compiler/ast_canon.py — as compiler/parser.py,
the Python reference parser, for real Kuro source within the grammar
subset self_host/parser.kuro covers this session (see its header comment
and ADR-0010 for exactly what that is and isn't).

Method: self_host/lexer.kuro (Source substituted, same technique as
tests/self_host/test_lexer_cross.py) is concatenated with self_host/
parser.kuro (with its own small standalone-token default stripped, since
the lexer now supplies real tokens instead — see parser.kuro's
BEGIN/END_STANDALONE_TOKENS markers) into one generated program. Running
it populates AstOut; that's compared against
compiler.ast_canon.canon_program() run on compiler/parser.py's real AST
for the same source.
"""
import re
from pathlib import Path

import pytest

from compiler.ast_canon import canon_program
from compiler.diagnostics import DiagnosticEngine
from compiler.lexer import tokenize
from compiler.parser import parse
from compiler.pipeline import run_source

ROOT = Path(__file__).resolve().parent.parent.parent
LEXER_KURO_PATH = ROOT / "self_host" / "lexer.kuro"
PARSER_KURO_PATH = ROOT / "self_host" / "parser.kuro"

_SOURCE_LINE_RE = re.compile(r'^Source = ".*";$', re.MULTILINE)
_STANDALONE_TOKENS_RE = re.compile(
    r"^# --- BEGIN_STANDALONE_TOKENS.*?^# --- END_STANDALONE_TOKENS.*?$\n?",
    re.MULTILINE | re.DOTALL,
)


def kuro_escape(s: str) -> str:
    return (
        s.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
        .replace("\t", "\\t")
        .replace("\r", "\\r")
    )


def python_ast(source: str) -> list[str]:
    toks, diags = tokenize(source)
    assert not diags.diagnostics, diags.render_all()
    program = parse(toks, diags)
    assert not diags.diagnostics, diags.render_all()
    return canon_program(program)


_parser_body_cache: str | None = None


def _parser_body_without_standalone_tokens() -> str:
    global _parser_body_cache
    if _parser_body_cache is None:
        raw = PARSER_KURO_PATH.read_text(encoding="utf-8")
        stripped, n = _STANDALONE_TOKENS_RE.subn("", raw, count=1)
        assert n == 1, "could not find the BEGIN/END_STANDALONE_TOKENS block to strip"
        _parser_body_cache = stripped
    return _parser_body_cache


def kuro_ast(source: str):
    lexer_template = LEXER_KURO_PATH.read_text(encoding="utf-8")
    new_line = f'Source = "{kuro_escape(source)}";'
    lexer_body, n = _SOURCE_LINE_RE.subn(lambda m: new_line, lexer_template, count=1)
    assert n == 1, "could not find the Source assignment line to substitute"

    generated = lexer_body + "\n" + _parser_body_without_standalone_tokens()
    result = run_source(generated, filename="<generated lexer+parser>")
    assert result.ok, (
        result.compile.diags.render_all() if not result.compile.ok else result.runtime_error
    )
    ast_out = result.interpreter.env.get("AstOut")
    parse_failed = result.interpreter.env.get("ParseFailed")
    return ast_out, parse_failed


# --- differential test corpus (restricted to the covered grammar subset,
# see self_host/parser.kuro's header comment) ---------------------------

SNIPPETS = [
    'Name = "Kuro";\nPrint Name.',
    "Age : Integers = 25;",
    'Names = "A", "B", "C";\nPrint Names.',
    "Print 2 + 3 * 4.",
    "Print (2 + 3) * 4.",
    "N = -5;\nPrint N.",
    "Score is Integers;\nScore = 0;\nAdd 1 to Score;\nPrint Score.",
    "Score is Integers;\nScore = 0;\nUpdate Score to 5;\nPrint Score.",
    'Age is Integers;\nAge = 25;\nIf Age is greater than 20;\nPrint "Old".\nElse;\nPrint "Young".\nDone.',
    "N is Integers;\nN = 5;\nIf N is greater than 1 and N is less than 10;\nPrint N.\nDone.",
    "N is Integers;\nN = 20;\nIf N is less than 1 or N is greater than 10;\nPrint N.\nDone.",
    'C = "5";\nIf C is digit;\nPrint "yes".\nDone.',
    "Repeat 3;\nPrint Index.\nDone.",
    "Repeat 2;\nIf Index is greater than 0;\nPrint Index.\nDone.\nDone.",
    "N is Integers;\nN = 0;\nWhile N is less than 3;\nPrint N.\nAdd 1 to N;\nDone.",
    "Action Add A, B;\nReturn A + B;\nDone.\nCall Add 3, 4;\nPrint @_.",
    "Action Add(A, B);\nReturn A + B;\nDone.\nCall Add(3, 4);\nPrint @_.",
    "Action Add A: Integers, B: Integers;\nReturn A + B;\nDone.",
    "Action Fact N;\nIf N is less than or equal to 1;\nReturn 1;\nDone.\nCall Fact N - 1;\nReturn N * @_;\nDone.\nCall Fact 5;\nPrint @_.",
    "N is Integers;\nN = 3;\nIf N is greater than or equal to 3;\nPrint N.\nDone.",
    "N is Integers;\nN = 3;\nIf N is at least 3;\nPrint N.\nDone.",
    "N is Integers;\nN = 3;\nIf N is at most 3;\nPrint N.\nDone.",
    # Regression coverage for the reentrancy bug found while building this
    # parser (see self_host/parser.kuro's header comment): a construct
    # that recurses back through the SAME repetition it's part of, which
    # a while+flag loop cannot survive but tail recursion can.
    "Print 2 * (3 * 4).",  # nested parens re-enter ParseFactor's own repetition
    "N is Integers;\nN = 2 * (3 + 4 * 5) - 1;\nPrint N.",
    "Action Outer;\nIf 1 is equal to 1;\nPrint 1.\nDone.\nDone.\nCall Outer;\nPrint 2.",
    (
        "Action A X;\nReturn X;\nDone.\n"
        "Action B X;\nIf X is greater than 0;\nPrint X.\nDone.\nReturn X;\nDone.\n"
        "Call B 1;\nPrint 2."
    ),
]


@pytest.mark.parametrize("source", SNIPPETS, ids=[f"snippet{i}" for i in range(len(SNIPPETS))])
def test_self_hosted_parser_matches_python_parser_ast(source):
    expected = python_ast(source)
    actual, parse_failed = kuro_ast(source)
    assert parse_failed == 0, f"self-hosted parser reported ParseFailed for: {source!r}"
    assert actual == expected


# --- malformed input: must not hang or crash (ADR-0010's "Error behavior") --

MALFORMED_SNIPPETS = [
    "Name = ",                      # incomplete expression, EOF
    "If Age is greater than 20\nPrint",  # missing ';' after condition
    "Repeat 3;\nPrint Index.",      # missing Done.
    "Action Add A, B;\nReturn A;",  # missing Done.
    "N = 1 +",                      # dangling operator, EOF
    "((((((",                       # unbalanced grouping
]


@pytest.mark.parametrize("source", MALFORMED_SNIPPETS, ids=[f"malformed{i}" for i in range(len(MALFORMED_SNIPPETS))])
def test_malformed_input_does_not_hang_or_crash(source):
    # Deliberately not comparing against the Python parser's diagnostics -
    # ADR-0010 documents this parser doesn't yet produce equivalent
    # structured errors. The property under test is termination.
    ast_out, parse_failed = kuro_ast(source)
    assert parse_failed == 1
