from enum import Enum

class TokenType(Enum):
    STRING = 0
    VAR = 1
    DEFINITION = 2
    VAR_CAPTURE = 3
    LEFT_BRACKET = 4
    RIGHT_BRACKET = 5
    COLON = 6