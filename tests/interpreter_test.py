import unittest
from hi_em.scanner.scanner import Scanner
from hi_em.parser.parser import Parser
from hi_em.interpreter import Interpreter


class InterpreterTest(unittest.TestCase):
    def test_arithmetic_1(self):
        scanner = Scanner("(3 + 2) / 4")
        parser = Parser(scanner.tokens)
        expr = parser.parse()
        interpreter = Interpreter()

        self.assertEqual(interpreter.interpret(expr), 5 / 4)

    def test_arithmetic_2(self):
        scanner = Scanner("((6 + 2)*3)/4")
        parser = Parser(scanner.tokens)
        expr = parser.parse()
        interpreter = Interpreter()

        self.assertEqual(interpreter.interpret(expr), 24 / 4)
