import ast
import traceback

from compiler.compiler import Compiler
from compiler.vm import VM


class CompilerREPL:
    def __init__(self):
        """
        Initialize the REPL with a compiler, VM, and optional disassemble function.

        :param compiler: The custom Compiler instance
        :param vm: The custom VM instance
        :param disassemble_func: Optional function to disassemble code objects
        """
        self.compiler = Compiler()

    def run(self):
        """
        Start the interactive REPL loop.
        """
        print("Custom Python Compiler REPL")
        print("Type 'exit()' or press Ctrl-D to exit")
        print("Type ':disassemble' to see bytecode of last compiled code")

        # Store the last compiled code object for potential disassembly
        self.last_code_object = None
        lines = []

        while True:
            try:
                # Collect input, supporting multiline input
                user_input = self._get_multiline_input()

                # Check for special commands
                if user_input[-1] == "exit()":
                    break
                elif user_input[-1] == ":disassemble":
                    self._show_last_disassembly()
                    continue

                try:
                    parse_tree = ast.parse("\n".join(lines + user_input))
                except Exception as e:
                    print(f"\nParseError {e}")
                    traceback.print_exc()
                    continue
                lines += user_input
                # Parse the input

                # Compile the code
                code_object = self.compiler.compile(parse_tree)
                self.last_code_object = code_object
                vm = VM(code_object=code_object)

                # Execute the code
                result = vm.run()
                # Print the result if it's not None
                if result is not None:
                    print(repr(result))

            except KeyboardInterrupt:
                print("\nInterrupted")
                break
            except SystemExit:
                break
            except Exception as e:
                print(f"Error: {e}")
                traceback.print_exc()

    def _get_multiline_input(self):
        """
        Collect multiline input from the user.
        Supports continuing input with '\' at line end or by leaving a line blank after an indented block.
        """
        lines = []
        is_multiline = False
        while True:
            try:
                if not lines:
                    prompt = ">>> "
                else:
                    prompt = "... "

                line = input(prompt)

                # Check for multiline continuation
                if line.endswith("\\"):
                    lines.append(line[:-1])
                    is_multiline = True
                    continue

                lines.append(line)
                if not is_multiline:
                    break

                if not line:
                    break

                # Check if we should stop collecting input
                if not line and lines and not lines[-2].strip().endswith(":"):
                    break

                # Check for complete block after an indented section
                # if (
                #     lines
                #     and not line.startswith(" ")
                #     and lines[-2].strip().endswith(":")
                # ):
                #     break

            except EOFError:
                print()  # New line
                break

        return lines

    def _show_last_disassembly(self):
        """
        Show disassembly of the last compiled code object.
        """
        if self.last_code_object and self.disassemble:
            print("Last Compiled Code Object Disassembly:")
            self.disassemble(self.last_code_object)
        else:
            print("No previous code object to disassemble")


# Usage example (commented out, as actual Compiler and VM are not provided)
def main():
    repl = CompilerREPL()
    repl.run()


if __name__ == "__main__":
    main()
