import ast
import traceback

from compiler.compiler import Compiler
from compiler.vm import VM


def run_repl():
    compiler = Compiler()
    print("Simple Python Compiler REPL")
    print("Enter your code (Ctrl+D or Ctrl+Z to exit, 'dis' to see bytecode)")
    print("---------------------------------------------")

    while True:
        try:
            # Collect input (support multiple lines)
            lines = []
            while True:
                try:
                    if not lines:
                        line = input(">>> ")
                    else:
                        line = input("... ")

                    if line.strip() == "":  # Empty line ends input
                        break
                    lines.append(line)
                except EOFError:
                    return

            code = "\n".join(lines)

            if code.strip() == "":
                continue

            if code.strip() == "dis":
                print("No code to disassemble")
                continue

            # Parse and compile
            try:
                tree = ast.parse(code)
                code_object = compiler.compile(tree)

                # Execute
                vm = VM(code_object=code_object)
                result = vm.run()
                if result is not None:
                    print(result)

            except Exception as e:
                traceback.print_exc()
                print(f"Error: {str(e)}")

        except KeyboardInterrupt:
            print("\nKeyboardInterrupt")
            continue


if __name__ == "__main__":
    run_repl()
