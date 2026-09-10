"""Recursive-descent parser for Kuro.

Error recovery: a syntax error inside one statement is reported as a
diagnostic and the parser synchronizes to the next statement boundary
(the next `;`, `.`, or a token that opens a new statement) instead of
aborting the whole parse — so one file with several unrelated mistakes
reports several diagnostics in one run (spec section 33/54).
"""
from __future__ import annotations

from .ast_nodes import (
    ActionDecl, AddStmt, Assign, BinaryExpr, BoolAnd, BoolOr, CallStmt,
    Comparison, CompareStmt, Condition, Decl, Expr, GetStmt, IfStmt, Input,
    IsClass, Literal, LengthStmt, AppendStmt, Param, PrintStmt, Program,
    RepeatStmt, ReturnStmt, SetStmt, Stmt, UpdateStmt, VarRef,
)

CLASSIFY_WORDS = {"digit", "alpha", "space", "alnum", "quote"}
from .diagnostics import DiagnosticEngine, Span
from .tokens import Token, TokKind

_STMT_START_WORDS = {
    "Take", "Print", "Add", "Update", "Get", "Length", "Set", "Append",
    "Compare", "If", "Else", "Repeat", "Action", "Return", "Call", "Done",
    "Entered",
}


class _Synchronize(Exception):
    pass


class Parser:
    def __init__(self, tokens: list[Token], diags: DiagnosticEngine):
        self.t = tokens
        self.i = 0
        self.diags = diags

    # --- token stream helpers ---------------------------------------
    def c(self) -> Token:
        return self.t[self.i]

    def peek(self, n: int = 1) -> Token:
        return self.t[min(self.i + n, len(self.t) - 1)]

    def adv(self) -> Token:
        tok = self.c()
        if tok.kind is not TokKind.EOF:
            self.i += 1
        return tok

    def isw(self, *words: str) -> bool:
        return self.c().is_word(*words)

    def span(self, tok: Token) -> Span:
        return Span(tok.line, tok.col, tok.end_line, tok.end_col)

    def fail(self, code: str, msg: str, tok: Token | None = None, help: str | None = None):
        tok = tok or self.c()
        self.diags.error(code, msg, self.span(tok), help=help)
        raise _Synchronize()

    def expect_kind(self, kind: TokKind, what: str) -> Token:
        if self.c().kind is not kind:
            self.fail("E2002", f"expected {what}, found {self._describe(self.c())}")
        return self.adv()

    def expect_word(self, word: str) -> Token:
        if not self.isw(word):
            self.fail("E2002", f"expected {word!r}, found {self._describe(self.c())}")
        return self.adv()

    def _describe(self, tok: Token) -> str:
        if tok.kind is TokKind.EOF:
            return "end of file"
        return repr(tok.value)

    def ident(self) -> str:
        if self.c().kind is not TokKind.IDENT:
            self.fail("E2001", f"expected an identifier, found {self._describe(self.c())}")
        return self.adv().value

    # --- top level -----------------------------------------------------
    def parse_program(self) -> Program:
        return Program(self.block(set()))

    def block(self, stops: set[str]) -> list[Stmt]:
        out: list[Stmt] = []
        while self.c().kind is not TokKind.EOF:
            if self.c().kind is TokKind.IDENT and self.c().value in stops:
                break
            try:
                out.append(self.stmt())
            except _Synchronize:
                self._synchronize(stops)
        return out

    def _synchronize(self, stops: set[str]):
        while self.c().kind is not TokKind.EOF:
            if self.c().kind is TokKind.IDENT and (
                self.c().value in stops or self.c().value in _STMT_START_WORDS
            ):
                return
            if self.c().kind in (TokKind.SEMI, TokKind.DOT):
                self.adv()
                return
            self.adv()

    # --- expressions -----------------------------------------------------
    # precedence: term := factor (('+'|'-') factor)*
    #             factor := atom (('*'|'/') atom)*
    def expr(self) -> Expr:
        return self._term()

    def _term(self) -> Expr:
        left = self._factor()
        while self.c().kind in (TokKind.PLUS, TokKind.MINUS):
            op_tok = self.adv()
            right = self._factor()
            left = BinaryExpr("+" if op_tok.kind is TokKind.PLUS else "-", left, right, self.span(op_tok))
        return left

    def _factor(self) -> Expr:
        left = self._atom()
        while self.c().kind in (TokKind.STAR, TokKind.SLASH):
            op_tok = self.adv()
            right = self._atom()
            left = BinaryExpr("*" if op_tok.kind is TokKind.STAR else "/", left, right, self.span(op_tok))
        return left

    def _atom(self) -> Expr:
        t = self.c()
        if t.kind is TokKind.LPAREN:
            self.adv()
            e = self.expr()
            self.expect_kind(TokKind.RPAREN, "')'")
            return e
        if t.kind is TokKind.STRING:
            self.adv()
            return Literal(t.value, self.span(t))
        if t.kind is TokKind.INTEGER:
            self.adv()
            return Literal(int(t.value), self.span(t))
        if t.kind is TokKind.DECIMAL:
            self.adv()
            try:
                val = float(t.value)
            except ValueError:
                val = 0.0
            return Literal(val, self.span(t))
        if t.kind is TokKind.AT:
            self.adv()
            name = self.ident()
            return VarRef(name, True, self.span(t))
        if t.kind is TokKind.MINUS:
            self.adv()
            inner = self._atom()
            return BinaryExpr("-", Literal(0, self.span(t)), inner, self.span(t))
        if t.kind is TokKind.IDENT:
            self.adv()
            return VarRef(t.value, False, self.span(t))
        self.fail("E2003", f"expected a value, found {self._describe(t)}")

    # values with legacy list syntax: `v1, v2, v3` (used by Assign)
    def expr_list(self) -> list[Expr]:
        vals = [self.expr()]
        while self.c().kind is TokKind.COMMA:
            self.adv()
            vals.append(self.expr())
        return vals

    # --- conditions --------------------------------------------------
    # cond := and_cond (('or') and_cond)*      -- 'or' binds loosest
    # and_cond := comparison (('and') comparison)*
    def condition(self) -> Condition:
        left = self._and_condition()
        while self.isw("or"):
            tok = self.adv()
            right = self._and_condition()
            left = BoolOr(left, right, self.span(tok))
        return left

    def _and_condition(self) -> Condition:
        left = self._comparison()
        while self.isw("and") and not self._and_is_take_list():
            tok = self.adv()
            right = self._comparison()
            left = BoolAnd(left, right, self.span(tok))
        return left

    def _and_is_take_list(self) -> bool:
        # 'and' is also used by `Take user Name and Age;`; conditions never
        # appear there, so this only exists to make intent explicit at the
        # call site rather than relying on caller discipline.
        return False

    def _comparison(self) -> Condition:
        left = self.expr()
        # 'is' is required by the historic `If`/`Entered` grammar and
        # optional-but-accepted for `Compare`, which never had it in the
        # bootstrap grammar (spec compatibility: don't require a token that
        # didn't used to exist there).
        if self.isw("is"):
            self.adv()
        if self.c().kind is TokKind.IDENT and self.c().value in CLASSIFY_WORDS:
            cls_tok = self.adv()
            return IsClass(left, cls_tok.value, left.span)
        op = self.comparison_op()
        right = self.expr()
        return Comparison(left, op, right, left.span)

    def comparison_op(self) -> str:
        if self.isw("greater"):
            self.adv()
            self.expect_word("than")
            if self.isw("or"):
                self.adv()
                self.expect_word("equal")
                if self.isw("to"):
                    self.adv()
                return "ge"
            return "gt"
        if self.isw("less"):
            self.adv()
            self.expect_word("than")
            if self.isw("or"):
                self.adv()
                self.expect_word("equal")
                if self.isw("to"):
                    self.adv()
                return "le"
            return "lt"
        if self.isw("equal"):
            self.adv()
            if self.isw("to"):
                self.adv()
            return "eq"
        if self.isw("equals"):
            self.adv()
            if self.isw("to"):
                self.adv()
            return "eq"
        if self.isw("not"):
            self.adv()
            self.expect_word("equal")
            if self.isw("to"):
                self.adv()
            return "ne"
        if self.isw("at"):
            self.adv()
            if self.isw("least"):
                self.adv()
                return "ge"
            if self.isw("most"):
                self.adv()
                return "le"
            self.fail("E2004", "expected 'least' or 'most' after 'at'")
        self.fail("E2004", f"expected a comparison operator, found {self._describe(self.c())}")

    # --- statements ----------------------------------------------------
    def stmt(self) -> Stmt:
        t = self.c()

        if (
            t.kind is TokKind.IDENT
            and self.peek().is_word("is")
            and not self.peek(2).is_word("greater", "less", "equal", "equals", "not")
        ):
            name = self.ident()
            self.expect_word("is")
            typ = self.ident()
            self.expect_kind(TokKind.SEMI, "';'")
            return Decl(name, typ, self.span(t))

        if t.kind is TokKind.IDENT and self.peek().kind is TokKind.COLON:
            name = self.ident()
            self.adv()  # ':'
            typ = self.ident()
            self.expect_kind(TokKind.EQUAL, "'='")
            vals = self.expr_list()
            self.expect_kind(TokKind.SEMI, "';'")
            return Assign(name, vals, typ, self.span(t))

        if self.isw("Take"):
            self.adv()
            if self.isw("user"):
                self.adv()
            names = [self.ident()]
            while self.isw("and"):
                self.adv()
                names.append(self.ident())
            self.expect_kind(TokKind.SEMI, "';'")
            return Input(names, self.span(t))

        if self.isw("Print"):
            self.adv()
            v = self.expr()
            self.expect_kind(TokKind.DOT, "'.'")
            return PrintStmt(v, self.span(t))

        if self.isw("Add"):
            self.adv()
            v = self.expr()
            self.expect_word("to")
            n = self.ident()
            self.expect_kind(TokKind.SEMI, "';'")
            return AddStmt(v, n, self.span(t))

        if self.isw("Update"):
            self.adv()
            n = self.ident()
            self.expect_word("to")
            v = self.expr()
            self.expect_kind(TokKind.SEMI, "';'")
            return UpdateStmt(n, v, self.span(t))

        if self.isw("Append"):
            self.adv()
            v = self.expr()
            self.expect_word("to")
            n = self.ident()
            self.expect_kind(TokKind.SEMI, "';'")
            return AppendStmt(v, n, self.span(t))

        if self.isw("Get"):
            self.adv()
            n = self.ident()
            idx = None if self.c().kind is TokKind.SEMI else self.expr()
            self.expect_kind(TokKind.SEMI, "';'")
            return GetStmt(n, idx, self.span(t))

        if self.isw("Length"):
            self.adv()
            n = self.ident()
            self.expect_kind(TokKind.SEMI, "';'")
            return LengthStmt(n, self.span(t))

        if self.isw("Set"):
            self.adv()
            n = self.ident()
            idx = self.expr()
            self.expect_word("to")
            v = self.expr()
            self.expect_kind(TokKind.SEMI, "';'")
            return SetStmt(n, idx, v, self.span(t))

        if self.isw("Compare"):
            self.adv()
            n = self.ident()
            cond = self.condition()
            self.expect_kind(TokKind.SEMI, "';'")
            return CompareStmt(n, cond, self.span(t))

        if self.isw("If"):
            self.adv()
            cond = self.condition()
            self.expect_kind(TokKind.SEMI, "';'")
            tb = self.block({"Else", "Done"})
            eb: list[Stmt] = []
            if self.isw("Else"):
                self.adv()
                self.expect_kind(TokKind.SEMI, "';'")
                eb = self.block({"Done"})
            self.expect_word("Done")
            self.expect_kind(TokKind.DOT, "'.'")
            return IfStmt(cond, tb, eb, self.span(t))

        if self.isw("Repeat"):
            self.adv()
            count = self.expr()
            self.expect_kind(TokKind.SEMI, "';'")
            body = self.block({"Done"})
            self.expect_word("Done")
            self.expect_kind(TokKind.DOT, "'.'")
            return RepeatStmt(count, body, self.span(t))

        if self.isw("Action"):
            self.adv()
            name = self.ident()
            params = self._param_list()
            self.expect_kind(TokKind.SEMI, "';'")
            body = self.block({"Done"})
            self.expect_word("Done")
            self.expect_kind(TokKind.DOT, "'.'")
            return ActionDecl(name, params, body, None, self.span(t))

        if self.isw("Return"):
            self.adv()
            v = self.expr()
            self.expect_kind(TokKind.SEMI, "';'")
            return ReturnStmt(v, self.span(t))

        if self.isw("Call"):
            self.adv()
            n = self.ident()
            args = self._arg_list()
            self.expect_kind(TokKind.SEMI, "';'")
            return CallStmt(n, args, self.span(t))

        if self.isw("Entered"):
            self.adv()
            left = VarRef(self.ident(), False, self.span(self.c()))
            self.expect_word("is")
            op = self.comparison_op()
            right = self.expr()
            self.expect_word("then")
            self.expect_word("Print")
            tv = self.expr()
            self.expect_word("otherwise")
            self.expect_word("Print")
            fv = self.expr()
            self.expect_kind(TokKind.SEMI, "';'")
            cond = Comparison(left, op, right, self.span(t))
            return IfStmt(cond, [PrintStmt(tv, self.span(t))], [PrintStmt(fv, self.span(t))], self.span(t))

        if t.kind is TokKind.IDENT and self.peek().kind is TokKind.EQUAL:
            name = self.ident()
            self.adv()  # '='
            vals = self.expr_list()
            self.expect_kind(TokKind.SEMI, "';'")
            return Assign(name, vals, None, self.span(t))

        self.fail("E2001", f"unknown statement starting with {self._describe(t)}")

    def _param_list(self) -> list[Param]:
        # Canonical (ADR-0002): `Action Name A, B: Integer;` (no parens).
        # Legacy (bootstrap-compatible): `Action Name(A, B);`.
        if self.c().kind is TokKind.LPAREN:
            self.adv()
            params: list[Param] = []
            if self.c().kind is not TokKind.RPAREN:
                params.append(self._param())
                while self.c().kind is TokKind.COMMA:
                    self.adv()
                    params.append(self._param())
            self.expect_kind(TokKind.RPAREN, "')'")
            self._check_duplicate_params(params)
            return params
        params = []
        if self.c().kind is TokKind.IDENT and not self.c().is_word("Done"):
            params.append(self._param())
            while self.c().kind is TokKind.COMMA:
                self.adv()
                params.append(self._param())
        self._check_duplicate_params(params)
        return params

    def _param(self) -> Param:
        tok = self.c()
        name = self.ident()
        typ = None
        if self.c().kind is TokKind.COLON:
            self.adv()
            typ = self.ident()
        return Param(name, typ, self.span(tok))

    def _check_duplicate_params(self, params: list[Param]):
        seen: set[str] = set()
        for p in params:
            if p.name in seen:
                self.diags.error(
                    "E2005",
                    f"duplicate action parameter {p.name!r}",
                    self.span(self.c()),
                )
            seen.add(p.name)

    def _arg_list(self) -> list[Expr]:
        if self.c().kind is TokKind.LPAREN:
            self.adv()
            args: list[Expr] = []
            if self.c().kind is not TokKind.RPAREN:
                args.append(self.expr())
                while self.c().kind is TokKind.COMMA:
                    self.adv()
                    args.append(self.expr())
            self.expect_kind(TokKind.RPAREN, "')'")
            return args
        args = []
        if self.c().kind is not TokKind.SEMI:
            args.append(self.expr())
            while self.c().kind is TokKind.COMMA:
                self.adv()
                args.append(self.expr())
        return args


def parse(tokens: list[Token], diags: DiagnosticEngine) -> Program:
    return Parser(tokens, diags).parse_program()
