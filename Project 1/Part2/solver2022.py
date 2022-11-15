#!/usr/local/bin/python3
# solver2022.py : 2022 Sliding tile puzzle solver
#
#
# Based on skeleton code by D. Crandall & B551 Staff, Fall 2022
#

import sys
from queue import PriorityQueue
from copy import deepcopy
import math

ROWS = 5
COLS = 5


def printable_board(board):
    return [('%3d ') * COLS % board[j:(j + COLS)] for j in range(0, ROWS * COLS, COLS)]


def move_right(row):
    # e.g. [1,2,3,4] -> [4,1,2,3]
    start = [row[-1]]
    start.extend(row)
    return start[:len(start) - 1]


def move_left(row):
    # e.g. [1,2,3,4] -> [2,3,4,1]
    start = row[1:len(row)]
    start.extend([row[0]])
    return start


def occ(state):
    new_state = deepcopy(list(state))
    new_state[0] = state[1]
    new_state[1] = state[2]
    new_state[2] = state[3]
    new_state[3] = state[4]
    new_state[4] = state[9]

    new_state[5] = state[0]
    new_state[9] = state[14]

    new_state[10] = state[5]
    new_state[14] = state[19]

    new_state[15] = state[10]
    new_state[19] = state[24]

    new_state[20] = state[15]
    new_state[21] = state[20]
    new_state[22] = state[21]
    new_state[23] = state[22]
    new_state[24] = state[23]

    return tuple(new_state)


def oc(state):
    res = occ(state)
    for i in range(0, 14):
        res = occ(res)
    return res


def ic(state):
    new_state = deepcopy(list(state))
    new_state[6] = state[11]
    new_state[7] = state[6]
    new_state[8] = state[7]

    new_state[11] = state[16]
    new_state[13] = state[8]

    new_state[16] = state[17]
    new_state[17] = state[18]
    new_state[18] = state[13]

    return tuple(new_state)


def icc(state):
    res = ic(state)
    for i in range(0, 6):
        res = ic(res)
    return res


# return a list of possible successor states
def successors(state):
    # return format should be like this:
    # [(operation code, [state]), (operation code, [state]), ...]
    # doint 'L' operation
    successors = []

    # left operation for each row
    for i in range(1, 6):
        operation = "L" + str(i)
        new_state = list(deepcopy(state))
        new_state[(i - 1) * 5:i * 5] = move_left(new_state[(i - 1) * 5:i * 5])
        successors.append((operation, tuple(new_state)))

    # right operation for each row
    for i in range(1, 6):
        operation = "R" + str(i)
        new_state = list(deepcopy(state))
        new_state[(i - 1) * 5:i * 5] = move_right(new_state[(i - 1) * 5:i * 5])
        successors.append((operation, tuple(new_state)))

    # down operation for each column
    for i in range(1, 6):
        operation = "D" + str(i)
        state_in_2d = []
        for col in range(1, 6):
            temp_col = []
            for row in range(1, 6):
                # print('col:'+str(col)+' row:'+str(row))
                temp_col.append(state[(row - 1) * 5 + col - 1])
            state_in_2d.append(temp_col)

        # print(state_in_2d)
        state_in_2d[i - 1] = move_right(state_in_2d[i - 1])
        # print(state_in_2d)
        new_state = []
        for row in range(1, 6):
            for col in state_in_2d:
                new_state.append(col[row - 1])

        # print(new_state)
        successors.append((operation, tuple(new_state)))

    # up operation for each column
    for i in range(1, 6):
        operation = "U" + str(i)
        state_in_2d = []
        for col in range(1, 6):
            temp_col = []
            for row in range(1, 6):
                # print('col:'+str(col)+' row:'+str(row))
                temp_col.append(state[(row - 1) * 5 + col - 1])
            state_in_2d.append(temp_col)

        # print(state_in_2d)
        state_in_2d[i - 1] = move_left(state_in_2d[i - 1])
        # print(state_in_2d)
        new_state = []
        for row in range(1, 6):
            for col in state_in_2d:
                new_state.append(col[row - 1])

        # print(new_state)
        successors.append((operation, tuple(new_state)))

    successors.append((("Oc"), oc(state)))
    successors.append((("Occ"), occ(state)))
    successors.append((("Ic"), ic(state)))
    successors.append((("Icc"), icc(state)))

    return successors


def heuristic(state):
    dist = 0
    for row in range(1, 6):
        for column in range(1, 6):
            val = state[(row - 1) * 5 + column - 1]
            dest_row = (val - 1) // 5 + 1
            dest_col = (val - 1) % 5 + 1
            dist+=((row-dest_row)**2+(column-dest_col)**2)**(1/2)
           # dist += abs(dest_col-column)+abs(dest_row-row)
    return dist/4


# check if we've reached the goal
def is_goal(state):
    return state == tuple(range(1, len(state) + 1))


def solve(initial_board):
    """
    1. This function should return the solution as instructed in assignment, consisting of a list of moves like ["R2","D2","U1"].
    2. Do not add any extra parameters to the solve() function, or it will break our grading and testing code.
       For testing we will call this function with single argument(initial_board) and it should return 
       the solution.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """
    if is_goal(initial_board):
        return []
    fringe = PriorityQueue()
    initial_g = 0
    initial_h = heuristic(initial_board)
    dict1 = {}
    fringe.put((initial_h + initial_g, initial_h, initial_g, initial_board, []))
    dict1[initial_board] = 1
    while not fringe.empty():
        (curr_f, curr_h, curr_g, board, operations) = fringe.get()

        print(str(curr_h) + "  " + str(operations) + "\n" + "\n".join(printable_board(board)))

        if is_goal(board):
            return operations
        successors_lst = successors(board)
        # for s in successors_lst:
        #     print(s[0]+"\n" +"\n".join(printable_board(tuple(s[1]))))
        heu_lst = []
        for s in successors_lst:
            heu = heuristic(s[1])
            heu_lst.append(heu)
            # next_f = curr_g + 1 + heuristic(s[1])
            # if 'L' in s[0] or 'R' in s[0]  or 'U' in s[0] or 'D' in s[0]:
            #     next_g = curr_g + 5
            # elif 'O' in s[0]:
            #     next_g = curr_g + 16
            # else:
            #     next_g = curr_g + 8
            next_g = curr_g + 1
            next_h = heuristic(s[1])
            next_f = next_g + next_h
            if s[1] not in dict1.keys():
                fringe.put((next_f, next_h, next_g, s[1], operations + [s[0]]))
                dict1[s[1]] = 1

        print("min heu in successors: " + str(min(heu_lst)))

    return []


# Please don't modify anything below this line
#
if __name__ == "__main__":
    if (len(sys.argv) != 2):
        raise (Exception("Error: expected a board filename"))

    start_state = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [int(i) for i in line.split()]

    if len(start_state) != ROWS * COLS:
        raise (Exception("Error: couldn't parse start state file"))

    print("Start state: \n" + "\n".join(printable_board(tuple(start_state))))

    print("Solving...")
    route = solve(tuple(start_state))

    print("Solution found in " + str(len(route)) + " moves:" + "\n" + " ".join(route))
