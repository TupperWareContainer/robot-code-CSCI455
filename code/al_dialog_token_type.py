from enum import Enum, auto

class TokenType(Enum):
    STRING = auto()
    VAR = auto()
    DEFINITION = auto()
    VAR_CAPTURE = auto()
    VAR_RECALL = auto()  # $name
    LEFT_BRACKET = auto()
    RIGHT_BRACKET = auto()
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    COLON = auto()
    ACTION = auto()
    LEVEL = auto()  # u, u1, u2
    NEWLINE = auto()
    EOF = auto()
    RIGHT_CURLY = auto()
    LEFT_CURLY = auto()