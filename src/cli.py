import time

from src.Move import Move
from src.Player import Player, MinimaxBot
from src.TicTacToe import TicTacToe
from src.constants import Symbol


def cli_game():
    player_symbol = input("Choose your symbol: X or O: ")
    player_symbol = Symbol.CROSS if player_symbol == "X" else Symbol.CIRCLE
    player = Player(player_symbol)
    bot = MinimaxBot(Symbol.CROSS if player_symbol == Symbol.CIRCLE else Symbol.CIRCLE)
    game = TicTacToe((player, bot), 3)
    board = game.board

    while not board.game_over():
        print(str(board))
        if game.turn == player.symbol:
            valid_move = False
            while not valid_move:
                try:
                    pos: tuple = tuple(int(element) for element in
                                       input("Enter your move (row and col with a space between them): ").split(" "))
                    game.make_move(Move(pos, player.symbol))
                    valid_move = True
                except ValueError:
                    print("Invalid move\n")
                    continue
        else:
            time.sleep(0.5)
            game.make_move(bot.make_move(board))

    print(str(board))
    print("Game over.")


if __name__ == "__main__":
    cli_game()