"""Stage 7 differential test, pass 1 only: self_host/resolver.kuro's
top-level collection (Decl/Assign-literal-inference/Action registration)
compared against compiler/resolver.py's `_collect_globals` — the same
logic, via `compiler/pipeline.py::compile_source`'s `symbols` result.

Pass 2 (usage/type checking) lives in self_host/typecheck.kuro and is
compared in tests/self_host/test_typecheck_cross.py — see ADR-0014 for why
these are two Kuro-side files (mirroring compiler/resolver.py's own two
internal passes) even though pass 2 there is combined with type checking.

Comparison is sorted/order-independent (ADR-0014, compiler/
semantic_canon.py's docstring): only the *set* of collected symbols/
actions and the *set* of (code, line, col) diagnostics need to match.
"""
import re
from pathlib import Path

import pytest

from compiler.pipeline import compile_source, run_source

ROOT = Path(__file__).resolve().parent.parent.parent
LEXER_KURO_PATH = ROOT / "self_host" / "lexer.kuro"
PARSER_KURO_PATH = ROOT / "self_host" / "parser.kuro"
RESOLVER_KURO_PATH = ROOT / "self_host" / "resolver.kuro"

_SOURCE_LINE_RE = re.compile(r'^Source = ".*";$', re.MULTILINE)


def _strip_marked_block(text: str, begin: str, end: str) -> str:
    pat = re.compile(rf"^# --- {begin}.*?^# --- {end}.*?$\n?", re.MULTILINE | re.DOTALL)
    stripped, n = pat.subn("", text, count=1)
    assert n == 1, f"marker pair {begin}/{end} not found"
    return stripped


def kuro_escape(s: str) -> str:
    return (
        s.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
        .replace("\t", "\\t")
        .replace("\r", "\\r")
    )


_parser_body_cache: str | None = None
_resolver_body_cache: str | None = None


def _parser_body() -> str:
    global _parser_body_cache
    if _parser_body_cache is None:
        raw = PARSER_KURO_PATH.read_text(encoding="utf-8")
        _parser_body_cache = _strip_marked_block(raw, "BEGIN_STANDALONE_TOKENS", "END_STANDALONE_TOKENS")
    return _parser_body_cache


def _resolver_body() -> str:
    global _resolver_body_cache
    if _resolver_body_cache is None:
        raw = RESOLVER_KURO_PATH.read_text(encoding="utf-8")
        _resolver_body_cache = _strip_marked_block(raw, "BEGIN_STANDALONE", "END_STANDALONE")
    return _resolver_body_cache


def kuro_pass1(source: str):
    lexer_template = LEXER_KURO_PATH.read_text(encoding="utf-8")
    new_line = f'Source = "{kuro_escape(source)}";'
    lexer_body, n = _SOURCE_LINE_RE.subn(lambda m: new_line, lexer_template, count=1)
    assert n == 1

    generated = lexer_body + "\n" + _parser_body() + "\n" + _resolver_body()
    result = run_source(generated, filename="<generated lexer+parser+resolver>")
    assert result.ok, (
        result.compile.diags.render_all() if not result.compile.ok else result.runtime_error
    )
    env = result.interpreter.env
    sym_names = (env.get("SymNames") or [""])[1:]  # drop the sentinel row
    sym_types = (env.get("SymTypes") or [""])[1:]
    action_names = (env.get("ActionNames") or [""])[1:]
    action_arity = (env.get("ActionArity") or [-1])[1:]
    codes = env.get("DiagCodes") or []
    lines = env.get("DiagLines") or []
    cols = env.get("DiagCols") or []
    return {
        "symbols": sorted(zip(sym_names, sym_types)),
        "actions": sorted(zip(action_names, action_arity)),
        "diagnostics": sorted(zip(codes, lines, cols)),
    }


def python_pass1(source: str):
    # Isolates compiler/resolver.py's pass 1 (_collect_globals) alone -
    # compile_source() runs the *whole* pipeline (pass 1, pass 2, typecheck,
    # lower), whose diagnostics/symbols include things pass 2 alone adds
    # (e.g. a Compare statement's result variable, or a usage-level E4001)
    # that self_host/resolver.kuro (pass 1 only - see ADR-0014) never
    # produces. Comparing against the full pipeline's result would be
    # comparing two different scopes of work, not validating pass 1.
    from compiler.diagnostics import DiagnosticEngine
    from compiler.lexer import tokenize
    from compiler.parser import parse
    from compiler.resolver import Resolver

    toks, diags = tokenize(source)
    program = parse(toks, diags)
    if diags.has_errors():
        return {"symbols": [], "actions": [], "diagnostics": sorted(
            (d.code, d.span.line, d.span.col) for d in diags.diagnostics
        )}
    resolver = Resolver(program, diags)
    resolver._collect_globals()
    return {
        "symbols": sorted(resolver.symbols.types.items()),
        "actions": sorted((n, sig.arity) for n, sig in resolver.symbols.actions.items()),
        "diagnostics": sorted((d.code, d.span.line, d.span.col) for d in diags.diagnostics),
    }


SNIPPETS = [
    # Deliberately no empty-string case: a truly empty Source never causes
    # self_host/lexer.kuro's TokenKinds to be Appended to at all, so it has
    # no runtime env entry (Decl-only lists get one only on first Append -
    # see self_host/resolver.kuro's sentinel-seeding comment). This is the
    # same pre-existing, already-documented limitation the Stage 5/6 cross-
    # tests also avoid (ADR-0011: "None of the fixtures contain... empty
    # source"), not a new gap introduced here.
    'Name = "Kuro";\nPrint Name.',
    "Age is Integers;\nAge = 25;",
    "Score = 5, 10;",
    'Names = "A", "B", "C";',
    "Mixed = 1, \"x\";",          # mixed literal kinds - no inference
    "Weird = 1 + 2;",              # non-literal value - no inference
    "Typed : Decimals = 5;",
    "Age is Integers;\nAge is Text;",           # duplicate decl -> E4002
    "Name is Number;",                            # unknown type -> E3003
    "Action Add A, B;\nReturn A + B;\nDone.",
    "Action Add A;\nReturn A;\nDone.\nAction Add B;\nReturn B;\nDone.",  # duplicate action
    "Action Add(A, B);\nReturn A + B;\nDone.",   # legacy parens
    # nested Decl/Action are semantically inert at the TOP-LEVEL pass -
    # they must NOT be collected (docs/architecture/self-hosted-semantics.md §3a/3b)
    "If 1 is equal to 1;\nAge is Integers;\nDone.",
    "If 1 is equal to 1;\nAction Nested A;\nReturn A;\nDone.\nDone.",
    # a normal program exercising many statement kinds at once, to prove
    # pass 1 correctly skips all of them without misinterpreting internals
    (
        'Name is Text;\nName = "Kuro";\n'
        "Repeat 3;\nPrint Index.\nDone.\n"
        "N is Integers;\nN = 0;\nWhile N is less than 3;\nAdd 1 to N;\nDone.\n"
        "Take user Age;\nGet Name;\nLength Name;\n"
        'Set Name 0 to "k";\nAppend "x" to Name;\n'
        "Compare R N greater than 0;\n"
        'Entered N is greater than 0 then Print "yes" otherwise Print "no";\n'
        "Action Helper X;\nReturn X;\nDone.\nCall Helper 1;"
    ),
]


@pytest.mark.parametrize("source", SNIPPETS, ids=[f"snippet{i}" for i in range(len(SNIPPETS))])
def test_self_hosted_resolver_pass1_matches_python(source):
    assert kuro_pass1(source) == python_pass1(source)
