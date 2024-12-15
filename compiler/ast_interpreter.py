from ast import *
from typing import Any


class Interpreter:
    def _eval_exp(self, e: expr) -> any:
        match e:
            case BinOp(lexp, Add(), rexp):
                lval = self._eval_exp(lexp)
                rval = self._eval_exp(rexp)
                return lval + rval
            case BinOp(lexp, Sub(), rexp):
                lval = self._eval_exp(lexp)
                rval = self._eval_exp(rexp)
                return lval + rval
            case BinOp(lexp, Mult(), rexp):
                lval = self._eval_exp(lexp)
                rval = self._eval_exp(rexp)
                return lval + rval
            case BinOp(lexp, Div(), rexp):
                lval = self._eval_exp(lexp)
                rval = self._eval_exp(rexp)
                return lval + rval
            case Constant(value):
                return value
            case _:
                raise Exception(f"Unsupported expression node type {e}")

    def _eval_stmt(self, s: stmt, env: dict[str, any]) -> any:
        match s:
            case Assign(targets=[Name(var_name)], value=val_exp):
                value = self._eval_exp(val_exp)
                env[var_name] = value
            case Expr(exp):
                return self._eval_exp(exp)
            case _:
                raise Exception(f"Unsupported statement node {s}")

    def _eval_stmts(self, body: list[stmt], env: dict[str, any]) -> any:
        for s in body:
            result = self._eval_stmt(s, env)
        return result

    def evaluate(self, parse_tree: Module) -> Any:
        env = {}
        match parse_tree:
            case Module(body):
                return self._eval_stmts(body, env)
            case _:
                raise Exception(f"Unsupported program {parse_tree}")
