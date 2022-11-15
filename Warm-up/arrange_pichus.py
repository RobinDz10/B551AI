#!/usr/local/bin/python3
#
# arrange_pichus.py : arrange agents on a grid, avoiding conflicts
#
# Submitted by : [PUT YOUR NAME AND USERNAME HERE]
#
# Based on skeleton code in CSCI B551, Fall 2022.

import sys

# Parse the map from a given filename
def parse_map(filename):
	with open(filename, "r") as f:
		return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]

# Count total # of pichus on house_map
def count_pichus(house_map):
    return sum([ row.count('p') for row in house_map ] )

# Return a string with the house_map rendered in a human-pichuly format
def printable_house_map(house_map):
    return "\n".join(["".join(row) for row in house_map])

# Add a pichu to the house_map at the given position, and return a new house_map (doesn't change original)
def add_pichu(house_map, row, col):
    return house_map[0:row] + [house_map[row][0:col] + ['p',] + house_map[row][col+1:]] + house_map[row+1:]

# Judge if curr position can add pichu
def can_add_pichu(house_map, x, y):
    row = len(house_map)
    col = len(house_map[0])
    # Check availability vertically
    r = x - 1
    while r >= 0:
        if house_map[r][y] == 'p':
            return False
        if house_map[r][y] == 'X':
            break
        r -= 1

    r = x + 1
    while r < row:
        if house_map[r][y] == 'p':
            return False
        if house_map[r][y] == 'X':
            break
        r += 1

    # Check availability horizontally
    c = y - 1
    while c >= 0:
        if house_map[x][c] == 'p':
            return False
        if house_map[x][c] == 'X':
            break
        c -= 1

    c = y + 1
    while c < col:
        if house_map[x][c] == 'p':
            return False
        if house_map[x][c] == 'X':
            break
        c += 1

    # Check availability diagonally
    r = x - 1
    c = y - 1
    while r >= 0 and c >= 0:
        if house_map[r][c] == 'p':
            return False
        if house_map[r][c] == 'X':
            break
        r -= 1
        c -= 1

    r = x + 1
    c = y + 1
    while r < row and c < col:
        if house_map[r][c] == 'p':
            return False
        if house_map[r][c] == 'X':
            break
        r += 1
        c += 1

    r = x - 1
    c = y + 1
    while r >= 0 and c < col:
        if house_map[r][c] == 'p':
            return False
        if house_map[r][c] == 'X':
            break
        r -= 1
        c += 1

    r = x + 1
    c = y - 1
    while r < row and c >= 0:
        if house_map[r][c] == 'p':
            return False
        if house_map[r][c] == 'X':
            break
        r += 1
        c -= 1

    return True

# Get list of successors of given house_map state
# def successors(house_map):
#     for i in range(0, len(house_map)):
#         for j in range(0, len(house_map[0])):
#             if house_map[i][j] == '.' and can_add_pichu(house_map, i, j):
#                 new_map = house_map
#                 return [add_pichu(new_map, i, j)]

    # return [ add_pichu(house_map, r, c) for r in range(0, len(house_map)) for c in range(0,len(house_map[0])) if house_map[r][c] == '.' ]

# check if house_map is a goal state
# def is_goal(house_map, k):
#     return count_pichus(house_map) == k

# Arrange agents on the map
#
# This function MUST take two parameters as input -- the house map and the value k --
# and return a tuple of the form (new_house_map, success), where:
# - new_house_map is a new version of the map with k agents,
# - success is True if a solution was found, and False otherwise.
#

def getSuccessors(house_map, fringe):
    row = len(house_map)
    col = len(house_map[0])
    for i in range(0, row):
        for j in range(0, col):
            if house_map[i][j] == '.' and can_add_pichu(house_map, i, j):
                fringe.append(add_pichu(house_map, i, j))

def solve(initial_house_map,k):
    fringe = []
    fringe.append(initial_house_map)
    level = count_pichus(initial_house_map)
    while len(fringe) > 0:
        if level < k:
            if len(fringe) == 0:
                return ([], False)
        if level == k:
            if len(fringe) == 0:
                return ([], False)
            else:
                return (fringe.pop(0), True)
        size = len(fringe)
        for i in range(0, size):
            new_map = fringe.pop(0)
            getSuccessors(new_map, fringe)
        level += 1
    return ([], False)

# Main Function
if __name__ == "__main__":
    house_map=parse_map(sys.argv[1])
    # This is k, the number of agents
    k = int(sys.argv[2])
    print ("Starting from initial house map:\n" + printable_house_map(house_map) + "\n\nLooking for solution...\n")
    solution = solve(house_map,k)
    print ("Here's what we found:")
    print (printable_house_map(solution[0]) if solution[1] else "False")