"""
Tic Tac Toe Player
"""

from copy import deepcopy
from math import inf

X = "X"
O = "O"
EMPTY = None

# ---------------HELPER---------------


def maxMinValue(board):
    if terminal(board):
        return utility(board)
    value = -inf
    for action in actions(board):
        value = max(value, minimum(result(board, action)))

    return value


def minimum(board):
    if terminal(board):
        return utility(board)
    value = inf
    for action in actions(board):
        value = min(value, maxMinValue(result(board, action)))

    return value
# ---------------HELPER----------------


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
    xCount = 0
    oCount = 0

    for row in board:
        for cell in row:
            if cell == X:
                xCount += 1
            elif cell == O:
                oCount += 1

    if xCount <= oCount:
        return 'X'
    else:
        return 'O'


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    possibleActionSet = set()

    for row in range(3):
        for cell in range(3):
            if board[row][cell] == EMPTY:
                possibleActionSet.add((row, cell))

    return possibleActionSet


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    if terminal(board):
        raise ValueError("Game over.")

    row = action[0]
    cell = action[1]
    copyBoard = deepcopy(board)
    copyBoard[row][cell] = player(board)

    return copyBoard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # checks diagonal decline
    diagonalCheck = board[0][0]
    diagonalCount = 0
    for cell in range(3):
        if board[cell][cell] == diagonalCheck:
            diagonalCount += 1
        else:
            break
    if diagonalCount == 3:
        return diagonalCheck

    # checks horizontally for wins
    for row in range(3):
        xScore = 0
        oScore = 0
        for column in range(3):
            if board[row][column] == X:
                xScore += 1
            elif board[row][column] == O:
                oScore += 1
        if xScore == 3:
            return X
        elif oScore == 3:
            return O

    # checks vertically for wins
    for row in range(3):
        xScore = 0
        oScore = 0
        for column in range(3):
            if board[column][row] == X:
                xScore += 1
            elif board[column][row] == O:
                oScore += 1
        if xScore == 3:
            return X
        elif oScore == 3:
            return O

    if board[0][2] == board[1][1] == board[2][0] != None:
        return board[0][2]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    # if there is a winner end game
    if winner(board) != None:
        return True

    # if there are no more space return true
    for row in range(3):
        for column in range(3):
            if board[row][column] == None:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    if winner(board) == X:
        return 1

    elif winner(board) == O:
        return -1

    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if board == initial_state():
        return (0, 0)

    elif player(board) == X:
        optimalMove = None
        value = -inf
        for action in actions(board):
            minValueResult = inf
            if terminal(board):
                minValueResult = utility(board)
            else:
                for action in actions(board):
                    minValueResult = min(
                        minValueResult, maxMinValue(result(board, action)))

            if minValueResult > value:
                value = minValueResult
                optimalMove = action

    elif player(board) == O:
        optimalMove = None
        value = inf
        for action in actions(board):
            maxValueResult = -inf
            if terminal(board):
                maxValueResult = utility(board)
            else:
                for action in actions(board):
                    maxValueResult = max(maxValueResult, minimum(result(board, action)))
            
            if maxValueResult < value:
                value = maxValueResult
                optimalMove = action

    return optimalMove
