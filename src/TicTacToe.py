from src.Move import Move
from src.constants import BOARD_SIZE, Symbol, symbol_to_string
from copy import deepcopy


class TicTacToe:

    def __init__(self, players: tuple, board_size=BOARD_SIZE):
        self.players = players
        self.board = Board(board_size)
        self.turn = Symbol.CROSS

    def change_turn(self):
        self.turn = Symbol.CROSS if self.turn == Symbol.CIRCLE else Symbol.CIRCLE

    def make_move(self, move):
        self.board.make_move(move)
        self.change_turn()


class Board:
    def __init__(self, size: int):
        self.size = size
        self.fields = self.empty_board()

    def __getitem__(self, row):
        return self.fields[row]

    def __setitem__(self, indices, value: Symbol):
        row, col = indices
        self.fields[row][col] = value

    def empty_board(self):
        return [[Symbol.EMPTY for _ in range(self.size)] for _ in range(self.size)]

    def is_empty(self, pos):
        row, col = pos
        return self[row][col] == Symbol.EMPTY

    def available_moves(self):
        return [(row, col) for row in range(self.size) for col in range(self.size) if self.is_empty((row, col))]

    def after_move(self, move: Move):
        """Returns a copy of the board after making a move"""
        if move.pos not in self.available_moves():
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
        lines.extend([tuple(self[2 - i][i] for i in range(self.size))])
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

    def game_over(self):
        return self.winner() is not None or not self.available_moves()

    def __str__(self):
        result = ""
        for row in self:
            row_str = "|"
            for cell in row:
                row_str += f" {symbol_to_string(cell)} |"
            row_str += "\n"
            result += row_str
        return result
