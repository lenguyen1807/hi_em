from .expr.expr import Expr, BinaryExpr, GroupingExpr, LiteralExpr, UnaryExpr
from .expr.visitor import VisitorExpr


class ASTPrinter(VisitorExpr):
    def get_expr(self, expr: Expr) -> str:
        return expr.accept(self)

    def visit_binary(self, expr: BinaryExpr) -> str:
        return self.parenthesize(expr.op.type.name, expr.left, expr.right)

    def visit_grouping(self, expr: GroupingExpr) -> str:
        return self.parenthesize("group", expr.expr)

    def visit_literal(self, expr: LiteralExpr) -> str:
        if expr.literal is None:
            return "nil"
        return str(expr.literal)

    def visit_unary(self, expr: UnaryExpr) -> str:
        return self.parenthesize(expr.op.type.name, expr.expr)

    def parenthesize(self, name: str, *args: Expr) -> str:
        val = f"( {name}"
        for expr in args:
            val += f" {expr.accept(self)}"
        val += " )"
        return val
