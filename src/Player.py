from src.Move import Move
from src.constants import Symbol
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


class MinimaxBot(Bot):
    def __init__(self, symbol: Symbol):
        super().__init__(symbol)

    def minimax(self, maximizing, board, alpha=float('-inf'), beta=float('inf')):
        """Evaluate the board using the minimax algorithm"""
        if board.game_over():
            return self.eval(board)

        possible_moves = [Move(pos, Symbol.CROSS if maximizing else Symbol.CIRCLE) for pos in board.available_moves()]
        possible_positions = [board.after_move(move) for move in possible_moves]

        if maximizing:
            best_outcome = float('-inf')
            for position in possible_positions:
                evaluation = self.minimax(not maximizing, position, alpha, beta)
                best_outcome = max(best_outcome, evaluation)
                if evaluation > beta:
                    break
                beta = min(beta, evaluation)

        else:
            best_outcome = float('inf')
            for position in possible_positions:
                evaluation = self.minimax(not maximizing, position, alpha, beta)
                best_outcome = min(best_outcome, evaluation)
                if evaluation < alpha:
                    break
                alpha = max(alpha, evaluation)

        return best_outcome

    def make_move(self, board):
        if board.is_empty((1, 1)):
            return Move((1, 1), self.symbol)
        maximizing = self.symbol == Symbol.CROSS
        moves = [(move, self.minimax(not maximizing, board.after_move(move))) for move in self.possible_moves(board)]
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

    def make_move(self, board):
        return random.choice(self.possible_moves(board))
