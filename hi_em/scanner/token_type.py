from enum import Enum


class TokenType(Enum):
    # single-character token
    LEFT_PAREN = "{"
    RIGHT_PAREN = "}"
    LEFT_BRACE = "("
    RIGHT_BRACE = ")"
    COMMA = ","
    DOT = "."
    SEMICOLON = ";"
    MINUS = "-"
    PLUS = "+"
    SLASH = "/"
    STAR = "*"

    # One or two character token
    BANG = "!"
    BANG_EQUAL = "!="
    EQUAL = "="
    EQUAL_EQUAL = "=="
    GREATER = ">"
    GREATER_EQUAL = ">="
    LESS = "<"
    LESS_EQUAL = "<="

    # literals
    IDENTIFIER = "identifier"
    STRING = "string"
    NUMBER = "number"

    # keywords
    AND = "and"
    CLASS = "class"
    ELSE = "else"
    FALSE = "false"
    FUN = "function"
    FOR = "for"
    IF = "if"
    NIL = "nil"
    OR = "or"
    PRINT = "print"
    RETURN = "return"
    SUPER = "super"
    THIS = "this"
    TRUE = "true"
    VAR = "variable"
    WHILE = "while"

    # eof
    EOF = "eof"


keyword_map = {
    "và": TokenType.AND,
    "lớp": TokenType.CLASS,
    "còn không": TokenType.ELSE,
    "sai": TokenType.FALSE,
    "hàm": TokenType.FUN,
    "lặp": TokenType.FOR,
    "nếu": TokenType.IF,
    "nil": TokenType.NIL,
    "hoặc": TokenType.OR,
    "in": TokenType.PRINT,
    "trả về": TokenType.RETURN,
    "lớp cha": TokenType.SUPER,
    "lớp hiện tại": TokenType.THIS,
    "đúng": TokenType.TRUE,
    "đặt": TokenType.VAR,
    "trong khi": TokenType.WHILE,
}
