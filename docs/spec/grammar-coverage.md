# Kuro Grammar Coverage Matrix

Stage 6 completion audit (this document is the Phase 1 deliverable that
gated implementation work — see
[ADR-0010](../engineering/ADR-0010-stage6-parser.md) and
[ADR-0011](../engineering/ADR-0011-stage6-completion.md)). It is also the
first real content in `docs/spec/` (spec section 39); a full formal
lexical/grammar specification is still future work — this document
captures *coverage*, not the grammar's prose definition.

## Method

Every statement kind in `compiler/ast_nodes.py` was checked against every
phase that should recognize it, by grepping each phase's `isinstance`/`op
==` dispatch (`compiler/resolver.py`, `compiler/typecheck.py`,
`compiler/lower.py`, `compiler/interpreter.py`, `compiler/ast_canon.py`)
and cross-referencing `self_host/parser.kuro`'s own keyword dispatch and
`tests/self_host/test_parser_cross.py`'s snippet corpus by hand.

## Coverage matrix (before this session's work)

| Statement | Python parser | Resolver | Typecheck | Lower/IR | Interpreter | Canon AST | Self-hosted parser | Self-hosted test coverage |
|---|---|---|---|---|---|---|---|---|
| `Decl` | yes | yes | yes | yes | yes | yes | yes | yes |
| `Assign` (typed/untyped) | yes | yes | yes | yes | yes | yes | yes | yes |
| `Input` (`Take`) | yes | yes | n/a¹ | yes | yes | yes | **no** | **no** |
| `AddStmt` | yes | yes | yes | yes | yes | yes | yes | yes |
| `UpdateStmt` | yes | yes | n/a¹ | yes | yes | yes | yes | yes |
| `PrintStmt` | yes | yes | n/a¹ | yes | yes | yes | yes | yes |
| `GetStmt` | yes | yes | n/a¹ | yes | yes | yes | **no** | **no** |
| `LengthStmt` | yes | yes | n/a¹ | yes | yes | yes | **no** | **no** |
| `SetStmt` | yes | yes | yes | yes | yes | yes | **no** | **no** |
| `AppendStmt` | yes | yes | n/a¹ | yes | yes | yes | **no** | **no** |
| `CompareStmt` | yes | yes | n/a¹ | yes | yes | yes | **no** | **no** |
| `IfStmt` | yes | yes | n/a² | yes | yes | yes | yes | yes |
| `RepeatStmt` | yes | yes | n/a² | yes | yes | yes | yes | yes |
| `WhileStmt` | yes | yes | n/a² | yes | yes | yes | yes | yes |
| `ActionDecl` | yes | yes | n/a² | yes | yes | yes | yes | yes |
| `ReturnStmt` | yes | yes | n/a¹ | yes | yes | yes | yes | yes |
| `CallStmt` | yes | yes | n/a¹ | yes | yes | yes | yes | yes |
| legacy `Entered ... then ... otherwise ...;` | yes (desugars to `IfStmt`) | yes (same) | n/a² | yes (same) | yes (same) | yes (same, no special case needed) | **no** | **no** |

¹ `typecheck.py` only implements type-specific checks for `Assign`/
`AddStmt`/`SetStmt` (the only statements where a static type mismatch is a
meaningful concept given Kuro's current type system); every other
statement is intentionally not special-cased there — this is complete by
design, not a gap (`compiler/typecheck.py`'s `_check_stmt` always walks
child blocks generically afterward regardless of which branch fired).

² Control-flow/declaration statements (`If`/`Repeat`/`While`/`Action`)
have no type-check of their own beyond the generic child-block walk that
recurses into their bodies (`compiler/typecheck.py::_child_blocks`).

**Finding**: every Python-side phase (parser, resolver, typecheck, lower,
interpreter, canonicalizer) already had complete coverage of all 17
statement kinds before this session. The *only* gap was
`self_host/parser.kuro` (6 statement kinds + the legacy `Entered` surface
syntax) and the total absence of self-hosted diagnostics — confirming the
task's expectation, not just assuming it; no other phase mismatch was
found.

## Expression/condition grammar coverage (checked separately)

`self_host/parser.kuro`'s `ParseAtom` was checked line-for-line against
`compiler/parser.py::_atom()` (7 cases: `LPAREN`, `STRING`, `INTEGER`,
`DECIMAL`, `AT`, unary `MINUS`, `IDENT`) and its `ParseComparisonOp`
against `compiler/parser.py::comparison_op()` (`greater [than [or equal
[to]]]`, `less [than [or equal [to]]]`, `equal/equals [to]`, `not equal
[to]`, `at least`/`at most`) — both already complete; no gap here.

## Parse-order audit for the newly-implemented statements

`compiler/ast_canon.py`'s encoding for every statement must match the
order information actually becomes available while parsing left to right
(the same constraint that forced `ADD`/`APPEND` to reorder — ADR-0010's
Decision 4 / the module docstring). Checked for each newly-implemented
statement before writing any Kuro code, not after:

- `Input` (`Take [user] N1 [and N2 ...];`): all fields are plain tokens
  (no recursive sub-expression parsing), so order is unconstrained. Stays
  prefix: `INPUT n1 n2 ... END_NAMES`.
- `GetStmt` (`Get N [idx];`): target `N` is a plain token read *before*
  the optional index expression is parsed. Stays prefix:
  `GET target has_index [idx...]`.
- `LengthStmt` (`Length N;`): single plain token, trivially prefix-safe.
- `SetStmt` (`Set N idx to v;`): target `N` is a plain token read before
  either expression is parsed. Stays prefix:
  `SET target [idx...] [value...]`.
- `AppendStmt` (already implemented pre-session, included for
  completeness): target is read *after* the value expression
  (`Append v to N;`) — postfix-ordered: `APPEND [value...] target`.
- `CompareStmt` (`Compare N <condition>;`): result name `N` is a plain
  token read before the condition is parsed. Stays prefix:
  `COMPARE name [condition...]`.
- legacy `Entered`: desugars to the existing `IfStmt` encoding — no new
  canon rule needed. Its condition's left side is a bare identifier
  (`VarRef`, not a general expression — `compiler/parser.py`'s `Entered`
  branch never calls `self.expr()` for the left operand, only
  `self.ident()`), which the self-hosted parser must replicate exactly
  (not accept an `@var` or literal on the left of `Entered`, matching the
  Python parser's actual restriction rather than a more permissive
  reading of the informal syntax).

**Conclusion**: no changes to `compiler/ast_canon.py`'s *encoding scheme*
were needed — every remaining statement's Python-side canonical form
already existed (`Input`/`GetStmt`/`LengthStmt`/`SetStmt`/`CompareStmt`
were already implemented in `ast_canon.py` before this session, just never
exercised by the self-hosted parser or any differential test). Verified
by new unit tests in `tests/parser/test_ast_canon.py` alongside the
existing ones.

## Stage 7 update: semantic coverage

`self_host/resolver.kuro` (top-level collection) and `self_host/
typecheck.kuro` (usage resolution + type checking, combined per
ADR-0014) bring name resolution and type checking to parity with
`compiler/resolver.py` + `compiler/typecheck.py` for every statement kind
and every diagnostic code those two files can *statically* produce:
`E3001`, `E3002`, `E3003`, `E3004`, `E3006`-`E3011`, and `E4001`-`E4005`.
(`E3005`, "value is not indexable," is a *runtime*-only check —
`compiler/interpreter.py`, not `compiler/typecheck.py` — so it has no
static self-hosted counterpart; no self-hosted interpreter exists yet,
Stage 8.) The full audit behind this —
resolver/typechecker behavior, scope semantics, type rules, and every
known bootstrap/current limitation — lives in `docs/architecture/
self-hosted-semantics.md`, not duplicated here; this file's job is
grammar/statement coverage, that one's is semantic behavior.

Not yet self-hosted: `E2005` (duplicate Action parameter — deliberately
not ported to the resolver, since Python's own copy is dead code in
practice; the *reachable* check belongs in the parser and is still a
named, open gap there — see ADR-0011), IR lowering, and any backend.

