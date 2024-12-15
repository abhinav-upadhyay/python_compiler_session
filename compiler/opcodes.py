from enum import Enum

# a = 10
# b = 20
# c = a + b
# a + b


class Opcode(Enum):
    LOAD_CONST = 0
    STORE_GLOBAL = 1
    LOAD_GLOBAL = 2
    BINARY_OP = 3
