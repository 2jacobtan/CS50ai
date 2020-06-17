"""
Tic Tac Toe Player
"""

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


def minimax_(board, prune):  # with pruning
    if terminal(board):
        outcome = utility(board)
        return (None, outcome)

    player_turn = player(board)
    isBetterOutcome = isBetterOutcome_factory(player_turn)
    next_prune = prune_factory(player_turn)

    action_set = actions(board)
    action_outcome_list = []

    for action in action_set:
        next_board = result(board, action)

        outcome = minimax_(next_board, next_prune)[1]

        # short-circuit when outcome is better or equal to prune
        if isBetterOutcome(outcome, prune):
            return (action,outcome)
        
        if isBetterOutcome(outcome,next_prune):
            next_prune = outcome 

        action_outcome_list.append((action,outcome))

    def reducer(x,y):
        return (x if isBetterOutcome(x[1],y[1]) else y)

    return reduce(reducer, action_outcome_list)


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    player_turn = player(board)
    
    prune = 1 if player_turn == X else -1 # opposite of prune_factory

    return minimax_(board, prune)[0]

def prune_factory(player_turn):
    # initialise with worst posible outcome for current player
    return (-1 if player_turn == X else 1)

def isBetterOutcome_factory(player_turn):
    return (
        (lambda x, y: x >= y) if player_turn == X else
        (lambda x, y: x <= y)
    )
