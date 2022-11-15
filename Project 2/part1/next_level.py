"""
给定某一时刻的状态，返回下一步所有状态的集合
当然还要给定下一步是B操作还是W操作
"""
import math
import numpy as np
from copy import deepcopy


def numpy_debug_board(state_2d):
    debugg = np.array(state_2d)
    # print('break here')
    return debugg


def pichu_normal_move(size, position, operate_color):
    """
    棋盘的边界限制（和棋子无关）
    size: integer，棋盘尺寸，比如8
    position: tuple，当前坐标

    返回：diagonal ！向前！移动1步后，所有不越界的坐标合集，[(row1, col1), (row2, col2), (row3, col3)...]
    """
    next = []
    row = position[0]
    col = position[1]
    newRow = row + 1 if operate_color == 'w' else row -1

    if newRow <= size - 1 and newRow >= 0:
        #前左
        if col - 1 >= 0: next.append([newRow, col - 1])
        #前右
        if col + 1 <= size - 1 : next.append([newRow, col + 1])
    return next


def pikachu_move_search(current_state, board_size, pawns, operate_color, row, col, rOffset, cOffset):
    
    state = deepcopy(current_state)
    next_board_str_lst = []

    #先向搜索方向位移一格
    r = row + rOffset
    c = col + cOffset
    jump = False
    edge = board_size - 1 if operate_color == 'w' else 0

    step = 0;
    while r >= 0 and r <= board_size - 1 and c >= 0 and c <= board_size - 1 and step < 2:
        #遇到同颜色pokemon 停止
        if current_state[r][c] in pawns or current_state[r][c] in "@$": break
        #空白就占领
        elif current_state[r][c] == '.':
            next_candidate = deepcopy(state)
            next_candidate[row][col] = '.'
            next_candidate[r][c] = current_state[row][col] if r != edge else pawns[-1]# Raichu
            # 并保存
            next_board_str_lst.append(convert_board2d_to_boardstr(next_candidate, board_size))
        #如果跳跃过一次了 还遇到不同色的pokemon
        elif jump: break 
        #没有跳跃过 遇到不同色的pokemon
        else:
            #吃掉不同色pokemon 记录到当前棋盘(复制)
            step-=1
            state[r][c] = '.'
            jump = True
            next_candidate = deepcopy(state)
            next_candidate[row][col] = '.'
            next_candidate[r][c] = current_state[row][col] if r != edge else pawns[-1]# Raichu
            # 并保存
            next_board_str_lst.append(convert_board2d_to_boardstr(next_candidate, board_size))
        r += rOffset
        c += cOffset
        step-=1
    return next_board_str_lst


def raichu_move_search(current_state, board_size, pawns, row, col, rOffset, cOffset):
    
    state = deepcopy(current_state)
    next_board_str_lst = []

    #先向搜索方向位移一格
    r = row + rOffset
    c = col + cOffset
    jump = False

    while r >= 0 and r <= board_size - 1 and c >= 0 and c <= board_size - 1:
        #遇到同颜色pokemon 停止
        if current_state[r][c] in pawns: break
        #空白就占领
        elif current_state[r][c] == '.':
            next_candidate = deepcopy(state)
            next_candidate[row][col] = '.'
            next_candidate[r][c] = current_state[row][col]
            # 并保存
            next_board_str_lst.append(convert_board2d_to_boardstr(next_candidate, board_size))
        #如果跳跃过一次了 还遇到不同色的pokemon
        elif jump: break 
        #没有跳跃过 遇到不同色的pokemon
        else:
            #吃掉不同色pokemon 记录到当前棋盘(复制)
            state[r][c] = '.'
            jump = True
            next_candidate = deepcopy(state)
            next_candidate[row][col] = '.'
            next_candidate[r][c] = current_state[row][col]
            # 并保存
            next_board_str_lst.append(convert_board2d_to_boardstr(next_candidate, board_size))
        r += rOffset
        c += cOffset
    return next_board_str_lst

def pichu(current_state, operate_color, board_size):
    current_state = convert_boardstr_to_board2d(current_state, board_size)
    """
    移动皮丘！
    """
    operate_color = operate_color.lower()
    pawns = [operate_color, operate_color.upper(), '@' if operate_color == 'w' else '$']
    #turn to Raichu
    edge = board_size - 1 if operate_color == 'w' else 0

    #numpy_debugg = numpy_debug_board(current_state)
    next_board_str_lst = []  # 列举所有：因为移动pichu导致的下一轮棋盘状态（压缩string），用list of str表示
    for row in range(0, board_size):
        for col in range(0, board_size):
            # 抓一只颜色相同的，并且需要是皮丘
            if current_state[row][col] == operate_color:
                # 先看看不越界是什么结果
                next_pos_lst = pichu_normal_move(board_size, (row, col), operate_color)
                for next_pos in next_pos_lst:
                    next_candidate = deepcopy(current_state)
                    # 首先不能颜色相同
                    if current_state[next_pos[0]][next_pos[1]] not in pawns:
                        # 如果目标为空 或 对手 pichu，就占领
                        if current_state[next_pos[0]][next_pos[1]] in '.wb':
                            next_candidate[row][col] = '.'
                            next_candidate[next_pos[0]][next_pos[1]] = current_state[row][col] if next_pos[0] != edge else pawns[-1]# Raichu
                            # 并保存
                            next_board_str_lst.append(convert_board2d_to_boardstr(next_candidate, board_size))
                        if current_state[next_pos[0]][next_pos[1]] in 'wb':
                            # 如果目标为异色的皮丘
                            # 尝试jump over，但需要先检查降落点是否有效且为空
                            jump_row = next_pos[0] + (next_pos[0] - row)
                            jump_col = next_pos[1] + (next_pos[1] - col)
                            if jump_row >= 0 and jump_row <= board_size - 1 and jump_col >= 0 and jump_col <= board_size - 1:
                                if current_state[jump_row][jump_col] == '.':
                                    # 现在才可以降落
                                    next_candidate[row][col] = '.'
                                    next_candidate[next_pos[0]][next_pos[1]] = '.'
                                    next_candidate[jump_row][jump_col] = current_state[row][col] if jump_row != edge else pawns[-1]# Raichu
                                    # 并保存
                                    next_board_str_lst.append(convert_board2d_to_boardstr(next_candidate, board_size))

                # for next in next_board_str_lst:
                #     debugg=numpy_debug_board(convert_boardstr_to_board2d(next, board_size))
                #     print('debug here')

    # 去重，虽然在理论上不可能有重复
    next_board_str_lst = list(set(next_board_str_lst))
    # for next in next_board_str_lst:
    #     debugg=numpy_debug_board(convert_boardstr_to_board2d(next, board_size))
    #     print('debug here')
    return next_board_str_lst


def pikachu(current_state, operate_color, board_size):
    current_state = convert_boardstr_to_board2d(current_state, board_size)
    """
    移动皮卡丘！
    """
    operate_color = operate_color.lower()
    pawns = [operate_color, operate_color.upper(), '@' if operate_color == 'w' else '$']
    next_board_str_lst =[]
    for row in range(0, board_size):
        for col in range(0, board_size):
             # 抓一只颜色相同的，并且需要是皮卡丘
            if current_state[row][col] == pawns[1]:
                #向前搜索
                next_board_str_lst += pikachu_move_search(current_state, board_size, pawns,operate_color, row, col, 1  if operate_color == 'w' else -1, 0)
                #向右搜索
                next_board_str_lst += pikachu_move_search(current_state, board_size, pawns,operate_color, row, col, 0, 1)
                #向左搜索
                next_board_str_lst += pikachu_move_search(current_state, board_size, pawns, operate_color,row, col, 0, -1)

    # 去重，虽然在理论上不可能有重复
    next_board_str_lst = list(set(next_board_str_lst))
    # for next in next_board_str_lst:
    #     debugg=numpy_debug_board(convert_boardstr_to_board2d(next, board_size))
    #     print('debug here')
    return next_board_str_lst

def raichu(current_state, operate_color, board_size):
    current_state = convert_boardstr_to_board2d(current_state, board_size)
    """
    移动雷丘！
    """
    operate_color = operate_color.lower()
    pawns = [operate_color, operate_color.upper(), '@' if operate_color == 'w' else '$']

    next_board_str_lst = []  # 列举所有：因为移动pichu导致的下一轮棋盘状态（压缩string），用list of str表示
    for row in range(0, board_size):
        for col in range(0, board_size):
             # 抓一只颜色相同的，并且需要是雷丘
            if current_state[row][col] == pawns[-1]:
                #向上搜索
                next_board_str_lst += raichu_move_search(current_state, board_size, pawns, row, col, -1, 0)
                #向下搜索
                next_board_str_lst += raichu_move_search(current_state, board_size, pawns, row, col, 1, 0)
                #向左搜索
                next_board_str_lst += raichu_move_search(current_state, board_size, pawns, row, col, 0, -1)
                #向右搜索
                next_board_str_lst += raichu_move_search(current_state, board_size, pawns, row, col, 0, 1)
                #向左上搜索
                next_board_str_lst += raichu_move_search(current_state, board_size, pawns, row, col, -1, -1)
                #向右上搜索
                next_board_str_lst += raichu_move_search(current_state, board_size, pawns, row, col, -1, 1)
                #向左下搜索
                next_board_str_lst += raichu_move_search(current_state, board_size, pawns, row, col, 1, -1)
                #向右下搜索
                next_board_str_lst += raichu_move_search(current_state, board_size, pawns, row, col, 1, 1)
    
     # 去重，虽然在理论上不可能有重复
    next_board_str_lst = list(set(next_board_str_lst))
    # for next in next_board_str_lst:
    #     debugg=numpy_debug_board(convert_boardstr_to_board2d(next, board_size))
    #     print('debug here')
    return next_board_str_lst

def convert_boardstr_to_board2d(state_str, board_size):
    board_2d = []
    for row in range(board_size):
        board_2d.append(list(state_str[ row * board_size : row * board_size +board_size]))
    return board_2d


def convert_board2d_to_boardstr(state_2d, board_size):
    res = ''
    for row in range(0, board_size):
        for col in range(0, board_size):
            res = res + state_2d[row][col]
    return res


if __name__ == '__main__':
    board_size = 8
    # current_state = '........W.W.W.W..w.w.w.w................b.b.b.b..B.B.B.B........'
    # current_state_2d=[['.', '.', '.', '.', '.', '.', '.', '.'],
    #                            ['W', '.', 'W', '.', 'W', '.', 'W', '.'],
    #                            ['.', 'w', '.', 'w', '.', 'w', '.', 'w'],
    #                            ['.', '.', '.', '.', '.', '.', '.', '.'],
    #                            ['.', '.', '.', '.', '.', '.', '.', '.'],
    #                            ['b', '.', 'b', '.', 'b', '.', 'b', '.'],
    #                            ['.', 'B', '.', 'B', '.', 'B', '.', 'B'],
    #                            ['.', '.', '.', '.', '.', '.', '.', '.']]
    current_state_2d_np=np.loadtxt('./board1.csv', dtype=str, delimiter=',').astype('str')
    current_state_2d = current_state_2d_np.tolist()
    current_state = convert_board2d_to_boardstr(current_state_2d, board_size)
    operate_color = 'B'
    debug1 = pichu(convert_boardstr_to_board2d(current_state, board_size), operate_color, board_size)
    debug2 = pikachu(convert_boardstr_to_board2d(current_state, board_size), operate_color, board_size)
    print('debug here')
    for next in debug1:
        debugg=numpy_debug_board(convert_boardstr_to_board2d(next, board_size))
        print('debug here')
