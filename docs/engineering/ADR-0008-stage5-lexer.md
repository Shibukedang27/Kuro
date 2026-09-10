# ADR-0008: Stage 5 self-hosted lexer — approach, scope, and what it deliberately skips

## Problem

Spec section 61 sets "a real Kuro lexer written in Kuro, tested against the
Python lexer" as this project's first self-hosting milestone. Three
sub-problems had to be solved with the language as it actually exists
today (see `docs/architecture/current-state.md`, plus ADR-0004/0005/0006's
additions), not the language as some future spec might wish it to be:

1. **How does a Kuro program receive the text it's supposed to tokenize?**
   There is no file I/O in the language yet (honestly not built — spec
   section 55).
2. **How does a Kuro program report a stream of tokens observably, so a
   test harness can check it?** There's no structured return value from
   top-level code, only `Print`.
3. **How does a hand-written recursive-descent-style scan even work
   without `while`/`break`?** `Repeat` only takes a fixed iteration count
   decided up front, with no early exit.

## Decisions

1. **Input**: `self_host/lexer.kuro` reads from a single `Text` variable,
   `Source`, assigned once near the top of the file. There is no `Take`
   (stdin) or file read involved. `tests/self_host/test_lexer_cross.py`
   treats the file as a template and substitutes real source text into
   that one line for each test case (see its module docstring for exactly
   how). This is a test-harness technique, not a language feature; it does
   not pretend Kuro has file I/O.
2. **Output protocol**: for each token, the lexer prints exactly two
   lines — the token kind name (`"IDENT"`, `"INTEGER"`, ...) then the raw
   token text — deliberately mirroring `compiler/tokens.py`'s `TokKind`
   names so cross-comparison is a straight list-of-pairs equality check.
   Source locations (line/col) are not printed: doing so would need
   integer-to-text conversion, which does not exist in the language (see
   ADR-0004's consequences) and was out of scope for this milestone.
3. **No `while`/`break`**: every unbounded-looking scan (an identifier run,
   a number, a quoted string, a comment) is written as a `Repeat`
   bounded by `SourceLen` (a safe upper bound on remaining input) guarded
   by an explicit integer flag (`XScanning = 1` / `= 0`) checked at the
   top of each iteration — the standard "simulate `while` with a bounded
   loop plus a guard flag" pattern for languages without early exit. This
   makes the lexer correct but **not** efficient: it is roughly
   O(n²) in the length of the input, because a loop that has already
   "logically" stopped (flag = 0) still burns its remaining bounded
   iterations doing nothing. A `break`/early-exit primitive would fix this
   cleanly and is real future work, not added speculatively here (spec
   section 55).

## What this milestone does and does not prove

**Proven** (`tests/self_host/test_lexer_cross.py`, 23 passing cases): the
Kuro program in `self_host/lexer.kuro`, executed by `compiler/`'s own
interpreter, tokenizes 21 real `.kuro` fixtures from this repository plus a
hand-written all-punctuation-kinds snippet identically —
token kind and token text, in order — to `compiler/lexer.py`, across every
`TokKind` except `EOF` (`test_cross_test_actually_exercises_every_token_kind`
asserts the fixture set actually exercises all sixteen).

**Not proven, and not claimed**: this is not a native compiler compiling
itself (Stage 8); it still runs entirely on the Stage 1-4 Python
interpreter. It has no error recovery or diagnostics of its own (a
character it can't classify is silently skipped, not reported — unlike
`compiler/lexer.py`'s E1xxx diagnostics). It doesn't track source
locations. It doesn't replicate the Unicode combining-mark identifier rule
from ADR-0003 (plain `is alpha`/`is alnum` only). None of these are silently
missing — each is named in `self_host/lexer.kuro`'s header comment and here,
per spec section 55 ("if something is incomplete, represent it explicitly").

## Consequences

- The next self-hosting milestone (Stage 6, a Kuro-in-Kuro parser) will hit
  the same missing-`break` problem harder — a recursive-descent parser
  does much more "scan until a condition, then stop" work than a lexer.
  Whether to add a real early-exit/`while` primitive before attempting
  Stage 6, versus continuing the bounded-loop-plus-flag pattern, is an open
  question for whoever picks up that stage next, not decided by this ADR.
- If the language later adds integer-to-text conversion (for building
  formatted output generally, not just for this), the location-tracking
  gap here becomes cheap to close as a follow-up.
