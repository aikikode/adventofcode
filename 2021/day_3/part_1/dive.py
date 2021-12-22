import sys
from typing import Iterable


def get_power_consumption(data: Iterable[str]) -> int:
    total_rows = 0
    counters = None
    for binary in data:
        if counters is None:
            counters = [0] * len(binary)
        for idx, el in enumerate(binary):
            counters[idx] += 1 if el == "1" else 0

        total_rows += 1

    gamma = ["1" if c >= (total_rows / 2) else "0" for c in counters]
    epsilon = ["0" if c == "1" else "1" for c in gamma]

    return int("".join(gamma), 2) * int("".join(epsilon), 2)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        with open(input_file) as fin:
            print(get_power_consumption(line.strip() for line in fin))


assert get_power_consumption(["00100"]) == 108
assert get_power_consumption(
"""00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010""".split()) == 198
