import sys
from pprint import pprint
from typing import List, Tuple


def walk(a, b):
    start_x, start_y = a
    end_x, end_y = b
    (start_x, start_y), (end_x, end_y) = sorted([(start_x, start_y), (end_x, end_y),])
    if start_x == end_x:
        start_y, end_y = sorted([start_y, end_y])
        for y in range(start_y, end_y + 1):
            yield start_x, y
    elif start_y == end_y:
        start_x, end_x = sorted([start_x, end_x])
        for x in range(start_x, end_x + 1):
            yield x, start_y
    else:
        delta_y = 1 if end_y > start_y else -1
        for x in range(start_x, end_x + 1):
            yield x, start_y
            start_y += delta_y


def get_dangerous_areas(data: List[str]) -> int:
    # First we need to get grid dimensions
    max_x, max_y = 0, 0
    for line in data:
        if not line:
            continue
        for x, y in (map(int, coords.split(",")) for coords in line.split(" -> ")):
            if x > max_x:
                max_x = x
            if y > max_y:
                max_y = y
    # Build grid
    grid = []
    for x in range(max_x + 1):
        grid.append([0] * (max_y + 1))

    dangerous_areas = set()
    for line in data:
        if not line:
            continue
        for x, y in walk(*list(map(int, coords.split(",")) for coords in line.split(" -> "))):
            grid[x][y] += 1
            if grid[x][y] >= 2:
                dangerous_areas.add(f"{x}-{y}")
    return len(dangerous_areas)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        with open(input_file) as fin:
            print(get_dangerous_areas([line.strip() for line in fin]))


_input = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
"""
assert get_dangerous_areas([line for line in _input.split("\n")]) == 12
