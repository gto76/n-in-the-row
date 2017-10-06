#!/usr/bin/python3
#
# Usage: four.py 
# 

from enum import Enum
import copy
import sys


SIZE = 6
GOAL = 4


class D(Enum):
    HOR = 0
    VER = 1
    DIA = 2
    DIA2 = 3


class F(Enum):
    E = 0
    X = 1
    O = 2


class Board:
    def __init__(self, size):
        self.brd = [size*[F.E] for _ in range(size)]

    def __repr__(self):
        out = ""
        for row in self.brd:
            for cell in row:
                symbol = "."
                if cell == F.X:
                    symbol = "X"
                elif cell == F.O:
                    symbol = "O"
                out += " {}".format(symbol)
            out += '\n'
        return out


def main():
    board = Board(SIZE)
    sign = F.X
    print(score(board, F.X))
    print(board)

    while True:
        cell = get_next_move(board, sign)
        board.brd[cell[0]][cell[1]] = sign
        print(score(board, F.X))
        print(board)
        sys.stdout.flush()
        sign = get_oposite(sign)
        input()


def get_next_move(board, sign):
    empty_cells = get_coordinates_of(board, F.E)
    scores = [score_for_move(board, sign, cell) for cell in empty_cells]
    options = sorted(zip(scores, empty_cells))
    return options[-1][1]


def score_for_move(board, sign, cell):
    next_board = copy.deepcopy(board)
    next_board.brd[cell[0]][cell[1]] = sign
    return score(next_board, sign)


def score(board, sign):
    if sign == F.X:
        return score_for(board, F.X) - score_for(board, F.O)
    return score_for(board, F.O) - score_for(board, F.X)


def score_for(board, sign):
    out = 0
    for cell in get_coordinates_of(board, sign):
        for direction in D:
            out += get_score_for_cell(board, cell, sign, direction)
    return out


def get_coordinates_of(board, sign):
    out = []
    for i, row in enumerate(board.brd):
        for j, cell in enumerate(row):
            if cell == sign:
                out.append([i, j])
    return out


def get_score_for_cell(board, cell, sign, direction):
    out = 0
    for delta in range(-(GOAL-1), 1):
        coordinates = get_coordinates(cell, delta, direction)
        if not coordinates:
            continue
        signs = get_window(board, coordinates)
        out += score_window(signs, sign)
    return out


def score_window(signs, sign):
    oposite_sign = get_oposite(sign)
    if signs.count(sign) == 0:
        return -signs.count(oposite_sign)
    elif signs.count(oposite_sign) == 0:
        return signs.count(sign)
    return 0


def get_coordinates(cell, delta, direction):
    if direction == D.HOR:
        start = cell[0] + delta
        end = start + GOAL - 1
        if start < 0:
            return
        if end >= SIZE:
            return
        return list(zip(list(range(start, end+1)), GOAL*[cell[1]]))

    elif direction == D.VER:
        start = cell[1] + delta
        end = start + GOAL - 1
        if start < 0:
            return
        if end >= SIZE:
            return
        return list(zip(GOAL*[cell[0]], list(range(start, end+1))))

    elif direction == D.DIA:
        start_x = cell[0] + delta
        start_y = cell[1] + delta
        end_x = start_x + GOAL - 1
        end_y = start_y + GOAL - 1
        if start_x < 0 or start_y < 0:
            return
        if end_x >= SIZE or end_y >= SIZE:
            return
        return list(zip(list(range(start_x, end_x+1)),
                        list(range(start_y, end_y+1))))

    else:
        start_x = cell[0] + delta
        start_y = cell[1] - delta
        end_x = start_x + GOAL - 1
        end_y = start_y - GOAL + 1
        extremes = [start_x, start_y, end_x, end_y]
        if any(extreme < 0 or extreme >= SIZE for extreme in extremes):
            return
        return list(zip(uni_range(start_x, end_x),
                        uni_range(start_y, end_y)))


###
##  UTIL
#

def uni_range(a, b):
    if b >= a:
        return list(range(a, b+1))
    return list(reversed(range(b, a+1)))


def get_window(board, cells):
    out = []
    for cell in cells:
        out.append(board.brd[cell[0]][cell[1]])
    return out


def column(matrix, i):
    return [row[i] for row in matrix]


def get_oposite(sign):
    if sign == F.X:
        return F.O
    return F.X


if __name__ == '__main__':
    main()
