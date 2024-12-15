from typing import Any

from .compiler import CodeObject
from .opcodes import Opcode


class Frame:
    def __init__(
        self,
        bytecode: bytearray,
        globals: dict[str, Any] | None = None,
        locals: list[Any] | None = None,
        names: dict[int, str] = None,
    ):
        self.bytecode: CodeObject = bytecode
        self.stack: list[Any] = []

        if locals is not None:
            self.locals: list[Any] = locals
        else:
            self.locals: list[Any] = []

        if globals is None:
            self.globals = {}
        else:
            self.globals = globals

        self.ip: int = 0
        self.names: dict[int, str] = names if names else {}


class VM:
    def __init__(self, code_object: CodeObject):
        """
        code_object is the compiled bytecode of the Python program we wish to
        execute
        """
        self.frames: list[Frame] = []
        self.frames.append(Frame(code_object.bytecode, names=code_object.names))
        self.constants: list[any] = code_object.constants

    def _eval_frame(self, frame: Frame) -> any:
        bytecode = frame.bytecode
        ip = 0
        stack = frame.stack
        while ip < len(bytecode):
            opcode = bytecode[ip]
            oparg = bytecode[ip + 1]
            ip += 2

            match opcode:
                case Opcode.LOAD_CONST.value:
                    const_value = self.constants[oparg]
                    stack.append(const_value)
                case Opcode.STORE_GLOBAL.value:
                    value = stack.pop()
                    var_name = frame.names[oparg]
                    frame.globals[var_name] = value
                case Opcode.LOAD_GLOBAL.value:
                    var_name = frame.names[oparg]
                    value = frame.globals[var_name]
                    stack.append(value)
                case Opcode.BINARY_OP.value:
                    rval = stack.pop()
                    lval = stack.pop()
                    result = lval + rval
                    stack.append(result)
                case _:
                    raise Exception(f"Unsupported opcode {opcode}")
        if stack:
            return stack.pop()
        return None

    def run(self) -> Any:
        return self._eval_frame(self.frames[0])
