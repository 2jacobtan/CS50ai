"""
Tic Tac Toe Player
"""

import math
from functools import reduce

X = "X"
O = "O"
EMPTY = None


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
    x_count = 0
    o_count = 0
    for row in board:
        for cell in row:
            if cell == X:
                x_count += 1
            elif cell == O:
                o_count += 1
    return X if x_count == o_count else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell is None:
                possible_actions.add((i, j))
    
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        # print("terminal(board):", terminal(board))
        # for row in board:
        #     print(row)
        # print(action)
        raise ValueError("invalid action")

    new_board = [[cell for cell in row] for row in board]
    new_board[action[0]][action[1]] = player(board)

    return new_board


winning_lines = (
    [[(i, j) for j in range(3)] for i in range(3)] +  # horizontals
    [[(i, j) for i in range(3)] for j in range(3)] +  # verticals
    [[(k, k) for k in range(3)]] +  # backslash diagonal
    [[(k, 2-k) for k in range(3)]]  # forwardslash diagonal
)


def line_winner(line, board):
    x2, y2 = line[2]
    symbol = board[x2][y2]
    for i in range(2):
        x, y = line[i]
        if board[x][y] != symbol:
            return None
    return symbol


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for line in winning_lines:
        maybe_winner = line_winner(line, board)
        if maybe_winner != None:
            return maybe_winner
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True
    
    # if no winner and at least one empty cell available
    for row in board:
        for cell in row:
            if cell is None:
                return False

    # else game is over
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    maybe_winner = winner(board)
    symbols = [None, X, O]
    values = [0, 1, -1]
    for symbol, value in zip(symbols, values):
        if maybe_winner == symbol:
            return value

# mutual recursion with minimax()
def action_outcome(board, action): # ::board, action -> int
    
    # print("__action_outcome__ board before result()")
    # for row in board:
    #     print(row)
    
    next_board = result(board,action)

    # print("__action_outcome__ next_board after result()")
    # for row in next_board:
    #     print(row)
    
    if terminal(next_board):
        # print("*** action_outcome early return")
        return utility(next_board)
    else:
        next_action = minimax(next_board)

        # print("*** action_outcome calls action_outcome")
        return action_outcome(next_board, next_action)


# mutual recursion with action_outcome()
def minimax(board):  # with pruning
    """
    Returns the optimal action for the current player on the board.
    """
    player_turn = player(board)
    preferred_outcome = 1 if player_turn == X else -1

    action_list = list(actions(board))
    outcome_list = []

    for action in action_list:
        # print("*** minimax calls action_outcome")
        outcome = action_outcome(board, action)

        # pruning
        if outcome == preferred_outcome:
            return action

        outcome_list.append(outcome)

    action_outcome_zip = zip(action_list, outcome_list)

    comparison_function = (
        (lambda x, y: x if x[1] >= y[1] else y) if player_turn == X else
        (lambda x, y: x if x[1] <= y[1] else y)
    )
    # try:
    return reduce(comparison_function, action_outcome_zip)[0]
    # except Exception as e:
    #     print(list(zip(action_list, outcome_list)))
    #     for row in board:
    #         print(row)
    #     raise e
