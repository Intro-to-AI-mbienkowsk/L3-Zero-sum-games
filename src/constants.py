from enum import Enum

BOARD_SIZE = 3


class Symbol(Enum):
    CROSS = 1,
    CIRCLE = 2,
    EMPTY = 3


class Gamemode(Enum):
    PVB = 1
    BVB = 2
    NONE = 3


def symbol_to_string(symbol):
    if symbol == Symbol.CROSS:
        return 'X'
    elif symbol == Symbol.CIRCLE:
        return 'O'
    return ' '
