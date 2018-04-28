import sys


class LoxError:
    had_error = False

    def __init__(self):
        pass

    @staticmethod
    def error(line, message):
        LoxError.report(line, "", message)

    @staticmethod
    def report(line, where, message):
        sys.stderr.write("[line " + str(line) + "] Error "
                         + where + ": " + message + "\n")
        LoxError.had_error = True
