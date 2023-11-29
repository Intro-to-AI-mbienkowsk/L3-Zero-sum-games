from src.Player import RandomBot, MinimaxBot
from src.TicTacToe import TicTacToe
from src.constants import Symbol, EXP_DEFAULT_NUM_OF_GAMES
from argparse import ArgumentParser
import matplotlib.pyplot as plt


def plot_results(data, bots):
    fig = plt.figure()
    labels = [str(bot) for bot in bots]
    labels.append("Draw")

    x_data = labels
    plt.bar(x_data, data, color=["#e3d97f", "#5c4219", "#e6cea8"])

    fig.set_facecolor("lightblue")
    plt.ylabel('Number of games')
    plt.title(f'Count of winners in {sum(data)} matches', weight='semibold')
    plt.show()


def single_game(bots):
    bot_1, bot_2 = bots
    game = TicTacToe(bots)
    while not game.board.game_over():
        bot_to_move = bot_1 if bot_1.symbol == game.turn else bot_2
        game.make_move(bot_to_move.make_move(game.board))
    winner = game.board.winner()
    return winner if winner is not None else Symbol.EMPTY


def experiment(bots, n_games):
    results = {Symbol.CROSS: 0, Symbol.CIRCLE: 0, Symbol.EMPTY: 0}
    for _ in range(n_games):
        results[single_game(bots)] += 1

    plot_results((results[Symbol.CROSS], results[Symbol.CIRCLE], results[Symbol.EMPTY]), bots)
    return results


def minimax_vs_minimax_experiment(n_games):
    experiment((MinimaxBot(Symbol.CROSS), MinimaxBot(Symbol.CIRCLE)), n_games)


def random_vs_random_experiment(n_games):
    experiment((RandomBot(Symbol.CROSS), RandomBot(Symbol.CIRCLE)), n_games)


def minimax_vs_random_experiment(n_games, minimax_symbol=Symbol.CROSS):
    random_symbol = Symbol.CIRCLE if minimax_symbol == Symbol.CROSS else Symbol.CROSS
    bots = (MinimaxBot(minimax_symbol), RandomBot(random_symbol)) if minimax_symbol == Symbol.CROSS else (
        RandomBot(random_symbol), MinimaxBot(minimax_symbol))
    return experiment(bots, n_games)


def launch_experiment(x_bot, o_bot, n):
    if x_bot == o_bot == "m":
        minimax_vs_minimax_experiment(n)
    elif x_bot == o_bot == "r":
        random_vs_random_experiment(n)
    else:
        minimax_symbol = Symbol.CROSS if x_bot == "m" else Symbol.CIRCLE
        minimax_vs_random_experiment(n, minimax_symbol)


def main():
    parser = ArgumentParser(description='Run a tic-tac-toe bot experiment.')
    parser.add_argument('-n', '--num_games', type=int, default=EXP_DEFAULT_NUM_OF_GAMES)
    parser.add_argument('-X', type=str, default="m",
                        help="Which bot should play X (go first) - m for minimax, r for random")
    parser.add_argument('-O', type=str, default="r",
                        help="Which bot should play O (go second) - m for minimax, r for random")
    args = parser.parse_args()
    if args.n <= 0:
        raise ValueError("Number of games has to be a positive integer.")
    if not (args.X and args.O in ("m", "r")):
        raise ValueError("X and O bots have to be one of (m, r)")


if __name__ == '__main__':
    main()
