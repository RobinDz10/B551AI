#
# raichu.py : Play the game of Raichu
#
#
# Based on skeleton code by D. Crandall, Oct 2021
#
import sys
import time
import math
import multiprocessing
import next_level as nl

def board_to_string(board, N):
    return "\n".join(board[i:i+N] for i in range(0, len(board), N))

def terminate(board):
    return ('w' not in board and 'W' not in board and '@' not in board) or \
           ('b' not in board and 'B' not in board and '$' not in board)

def evaluate(board):
    pawns = "wW@bB$"
    n = [board.count(p) for p in pawns]

    return n[0] + 10*n[1] + 100*n[2] -n[3] -10*n[4] -100*n[5]


def minimax(board, depth, player, alpha, beta, boardSize):
    if depth == 0 or terminate(board):
        return evaluate(board), board
    children = nl.pichu(board, player, boardSize) + nl.pikachu(board, player, boardSize) +nl.raichu(board, player, boardSize)
    children = children[::-1]
    if not children: return 0, board
    bestMove = ""
    if player == 'w':
        value = -math.inf
        for child in children:
            score, tmp= minimax(child, depth - 1, 'b', alpha, beta, boardSize)
            if value < score:
                value = score
                bestMove = child
            if score > beta:
               break #β cutoff
            alpha = max(alpha, value)
            return value, bestMove

    else:
        value = math.inf
        for child in children:
            score, tmp = minimax(child, depth - 1, 'w', alpha, beta, boardSize)
            if score < value:
                value = score
                bestMove = child
            if value < alpha:
               break #α cutoff
            beta = min(beta, value)
            return value, bestMove

def minimax_search(board, player, boardSize):
    depth = 10
    while(True):
        s, nextMove = minimax(board, depth, player, -math.inf, math.inf, boardSize)
        print(nextMove)
        s+= 5

def find_best_move(board, N, player, timelimit):
    # This sample code just returns the same board over and over again (which
    # isn't a valid move anyway.) Replace this with your code!
    #
    
    p = multiprocessing.Process(target=minimax_search, name="minimax_search", args=(board, player, N))
    p.start()
    p.join(timelimit)
    p.terminate()

if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise Exception("Usage: Raichu.py N player board timelimit")
        
    (_, N, player, board, timelimit) = sys.argv
    N=int(N)
    timelimit=int(timelimit)
    if player not in "wb":
        raise Exception("Invalid player.")

    #if len(board) != N*N or 0 in [c in "wb.WB@$" for c in board]:
    #    raise Exception("Bad board string.")

    print("Searching for best move for " + player + " from board state: \n" + board_to_string(board, N))
    print("Here's what I decided:")

    find_best_move(board, N, player, timelimit)
