#!/usr/local/bin/python3
#
# route_pichu.py : a maze solver
#
# Submitted by : Duozhao Wang (duozwang)
#
# Based on skeleton code provided in CSCI B551, Fall 2022.
import heapq
import sys
import math
from queue import Queue
from queue import PriorityQueue


# Parse the map from a given filename
def parse_map(filename):
        with open(filename, "r") as f:
                return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]
                
# Check if a row,col index pair is on the map
def valid_index(pos, n, m):
        return 0 <= pos[0] < n  and 0 <= pos[1] < m

# Find the possible moves from position (row, col)
def moves(map, row, col):
        moves=((row+1,col), (row-1,col), (row,col-1), (row,col+1))

        # Return only moves that are within the house_map and legal (i.e. go through open space ".")
        return [ move for move in moves if valid_index(move, len(map), len(map[0])) and (map[move[0]][move[1]] in ".@" ) ]

# Perform search on the map
#
# This function MUST take a single parameter as input -- the house map --
# and return a tuple of the form (move_count, move_string), where:
# - move_count is the number of moves required to navigate from start to finish, or -1
#    if no such route exists
# - move_string is a string indicating the path, consisting of U, L, R, and D characters
#    (for up, left, right, and down)

def search(house_map):

        # Get the coordinates of start point and end point
        # start point: [x1, y1]
        # end point: [x2, y2]
        x1 = -1
        y1 = -1
        x2 = -1
        y2 = -1
        row = len(house_map)
        col = len(house_map[0])
        for i in range(row):
                for j in range(col):
                        if house_map[i][j] == 'p':
                                x1 = i
                                y1 = j
                        if house_map[i][j] == '@':
                                x2 = i
                                y2 = j

        # Initialize all the distances
        distance = []
        visited = []
        for i in range(row):
                level1 = []
                level2 = []
                for j in range(col):
                        level1.append(-1)
                        level2.append(False)
                distance.append(level1)
                visited.append(level2)

        distance[x1][y1] = 0
        visited[x1][y1] = True

        # Initialize a queue for BFS
        q = Queue()
        q.put([x1, y1])
        nextDir = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        while not q.empty():
                size = q.qsize()
                for i in range(size):
                        curr = q.get()
                        currX = curr[0]
                        currY = curr[1]
                        for j in range(len(nextDir)):
                                nextX = currX + nextDir[j][0]
                                nextY = currY + nextDir[j][1]
                                if valid_index([nextX, nextY], row, col) and house_map[nextX][nextY] != 'X' and visited[nextX][nextY] == False:
                                        q.put([nextX, nextY])
                                        visited[nextX][nextY] = True
                                        distance[nextX][nextY] = distance[currX][currY] + 1
        print(distance)

        # Traverse from the destination to source
        posX = x2
        posY = y2
        # print(posX, posY)
        # print(x1, y1)
        path = ""
        step = 0
        if distance[x2][y2] == -1:
                return [-1, "No solution"]
        while posX != x1 or posY != y1:
                step += 1
                if valid_index([posX - 1, posY], row, col) and distance[posX - 1][posY] == distance[posX][posY] - 1:
                        path += 'D'
                        posX -= 1
                elif valid_index([posX + 1, posY], row, col) and distance[posX + 1][posY] == distance[posX][posY] - 1:
                        path += 'U'
                        posX += 1
                elif valid_index([posX, posY - 1], row, col) and distance[posX][posY - 1] == distance[posX][posY] - 1:
                        path += 'R'
                        posY -= 1
                elif valid_index([posX, posY + 1], row, col) and distance[posX][posY + 1] == distance[posX][posY] - 1:
                        path += 'L'
                        posY += 1

        print("Path: " + path)
        final_path = path[::-1]
        return [step, final_path]




# Main Function
if __name__ == "__main__":
        house_map = parse_map(sys.argv[1])
        print("Shhhh... quiet while I navigate!")
        for i in range(len(house_map)):
                print(house_map[i])
        solution = search(house_map)
        print("Here's the solution I found:")
        print(str(solution[0]) + " " + solution[1])


