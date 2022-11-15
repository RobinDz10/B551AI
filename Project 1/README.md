# a1-release

# Part 1
## Details:
In this part, I choose to use priority queue (min heap) instead of queue. What included in a single element in this priority queue should consist f(s) of curr state, the curr state itself, and the path to curr state. When we construct the element and try to push it into the priority queue, we should construct like this: [f(curr_state), curr_state, path + curr_state]. By using this way we can optimize the original BFS method.  
Also, when we determine the heuristic value of each state, we have to use the admissible heuristic value. In my program, I choose to use the total number of wrongly tiled in a state. For example, the target sequence is 12345, and now curr_state is 13542. So, in this state, the heuristic value is 4, because 1, 3, 5 and 2 are placed incorrectly, only 4 has been placed to the correct place. Therefore the heuristic value of this state is 4. For the cost part of this state, it should use the value of the previous state, and plus 1. This is the way how I compute f(s) = g(s) + h(s), where g(s) is the cost of curr_state and h(s) is the heuristic value of curr_state.

# Part 2

In this part, I choose to use priority queue to do the searching procedure (instead of BFS). So overally the algorithm is an A* algorithm: the state space is the whole 2D "board"; the successor function is the function that returns all the 24 successors in the next possible move (number 24 is explained in the next section); the edge weight is constant; goal state is the 2D board {1, 2, 3, 4, ... 25}. 

In the design of priority queue, we use 3 different priority factors to keep the min-heap state: g(s) + h(s), h(s) and g(s). Each time we retrive the element from priority queue, we first look for the element with minimal g(s) + h(s), then if we can't find such minimal g(s) + h(s) in the previous step, we use altertnative comparison factors h(s) and g(s). By using this way we can optimize the original BFS method and make our algorithm faster.  

In the process of designing heuristic function, we are using manhattan distance as the core distance calculation function, and a special factor to let the heuristic function admissable: assuming there's a random point in the board, by moving the board (using operations of  `L`, `R`, `U` ,`D` and 4 rotates), the point can reach any place in the board within finity steps. The maximum step is 4 (moving 4 corner points to the middle), and the average step should be < 4). That is to say, if we calculate the heuristic function as (manhattan_distance/4), the heurictic function becomes admissable. 

**In this problem, what is the branching factor of the search tree?**

The branching factor is 24. For operation `L`, `R`, `U` and `D`, we have 4*5=20 different successors. For operation of inner/outer rotate, we have 4 different successors. So generally we have 24 successors and that is the branching factor of the search tree.

**If the solution can be reached in 7 moves, about how many states would we need to explore before we found it if we used BFS instead of A\* search? A rough answer is fine.**

We may need about 24^7=4586471424 states to explore.

# Part 3
##### 1. a description of how you formulated the search problem, including precisely defining the state space, the successor function, the edge weights, the goal state, and (if applicable) the heuristic function(s) you designed, including an argument for why they are admissible.

    I used A* search with different cost function to find optimal path.

   - state space : Any city or highway intersection in the road-segments.txt
   - Successor function : All cities and intersections that haven't been visited and connected with current states by road
   - Cost function (edge weights):
   
            - segments:     G(node) = G(current) + 1000   
              //Because we only care about minimal # of segments, the edge weights should be a fixed value 
              that ignore the distance
           
            - distance:     G(node) = G(current) + distance(current, node) 
              //we need to minimize the total distance, the edge weights should be the distance from current
              city to nearby  city
           
            - time:         G(node) = G(current) + 55 * distance(current, node) / speed(current, node) 
              //The edge weight is the travel time between two city multiple by certain value, otherwise the
              cost function will be too small comparing to the heuristic function

            - delivery:     G(node) = G(current) + 55 * tRoad (if speed limit <50)
                            G(node) = G(current) + 55 * tRoad + 2 * 55 * (tRoad + tTrip) (if speed limit >=50)

    - Goal state definition : Current state is the end city 
      
    - Initial state : Start city in open List
      
    - heuristic function: distance between current city and nearby city computed by Haversine formula 
      with two sets of latitudes and longitudes

##### 2. a brief descrip- tion of how your search algorithm works.
    1) prepare dictionaries of road and gps for successor function and heuristic function
    2) put start node to priority queue
    3) Using A* to search goal with selected cost function
    4) reverse parent to genereate path
##### 3. (3) and discussion of any problems you faced, any assumptions, simplifications, and/or design decisions you made. 
    Since we don't have Lat/Lon for highway intersections, we need to approximate its location, we made the assumption
    that the road between start and end should follow the bearing angle between start and end. If we have a place that 
    we don't know the Lat/Lon, we could assume that its Lat/Lon can be calculated by offsetting its parent's Lat/Lon 
    by 2/3 of length of road in the direction of the bearing angle between start and end. Then we can use Haversine 
    formula to compute distance between two cities
