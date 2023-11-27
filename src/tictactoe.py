from random import shuffle
from copy import deepcopy
from enum import Enum


X = 'X'
O = 'O'
EMPTY = None

class InvalidMoveError(ValueError):
    """
    Error called when an invalid move is passed into the result function
    """
    pass


def count_occurences(board: list, symbol: str):
    """
    Count the occurences of a symbol on the board - how
    many moves has a certain player already made
    """
    return sum(
        row.count(symbol)
        for row in board
    )


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if count_occurences(board, X) == count_occurences(board, O):
        return X
    return O


def is_empty(field: str):
    return field == EMPTY


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    return set((x, y)
               for x in range(3)
               for y in range(3)
               if is_empty(board[x][y]))


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    Does not modify the original board.
    """
    if action not in actions(board):
        raise InvalidMoveError("This field is taken!")

    row, col = action
    board_copy = deepcopy(board)
    board_copy[row][col] = player(board_copy)
    return board_copy


def possible_winning_lines(board):
    """
    Returns a list of tuples, where each tuple is
    the contents of one of the lines that one can
    win the game by taking
    """
    lines = [tuple(row) for row in board]  # initialize the list with all the horizontal lines
    lines.extend([(board[0][i], board[1][i], board[2][i]) for i in range(3)])  # add vertical lines
    lines.extend([(board[0][i], board[1][1], board[2][2 if i == 0 else 0]) for i in range(0, 3, 2)])  # diagonals
    return lines


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    state_of_lines = possible_winning_lines(board)
    for line in state_of_lines:
        if line[0] == line[1] == line[2] != EMPTY:
            return line[0]
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None or len(actions(board)) == 0:
        return True
    return False


def eval(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winning_player = winner(board)
    if winning_player == X:
        return 1
    elif winning_player == O:
        return -1
    return 0


def min_or_max_value(board, alpha=float('-inf'), beta=float('inf')):
    """
    Both min and max value methods combined into one - chooses to return either the min or max
    value in the tree, depending on the player to move. Alpha-beta pruning is also implemented.
    """

    maximizing = True if player(board) == X else False
    possible_positions = [result(board, action) for action in actions(board)]

    if terminal(board):
        return eval(board)

    if maximizing:
        best_val = float('-inf')
        sorting_fun = max
    else:
        best_val = float('inf')
        sorting_fun = min

    for position in possible_positions:
        position_eval = min_or_max_value(position, alpha, beta)
        best_val = sorting_fun(best_val, position_eval)
        alpha = sorting_fun(alpha,
                            position_eval)
        if beta <= alpha:
            break

    return best_val


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    Since the evaluation function rates the position just based on the end result
    with optimal play, during the 1st turn, all moves are evaluated equally (as draws),
    so taking the middle square if it is empty during the bot's first turn is hardcoded.
    """

    if board == initial_state() or (len(actions(board)) == 8 and is_empty(board[1][1])):
        return 1, 1

    move_eval_dict = {action: min_or_max_value(result(board, action)) for action in
                      actions(board)}
    possible_positions = [(k, v) for k, v in move_eval_dict.items()]
    shuffle(possible_positions)  # we want the bot to be non-deterministic, so we
    # shuffle the options, as many moves will be rated equally - even though the
    # list will be sorted later, the order here matters

    reverse = True if player(board) == X else False
    # The order we want the positions in - either the min or the max will be first, since
    # the first element of the list is chosen as the move to go for
    possible_positions.sort(reverse=reverse, key=lambda x: x[1])

    return possible_positions[0][0]
