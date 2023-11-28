from dataclasses import dataclass

from src.constants import BOARD_SIZE, Symbol
from src.Player import Player
from copy import deepcopy


@dataclass(frozen=True)
class Move:
    pos: tuple[int, int]
    symbol: Symbol


class TicTacToe:

    def __init__(self, players: tuple, board_size=BOARD_SIZE):
        self.players = players
        self.board = Board(board_size)
        self.turn = Symbol.CROSS


class Board:
    def __init__(self, size: int):
        self.size = size
        self.fields = self.empty_board()

    def __getitem__(self, indices):
        row, col = indices
        return self.fields[row][col]

    def __setitem__(self, indices, value: Symbol):
        row, col = indices
        self.fields[row][col] = value

    def empty_board(self):
        return [[Symbol.EMPTY for _ in range(self.size)] for _ in range(self.size)]

    def is_empty(self, pos):
        row, col = pos
        return self[row][pos] == Symbol.EMPTY

    def available_moves(self):
        return [(row, col) for row in range(self.size) for col in range(self.size) if self.is_empty((row, col))]

    def after_move(self, move: Move):
        """Returns a copy of the board after making a move"""
        if move not in self.available_moves():
            raise ValueError("Invalid move")

        board_copy = deepcopy(self)
        board_copy.make_move(move)
        return board_copy

    def possible_winning_lines(self):
        """ Return lists of board cell content, representing lines, that if taken by a player.
        would mean he won
        """
        lines = [tuple(row) for row in self]
        lines.extend([tuple(self[i][j] for i in range(self.size)) for j in range(self.size)])
        lines.extend([tuple(self[i][i] for i in range(self.size))])
        return lines

    def make_move(self, move: Move):
        """Makes a move on the board"""
        if move.pos not in self.available_moves():
            raise ValueError("Invalid move")
        row, col = move.pos
        self[row][col] = move.symbol

    def winner(self):
        """ Return the winner of the game, if there is one """
        for line in self.possible_winning_lines():
            if all(cell == line[0] for cell in line) and line[0] != Symbol.EMPTY:
                return line[0]
        return None

    def is_tie(self):
        return self.winner() is None and len(self.available_moves()) == 0

    def game_over(self):
        return self.winner() is not None or self.is_tie()