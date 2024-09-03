class VisitorStmt:
    def visit_print(self, stmt):
        raise NotImplementedError

    def visit_block(self, stmt):
        raise NotImplementedError

    def visit_class(self, stmt):
        raise NotImplementedError

    def visit_expression(self, stmt):
        raise NotImplementedError

    def visit_if(self, stmt):
        raise NotImplementedError

    def visit_function(self, stmt):
        raise NotImplementedError

    def visit_varstmt(self, stmt):
        raise NotImplementedError

    def visit_block(self, stmt):
        raise NotImplementedError

    def visit_while(self, stmt):
        raise NotImplementedError
