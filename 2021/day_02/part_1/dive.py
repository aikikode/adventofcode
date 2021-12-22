import sys
from typing import Iterable


def get_result_coordinates(data: Iterable[str]) -> int:
    x, y = 0, 0
    for command in data:
        direction, distance = command.split()
        distance = int(distance)
        if direction == "forward":
            x += distance
        elif direction == "down":
            y += distance
        else:
            y -= distance
    return x * y


if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        with open(input_file) as fin:
            print(get_result_coordinates(line.strip() for line in fin))


assert get_result_coordinates(["forward 10", "down 3", "up 1"]) == 20
assert get_result_coordinates(["forward 5", "down 5", "forward 8", "up 3", "down 8", "forward 2"]) == 150
