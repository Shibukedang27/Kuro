"""Stage 5 cross-test (spec section 61): the Kuro-in-Kuro lexer
(self_host/lexer.kuro) must tokenize real Kuro source identically to
compiler/lexer.py, the Python reference lexer.

Method: self_host/lexer.kuro's `Source = "...";` line is a template. This
harness substitutes each test snippet into that line (escaped as a Kuro
string literal), runs the *whole* generated program through
compiler/pipeline.py (the Stage 1-4 Python-hosted compiler executing real
Kuro code — this is what "self-hosted" means before a native backend
exists: Kuro logic, not Python logic, is doing the tokenizing), and
compares its printed (KIND, VALUE) pairs against compiler/lexer.py's own
tokens for the same snippet.

Snippets are drawn from this project's own real fixtures
(bootstrap/python/tests/*.kuro) — "tokenizing real Kuro compiler source"
per the spec's Stage 5 requirement — plus one hand-written snippet
exercising every punctuation kind. None of the fixtures contain string
escapes, which keeps this test's line-based protocol simple; see
self_host/lexer.kuro's header comment for what's knowingly out of scope
this session (source locations, error recovery, Unicode combining marks).
"""
import re
from pathlib import Path

import pytest

from compiler.lexer import tokenize
from compiler.pipeline import run_source

ROOT = Path(__file__).resolve().parent.parent.parent
LEXER_KURO_PATH = ROOT / "self_host" / "lexer.kuro"
FIXTURES_DIR = ROOT / "bootstrap" / "python" / "tests"

_SOURCE_LINE_RE = re.compile(r'^Source = ".*";$', re.MULTILINE)


def kuro_escape(s: str) -> str:
    return (
        s.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
        .replace("\t", "\\t")
        .replace("\r", "\\r")
    )


def python_tokens(source: str) -> list[tuple[str, str]]:
    toks, diags = tokenize(source)
    assert not diags.diagnostics, diags.render_all()
    return [(t.kind.name, t.value) for t in toks if t.kind.name != "EOF"]


def kuro_tokens(source: str) -> list[tuple[str, str]]:
    template = LEXER_KURO_PATH.read_text(encoding="utf-8")
    new_line = f'Source = "{kuro_escape(source)}";'
    # NOTE: the replacement must be a function, not a string. re.subn()
    # reinterprets backslash escapes (\n, \1, \g<...>, ...) inside a string
    # replacement, which would silently turn the literal two-character
    # sequence "\n" this function just produced back into a real newline
    # and corrupt the generated single-line Source assignment. A callable
    # replacement's return value is used verbatim.
    generated, n = _SOURCE_LINE_RE.subn(lambda m: new_line, template, count=1)
    assert n == 1, "could not find the Source assignment line to substitute"

    result = run_source(generated, filename="<generated self_host/lexer.kuro>")
    assert result.ok, (
        result.compile.diags.render_all() if not result.compile.ok else result.runtime_error
    )
    lines = result.stdout.splitlines()
    assert len(lines) % 2 == 0, f"odd number of output lines: {lines!r}"
    return [(lines[i], lines[i + 1]) for i in range(0, len(lines), 2)]


PUNCTUATION_SNIPPET = "A = 1, 2.5; Print (A + B) - C * D / E. @X : Y."

FIXTURE_SNIPPETS = [p.read_text(encoding="utf-8") for p in sorted(FIXTURES_DIR.glob("*.kuro"))]

SNIPPETS = [PUNCTUATION_SNIPPET] + FIXTURE_SNIPPETS


@pytest.mark.parametrize("source", SNIPPETS, ids=[f"snippet{i}" for i in range(len(SNIPPETS))])
def test_self_hosted_lexer_matches_python_lexer_token_for_token(source):
    expected = python_tokens(source)
    actual = kuro_tokens(source)
    assert actual == expected


def test_cross_test_actually_exercises_every_token_kind():
    # guards against the harness silently producing an empty/degenerate
    # comparison for every snippet (a real risk with a substitution-based
    # harness like this one).
    seen_kinds = set()
    for source in SNIPPETS:
        for kind, _ in python_tokens(source):
            seen_kinds.add(kind)
    expected_kinds = {
        "STRING", "INTEGER", "DECIMAL", "IDENT", "EQUAL", "COMMA", "SEMI",
        "DOT", "LPAREN", "RPAREN", "AT", "PLUS", "MINUS", "STAR", "SLASH",
        "COLON",
    }
    missing = expected_kinds - seen_kinds
    assert not missing, f"no snippet exercises these token kinds: {missing}"
