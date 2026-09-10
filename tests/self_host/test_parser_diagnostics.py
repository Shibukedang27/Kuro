"""Stage 6 completion, Phase 6/8: tests for self_host/parser.kuro's
structured diagnostics (DiagCodes/DiagLines/DiagCols/DiagMessages).

Diagnostic *compatibility policy* (ADR-0011): this suite does not assert
that self_host/parser.kuro's message text matches compiler/parser.py's
wording. It asserts the things spec section 18's diagnostic model actually
promises and that are meaningful to compare across two independent
implementations: error *code* (reusing compiler/diagnostics.py's existing
E2xxx registry, not a second taxonomy), and *source location*
(line/column, computed from the token stream's recorded character offsets
— see self_host/lexer.kuro's TokenStarts and self_host/parser.kuro's
ComputeLineCol). A message is still required to be present and
non-empty — "basic message" per the task's Phase 6 bar — just not
byte-identical to Python's.
"""
import re
from pathlib import Path

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


def parse_and_get_diagnostics(source: str):
    lexer_template = LEXER_KURO_PATH.read_text(encoding="utf-8")
    new_line = f'Source = "{kuro_escape(source)}";'
    lexer_body, n = _SOURCE_LINE_RE.subn(lambda m: new_line, lexer_template, count=1)
    assert n == 1

    parser_raw = PARSER_KURO_PATH.read_text(encoding="utf-8")
    parser_body, n2 = _STANDALONE_TOKENS_RE.subn("", parser_raw, count=1)
    assert n2 == 1

    generated = lexer_body + "\n" + parser_body
    result = run_source(generated, filename="<generated lexer+parser>")
    assert result.ok, (
        result.compile.diags.render_all() if not result.compile.ok else result.runtime_error
    )
    env = result.interpreter.env
    codes = env.get("DiagCodes") or []
    lines = env.get("DiagLines") or []
    cols = env.get("DiagCols") or []
    messages = env.get("DiagMessages") or []
    parse_failed = env.get("ParseFailed", 0)
    # Every diagnostic-producing site appends to all four lists together
    # (RecordDiag), so they must always stay the same length.
    assert len(codes) == len(lines) == len(cols) == len(messages)
    return {
        "parse_failed": parse_failed,
        "codes": codes,
        "lines": lines,
        "cols": cols,
        "messages": messages,
    }


# --- valid input: no diagnostics at all ----------------------------------

def test_valid_input_produces_no_diagnostics():
    d = parse_and_get_diagnostics('Name = "Kuro";\nPrint Name.')
    assert d["parse_failed"] == 0
    assert d["codes"] == []


# --- minimum categories the task requires --------------------------------

def test_unknown_token_category():
    d = parse_and_get_diagnostics("Frobnicate Name;")
    assert d["parse_failed"] == 1
    assert "E2001" in d["codes"]


def test_unexpected_token_category():
    d = parse_and_get_diagnostics("N = * 5;")
    assert d["parse_failed"] == 1
    assert "E2003" in d["codes"]  # expected a value, found '*'


def test_missing_token_category():
    d = parse_and_get_diagnostics('Name = "Kuro"\nPrint Name.')
    assert d["parse_failed"] == 1
    assert "E2002" in d["codes"]  # missing ';'


def test_unexpected_eof_category():
    d = parse_and_get_diagnostics("Print")
    assert d["parse_failed"] == 1
    assert len(d["codes"]) >= 1
    # the diagnostic must point somewhere sane, not crash computing a
    # location for a position past the end of the source.
    assert d["lines"][0] >= 1 and d["cols"][0] >= 1


def test_malformed_expression_category():
    d = parse_and_get_diagnostics("N = 1 +")
    assert d["parse_failed"] == 1
    assert "E2003" in d["codes"]


def test_malformed_statement_category():
    d = parse_and_get_diagnostics("Bogus;")
    assert d["parse_failed"] == 1
    assert "E2001" in d["codes"]


def test_malformed_block_category():
    d = parse_and_get_diagnostics("Repeat 3;\nPrint Index.")  # missing Done.
    assert d["parse_failed"] == 1
    assert "E2002" in d["codes"]


# --- every diagnostic has a non-empty basic message ----------------------

def test_every_diagnostic_has_a_message():
    d = parse_and_get_diagnostics("If Age is greater than 20\nPrint Age.")
    assert d["codes"]
    for msg in d["messages"]:
        assert isinstance(msg, str) and len(msg) > 0


# --- source locations correspond to the actual source (task explicitly
# asks to verify line 1, line 2, line 5, etc.) -----------------------------

def test_source_location_line_1():
    d = parse_and_get_diagnostics("Bogus;")
    assert d["lines"][0] == 1


def test_source_location_line_2():
    d = parse_and_get_diagnostics('Name = "Kuro";\nBogus;')
    assert d["lines"][0] == 2


def test_source_location_line_5():
    src = "Name is Text;\nName = \"Kuro\";\nPrint Name.\nAge is Integers;\nBogus;"
    d = parse_and_get_diagnostics(src)
    assert d["lines"][0] == 5


def test_source_location_column_matches_token_start():
    # "    Bogus;" - the bad token starts at column 5 (four spaces then B).
    d = parse_and_get_diagnostics("    Bogus;")
    assert d["lines"][0] == 1
    assert d["cols"][0] == 5


def test_source_location_after_multiple_lines_and_columns():
    src = 'Action Add A, B;\nReturn A + B;\nDone.\n    Bogus;'
    d = parse_and_get_diagnostics(src)
    assert d["lines"][0] == 4
    assert d["cols"][0] == 5


# --- diagnostic codes reuse the existing Python registry, not a second
# taxonomy (Phase 6: "do not create a completely separate error taxonomy") -

def test_diagnostic_codes_are_from_the_existing_e2xxx_family():
    from compiler.diagnostics import REGISTRY

    samples = [
        parse_and_get_diagnostics("Bogus;"),
        parse_and_get_diagnostics("N = * 5;"),
        parse_and_get_diagnostics('Name = "Kuro"\nPrint Name.'),
        parse_and_get_diagnostics("Compare Bigger A greater"),
    ]
    for d in samples:
        for code in d["codes"]:
            assert code in REGISTRY, f"{code} is not in compiler/diagnostics.py's registry"
            assert code.startswith("E2"), f"{code} is not a parser-family code"
