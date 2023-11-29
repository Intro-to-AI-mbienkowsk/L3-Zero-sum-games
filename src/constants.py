from dataclasses import dataclass
from enum import Enum

BOARD_SIZE = 3
EXP_DEFAULT_NUM_OF_GAMES = 50


class Symbol(Enum):
    CROSS = 1,
    CIRCLE = 2,
    EMPTY = 3


class Gamemode(Enum):
    PVB = 1
    BVB = 2
    NONE = 3


@dataclass(frozen=True)
class Move:
    pos: tuple[int, int]
    symbol: Symbol


def symbol_to_string(symbol):
    if symbol == Symbol.CROSS:
        return 'X'
    elif symbol == Symbol.CIRCLE:
        return 'O'
    return ' '
