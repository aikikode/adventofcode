import sys
from functools import reduce
from typing import List, Set, Tuple


def convert_input(data: List[str]) -> List[List[int]]:
    return [list(map(int, list(line))) for line in data if line]


def get_neighbours(i, j, X, Y):
    for a, b in [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]:
        if not (a < 0 or b < 0 or a >= X or b >= Y):
            yield a, b


def get_low_locations(height_map: List[List[int]]) -> List[Tuple[int, int]]:
    X, Y = len(height_map), len(height_map[0])
    minimums = []
    for x in range(X):
        for y in range(Y):
            if all(map(lambda a: height_map[a[0]][a[1]] > height_map[x][y], get_neighbours(x, y, X, Y))):
                minimums.append((x, y))
    return minimums


def get_low_locations_sum(height_map: List[List[int]]) -> int:
    minimums = 0
    for x, y in get_low_locations(height_map):
        minimums += 1 + height_map[x][y]
    return minimums


def extend_basin(x, y: int, height_map: List[List[int]], visited: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
    X, Y = len(height_map), len(height_map[0])
    visited.add((x, y))
    basin = {(x, y), }
    for i, j in get_neighbours(x, y, X, Y):
        if (i, j) not in visited and height_map[i][j] > height_map[x][y] and height_map[i][j] != 9:
            basin |= extend_basin(i, j, height_map, visited)
    return basin


def get_basins_sizes(height_map: List[List[int]]) -> int:
    visited = set()
    basins = []
    for min_x, min_y in get_low_locations(height_map):
        b = extend_basin(min_x, min_y, height_map, visited)
        basins.append(b)
    return reduce(lambda a, b: a * b, map(len, sorted(basins, key=len, reverse=True)[:3]))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        with open(input_file) as fin:
            data = [line.strip() for line in fin]
            print("part 1:", get_low_locations_sum(convert_input(data)))
            print("part 2:", get_basins_sizes(convert_input(data)))

assert get_low_locations_sum(convert_input("""2199943210
3987894921
9856789892
8767896789
9899965678""".split("\n"))) == 15
assert get_basins_sizes(convert_input("""2199943210
3987894921
9856789892
8767896789
9899965678""".split("\n"))) == 1134
