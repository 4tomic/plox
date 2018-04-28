from token import Token
from token_type import TokenType
from error import LoxError
fro utils import log

# Lexical analysis
class Scanner:
    tokens = []
    start = 0
    current = 0
    line = 1

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
            '*': TokenType.STAR
        }

        c = self.advance()
        if c in tokens.keys():
            self.add_token(tokens[c])
        else:
            LoxError.error(self.line, "Unexpected character.")

    def is_at_end(self):
        return self.current >= len(self.source)

    # 移进一位，并返回当前 char
    def advance(self):
        self.current += 1
        return self.source[self.current - 1]

    def add_token(self, token_type, literal=''):
        # log(type (self.current))
        # log(self.source)
        text = self.source[self.start : self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))

    def clear_input(self):
        self.tokens = []