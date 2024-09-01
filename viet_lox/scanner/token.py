from .token_type import TokenType


class Token:
    def __init__(
        self, token_type: TokenType, lexeme: str, literal: object, line: int
    ) -> None:
        self.type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __repr__(self) -> str:
        return f"<Token(type = {self.type.value}, lexeme = {self.lexeme}, literal = {self.literal}, line = {self.line})>"

    def __str__(self) -> str:
        return f"Token(type = {self.type.value}, lexeme = {self.lexeme}, literal = {self.literal}, line = {self.line})"
