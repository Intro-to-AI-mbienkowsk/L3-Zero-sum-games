from src.constants import Symbol
from TicTacToe import Move
import random


class Player:
    def __init__(self, symbol: Symbol):
        self.symbol = symbol

    def possible_moves(self, board):
        return [Move(pos, self.symbol) for pos in board.available_moves()]


class Bot(Player):

    def __init__(self, symbol: Symbol):
        super().__init__(symbol)

    def make_move(self, board):
        pass


class MinimaxBot(Bot):
    def __init__(self, symbol: Symbol, depth):
        super().__init__(symbol)
        self.depth = depth

    def minimax(self, maximizing, board, alpha=float('-inf'), beta=float('inf')):
        """Evaluate the board using the minimax algorithm"""
        if board.game_over():
            return self.eval(board)

        if maximizing:
            best_outcome = float('-inf')
            sorting_key = max
        else:
            best_outcome = float('inf')
            sorting_key = min

        possible_positions = [board.after_move(move) for move in self.possible_moves(board)]
        for position in possible_positions:
            evaluation = self.minimax(maximizing, position)
            best_outcome = sorting_key(best_outcome, evaluation)
            alpha = max(alpha, evaluation)
            beta = min(beta, evaluation)
            if alpha >= beta:
                break

        return best_outcome

    def make_move(self, board):
        if board.is_empty((1, 1)):
            return Move((1, 1), self.symbol)
        maximizing = self.symbol == Symbol.CROSS
        moves = [(move, self.minimax(maximizing, board.after_move(move))) for move in self.possible_moves(board)]
        random.shuffle(moves)
        moves.sort(key=lambda t: t[1], reverse=maximizing)
        return moves[0][0]

    @staticmethod
    def eval(board):
        """Returns 1 if X has won the game, -1 if O has won, 0 otherwise."""
        winner = board.winner()
        if winner == Symbol.CROSS:
            return 1
        elif winner == Symbol.CIRCLE:
            return -1
        return 0


class RandomBot(Bot):
    def __init__(self, symbol: Symbol):
        super().__init__(symbol)

    def make_move(self, game):
        return random.choice(game.available_moves())
