from viet_lox.lox import Lox
from viet_lox.scanner.scanner import Scanner

if __name__ == "__main__":
    scanner = Scanner(Lox.read_file("./example/test1.hiem"))
    for token in scanner.tokens:
        print(token)
