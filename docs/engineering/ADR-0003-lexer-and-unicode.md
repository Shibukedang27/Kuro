# ADR-0003: Lexer stays line-oriented; identifiers are Unicode-aware with combining-mark continuation

## Problem

Two lexical questions had no prior specification: (1) should strings/comments
be allowed to span multiple lines, and (2) what counts as a valid identifier
character outside ASCII.

## Decision

1. Strings and comments remain line-bound, matching `kuro.py`'s behavior
   (`compiler/lexer.py` tokenizes one physical line at a time). Not changed
   this session.
2. Identifiers: `(alpha | '_') (alnum | '_' | combining-mark)*`, using
   Python's Unicode-aware `str.isalpha()`/`str.isalnum()` for the letter
   classes, plus `unicodedata.category(c) in ('Mn', 'Mc')` for the
   continuation set so a composed character like a Devanagari matra
   (e.g. "नाम") lexes as one identifier instead of splitting at the first
   combining vowel sign.

## Reasoning

- Multi-line strings/comments are a real grammar change (they'd need a
  paired delimiter, not just "read to end of line"), not a bugfix — so it
  was deliberately left alone rather than silently extended.
- Plain `isalnum()` continuation rejects valid identifiers in scripts that
  rely on combining marks (Devanagari, many Indic scripts, some Latin
  diacritics typed as base+combining rather than precomposed). Testing this
  directly (`tests/lexer/test_lexer.py::test_unicode_devanagari_identifier`)
  caught the gap — the naive `isalpha()`-only rule silently truncated the
  identifier one codepoint in, which the spec's "test Unicode behavior
  deliberately" requirement (section 61) exists specifically to catch.

## Consequences

- Source files must be valid UTF-8; there is no other declared source
  encoding.
- A future formal lexical grammar (`docs/spec/`) should cite Unicode
  Standard Annex #31 categories (ID_Start/ID_Continue) explicitly instead of
  this ADR's informal `Mn`/`Mc` shorthand, once the spec document exists.
