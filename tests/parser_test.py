import unittest
from hi_em.scanner.scanner import Scanner
from hi_em.parser.parser import Parser
from hi_em.parser.ast_printer import ASTPrinter


class ParserTest(unittest.TestCase):
    def test_ast(self):
        scanner = Scanner("(3 + 2) / 4")
        parser = Parser(scanner.tokens)
        expr = parser.parse()
        self.assertEqual(
            ASTPrinter().get_expr(expr), "( SLASH ( group ( PLUS 3.0 2.0 ) ) 4.0 )"
        )
