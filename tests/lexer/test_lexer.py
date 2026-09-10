"""Lexer unit tests (spec Stage 5 requirement list, section 61):
strings, numbers, identifiers, keywords, punctuation, operators,
whitespace, comments, source locations, EOF, invalid characters, unicode."""
from compiler.lexer import tokenize
from compiler.tokens import TokKind


def kinds(src):
    toks, _ = tokenize(src)
    return [t.kind for t in toks]


def test_empty_source_is_just_eof():
    toks, diags = tokenize("")
    assert [t.kind for t in toks] == [TokKind.EOF]
    assert not diags.diagnostics


def test_string_literal():
    toks, diags = tokenize('"hello"')
    assert not diags.diagnostics
    assert toks[0].kind is TokKind.STRING
    assert toks[0].value == "hello"


def test_string_escapes():
    toks, diags = tokenize(r'"a\nb\tc\"d\\e"')
    assert not diags.diagnostics
    assert toks[0].value == 'a\nb\tc"d\\e'


def test_unterminated_string_recovers_with_diagnostic():
    toks, diags = tokenize('"abc')
    assert diags.has_errors()
    assert diags.diagnostics[0].code == "E1001"
    assert toks[0].kind is TokKind.STRING  # recovered as a token anyway


def test_integer_literal():
    toks, diags = tokenize("42")
    assert not diags.diagnostics
    assert toks[0].kind is TokKind.INTEGER
    assert toks[0].value == "42"


def test_decimal_literal():
    toks, diags = tokenize("3.14")
    assert not diags.diagnostics
    assert toks[0].kind is TokKind.DECIMAL
    assert toks[0].value == "3.14"


def test_trailing_dot_is_not_absorbed_into_the_number():
    # '.' is also the Print-statement terminator; a digit run followed by a
    # '.' that is NOT itself followed by a digit must not be swallowed into
    # the number, or `Print 10 / 2.` could never find its terminator.
    toks, diags = tokenize("2.")
    assert not diags.diagnostics
    assert toks[0].kind is TokKind.INTEGER and toks[0].value == "2"
    assert toks[1].kind is TokKind.DOT


def test_two_dotted_numbers_back_to_back_tokenize_cleanly():
    toks, diags = tokenize("3.4.5")
    assert not diags.diagnostics
    assert [ (t.kind, t.value) for t in toks[:3] ] == [
        (TokKind.DECIMAL, "3.4"), (TokKind.DOT, "."), (TokKind.INTEGER, "5"),
    ]


def test_identifier_and_keyword_like_words_are_both_IDENT():
    toks, diags = tokenize("Print Age")
    assert not diags.diagnostics
    assert toks[0].kind is TokKind.IDENT and toks[0].value == "Print"
    assert toks[1].kind is TokKind.IDENT and toks[1].value == "Age"


def test_identifier_with_underscore_and_digits():
    toks, _ = tokenize("_a1_b2")
    assert toks[0].kind is TokKind.IDENT
    assert toks[0].value == "_a1_b2"


def test_punctuation():
    toks, diags = tokenize("=,;.()@+-*/:")
    assert not diags.diagnostics
    expected = [
        TokKind.EQUAL, TokKind.COMMA, TokKind.SEMI, TokKind.DOT,
        TokKind.LPAREN, TokKind.RPAREN, TokKind.AT, TokKind.PLUS,
        TokKind.MINUS, TokKind.STAR, TokKind.SLASH, TokKind.COLON,
        TokKind.EOF,
    ]
    assert [t.kind for t in toks] == expected


def test_whitespace_is_skipped():
    toks, _ = tokenize("  Print   \t  Age  ")
    assert [t.kind for t in toks] == [TokKind.IDENT, TokKind.IDENT, TokKind.EOF]


def test_hash_comment_stripped():
    toks, diags = tokenize('Print "x". # a comment')
    assert not diags.diagnostics
    assert toks[-1].kind is TokKind.EOF
    assert not any(t.kind is TokKind.IDENT and "comment" in t.value for t in toks)


def test_slash_slash_comment_stripped():
    toks, diags = tokenize('Print "x". // a comment')
    assert not diags.diagnostics


def test_hash_inside_string_is_not_a_comment():
    toks, diags = tokenize('Print "a#b".')
    assert not diags.diagnostics
    assert toks[1].value == "a#b"


def test_unexpected_character_reports_and_recovers():
    toks, diags = tokenize("Age $ Name")
    assert diags.has_errors()
    assert diags.diagnostics[0].code == "E1002"
    # lexing continued past the bad character
    assert [t.kind for t in toks] == [TokKind.IDENT, TokKind.IDENT, TokKind.EOF]


def test_source_locations_are_correct():
    toks, _ = tokenize("Name = 1;\n  Print Name.")
    name_tok = toks[0]
    assert (name_tok.line, name_tok.col) == (1, 1)
    print_tok = toks[4]
    assert print_tok.value == "Print"
    assert (print_tok.line, print_tok.col) == (2, 3)


def test_eof_token_present_and_last():
    toks, _ = tokenize("Name = 1;")
    assert toks[-1].kind is TokKind.EOF


def test_unicode_identifier():
    toks, diags = tokenize("Nämé = 1;")
    assert not diags.diagnostics
    assert toks[0].kind is TokKind.IDENT
    assert toks[0].value == "Nämé"


def test_unicode_devanagari_identifier():
    toks, diags = tokenize("नाम = 1;")
    assert not diags.diagnostics
    assert toks[0].value == "नाम"


def test_unicode_string_content():
    toks, diags = tokenize('Print "héllo wörld 日本語".')
    assert not diags.diagnostics
    assert toks[1].value == "héllo wörld 日本語"


def test_multiple_errors_reported_in_one_pass():
    toks, diags = tokenize('Age $ Name;\n"unterminated\nMore % text')
    codes = [d.code for d in diags.diagnostics]
    assert codes.count("E1002") == 2
    assert "E1001" in codes
