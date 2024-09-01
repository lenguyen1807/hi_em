class RuntimeError(Exception):
    """
    Raise when intepreter had error
    """


class Lox:
    had_error = False

    @staticmethod
    def read_file(path: str) -> str:
        with open(path, encoding="utf-8") as file:
            data = file.read().rstrip()
            return data

    @staticmethod
    def __run(source: str):
        pass

    @staticmethod
    def run_file(path: str):
        source = Lox.read_file(path)
        Lox.__run(source)
        if Lox.had_error:
            raise RuntimeError

    @staticmethod
    def run_prompt(self, path: str):
        while True:
            val = input("> ")
            Lox.__run(val)
            Lox.had_error = False

    @staticmethod
    def __report(line: int, where: str, message: str):
        print(f"[line: {line}] Error {where}: {message}")
        Lox.had_error = True

    @staticmethod
    def error(line: int, message: str):
        Lox.__report(line, "", message)
