from src.constants import Symbol
import random

class Player:
    def __init__(self, symbol: Symbol):
        self.symbol = symbol

class Bot(Player):

    def __init__(self, symbol: Symbol):
        super().__init__(symbol)

    def make_move(self, board):
        pass


class MinimaxBot(Bot):
    def __init__(self, symbol: Symbol, depth):
        super().__init__(symbol)
        self.depth = depth

    def minimax(self, board, depth, alpha, beta):
        pass

    def make_move(self, board):
        pass


class RandomBot(Bot):
    def __init__(self, symbol: Symbol):
        super().__init__(symbol)

    def make_move(self, game):
        return random.choice(game.available_moves())
