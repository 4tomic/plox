from scanner import Scanner
from utils import log
from error import LoxError
import sys


class Lox:
    def __init__(self):
        pass

    # read source file and execute
    def run_file(self, path):
        log(path)
        with open(path, 'r') as lines:
            for line in lines:
                self.run(line)
        if LoxError.had_error:
            sys.exit(65)

    # repl
    def run_prompt(self):
        while True:
            try:
                line = input(">>> ")
                self.run(line)
                LoxError.had_error = False
            except KeyboardInterrupt:
                sys.exit()

    def run(self, source):
        scanner = Scanner(source)
        scanner.clear_input()
        tokens = scanner.scan_tokens()

        for token in tokens:
            print(token)


if __name__ == "__main__":
    lox = Lox()
    arg_len = len(sys.argv)

    if arg_len > 2:
        print("Usage: plox [script]")
    elif arg_len == 2:
        lox.run_file(sys.argv[1])
    else:
        lox.run_prompt()
