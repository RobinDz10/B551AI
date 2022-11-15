def heuristic(state):
    dist = 0
    for row in range(1, 6):
        for column in range(1, 6):
            val = state[(row - 1) * 5 + column - 1]
            dest_row = (val - 1) // 5 + 1
            dest_col = (val - 1) % 5 + 1
            # dist+=((row-dest_row)**2+(column-dest_col)**2)**(1/2)
            dist += abs(dest_row - row) + abs(dest_col - column)
    return dist


print(heuristic((2, 3, 4, 5, 1, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25)))
