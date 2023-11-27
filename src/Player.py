from constants import Symbol


class Player:
    def __init__(self, symbol: Symbol):
        self.symbol = symbol

    def __str__(self):
        return 'X' if self.symbol == Symbol.CROSS else 'O'


class Bot(Player):

    def __init__(self, symbol: Symbol):
        super().__init__(symbol)

    def make_move(self):
        pass


class MinimaxBot(Bot):
    def __init__(self, symbol: Symbol, depth):
        super().__init__(symbol)
        self.depth = depth

    def minimax(self, board, depth, alpha, beta):
        pass

    def make_move(self):
        pass


class RandomBot(Bot):
    def __init__(self, symbol: Symbol):
        super().__init__(symbol)

    def make_move(self):
        pass
