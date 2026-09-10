"""Stage 7, Phases 27-28: adversarial semantic testing.

Unlike tests/self_host/test_parser_cross.py's malformed-input suite
(broken *syntax*, since the parser is the layer that must reject it),
self_host/resolver.kuro and self_host/typecheck.kuro only ever run on
input that already parsed successfully (ADR-0014's trust boundary) — so
"malformed" here means syntactically valid but structurally adversarial:
deep nesting, recursion, large collections, repeated reassignment,
mutually recursive/nested actions. The property under test is the same
one Stage 6 established: no crash, no hang — every case must terminate,
whether it ends up producing diagnostics or not.
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


def run_full_pipeline(source: str, max_while_iterations: int = 10_000_000):
    lexer_template = LEXER_KURO_PATH.read_text(encoding="utf-8")
    new_line = f'Source = "{kuro_escape(source)}";'
    lexer_body, n = _SOURCE_LINE_RE.subn(lambda m: new_line, lexer_template, count=1)
    assert n == 1

    parser_body = _body(PARSER_KURO_PATH, "BEGIN_STANDALONE_TOKENS", "END_STANDALONE_TOKENS", "parser")
    resolver_body = _body(RESOLVER_KURO_PATH, "BEGIN_STANDALONE", "END_STANDALONE", "resolver")
    typecheck_body = _body(TYPECHECK_KURO_PATH, "BEGIN_STANDALONE", "END_STANDALONE", "typecheck")

    generated = lexer_body + "\n" + parser_body + "\n" + resolver_body + "\n" + typecheck_body
    return run_source(generated, filename="<generated full pipeline>", max_while_iterations=max_while_iterations)


def get_diag_codes(result) -> list[str]:
    assert result.ok, (
        result.compile.diags.render_all() if not result.compile.ok else result.runtime_error
    )
    return result.interpreter.env.get("DiagCodes") or []


# --- deep nesting ----------------------------------------------------------

def test_deeply_nested_blocks_valid():
    depth = 25
    src = ""
    for i in range(depth):
        src += f"If {i} is equal to {i};\n"
    src += 'Print "center".\n'
    src += "Done.\n" * depth
    result = run_full_pipeline(src)
    assert get_diag_codes(result) == []


def test_deeply_nested_blocks_with_undefined_name_at_the_center():
    depth = 20
    src = ""
    for i in range(depth):
        src += f"If {i} is equal to {i};\n"
    src += "Print StillFindsThis.\n"
    src += "Done.\n" * depth
    result = run_full_pipeline(src)
    assert "E4001" in get_diag_codes(result)


def test_deeply_nested_expressions_valid():
    # (((...(1 + 1) + 1)...) + 1) - each source-level nesting level costs
    # several levels of the self-hosted walker's own Kuro-level call
    # depth (ParseAtom -> ParseExpr -> ParseTerm -> ParseFactor -> ...),
    # so this intentionally stays well under a depth that would trip
    # E6005 (see test_extremely_deep_recursion_is_a_controlled_error_
    # not_a_crash below, and its capacity-limitation note).
    depth = 15
    expr = "1"
    for _ in range(depth):
        expr = f"({expr} + 1)"
    src = f"N = {expr};\nPrint N."
    result = run_full_pipeline(src)
    assert get_diag_codes(result) == []


def test_deeply_nested_expressions_with_type_error():
    depth = 30
    expr = '"x"'
    for _ in range(depth):
        expr = f"({expr} + 1)"
    src = f"N = {expr};"
    result = run_full_pipeline(src)
    assert "E3011" in get_diag_codes(result)


# --- recursion ---------------------------------------------------------

def test_recursive_action_valid():
    src = (
        "Action Fact N;\n"
        "If N is less than or equal to 1;\n"
        "Return 1;\n"
        "Done.\n"
        "Call Fact N - 1;\n"
        "Return N * @_;\n"
        "Done.\n"
        "Call Fact 10;\nPrint @_."
    )
    result = run_full_pipeline(src)
    assert get_diag_codes(result) == []


def test_mutually_recursive_actions_valid():
    src = (
        "Action IsEven N;\n"
        "If N is equal to 0;\n"
        "Return 1;\n"
        "Done.\n"
        "Call IsOdd N - 1;\n"
        "Return @_;\n"
        "Done.\n"
        "Action IsOdd N;\n"
        "If N is equal to 0;\n"
        "Return 0;\n"
        "Done.\n"
        "Call IsEven N - 1;\n"
        "Return @_;\n"
        "Done.\n"
        "Call IsEven 4;\nPrint @_."
    )
    result = run_full_pipeline(src)
    assert get_diag_codes(result) == []


def test_nested_action_is_semantically_inert_and_does_not_crash():
    src = (
        "If 1 is equal to 1;\n"
        "Action Nested A;\n"
        "Return A;\n"
        "Done.\n"
        "Done.\n"
        "Print \"after\"."
    )
    result = run_full_pipeline(src)
    # Not crashing/hanging is the property under test; whether it's flagged
    # is Python's own established behavior (docs/architecture/
    # self-hosted-semantics.md §3b - it's inert, not an error by itself).
    assert get_diag_codes(result) == []


# --- large collections / repeated reassignment -------------------------

def test_large_collection_valid():
    # A comma-separated value list is walked by one tail-recursive Kuro
    # call per item (TCCheckValueList), so this also stays under the
    # interpreter's own call-depth guard - see the note on
    # test_deeply_nested_expressions_valid above.
    values = ", ".join(str(i) for i in range(80))
    src = f"Numbers = {values};\nPrint Numbers."
    result = run_full_pipeline(src)
    assert get_diag_codes(result) == []


def test_many_repeated_reassignments_valid():
    src = "N is Integers;\n" + "\n".join(f"N = {i};" for i in range(100)) + "\nPrint N."
    result = run_full_pipeline(src)
    assert get_diag_codes(result) == []


def test_many_top_level_statements_no_hang():
    lines = []
    for i in range(150):
        lines.append(f"V{i} = {i};")
    lines.append("Print V0.")
    src = "\n".join(lines)
    result = run_full_pipeline(src)
    assert get_diag_codes(result) == []


# --- pathological depth: must fail in a controlled way, not crash ------

def test_extremely_deep_recursion_is_a_controlled_error_not_a_crash():
    # Self_host/typecheck.kuro's expression walker is itself recursive
    # (tail recursion through the interpreter's own call stack), so a
    # pathologically deep expression can hit the interpreter's own
    # recursion guard (E6005) even though Python's oracle - a real
    # recursive-descent process, not reprocessed through an interpreted
    # call-stack guard - handles much deeper nesting without issue. This
    # is a real, documented difference in practical capacity, not a
    # correctness bug: the property under test is that it fails cleanly
    # (a structured runtime error) rather than hanging or crashing with
    # an unhandled Python exception.
    depth = 400
    expr = "1"
    for _ in range(depth):
        expr = f"({expr} + 1)"
    src = f"N = {expr};"
    result = run_full_pipeline(src)
    assert not result.ok
    assert result.runtime_error is not None
    assert result.runtime_error.code == "E6005"
