from __future__ import annotations

from ast import *
from dataclasses import dataclass, field
from enum import Enum

from .opcodes import Opcode

# 10
# a = 10
# a


@dataclass
class Instruction:
    opcode: Opcode
    oparg: int

    def __str__(self) -> str:
        return f"Opcode: {self.opcode}, arg: {self.oparg}"


@dataclass
class CodeObject:
    bytecode: bytearray = field(default_factory=bytearray)
    constants: list[any] = field(default_factory=list)
    names: dict[int, str] = field(default_factory=dict)


class Scope(Enum):
    GLOBAL = 0
    LOCAL = 1


@dataclass
class Symbol:
    name: str
    index: int  # index into the locals table
    name_index: int  # index into the names table
    scope: Scope


@dataclass
class SymbolTable:
    table: dict[str, Symbol] = field(default_factory=dict)
    globals_index: int = 0
    locals_index: int = 0
    names_index: int = 0
    names: dict[int, str] = field(default_factory=dict)

    def add_symbol(self, name: str, scope: Scope) -> Symbol:
        name_index = self.names_index
        self.names[name_index] = name
        self.names_index += 1
        if scope == Scope.GLOBAL:
            index = self.globals_index
            self.globals_index += 1
        else:
            index = self.locals_index
            self.locals_index += 1
        symbol = Symbol(name, index, name_index, scope)
        self.table[name] = symbol
        return symbol

    def resolve(self, name: str) -> Symbol | None:
        return self.table.get(name)


class Compiler:
    def __init__(self):
        self.constants: list[any] = []
        self.instructions: list[Instruction] = []
        self.symtab = SymbolTable()

    def _add_constant(self, const: any) -> int:
        self.constants.append(const)
        return len(self.constants) - 1

    def _emit(self, opcode: Opcode, arg: int) -> Instruction:
        instr = Instruction(opcode, arg)
        self.instructions.append(instr)
        return instr

    def _compile_exp(self, e: expr) -> None:
        match e:
            case Constant(value):
                const_index = self._add_constant(value)
                self._emit(Opcode.LOAD_CONST, const_index)
            case Name(name):
                symbol = self.symtab.resolve(name)
                if symbol is None:
                    raise Exception(f"Undefined symbol {name}")
                self._emit(Opcode.LOAD_GLOBAL, symbol.name_index)
            case BinOp(lexp, Add(), rexp):
                self._compile_exp(lexp)
                self._compile_exp(rexp)
                self._emit(Opcode.BINARY_OP, 0)  # oparg 0 for addition
            case _:
                raise Exception(f"Unsupported expr type {e}")

    def _compile_stmt(self, s: stmt) -> None:
        match s:
            case Assign(targets=[Name(var_name)], value=value_exp):
                self._compile_exp(value_exp)
                symbol = self.symtab.resolve(var_name)
                if symbol is None:
                    symbol = self.symtab.add_symbol(var_name, Scope.GLOBAL)
                self._emit(Opcode.STORE_GLOBAL, symbol.name_index)
            case Expr(exp):
                self._compile_exp(exp)
            case _:
                raise Exception(f"Unsupported stmt {s}")

    def _compile_stmts(self, statements: list[stmt]) -> None:
        for s in statements:
            self._compile_stmt(s)

    def _instructions_to_bytecode(self, instructions: list[Instruction]) -> bytearray:
        bytecode = bytearray()
        for instr in instructions:
            bytecode.append(instr.opcode.value)
            bytecode.append(instr.oparg)
        return bytecode

    def compile(self, parse_tree: Module) -> CodeObject:
        match parse_tree:
            case Module(body):
                self._compile_stmts(body)
                bytecode = self._instructions_to_bytecode(self.instructions)
                return CodeObject(bytecode, self.constants, self.symtab.names)
            case _:
                raise Exception(f"Unsupported program {parse_tree}")
