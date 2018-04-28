from token import Token
from token_type import TokenType
from error import LoxError
from utils import log


# Lexical analysis
class Scanner:
    tokens = []
    start = 0
    current = 0
    line = 1
    keywords = {
        "and": TokenType.AND,
        "class": TokenType.CLASS,
        "else": TokenType.ELSE,
        "false": TokenType.FALSE,
        "for": TokenType.FOR,
        "fun": TokenType.FUN,
        "if": TokenType.IF,
        "nil": TokenType.NIL,
        "or": TokenType.OR,
        "print": TokenType.PRINT,
        "return": TokenType.PRINT,
        "super": TokenType.SUPER,
        "this": TokenType.THIS,
        "true": TokenType.TRUE,
        "var": TokenType.VAR,
        "while": TokenType.WHILE,
    }

    def __init__(self, source):
        self.source = source

    # 
    def scan_tokens(self):
        while not self.is_at_end():
            # We are at the beginning of the next lexeme.
            self.start = self.current
            self.__scan_token()

        self.tokens.append(Token(TokenType.EOF, "", "", self.line))
        return self.tokens

    def __scan_token(self):

        tokens = {
            '(': TokenType.LEFT_PAREN,
            ')': TokenType.RIGHT_PAREN,
            '{': TokenType.LEFT_BRACE,
            '}': TokenType.RIGHT_PAREN,
            ',': TokenType.COMMA,
            '.': TokenType.DOT,
            '-': TokenType.MINUS,
            '+': TokenType.PLUS,
            ';': TokenType.SEMICOLON,
            '*': TokenType.STAR,
            '!': {
                '-1': TokenType.BANG,
                '=': TokenType.BANG_EQUAL
            },
            '=': {
                '-1': TokenType.EQUAL,
                '=': TokenType.EQUAL_EQUAL
            },
            '<': {
                '-1': TokenType.LESS,
                '=': TokenType.LESS_EQUAL
            },
            '>': {
                '-1': TokenType.GREATER,
                '=': TokenType.GREATER_EQUAL
            },
            '/': {
                '-1': TokenType.SLASH,
                '/': ''
            },
            ' ': TokenType.BLANK_CHAR,
            '\r': TokenType.BLANK_CHAR,
            '\t': TokenType.BLANK_CHAR,
            '\n': TokenType.BLANK_CHAR,
            '"': TokenType.STRING,
            # numbers in self.numbers()

            # identifiers in self.identifiers()

        }

        c = self.advance()
        if c.isdigit():
            self.number()
            return
        elif c.isalpha():
            self.identifier()
            return

        if c in tokens.keys():
            if c in '!=<>':
                m = '=' if self.match('=') else '-1'
                self.add_token(tokens[c][m])
            elif c == '/':
                if self.match('/'):
                    m = '/'
                    while (self.peek() != '\n') and (not self.is_at_end()):
                        self.advance()
                else:
                    m = '-1'
                self.add_token(tokens[c][m])
            elif c == '\n':
                self.line += 1
            elif c == '"':
                string = self.string()
                self.add_token(tokens[c], string)
            else:
                self.add_token(tokens[c])
        else:
            # LoxError 无法在扫描完整个文件后才输出错误
            LoxError.error(self.line, "Unexpected character.")

    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
            self.advance()

        # Unterminated string.
        if self.is_at_end():
            LoxError.error(self.line, "Unterminated string.")
            return

        # The closing ".
        self.advance()

        # Trim the surrounding quotes.
        literal = self.source[self.start + 1: self.current - 1]
        return literal

    def number(self):
        while (self.peek()).isdigit():
            self.advance()

        # Look for a fractional part.
        if self.peek() == '.' and (self.peek_next()).isdigit():
            # Consume the "."
            self.advance()

        while (self.peek()).isdigit():
            self.advance()

        self.add_token(TokenType.NUMBER, float(self.source[self.start: self.current]))

    def identifier(self):
        while Scanner.is_identifier(self.peek()):
            self.advance()

        literal = self.source[self.start: self.current]
        token_type = TokenType.IDENTIFIER
        if literal in self.keywords:
            token_type = self.keywords[literal]

        self.add_token(token_type)

    @staticmethod
    def is_identifier(c):
        return c.isalnum() or c == '_'

    def is_at_end(self):
        return self.current >= len(self.source)

    # 移进一位，并返回当前 char
    def advance(self):
        self.current += 1
        return self.source[self.current - 1]

    def match(self, expected):
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def peek(self):
        if self.is_at_end():
            return '\0'
        return self.source[self.current]

    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def add_token(self, token_type, literal=''):
        # log(type (self.current))
        # log(self.source)
        text = self.source[self.start: self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))

    def clear_input(self):
        self.tokens = []
