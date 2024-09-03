from ..expr.expr import Expr
from .visitor import VisitorStmt
from ...scanner.token import Token


class Stmt:
    def accept(self, visitor: VisitorStmt):
        raise NotImplementedError

    def __repr__(self):
        raise NotImplementedError

    def __str__(self):
        return repr(self)


class PrintStmt(Stmt):
    def __init__(self, expr: Expr) -> None:
        self.expr = expr

    def accept(self, visitor: VisitorStmt):
        return visitor.visit_print(self)

    def __repr__(self):
        return f"<PrintStmt(expr={repr(self.expr)})>"


class VarStmt(Stmt):
    def __init__(self, name: Token, initializer: Expr) -> None:
        self.initializer = initializer
        self.name = name

    def accept(self, visitor: VisitorStmt):
        return visitor.visit_varstmt(self)

    def __repr__(self):
        return f"<VariableStmt(name={repr(self.name)}, initializer={repr(self.initializer)})"


class ExprStmt(Stmt):
    def __init__(self, expr: Expr) -> None:
        self.expr = expr

    def accept(self, visitor: VisitorStmt):
        return visitor.visit_expression(self)

    def __repr__(self):
        return f"<ExprStmt(expr={repr(self.expr)})>"


class BlockStmt(Stmt):
    def __init__(self, statements: list[Stmt]) -> None:
        self.statements = statements

    def accept(self, visitor: VisitorStmt):
        return visitor.visit_block(self)

    def __repr__(self):
        rep = "<BlockStmt("
        for statement in self.statements:
            rep += f"\n\tstatement={repr(statement)}"
        return rep + ")>"


class IfStmt(Stmt):
    def __init__(self, condition: Expr, then_branch: Stmt, else_branch: Stmt) -> None:
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def accept(self, visitor: VisitorStmt):
        return visitor.visit_if(self)

    def __repr__(self):
        return f"<IfStmt(condition={repr(self.condition)}, then={repr(self.then_branch)}, else={repr(self.else_branch)})>"


class WhileStmt(Stmt):
    def __init__(self, condition: Expr, body: Stmt) -> None:
        self.condition = condition
        self.body = body

    def accept(self, visitor: VisitorStmt):
        return visitor.visit_while(self)

    def __repr__(self):
        return f"<WhileStmt(condition={repr(self.condition)}, body={repr(self.body)})>"


class FuncStmt(Stmt):
    def __init__(self, name: Token, params: list[Token], body: list[Stmt]) -> None:
        self.name = name
        self.params = params
        self.body = body

    def accept(self, visitor: VisitorStmt):
        return visitor.visit_function(self)


class ReturnStmt(Stmt):
    def __init__(self, keyword: Token, value: Expr) -> None:
        self.value = value
        self.keyword = keyword

    def accept(self, visitor: VisitorStmt):
        return visitor.visit_return(self)
