from functools import cache

from src.constants import Symbol, symbol_to_string, Move
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
        ...

    def __str__(self):
        ...


class MinimaxBot(Bot):
    def __init__(self, symbol: Symbol):
        super().__init__(symbol)

    def minimax(self, maximizing, board, moves_deep, alpha=float('-inf'), beta=float('inf')):
        """Evaluate the board using the minimax algorithm"""
        if board.game_over():
            depth_penalty = -.1 * moves_deep if maximizing else .1 * moves_deep
            return self.eval(board) - depth_penalty

        possible_moves = [Move(pos, Symbol.CROSS if maximizing else Symbol.CIRCLE) for pos in board.available_moves()]
        possible_positions = [board.after_move(move) for move in possible_moves]

        if maximizing:
            best_outcome = float('-inf')
            for position in possible_positions:
                evaluation = self.minimax(not maximizing, position, moves_deep + 1, alpha, beta)
                best_outcome = max(best_outcome, evaluation)
                if evaluation > beta:
                    break
                alpha = max(alpha, evaluation)

        else:
            best_outcome = float('inf')
            for position in possible_positions:
                evaluation = self.minimax(not maximizing, position, moves_deep + 1, alpha, beta)
                best_outcome = min(best_outcome, evaluation)
                if evaluation < alpha:
                    break
                beta = min(beta, evaluation)

        return best_outcome

    def make_move(self, board):
        if board.is_empty((1, 1)):
            return Move((1, 1), self.symbol)
        maximizing = self.symbol == Symbol.CROSS
        moves = [(move, self.minimax(not maximizing, board.after_move(move), 0)) for move in self.possible_moves(board)]
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

    def __str__(self):
        return f"Minimax ({symbol_to_string(self.symbol)})"


class RandomBot(Bot):
    def __init__(self, symbol: Symbol):
        super().__init__(symbol)

    def make_move(self, board):
        return random.choice(self.possible_moves(board))

    def __str__(self):
        return f"Random ({symbol_to_string(self.symbol)})"
