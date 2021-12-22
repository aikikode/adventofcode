import sys
from typing import List

X = Y = 10


def convert_input(data: List[str]) -> List[List[int]]:
    return [[int(char) for char in line] for line in data]


def increase_energy_level(data: List[List[int]]):
    for x in range(X):
        for y in range(Y):
            data[x][y] += 1


def process_flashes(data: List[List[int]]):
    flashed = set()
    for x in range(X):
        for y in range(Y):
            try_flash(data, flashed, x, y)


def get_neighbours(x, y):
    return filter(
        lambda a: a[0] >= 0 and a[0] < X and a[1] >= 0 and a[1] < Y, [
            (x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
            (x - 1, y), (x + 1, y),
            (x - 1, y + 1), (x, y + 1), (x + 1, y + 1),
        ]
    )


def try_flash(data, flashed, x, y):
    if data[x][y] <= 9 or (x, y) in flashed:
        return 0
    flashed.add((x, y))
    for a, b in get_neighbours(x, y):
        data[a][b] += 1
        try_flash(data, flashed, a, b)


def reset_flashed(data):
    f = 0
    for x in range(X):
        for y in range(Y):
            if data[x][y] > 9:
                f += 1
                data[x][y] = 0
    return f


def count_flashes(data: List[List[int]], steps: int = 100) -> int:
    f = 0
    for _ in range(steps):
        increase_energy_level(data)
        process_flashes(data)
        f += reset_flashed(data)
    # print(f)
    return f


def get_total_flash(data: List[List[int]]):
    step = 0
    while reset_flashed(data) != 100:
        increase_energy_level(data)
        process_flashes(data)
        step += 1
    return step


if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        with open(input_file) as fin:
            data = [line.strip() for line in fin]
            print("part 1", count_flashes(convert_input(data)))
            print("part 2", get_total_flash(convert_input(data)))

assert count_flashes(convert_input("""5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526""".split("\n"))) == 1656

assert get_total_flash(convert_input("""5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526""".split("\n"))) == 195
