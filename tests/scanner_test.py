import unittest
from hi_em.scanner.scanner import Scanner


class ScannerTest(unittest.TestCase):
    def test_single_token(self):
        scanner = Scanner("{ } ( ) + - * , . ;")

        self.assertEqual(
            str(scanner.tokens[0]),
            "Token(type = {, lexeme = {, literal = None, line = 1)",
        )

        self.assertEqual(
            str(scanner.tokens[2]),
            "Token(type = (, lexeme = (, literal = None, line = 1)",
        )

    def test_operator(self):
        scanner = Scanner("<= >= < >")

        self.assertEqual(
            str(scanner.tokens[0]),
            "Token(type = <=, lexeme = <=, literal = None, line = 1)",
        )

        self.assertEqual(
            str(scanner.tokens[3]),
            "Token(type = >, lexeme = >, literal = None, line = 1)",
        )

    def test_comment(self):
        scanner = Scanner("// hello baby \n /")

        self.assertEqual(
            str(scanner.tokens[0]),
            "Token(type = /, lexeme = /, literal = None, line = 2)",
        )

    def test_string(self):
        scanner = Scanner('"le nguyen"')

        self.assertEqual(
            str(scanner.tokens[0]),
            'Token(type = string, lexeme = "le nguyen", literal = le nguyen, line = 1)',
        )

    def test_number(self):
        scanner = Scanner("3.14 + 2")

        self.assertEqual(
            str(scanner.tokens[0]),
            "Token(type = number, lexeme = 3.14, literal = 3.14, line = 1)",
        )

        self.assertEqual(
            str(scanner.tokens[2]),
            "Token(type = number, lexeme = 2, literal = 2.0, line = 1)",
        )

    def test_identifier(self):
        scanner = Scanner("hàm trả về lớp hiện tại trong khi")

        self.assertEqual(
            str(scanner.tokens[1]),
            "Token(type = return, lexeme = trả về, literal = None, line = 1)",
        )

        self.assertEqual(
            str(scanner.tokens[2]),
            "Token(type = this, lexeme = lớp hiện tại, literal = None, line = 1)",
        )

        self.assertEqual(
            str(scanner.tokens[3]),
            "Token(type = while, lexeme = trong khi, literal = None, line = 1)",
        )
