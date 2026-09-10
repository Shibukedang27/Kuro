"""Stage 7 differential test, pass 2: self_host/typecheck.kuro (combined
resolution + type checking, per ADR-0014) compared against
compiler/resolver.py + compiler/typecheck.py's FULL result, via
compiler/semantic_canon.py's order-independent canonical form.

Symbols/actions comparisons include everything BOTH passes contribute
(e.g. a Compare statement's result variable, added during usage
checking) - unlike tests/self_host/test_resolver_cross.py, which
deliberately isolates pass 1 alone.
"""
import re
from pathlib import Path

import pytest

from compiler.pipeline import compile_source, run_source
from compiler.semantic_canon import canon_semantic

ROOT = Path(__file__).resolve().parent.parent.parent
LEXER_KURO_PATH = ROOT / "self_host" / "lexer.kuro"
PARSER_KURO_PATH = ROOT / "self_host" / "parser.kuro"
RESOLVER_KURO_PATH = ROOT / "self_host" / "resolver.kuro"
TYPECHECK_KURO_PATH = ROOT / "self_host" / "typecheck.kuro"

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


_cache: dict[str, str] = {}


def _body(path: Path, begin: str, end: str, key: str) -> str:
    if key not in _cache:
        _cache[key] = _strip_marked_block(path.read_text(encoding="utf-8"), begin, end)
    return _cache[key]


def kuro_semantic(source: str):
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
    env = result.interpreter.env
    sym_names = (env.get("SymNames") or [""])[1:]
    sym_types = (env.get("SymTypes") or [""])[1:]
    action_names = (env.get("ActionNames") or [""])[1:]
    action_arity = (env.get("ActionArity") or [-1])[1:]
    codes = env.get("DiagCodes") or []
    lines = env.get("DiagLines") or []
    # self_host/typecheck.kuro's SymNames/SymTypes conflates two things
    # Python keeps separate: Scope.names (definedness - a nested Assign's
    # name goes here even with no type) and SymbolTable.types (only ever
    # populated by pass 1 / _collect_globals - a nested Assign's name
    # never appears there at all, even a typed one, verified directly
    # against compiler/resolver.py). An empty-type entry here therefore
    # represents "defined but Python never records a type for it either" -
    # excluded from the symbols comparison since python_semantic()'s
    # symbols.types can never contain such an entry to compare against.
    typed_symbols = [(n, t) for n, t in zip(sym_names, sym_types) if t != ""]
    return {
        "symbols": sorted(typed_symbols),
        "actions": sorted(zip(action_names, action_arity)),
        "diagnostics": sorted(zip(codes, lines)),
    }


def python_semantic(source: str):
    r = compile_source(source)
    c = canon_semantic(r.symbols, r.diags)
    return {
        "symbols": sorted(c["symbols"]),
        "actions": sorted(c["actions"]),
        "diagnostics": sorted((code, line) for code, line, col in c["diagnostics"]),
    }


VALID_SNIPPETS = [
    'Name = "Kuro";\nPrint Name.',
    "Age is Integers;\nAge = 25;\nPrint Age.",
    "Score = 5, 10;\nPrint Score.",
    'Names = "A", "B", "C";\nGet Names 1;',
    "N is Integers;\nN = 0;\nAdd 1 to N;\nPrint N.",
    "N is Integers;\nN = 5;\nUpdate N to 10;\nPrint N.",
    'Name is Text;\nName = "Kuro";\nLength Name;\nPrint @_.',
    'Name is Text;\nName = "Kuro";\nSet Name 0 to "k";',
    'Tokens = "a";\nAppend "b" to Tokens;',
    "A = 5;\nCompare Bigger A greater than 3;\nPrint Bigger.",
    "Repeat 3;\nPrint Index.\nDone.",
    "Repeat 2;\nRepeat 3;\nPrint Index.\nDone.\nDone.",
    "N is Integers;\nN = 0;\nWhile N is less than 3;\nAdd 1 to N;\nDone.\nPrint N.",
    "Action Add A, B;\nReturn A + B;\nDone.\nCall Add 3, 4;\nPrint @_.",
    "Action Add A: Integers, B: Integers;\nReturn A + B;\nDone.\nCall Add 1, 2;",
    "Action Fact N;\nIf N is less than or equal to 1;\nReturn 1;\nDone.\nCall Fact N - 1;\nReturn N * @_;\nDone.\nCall Fact 5;\nPrint @_.",
    'Age is Integers;\nAge = 25;\nIf Age is greater than 20;\nPrint "Old".\nElse;\nPrint "Young".\nDone.',
    "N is Integers;\nN = 5;\nIf N is greater than 1 and N is less than 10;\nPrint N.\nDone.",
    'C = "5";\nIf C is digit;\nPrint "yes".\nDone.',
    'Age is Integers;\nAge = 25;\nEntered Age is greater than 20 then Print "Old" otherwise Print "Young";',
    "Age is Integers;\nTake user Age;\nPrint Age.",
    # a variable first assigned inside a Repeat/While/Action, read after -
    # the exact pattern that broke the resolver twice before (ADR-0012)
    "Repeat 3;\nX = Index;\nDone.\nPrint X.",
    "N is Integers;\nN = 0;\nWhile N is less than 3;\nY = N;\nAdd 1 to N;\nDone.\nPrint Y.",
    "Action A;\nZ = 1;\nReturn Z;\nDone.\nCall A;\nPrint Z.",
    "Action First;\nShared = 5;\nReturn Shared;\nDone.\nAction Second;\nReturn Shared;\nDone.\nCall First;\nCall Second;",
    'N = "a" + "b";\nPrint N.',
]

INVALID_SNIPPETS = [
    "Print Missing.",                                           # E4001
    "Age is Integers;\nAge is Text;",                            # E4002
    "Name is Number;",                                            # E3003
    "Repeat 3;\nPrint Index.\nDone.\nPrint Index.",              # E4001 (Index leaks past its own Repeat)
    "Action A Local;\nReturn Local;\nDone.\nPrint Local.",       # E4001 (param leaks past Action)
    "Action Add A, B;\nReturn A + B;\nDone.\nCall Add 1;",       # E4004
    "Call Missing 1;",                                            # E4003
    "Return 1;",                                                  # E4005
    'Age is Integers;\nAge = "hello";',                          # E3001
    'Name is Text;\nName = "hi";\nAdd 1 to Name;',              # E3002
    'N is Text;\nN = "x";\nIf N is greater than 5;\nPrint N.\nDone.',  # E3006
    'Action Add A: Integers, B: Integers;\nReturn A + B;\nDone.\nCall Add "x", "y";',  # E3007
    'Repeat "three";\nPrint Index.\nDone.',                      # E3008
    "N is Integers;\nN = 5;\nLength N;",                          # E3009
    'Names = "A", "B";\nGet Names "x";',                          # E3010
    'N = "a" + 5;',                                               # E3011
    'N is Text;\nN = "abc";\nSet N 0 to "kk";',                  # E3004
    "Take user Age;",                                             # E4001 (Take on undeclared name)
]


@pytest.mark.parametrize("source", VALID_SNIPPETS, ids=[f"valid{i}" for i in range(len(VALID_SNIPPETS))])
def test_valid_programs_match(source):
    assert kuro_semantic(source) == python_semantic(source)


@pytest.mark.parametrize("source", INVALID_SNIPPETS, ids=[f"invalid{i}" for i in range(len(INVALID_SNIPPETS))])
def test_invalid_programs_match(source):
    assert kuro_semantic(source) == python_semantic(source)
