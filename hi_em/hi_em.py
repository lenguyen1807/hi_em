import sys

from .scanner.token_type import TokenType
from .scanner.scanner import Scanner
from .parser.parser import Parser
from .parser.ast_printer import ASTPrinter
from .interpreter import Interpreter


class HiEm:
    had_error = False
    had_runtime_error = False

    @staticmethod
    def read_file(path: str) -> str:
        with open(path, encoding="utf-8") as file:
            data = file.read()
            return data

    @staticmethod
    def run(source: str):
        scanner = Scanner(source)
        parser = Parser(scanner.tokens)
        statements = parser.parse()
        interpreter = Interpreter()

        if HiEm.had_error:
            return
        if HiEm.had_runtime_error:
            return

        interpreter.interpret(statements)

    @staticmethod
    def run_file(path: str):
        source = HiEm.read_file(path)
        HiEm.run(source)
        if HiEm.had_error:
            sys.exit(65)
        if HiEm.had_runtime_error:
            sys.exit(70)

    @staticmethod
    def run_prompt():
        while True:
            val = input("> ")
            if val == "thoát":
                return
            HiEm.run(val)
            HiEm.had_error = False

    @staticmethod
    def report(line: int, where: str, message: str):
        print(f"[line: {line}] Error {where}: {message}")
        HiEm.had_error = True

    @staticmethod
    def error(line: int, message: str):
        HiEm.report(line, "", message)

    @staticmethod
    def error_token(token, message: str):
        if token.type == TokenType.EOF:
            HiEm.report(token.line, "at end", message)
        else:
            HiEm.report(token.line, f"at '{token.lexeme}'", message)

    @staticmethod
    def error_rumtime(error: Exception):
        print(
            f"{str(error)}\n[line {error.token.line}] Error at {error.token.type.value}"
        )
        HiEm.had_runtime_error = True
