import sys
from collections import defaultdict
from typing import List, Tuple


class Cell:
    def __init__(self, value):
        self.value = value
        self.marked = False

    def __repr__(self):
        return str(self.value)


def get_winner_score(board: List[List[Cell]]) -> Tuple[bool, int]:
    for row in board:
        if all(cell.marked for cell in row):
            break
    else:
        for col_idx in range(len(board[0])):
            if all(row[col_idx].marked for row in board):
                break
        else:
            return False, -1

    # Board is winner!
    return True, sum(cell.value for row in board for cell in row if not cell.marked)


def get_bingo_winner(data: List[str]) -> int:
    numbers_coords = defaultdict(list)
    boards, board = [], []
    for line in data[2:]:
        if not line:
            boards.append(board)
            board = []
            continue
        board_row = []
        for idx, number in enumerate(map(int, line.split())):
            board_row.append(Cell(number))
            numbers_coords[number].append((len(boards), len(board), idx))
        board.append(board_row)
    if board:
        boards.append(board)

    for draw in list(map(int, data[0].split(","))):
        # Mark all numbers
        for board_idx, row_idx, col_idx in numbers_coords[draw]:
            boards[board_idx][row_idx][col_idx].marked = True

        # Check all boards
        for board in boards:
            won, score = get_winner_score(board)
            if won:
                return score * draw


if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        with open(input_file) as fin:
            print(get_bingo_winner(list(line.strip() for line in fin)))


assert get_bingo_winner([line for line in """1,2

2 1
3 4

6 8
3 1
""".split("\n")]) == 14

input = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
"""
assert get_bingo_winner([line for line in input.split("\n")]) == 4512
