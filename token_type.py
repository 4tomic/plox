from enum import Enum

class TokenType(Enum):
    # Single - character tokens.
    LEFT_PAREN = 1
    RIGHT_PAREN =2
    LEFT_BRACE =3
    RIGHT_BRACE =4
    COMMA = 5
    DOT = 6
    MINUS = 7
    PLUS = 8
    SEMICOLON = 9
    SLASH = 10
    STAR = 11

    # One or two character tokens.
    BANG = 21
    BANG_EQUAL = 22
    EQUAL = 23
    EQUAL_EQUAL = 24
    GREATER = 25
    GREATER_EQUAL = 26
    LESS = 27
    LESS_EQUAL = 28

    # Literals.
    IDENTIFIER = 31
    STRING = 32
    NUMBER = 33

    # Keywords.
    AND = 41
    CLASS = 42
    ELSE = 43
    FALSE = 44
    FUN = 45
    FOR = 46
    IF = 47
    NIL =48
    OR = 49
    PRINT = 50
    RETURN = 51
    SUPER = 52
    THIS = 53
    TRUE = 54
    VAR = 55
    WHILE = 56

    EOF = 100