from copy import  deepcopy
def move_left(row):
    # e.g. [1,2,3,4] -> [2,3,4,1]
    start=row[1:len(row)]
    start.extend([row[0]])
    return start

def move_right(row):
    # e.g. [1,2,3,4] -> [4,1,2,3]
    start=[row[-1]]
    start.extend(row)
    return start[:len(start)-1]

def occ(state):
    new_state=deepcopy(list(state))
    new_state[0]=state[1]
    new_state[1]=state[2]
    new_state[2]=state[3]
    new_state[3]=state[4]
    new_state[4]=state[9]

    new_state[5]=state[0]
    new_state[9]=state[14]

    new_state[10]=state[5]
    new_state[14]=state[19]

    new_state[15]=state[10]
    new_state[19]=state[24]

    new_state[20]=state[15]
    new_state[21]=state[20]
    new_state[22] = state[21]
    new_state[23] = state[22]
    new_state[24] = state[23]

    return tuple(new_state)

def oc(state):
    res=occ(state)
    for i in range(0,14):
        res=occ(res)
    return res

def ic(state):
    new_state = deepcopy(list(state))
    new_state[6]=state[11]
    new_state[7]=state[6]
    new_state[8]=state[7]

    new_state[11]=state[16]
    new_state[13]=state[8]

    new_state[16]=state[17]
    new_state[17]=state[18]
    new_state[18]=state[13]

    return tuple(new_state)

def icc(state):
    res=ic(state)
    for i in range(0,6):
        res=ic(res)
    return res

def heuristic(state):
    dist = 0
    for row in range(1, 6):
        for column in range(1, 6):
            val = state[(row - 1) * 5 + column - 1]
            dest_row = (val - 1) // 5 + 1
            dest_col = (val - 1) % 5 + 1
            # dist+=((row-dest_row)**2+(column-dest_col)**2)**(1/2)
            dist += abs(dest_col-column)+abs(dest_row-row)
    return dist

i=5
# state=tuple(range(1, 26))
# state=(2, 23, 4,5,10,1,7,3,9,11,6,13,8,15,20,12,17,14,19,25,16,21,22,18,24)
# new_state = list(state)
# new_state[(i - 1) * 5:i * 5] = move_right(new_state[(i - 1) * 5:i * 5])
# print(new_state)
state=(2,3,4,5,1,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25)
print(heuristic(state))




