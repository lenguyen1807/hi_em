from enum import Enum


class TokenType(Enum):
    # single-character token
    LEFT_PAREN = "{"
    RIGHT_PAREN = "}"
    LEFT_BRACE = "("
    RIGHT_BRACE = ")"
    COMMA = ","
    DOT = "."
    COMMADOT = ";"
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
    AND = "và"
    CLASS = "lớp"
    ELSE = "còn không"
    FALSE = "sai"
    FUN = "hàm"
    FOR = "for"
    IF = "nếu"
    NIL = "nil"
    OR = "hoặc"
    PRINT = "in"
    RETURN = "trả về"
    SUPER = "lớp cha"
    THIS = "lớp hiện tại"
    TRUE = "đúng"
    VAR = "biến"
    WHILE = "while"

    # eof
    EOF = "eof"
