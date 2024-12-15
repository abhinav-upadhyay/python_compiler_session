import ast

import pytest
from compiler.ast_interpreter import Interpreter

TEST_CASES = [
    (
        "literal_addition",
        "5",
        """
2 + 3
""",
    ),
    (
        "assignment",
        "42",
        """
a = 42
a
""",
    ),
    (
        "addition_test",
        "42",
        """
a = 30
b = 12
a + b
""",
    ),
    (
        "arithmetic_test",
        "-16.0",
        """
a = 42
b = 10
c = b - a
c = c * 2
d = c / 4
d
""",
    ),
    (
        "greater_than",
        "greater",
        """
x = 10
if x > 5:
    "greater"
else:
    "smaller"
""",
    ),
    (
        "less_than",
        "less",
        """
a = 30
b = 665
if a < b:
    "less"
""",
    ),
    (
        "greater_than_or_equal",
        "42",
        """
a = 30
b = 12
if a >= b:
    a = a + b
a
""",
    ),
    (
        "less_than_or_equal",
        "42",
        """
a = 30
b = 12
if b <= a:
    a = a + b
a
""",
    ),
    (
        "if_condition_true_without_else",
        "42",
        """
a = 42
isTrue = a == 42
if isTrue:
    a
""",
    ),
    (
        "if_condition_false_without_else",
        "42",
        """
a = 42
isFalse = a > 42
if isFalse:
    a = a / 2
a
""",
    ),
    (
        "if_condition_true_with_else",
        "42",
        """
a = True
if a:
    42
else:
    0
""",
    ),
    (
        "if_condition_false_with_else",
        "0",
        """
a = False
if a:
    42
else:
    0
""",
    ),
    (
        "if_false_elif_true",
        "42",
        """
a = False
b = True
if a:
    0
elif b:
    42
else:
    -1
""",
    ),
    (
        "while_test",
        "42",
        """
a = 0
b = 42
while a < b:
    print(a)
    a = a + 1
a
""",
    ),
    (
        "if_else_and_more",
        "42",
        """
a = 30
b = 10
if b > a:
    print(b)
else:
    a = a + 1
a = a + 11
a
""",
    ),
    (
        "no_arg_func",
        "42",
        """
def foo():
    return 42
foo()
""",
    ),
    (
        "local_variable",
        "21",
        """
def foo(arg1):
    local_var = arg1 * 2
    return arg1
y = 21
foo(y)
""",
    ),
    (
        "single_arg_func",
        "42",
        """
def foo(arg1):
    local1 = arg1 * 2
    return local1
foo(21)
""",
    ),
    (
        "two_arg_func",
        "True",
        """
def add(a, b):
    return a + b
x = 30
y = 12
sum = add(x, y)
result = sum == 42
result
""",
    ),
    (
        "2_level_nested_function_calls",
        "42",
        """
def add_1(x):
    return x + 1

def make_42():
    x = 1
    while x < 42:
        x = add_1(x)
    return x

result = make_42()
result
""",
    ),
]


def run_test_program(program_code):
    """
    Execute the test program and return its result as a string.

    Args:
        program_code (str): The Python program to execute

    Returns:
        str: The string representation of the program's return value
    """

    # Execute the program code
    interpreter = Interpreter()
    parsetree = ast.parse(program_code)
    result = interpreter.evaluate(parsetree)
    return str(result)


@pytest.mark.parametrize("test_name,expected_output,code", TEST_CASES)
def test_compiler(test_name, expected_output, code):
    actual_output = run_test_program(code)
    assert actual_output == expected_output, (
        f"Test case '{test_name}' failed. "
        f"Expected {expected_output}, "
        f"but got {actual_output}"
    )
