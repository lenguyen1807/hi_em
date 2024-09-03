from .token import Token
from .token_type import TokenType, keyword_map


class Scanner:
    def __init__(self, source: str) -> None:
        self.start = 0
        self.current = 0
        self.line = 1

        self.source = source
        self.tokens: list[Token] = []

        # scan all tokens
        self.scan_tokens()

    def scan_tokens(self):
        while not self.is_end():
            self.start = self.current
            self.scan_token()
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))

    def scan_token(self):
        val = self.advance()
        match val:
            case "}":
                self.add_token(TokenType.RIGHT_PAREN)
            case "{":
                self.add_token(TokenType.LEFT_PAREN)
            case ")":
                self.add_token(TokenType.RIGHT_BRACE)
            case "(":
                self.add_token(TokenType.LEFT_BRACE)
            case ",":
                self.add_token(TokenType.COMMA)
            case ".":
                self.add_token(TokenType.DOT)
            case "-":
                self.add_token(TokenType.MINUS)
            case "+":
                self.add_token(TokenType.PLUS)
            case ";":
                self.add_token(TokenType.SEMICOLON)
            case "*":
                self.add_token(TokenType.STAR)
            case "/":
                if self.match("/"):
                    while (self.peek() != "\n") and (not self.is_end()):
                        self.advance()
                else:
                    self.add_token(TokenType.SLASH)
            case "!":
                (
                    self.add_token(TokenType.BANG_EQUAL)
                    if self.match("=")
                    else self.add_token(TokenType.BANG)
                )
            case "=":
                (
                    self.add_token(TokenType.EQUAL_EQUAL)
                    if self.match("=")
                    else self.add_token(TokenType.EQUAL)
                )
            case ">":
                (
                    self.add_token(TokenType.GREATER_EQUAL)
                    if self.match("=")
                    else self.add_token(TokenType.GREATER)
                )
            case "<":
                (
                    self.add_token(TokenType.LESS_EQUAL)
                    if self.match("=")
                    else self.add_token(TokenType.LESS)
                )
            case " ":  # ignore
                pass
            case "\r":
                pass
            case "\t":
                pass
            case "\n":
                self.line += 1
            case '"':  # string
                self.add_string()
            case _:  # default case
                if val.isdigit():  # number case
                    self.add_number()
                elif val.isalpha():
                    self.add_identifier()
                else:
                    from ..hi_em import HiEm

                    HiEm.error(line=self.line, message="Unexpected character")

    def is_end(self) -> bool:
        return self.current >= len(self.source)

    def match(self, expected: str) -> bool:
        if self.is_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def peek(self, n: int = 0) -> str:
        idx = self.current + n
        if idx >= len(self.source):
            return "\0"
        return self.source[idx]

    def peek_next(self) -> str:
        return self.peek(1)

    def advance(self) -> str:
        res = self.source[self.current]
        self.current += 1
        return res

    def add_token(self, token_type: TokenType, literal: object = None):
        text = self.source[self.start : self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))

    def add_string(self):
        while (self.peek() != '"') and (not self.is_end()):
            if self.peek() == "\n":
                self.line += 1
            self.advance()

        if self.is_end():
            from ..hi_em import HiEm

            HiEm.error(self.line, "Unterminated string")
            return

        self.advance()  # closing "

        self.add_token(TokenType.STRING, self.source[self.start + 1 : self.current - 1])

    def add_number(self):
        while self.peek().isdigit():
            self.advance()

        if (self.peek() == ".") and (self.peek_next().isdigit()):
            # consume the "."
            self.advance()
            # consume fraction part
            while self.peek().isdigit():
                self.advance()

        self.add_token(TokenType.NUMBER, float(self.source[self.start : self.current]))

    def is_alpha_numeric(self) -> bool:
        return self.peek().isdigit() or self.peek().isalpha() or self.peek() == "_"

    def add_identifier(self):
        def get_text():
            self.advance()  # get " "
            while self.is_alpha_numeric():
                self.advance()
            return self.source[self.start : self.current]

        while self.is_alpha_numeric():
            self.advance()

        # don't worry about wtf is this
        # just some magic and it works
        text = self.source[self.start : self.current]
        if text in ["còn", "trả", "trong"]:
            text = get_text()
        elif text == "lớp":
            if self.peek_next() == "c":
                text = get_text()
            elif self.peek_next() == "h":
                text = get_text()
                text = get_text()
            else:
                # TODO: put error here
                pass

        (
            self.add_token(keyword_map[text])
            if text in keyword_map
            else self.add_token(TokenType.IDENTIFIER)
        )
