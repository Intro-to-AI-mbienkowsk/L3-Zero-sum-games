from dataclasses import dataclass
from src.constants import Symbol


@dataclass(frozen=True)
class Move:
    pos: tuple[int, int]
    symbol: Symbol
