class VisitorExpr:
    def visit_binary(self, expr):
        raise NotImplementedError

    def visit_unary(self, expr):
        raise NotImplementedError

    def visit_literal(self, expr):
        raise NotImplementedError

    def visit_grouping(self, expr):
        raise NotImplementedError

    def visit_varexpr(self, expr):
        raise NotImplementedError

    def visit_assignexpr(self, expr):
        raise NotImplementedError

    def visit_logical(self, expr):
        raise NotImplementedError

    def visit_call(self, expr):
        raise NotImplementedError
