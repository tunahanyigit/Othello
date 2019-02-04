
import random
import sys
import time

from othello_shared import get_possible_moves, get_score, play_move

dictionary = {}


# computes the utility of a final game board state
def compute_utility(board, color):
    if (color == 1):
        utility = get_score(board)[0] - get_score(board)[1]
        return utility
    elif (color == 2):
        utility = get_score(board)[1] - get_score(board)[0]
        return utility


############ MINIMAX ###############################

def minimax_min_node(board, color):
    # part-3 caching states
    if board in dictionary:
        return dictionary[board]

    # if terminal-test returns a utility value
    if not get_possible_moves(board, color):
        return compute_utility(board, color)

    # v = +infinity
    v = float('inf')
    for move in get_possible_moves(board, color):
        # player could be 1 or 2 then 3 - color makes reversed.
        v = min(v, minimax_max_node(play_move(board, color, move[0], move[1]), 3 - color))
        dictionary[board] = v
    return v


def minimax_max_node(board, color):
    # part-3 caching states
    if board in dictionary:
        return dictionary[board]

    # if terminal-test returns a utility value
    if not get_possible_moves(board, color):
        return compute_utility(board, color)

    # v = -infinity
    v = float('-inf')
    for move in get_possible_moves(board, color):
        # player could be 1 or 2 then 3 - color makes reversed.
        v = max(v, minimax_min_node(play_move(board, color, move[0], move[1]), 3 - color))
        dictionary[board] = v
    return v


def select_move_minimax(board, color):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  
    """

    v = float('-inf')
    for move in get_possible_moves(board, color):
        v = (max(v, minimax_min_node(play_move(board, color, move[0], move[1]), color)))
    for move in get_possible_moves(board, color):
        if v == (
                max(v, minimax_min_node(play_move(board, color, move[0], move[1]), color))):
            return move


############ ALPHA-BETA PRUNING #####################

# part-5 depth limit
def alphabeta_min_node(board, color, alpha, beta, level, limit):
    # def alphabeta_min_node(board, color, alpha, beta):
    v = float('inf')

    # part-3 caching states
    if board in dictionary:
        return dictionary[board]

    # part-5 depth limit
    if level >= limit:
        return compute_utility(board, color)

    # if terminal-test returns a utility value
    if not get_possible_moves(board, color):
        return compute_utility(board, color)

    # part-4 node ordering
    moves = node_ordering_sort(board, color)
    for move in moves:

        # part-5 recursive call with adding + 1 to level
        v = min(v,
                alphabeta_max_node(play_move(board, color, move[0], move[1]), 3 - color, alpha, beta, level + 1, limit))
        # v = min(v, alphabeta_max_node(play_move(board, color, move[0], move[1]), color, alpha, beta))
        dictionary[board] = v

        if v <= alpha:
            return v
        beta = min(beta, v)
    return v


def alphabeta_max_node(board, color, alpha, beta, level, limit):
    # def alphabeta_max_node(board, color, alpha, beta):
    v = float('-inf')

    if board in dictionary:
        return dictionary[board]

    if level >= limit:
        return compute_utility(board, color)

    if not get_possible_moves(board, color):
        return compute_utility(board, color)

    # part-4 node ordering
    moves = node_ordering_sort(board, color)
    for move in moves:
        v = max(v,
                alphabeta_min_node(play_move(board, color, move[0], move[1]), 3 - color, alpha, beta, level + 1, limit))

        # v = max(v, alphabeta_min_node(play_move(board, color, a[0], a[1]), color, alpha, beta))

        dictionary[board] = v

        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v


def select_move_alphabeta(board, color):
    alpha = float('-inf')
    beta = float('inf')
    v = float('-inf')

    for move in get_possible_moves(board, color):
        # v = (max(v, alphabeta_min_node(play_move(board, color, a[0], a[1]), color, alpha, beta)))
        v = (
            max(v, alphabeta_min_node(play_move(board, color, move[0], move[1]), color, alpha, beta, level=1, limit=1)))

    for move in get_possible_moves(board, color):
        if v == (
                max(v, alphabeta_min_node(play_move(board, color, move[0], move[1]), color, alpha, beta, level=1,
                                          limit=1))):
            return move


# part-4 node ordering
# Function to do insertion sort
def node_ordering_sort(board, color):
    # Traverse through 1 to len(arr)
    arr = get_possible_moves(board, color)
    for i in range(1, len(arr)):

        # key = arr[i]
        key = compute_utility(play_move(board, color, arr[i][0], arr[i][1]), color)

        j = i - 1
        # while j >= 0 and key < arr[j]:
        while j >= 0 and key > compute_utility(play_move(board, color, arr[j][0], arr[j][1]), color):
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


####################################################
def run_ai():
    """
    This function establishes communication with the game manager. 
    It first introduces itself and receives its color. 
    Then it repeatedly receives the current score and current board state
    until the game is over. 
    """
    print("Minimax AI")  # First line is the name of this AI
    color = int(input())  # Then we read the color: 1 for dark (goes first),
    # 2 for light.

    while True:  # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input()
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL":  # Game is over.
            print
        else:
            board = eval(input())  # Read in the input and turn it into a Python
            # object. The format is a list of rows. The
            # squares in each row are represented by
            # 0 : empty square
            # 1 : dark disk (player 1)
            # 2 : light disk (player 2)

            # Select the move and send it to the manager 
            movei, movej = select_move_minimax(board, color)
            # movei, movej = select_move_alphabeta(board, color)
            print("{} {}".format(movei, movej))


if __name__ == "__main__":
    run_ai()
