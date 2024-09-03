from .stmt import FuncStmt
from .environment import Environment

from datetime import datetime


class HiEmCallable:
    def call(self, interpreter, arguments: list[object]) -> object:
        raise NotImplementedError

    def arity(self) -> int:
        raise NotImplementedError

    @classmethod
    def cast(cls, calle):
        # if calle is already HiEmCallable
        if isinstance(calle, cls):
            return calle
        else:
            calle.__class__ = cls
            assert isinstance(calle, cls)
            return calle


class HiEmFunction(HiEmCallable):
    def __init__(self, declaration: FuncStmt) -> None:
        self.declaration = declaration

    def call(self, interpreter, arguments: list[object]) -> object:
        environment = Environment()

        for i in range(len(self.declaration.params)):
            environment.define(self.declaration.params[i].lexeme, arguments[i])

        from ...interpreter import ReturnError

        try:
            interpreter.execute_block(self.declaration.body, environment)
        except ReturnError as err:
            return err.value

        return None

    def arity(self) -> int:
        return len(self.declaration.params)

    def __str__(self) -> str:
        return f"<Fn({self.declaration.name.lexeme})>"


# Some native function
class ClockNative(HiEmCallable):
    def call(self, interpreter, arguments: list[object]) -> object:
        return str(datetime.now())

    def arity(self) -> int:
        return 0

    def __str__(self) -> str:
        return "<Clock Fn>"
