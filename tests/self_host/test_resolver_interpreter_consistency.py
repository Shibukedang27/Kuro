"""Stage 7, Phase 29 (mandatory per this stage's task): resolver/typechecker
visibility vs. runtime visibility must agree.

For each representative program: (1) self_host/resolver.kuro +
self_host/typecheck.kuro must accept it with zero diagnostics, AND (2) the
same program must actually run correctly (the real interpreter -
compiler/interpreter.py, since no self-hosted interpreter exists yet -
Stage 8) and produce the expected output. A variable the self-hosted
semantic layer considers valid must behave consistently at runtime; this
is not implied by the differential tests elsewhere, which only check that
semantic *diagnostics* match the Python oracle's, not that a validated
program's *behavior* matches what a person reading the source would
expect.
"""
import re
from pathlib import Path

import pytest

from compiler.pipeline import run_source

ROOT = Path(__file__).resolve().parent.parent.parent
LEXER_KURO_PATH = ROOT / "self_host" / "lexer.kuro"
PARSER_KURO_PATH = ROOT / "self_host" / "parser.kuro"
RESOLVER_KURO_PATH = ROOT / "self_host" / "resolver.kuro"
TYPECHECK_KURO_PATH = ROOT / "self_host" / "typecheck.kuro"

_SOURCE_LINE_RE = re.compile(r'^Source = ".*";$', re.MULTILINE)


def _strip_marked_block(text: str, begin: str, end: str) -> str:
    pat = re.compile(rf"^# --- {begin}.*?^# --- {end}.*?$\n?", re.MULTILINE | re.DOTALL)
    stripped, n = pat.subn("", text, count=1)
    assert n == 1
    return stripped


def kuro_escape(s: str) -> str:
    return (
        s.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
        .replace("\t", "\\t")
        .replace("\r", "\\r")
    )


_cache: dict[str, str] = {}


def _body(path: Path, begin: str, end: str, key: str) -> str:
    if key not in _cache:
        _cache[key] = _strip_marked_block(path.read_text(encoding="utf-8"), begin, end)
    return _cache[key]


def self_hosted_diag_codes(source: str) -> list[str]:
    lexer_template = LEXER_KURO_PATH.read_text(encoding="utf-8")
    new_line = f'Source = "{kuro_escape(source)}";'
    lexer_body, n = _SOURCE_LINE_RE.subn(lambda m: new_line, lexer_template, count=1)
    assert n == 1

    parser_body = _body(PARSER_KURO_PATH, "BEGIN_STANDALONE_TOKENS", "END_STANDALONE_TOKENS", "parser")
    resolver_body = _body(RESOLVER_KURO_PATH, "BEGIN_STANDALONE", "END_STANDALONE", "resolver")
    typecheck_body = _body(TYPECHECK_KURO_PATH, "BEGIN_STANDALONE", "END_STANDALONE", "typecheck")
    generated = lexer_body + "\n" + parser_body + "\n" + resolver_body + "\n" + typecheck_body

    result = run_source(generated, filename="<generated full pipeline>")
    assert result.ok, (
        result.compile.diags.render_all() if not result.compile.ok else result.runtime_error
    )
    return result.interpreter.env.get("DiagCodes") or []


CASES = [
    ('Name = "Kuro";\nPrint Name.', "Kuro\n"),
    ("Age is Integers;\nAge = 25;\nPrint Age.", "25\n"),
    ("Repeat 3;\nX = Index;\nDone.\nPrint X.", "2\n"),
    (
        "N is Integers;\nN = 0;\nWhile N is less than 3;\nY = N;\nAdd 1 to N;\nDone.\nPrint Y.",
        "2\n",
    ),
    ("Action A;\nZ = 1;\nReturn Z;\nDone.\nCall A;\nPrint Z.", "1\n"),
    (
        "Action First;\nShared = 5;\nReturn Shared;\nDone.\n"
        "Action Second;\nReturn Shared;\nDone.\n"
        "Call First;\nCall Second;\nPrint @_.",
        "5\n",
    ),
    ("Action Add A, B;\nReturn A + B;\nDone.\nCall Add 3, 4;\nPrint @_.", "7\n"),
    (
        "Action Fact N;\nIf N is less than or equal to 1;\nReturn 1;\nDone.\n"
        "Call Fact N - 1;\nReturn N * @_;\nDone.\nCall Fact 5;\nPrint @_.",
        "120\n",
    ),
    ('N = "a" + "b";\nPrint N.', "ab\n"),
    ("A = 5;\nCompare Bigger A greater than 3;\nPrint Bigger.", "True\n"),
]


@pytest.mark.parametrize("source,expected_stdout", CASES, ids=[f"case{i}" for i in range(len(CASES))])
def test_semantically_valid_program_runs_and_produces_expected_output(source, expected_stdout):
    # (1) the self-hosted semantic layer must accept it with no diagnostics
    assert self_hosted_diag_codes(source) == []
    # (2) and running it (the only interpreter that exists - Stage 8 will
    # add a self-hosted one) must produce exactly the output a reader of
    # the source would expect - not just "doesn't crash."
    result = run_source(source)
    assert result.ok, (
        result.compile.diags.render_all() if not result.compile.ok else result.runtime_error
    )
    assert result.stdout == expected_stdout


REJECTED_CASES = [
    "Print Missing.",
    "Repeat 3;\nPrint Index.\nDone.\nPrint Index.",
    "Action A Local;\nReturn Local;\nDone.\nPrint Local.",
]


@pytest.mark.parametrize("source", REJECTED_CASES, ids=[f"rejected{i}" for i in range(len(REJECTED_CASES))])
def test_semantically_rejected_program_is_not_silently_runnable_either(source):
    # A program the self-hosted semantic layer flags must not be one the
    # real pipeline silently accepts and runs anyway - both must agree
    # it's invalid, not just the self-hosted side.
    assert self_hosted_diag_codes(source) != []
    result = run_source(source)
    assert not result.ok
    assert not result.compile.ok
