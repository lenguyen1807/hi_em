from __future__ import annotations
from ...scanner.token import Token


class Environment:
    def __init__(self, enclosing: Environment = None) -> None:
        self.values: dict[str, object] = {}
        self.enclosing: Environment = enclosing

    def define(self, name: str, value: object):
        self.values[name] = value

    def get(self, name: Token):
        if name.lexeme in self.values:
            return self.values[name.lexeme]

        if self.enclosing is not None:
            return self.enclosing.get(name)

        from ...interpreter import InterpreterError

        raise InterpreterError(f"Undefined variable '{name.lexeme}'.", name)

    def assign(self, name: Token, value: object):
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return

        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return

        from ...interpreter import InterpreterError

        raise InterpreterError(f"Undefined variable '{name.lexeme}'.", name)
