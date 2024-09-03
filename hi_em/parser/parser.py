from ..scanner.token import Token
from ..scanner.token_type import TokenType
from .expr.expr import (
    Expr,
    BinaryExpr,
    UnaryExpr,
    LiteralExpr,
    GroupingExpr,
    VariableExpr,
    AssignExpr,
    LogicalExpr,
    CallExpr,
)
from .stmt.stmt import Stmt, PrintStmt, ExprStmt, VarStmt, BlockStmt, IfStmt, WhileStmt


class ParserError(RuntimeError):
    """Error when parsing"""


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.current = 0

    def parse(self) -> list[Stmt]:
        # try:
        #     return self.expression()
        # except ParserError as e:
        #     return None

        stmts = []
        while not self.is_end():
            stmts.append(self.declaration())
        return stmts

    # --------------------
    # Expression
    # --------------------

    # expression     → equality ;
    def expression(self) -> Expr:
        return self.assignment()

    #     assignment     → IDENTIFIER "=" assignment
    #                    | logic_or ;
    def assignment(self) -> Expr:
        expr = self.logic_or()

        if self.match(TokenType.EQUAL):
            token = self.previous()
            value = self.assignment()

            if isinstance(expr, VariableExpr):
                name = expr.name
                return AssignExpr(name, value)
            else:
                from hi_em.hi_em import HiEm

                HiEm.error_token(token, "Invalid assignment target.")

        return expr

    # equality       → comparison ( ( "!=" | "==" ) comparison )* ;
    def equality(self) -> Expr:
        expr = self.comparision()

        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            op = self.previous()
            right = self.comparision()
            expr = BinaryExpr(expr, right, op)

        return expr

    # comparison     → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
    def comparision(self) -> Expr:
        expr = self.term()

        while self.match(
            TokenType.LESS,
            TokenType.LESS_EQUAL,
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
        ):
            op = self.previous()
            right = self.term()
            expr = BinaryExpr(expr, right, op)

        return expr

    # term           → factor ( ( "-" | "+" ) factor )* ;
    def term(self) -> Expr:
        expr = self.factor()

        while self.match(TokenType.MINUS, TokenType.PLUS):
            op = self.previous()
            right = self.factor()
            expr = BinaryExpr(expr, right, op)

        return expr

    # factor         → unary ( ( "/" | "*" ) unary )* ;
    def factor(self) -> Expr:
        expr = self.unary()

        while self.match(TokenType.SLASH, TokenType.STAR):
            op = self.previous()
            right = self.unary()
            expr = BinaryExpr(expr, right, op)

        return expr

    # unary          → ( "!" | "-" ) unary
    #                | primary ;
    def unary(self) -> Expr:
        if self.match(TokenType.BANG, TokenType.MINUS):
            op = self.previous()
            expr = self.unary()
            return UnaryExpr(expr, op)

        return self.call()

    # call           → primary ( "(" arguments? ")" )* ;
    def call(self) -> Expr:
        expr = self.primary()

        while True:
            if self.match(TokenType.LEFT_BRACE):
                expr = self.finish_call(expr)
            else:
                break

        return expr

    # arguments      → expression ( "," expression )* ;
    def finish_call(self, calle: Expr):
        arguments = []

        if not self.check(TokenType.RIGHT_BRACE):
            arguments.append(self.expression())

            while self.match(TokenType.COMMA):

                if len(arguments) >= 10:
                    from ..hi_em import HiEm

                    HiEm.error_token(self.peek(), "Can't have more than 10 arguments.")

                arguments.append(self.expression())

        paren = self.consume(TokenType.RIGHT_BRACE, "Expected ')' after arguments.")

        return CallExpr(calle, paren, arguments)

    # primary        → NUMBER | STRING | "true" | "false" | "nil"
    #                | "(" expression ")" ;
    #                | IDENTIFIER ;
    def primary(self) -> Expr:
        if self.match(TokenType.NIL):
            return LiteralExpr(None)

        if self.match(TokenType.TRUE):
            return LiteralExpr(True)

        if self.match(TokenType.FALSE):
            return LiteralExpr(False)

        if self.match(TokenType.NUMBER, TokenType.STRING):
            return LiteralExpr(self.previous().literal)

        if self.match(TokenType.LEFT_BRACE):
            expr = self.expression()
            self.consume(TokenType.RIGHT_BRACE, "Expect ')' after expression.")
            return GroupingExpr(expr)

        if self.match(TokenType.IDENTIFIER):
            return VariableExpr(self.previous())

        self.error(self.peek(), "Expect expression.")

    # logic_or       → logic_and ( "or" logic_and )* ;
    def logic_or(self):
        expr = self.logic_and()

        if self.match(TokenType.OR):
            op = self.previous()
            right = self.logic_and()
            expr = LogicalExpr(expr, op, right)

        return expr

    # logic_and      → equality ( "and" equality )* ;
    def logic_and(self):
        expr = self.equality()

        if self.match(TokenType.AND):
            op = self.previous()
            right = self.equality()
            expr = LogicalExpr(expr, op, right)

        return expr

    # --------------------
    # Statement
    # --------------------

    def declaration(self):
        try:
            if self.match(TokenType.VAR):
                return self.var_declaration()
            return self.statement()
        except:
            # TODO: implement synchronize
            pass

    # varDecl        → "var" IDENTIFIER ( "=" expression )? ";" ;
    def var_declaration(self):
        name = self.consume(TokenType.IDENTIFIER, "Expect variable name.")

        initializer = None
        if self.match(TokenType.EQUAL):
            initializer = self.expression()

        self.consume(TokenType.SEMICOLON, "Expect ';' after variable declaration")

        return VarStmt(name, initializer)

    # statement      → exprStmt
    #                | printStmt
    #                | block ;
    def statement(self) -> Stmt:
        if self.match(TokenType.PRINT):
            return self.print_statement()

        if self.match(TokenType.LEFT_PAREN):
            return BlockStmt(self.block())

        if self.match(TokenType.IF):
            return self.if_statement()

        if self.match(TokenType.WHILE):
            return self.while_statement()

        if self.match(TokenType.FOR):
            return self.for_statement()

        return self.expr_statement()

    # printStmt      → "print" expression ";" ;
    def print_statement(self):
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return PrintStmt(value)

    # exprStmt       → expression ";" ;
    def expr_statement(self):
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return ExprStmt(value)

    # block          → "{" declaration* "}" ;
    def block(self):
        statements = []
        while not self.check(TokenType.RIGHT_PAREN) and not self.is_end():
            statements.append(self.declaration())
        self.consume(TokenType.RIGHT_PAREN, "Expect '}' after block.")
        return statements

    # ifStmt         → "if" "(" expression ")" statement
    #            ( "else" statement )? ;
    def if_statement(self):
        self.consume(TokenType.LEFT_BRACE, "Expect '(' after 'if'")
        condition = self.expression()
        self.consume(TokenType.RIGHT_BRACE, "Expect ')' after if condition")

        then_branch = self.statement()
        else_branch = None

        if self.match(TokenType.ELSE):
            else_branch = self.statement()

        return IfStmt(condition, then_branch, else_branch)

    # whileStmt      → "while" "(" expression ")" statement ;
    def while_statement(self):
        self.consume(TokenType.LEFT_BRACE, "Expect '(' after 'while'")
        condition = self.expression()
        self.consume(TokenType.RIGHT_BRACE, "Expect ')' after while loop")
        body = self.statement()
        return WhileStmt(condition, body)

    # forStmt      → "for" "(" ( varDecl | exprStmt | ";" )
    #              expression? ";"
    #              expression? ")" statement ;
    def for_statement(self):
        self.consume(TokenType.LEFT_BRACE, "Expect '(' after 'for'")

        initializer = None
        if self.match(TokenType.SEMICOLON):
            initializer = None
        elif self.match(TokenType.VAR):
            initializer = self.var_declaration()
        else:
            initializer = self.statement()

        condition = None
        if not self.check(TokenType.SEMICOLON):
            condition = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after loop condition.")

        increment = None
        if not self.check(TokenType.RIGHT_BRACE):
            increment = self.expression()
        self.consume(TokenType.RIGHT_BRACE, "Expect ')' after for clauses.")

        body = self.statement()

        if increment is not None:
            body = BlockStmt([body, ExprStmt(increment)])

        if condition is None:
            condition = LiteralExpr(True)
        body = WhileStmt(condition, body)

        if initializer is not None:
            body = BlockStmt([initializer, body])

        return body

    # --------------------
    # Utils
    # --------------------

    def match(self, *args: TokenType) -> bool:
        for token_type in args:
            if self.check(token_type):
                self.advance()
                return True
        return False

    def is_end(self) -> bool:
        return self.peek().type == TokenType.EOF

    def check(self, token_type: TokenType) -> bool:
        if self.is_end():
            return False
        return self.peek().type == token_type

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def consume(self, token_type: TokenType, message: str) -> Token:
        if self.check(token_type):
            return self.advance()
        # error
        self.error(self.previous(), message)

    def advance(self):
        if not self.is_end():
            self.current += 1
        return self.previous()

    def error(self, token: Token, message: str):
        from ..hi_em import HiEm

        HiEm.error_token(token, message)

        raise ParserError
