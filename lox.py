import sys

def log(*args):
    print(*args)

class Lox:
    had_error = False

    def __init__(self):
        pass

    # 读入文件，执行
    def runFile(self, path):
        log(path)
        if self.had_error:
            sys.exit(65)

        source = open(path, 'r')
        self.run(source)
        source.close()

    # repl
    def runPrompt(self):
        while True:
            try:
                line = input(">>> ")
                self.run(line)
                self.had_error = False                
            except KeyboardInterrupt:
                sys.exit()

    def run(self, source):
        print(source)
        scanner = Scanner()
        tokens = []
        tokens.append(scanner.scanTokens())
        
        for token in tokens:
            print(token)
    
    @staticmethod
    def error(self, line, message):
        self.report(line, "", message)
    
    @staticmethod
    def report(self, line, where, message):
        sys.stderr.write("[line " + line + "] Error " + where + ": " + message)
        self.had_error = True
    
# Lexical analysis
class Scanner:
    def __init__(self):
        pass
    
    # 
    def scanTokens(self):
        pass

if __name__ == "__main__":
    lox = Lox()
    arg_len = len(sys.argv)

    if (arg_len > 2):
        print("Usage: plox [script]")
    elif arg_len == 2:
        lox.runFile(sys.argv[1])
    else:
        lox.runPrompt()