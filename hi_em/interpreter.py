from .scanner.token_type import TokenType
from .scanner.token import Token
from .parser.expr.visitor import VisitorExpr
from .parser.expr.expr import (
    BinaryExpr,
    LiteralExpr,
    GroupingExpr,
    UnaryExpr,
    Expr,
    VariableExpr,
    AssignExpr,
    LogicalExpr,
    CallExpr,
)
from .parser.stmt.visitor import VisitorStmt
from .parser.stmt.stmt import (
    Stmt,
    PrintStmt,
    ExprStmt,
    VarStmt,
    BlockStmt,
    IfStmt,
    WhileStmt,
)
from .parser.stmt.environment import Environment


class InterpreterError(RuntimeError):
    """Runtime Error of Interpreter"""

    def __init__(self, message: str, token: Token) -> None:
        super().__init__(message)
        self.token = token


class Interpreter(VisitorExpr, VisitorStmt):
    # --------------------
    # Expression
    # --------------------
    def __init__(self) -> None:
        self.env = Environment()

    def interpret(self, expr: Expr):
        try:
            value = self.evaluate(expr)
            return value
        except InterpreterError as err:
            from .hi_em import HiEm

            HiEm.error_rumtime(err)

    def evaluate(self, expr: Expr) -> object:
        return expr.accept(self)

    def visit_literal(self, expr: LiteralExpr):
        return expr.literal

    def visit_grouping(self, expr: GroupingExpr):
        return self.evaluate(expr.expr)

    def visit_unary(self, expr: UnaryExpr):
        right = self.evaluate(expr.expr)

        match expr.op.type:
            case TokenType.MINUS:
                self.check_number(expr.op, right)
                return -float(right)
            case TokenType.BANG:
                return not self.truthy(right)

        # unreachable
        return None

    def visit_binary(self, expr: BinaryExpr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        # check if number or string for plus
        if expr.op.type is TokenType.PLUS:
            self.check_plus(expr.op, left, right)
            if isinstance(left, float) and isinstance(right, float):
                return float(left) + float(right)
            if isinstance(left, str) and isinstance(right, str):
                return str(left) + str(right)

        if expr.op.type is TokenType.EQUAL_EQUAL:
            return left == right

        if expr.op.type is TokenType.BANG_EQUAL:
            return not left == right

        # all remain types are number
        self.check_number(expr.op, left, right)
        match expr.op.type:
            case TokenType.MINUS:
                return float(left) - float(right)
            case TokenType.STAR:
                return float(left) * float(right)
            case TokenType.SLASH:
                return float(left) / float(right)
            case TokenType.GREATER:
                return float(left) > float(right)
            case TokenType.GREATER_EQUAL:
                return float(left) >= float(right)
            case TokenType.LESS:
                return float(left) < float(right)
            case TokenType.LESS_EQUAL:
                return float(left) <= float(right)

        return None

    def visit_varexpr(self, expr: VariableExpr):
        return self.env.get(expr.name)

    def visit_assignexpr(self, expr: AssignExpr):
        value = self.evaluate(expr.value)
        self.env.assign(expr.name, value)
        return value

    def visit_logical(self, expr: LogicalExpr):
        left = self.evaluate(expr.left)

        if expr.op.type == TokenType.OR:
            if self.truthy(left):
                return left
        else:
            if not self.truthy(left):
                return left

        return self.evaluate(expr.right)

    def visit_call(self, expr: CallExpr):
        calle = self.evaluate(expr.calle)

        arguments = []
        for arg in expr.arguments:
            arguments.append(self.evaluate(arg))

    # --------------------
    # Statement
    # --------------------

    def interpret(self, statements: list[Stmt]):
        try:
            for statement in statements:
                self.execute(statement)
        except InterpreterError as err:
            from .hi_em import HiEm

            HiEm.error_rumtime(err)

    def execute(self, stmt: Stmt):
        stmt.accept(self)

    def visit_expression(self, stmt: ExprStmt):
        self.evaluate(stmt.expr)
        return None

    def visit_print(self, stmt: PrintStmt):
        value = self.evaluate(stmt.expr)
        print(value)
        return None

    def visit_varstmt(self, stmt: VarStmt):
        value = None
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)
        self.env.define(stmt.name.lexeme, value)
        return None

    def visit_block(self, stmt: BlockStmt):
        self.execute_block(stmt.statements, Environment(self.env))
        return None

    def execute_block(self, statements: list[Stmt], env: Environment):
        previous = self.env
        try:
            self.env = env
            for statement in statements:
                self.execute(statement)
        except:
            # TODO: add error
            pass
        finally:
            self.env = previous

    def visit_if(self, stmt: IfStmt):
        if self.truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.then_branch)
        elif stmt.else_branch is not None:
            self.execute(stmt.else_branch)
        return None

    def visit_while(self, stmt: WhileStmt):
        while self.truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.body)
        return None

    # --------------------
    # Utils
    # --------------------

    def truthy(self, value: object) -> bool:
        if value is None:
            return False
        if isinstance(value, bool):
            return bool(value)
        return True

    def check_number(self, op: Token, *values: object):
        for value in values:
            if not isinstance(value, float):
                raise InterpreterError("Operand must be a number.", op)

    def check_plus(self, op: Token, left: object, right: object):
        if not (isinstance(left, (str, float)) and isinstance(right, (str, float))):
            raise InterpreterError("Operands must be two numbers or two strings.", op)
