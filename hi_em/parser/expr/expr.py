from ...scanner.token import Token
from .visitor import VisitorExpr


class Expr:
    def accept(self, visitor: VisitorExpr):
        raise NotImplementedError

    def __repr__(self):
        raise NotImplementedError

    def __str__(self):
        return repr(self)


class BinaryExpr(Expr):
    def __init__(self, left: Expr, right: Expr, op: Token) -> None:
        self.left = left
        self.right = right
        self.op = op

    def accept(self, visitor: VisitorExpr):
        return visitor.visit_binary(self)

    def __repr__(self):
        return f"<BinaryExpr(left={repr(self.left)}, right={repr(self.right)}, op={repr(self.op)})>"


class UnaryExpr(Expr):
    def __init__(self, expr: Expr, op: Token) -> None:
        self.expr = expr
        self.op = op

    def accept(self, visitor: VisitorExpr):
        return visitor.visit_unary(self)

    def __repr__(self):
        return f"<UnaryExpr(expr={repr(self.expr)}, op={repr(self.op)})>"


class GroupingExpr(Expr):
    def __init__(self, expr: Expr) -> None:
        self.expr = expr

    def accept(self, visitor: VisitorExpr):
        return visitor.visit_grouping(self)

    def __repr__(self):
        return f"<GroupingExpr(expr={repr(self.expr)})>"


class LiteralExpr(Expr):
    def __init__(self, literal: object) -> None:
        self.literal = literal

    def accept(self, visitor: VisitorExpr):
        return visitor.visit_literal(self)

    def __repr__(self):
        return f"<LiteralExpr(literal={self.literal})>"


class VariableExpr(Expr):
    def __init__(self, name: Token) -> None:
        self.name = name

    def accept(self, visitor: VisitorExpr):
        return visitor.visit_varexpr(self)

    def __repr__(self):
        return f"<VariableExpr(name={repr(self.name)})>"


class AssignExpr(Expr):
    def __init__(self, name: Token, value: Expr) -> None:
        self.name = name
        self.value = value

    def accept(self, visitor: VisitorExpr):
        return visitor.visit_assignexpr(self)

    def __repr__(self):
        return f"<AssignExpr(name={repr(self.name)}, value={repr(self.value)})>"


class LogicalExpr(Expr):
    def __init__(self, left: Expr, op: Token, right: Expr) -> None:
        self.left = left
        self.op = op
        self.right = right

    def accept(self, visitor: VisitorExpr):
        return visitor.visit_logical(self)

    def __repr__(self):
        return f"<LogicalExpr(left={repr(self.left)}, op={repr(self.op)}, right={repr(self.right)})>"


class CallExpr(Expr):
    def __init__(self, calle: Expr, paren: Token, arguments: list[Expr]) -> None:
        self.calle = calle
        self.paren = paren
        self.arguments = arguments

    def accept(self, visitor: VisitorExpr):
        return visitor.visit_call(self)

    def __repr__(self):
        res = f"<CallExpr(\n\tcalle={repr(self.calle)}\n\tparen={repr(self.paren)}"
        for arg in self.arguments:
            res += f"\n\targ={repr(arg)}"
        return res + ")>"
