from constants import BOARD_SIZE, Symbol
from Player import Player
from copy import deepcopy


class TicTacToe:
    def empty_board(self):
        return [[Symbol.EMPTY for _ in range(self.board_size)] for _ in range(self.board_size)]

    def is_empty(self, pos):
        return self.board[pos[0]][pos[1]] == Symbol.EMPTY

    def __init__(self, players: tuple[Player], board_size=BOARD_SIZE):
        self.players = players
        self.board_size = board_size
        self.board = self.empty_board()
        self.turn = Symbol.CROSS

    def available_moves(self):
        return set((y, y) for y in range(self.board_size) for x in range(self.board_size) if self.is_empty((y, x)))

    def possible_winning_lines(self):
        """ Return lists of board cell content, representing lines, that if taken by a player.
        would mean he won
        """
        lines = [tuple(row) for row in self.board]
        lines.extend([tuple(self.board[i][j] for i in range(self.board_size)) for j in range(self.board_size)])
        lines.extend([tuple(self.board[i][i] for i in range(self.board_size))])
        return lines

    def winner(self):
        """ Return the winner of the game, if there is one """
        for line in self.possible_winning_lines():
            if all(cell == line[0] for cell in line) and line[0] != Symbol.EMPTY:
                return line[0]
        return None

    def is_tie(self):
        return self.winner() is None and len(self.available_moves()) == 0

    def eval(self):
        """Returns 1 if X has won the game, -1 if O has won, 0 otherwise."""
        winner = self.winner()
        if winner == Symbol.CROSS:
            return 1
        elif winner == Symbol.CIRCLE:
            return -1
        return 0

    def board_after_move(self, move):
        """Returns a copy of the board after making a move"""
        if move not in self.available_moves():
            raise ValueError("Invalid move")

        board_copy = deepcopy(self.board)
        row, col = move
        board_copy[row][col] = self.turn
        return board_copy

    def make_move(self, move):
        """Makes a move on the board"""
        if move not in self.available_moves():
            raise ValueError("Invalid move")

        row, col = move
        self.board[row][col] = self.turn
        self.turn = Symbol.CIRCLE if self.turn == Symbol.CROSS else Symbol.CROSS
