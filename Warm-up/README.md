# a0-release
# Assignment 0 Report
#
#
# Part 1:
#
# Algorithm Design: BFS algorithm (Breath-First-Search) 
# In this problem, I choose to use BFS to get the answer. I used extra O(M*N) space to store the minimum steps from the origin point to reach each point in the map. If the point is unreachable (wall), I will mark the distance as the biggest integer. After I get the distances of all the points in the original graph, start from the destination, I choose to backtrack the path to the origin point. For example, if it takes 8 steps from origin point to destination, I will start from destination point. First by looking at the 4-direction adjacent point. If one of the adjacent points' step is 8 - 1 = 7, I will move to this point and continue backtracking, until I find the origin point. If the number of steps of the destination point is still the biggest integer after I applied BFS on the graph, it means that there is no valid path for me to reach the destination point from the origin point.
# 
# The initial state is the origin point. The goal state is, by starting from the origin point, we can find the destination by moving 4 directions one step a time. If we can reach to the destination point, that means we have reach the goal state. Or if we can't reach to the destination point, that means the goal state is unreachable. Valid states are, for each point in the map, we can reach them. For each point, the successor function will be the points that are 4 direcionally adjacent to the current point. The cost function for each point will be from current state to its successor state, it will cost from 1 to 3, depends on how many points that adjacent to current point has been visited before, or it is unreachable (wall).
#
#
#
# Part 2:
#
# Algorithm Design: BFS algorithm (Breath-First-Search)
# In this problem, I still choose to use BFS algorithm. From the initial map, my program will first look for all possible successor maps which can arrange next pichu within the previous map. Continue to do the search by this way, if possible to arrange K pichus in the original map, my program will provide the solution. Otherwise it will return False, as the problem required.
#
# By given the initial map and an integer k, the goal state is to arrange K pichus in the map, or to find that it is impossible to arrange K pichus in the given map. The inital state is the given map. The successor functions are the set of all the maps which can arrange next pichu in the map of previous state, comparing with it's previous state. The cost function for each state the number of choices for the program to pick all the viable map to arrange next pichu in the map.