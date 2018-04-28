from scanner import Scanner
from utils import log
import sys

class Lox:
    had_error = False

    def __init__(self):
        pass

    # 读入文件，执行
    def run_file(self, path):
        log(path)
        source = open(path, 'r')
        self.run(source)
        if self.had_error:
            sys.exit(65)
        source.close()

    # repl
    def run_prompt(self):
        while True:
            try:
                line = input(">>> ")
                self.run(line)
                self.had_error = False
            except KeyboardInterrupt:
                sys.exit()

    def run(self, source):
        scanner = Scanner(source)
        scanner.clear_input()
        tokens = scanner.scan_tokens()

        for token in tokens:
            print(token)

    @staticmethod
    def error(line, message):
        Lox.report(line, "", message)

    @staticmethod
    def report(line, where, message):
        sys.stderr.write("[line " + str(line) + "] Error "
                         + where + ": " + message + "\n")
        Lox.had_error = True
    

if __name__ == "__main__":
    lox = Lox()
    arg_len = len(sys.argv)

    if arg_len > 2:
        print("Usage: plox [script]")
    elif arg_len == 2:
        lox.run_file(sys.argv[1])
    else:
        lox.run_prompt()