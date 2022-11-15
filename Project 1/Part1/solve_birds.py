#!/usr/local/bin/python3
# solve_birds.py : Bird puzzle solver
#
#
# Based on skeleton code by D. Crandall & B551 course staff, Fall 2022
#
# N birds stand in a row on a wire, each wearing a t-shirt with a number.
# In a single step, two adjacent birds can swap places. How can
# they rearrange themselves to be in order from 1 to N in the fewest
# possible steps?

# !/usr/bin/env python3
import sys
from queue import PriorityQueue
N=5

#####
# THE ABSTRACTION:
#
# Initial state:

# Goal state:
# given a state, returns True or False to indicate if it is the goal state
def is_goal(state):
    return state == list(range(1, N+1))

# Successor function:
# given a state, return a list of successor states
def successors(state):
    return [ state[0:n] + [state[n+1],] + [state[n],] + state[n+2:] for n in range(0, N-1) ]

# Heuristic function:
# given a state, return the heuristic value of current state
# The heuristic value in here is defined as the missed placed birds
# Since the maximum Δh could be 2 in here, I decide to divide the result by 2, therefore the heuristic value of each successor state would be admissible 
def h(state):
    num = 0
    for i in range(len(state)):
        if state[i] != i + 1:
            num += 1
    return num / 2
#########
#
# THE ALGORITHM:
#
# This is a generic solver using BFS.
# Also, instead of using a traditional queue, I choose to use priority queue (min heap)
#
def solve(initial_state):
    if is_goal(initial_state):
        return [initial_state]
    fringe = PriorityQueue()
    initial_g = 0
    initial_h = h(initial_state)
    fringe.put((initial_g + initial_h, initial_h, initial_g, initial_state, []))
    while not fringe.empty():
        (curr_f, curr_h, curr_g, state, path) = fringe.get()
        if is_goal(state):
            return path + [state, ]
        for s in successors(state):
            next_g = curr_g + 1
            next_h = h(s)
            next_f = next_g + next_h
            fringe.put((next_f, next_h, next_g, s, path + [state, ]))
    return []

# Please don't modify anything below this line
#
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected a test case filename"))

    test_cases = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            test_cases.append([ int(i) for i in line.split() ])
    for initial_state in test_cases:
        	print('From state ' + str(initial_state) + " found goal state by taking path: " + str(solve(initial_state)))

    

