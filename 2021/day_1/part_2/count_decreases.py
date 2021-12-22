import sys
from typing import List


def count_depth_increases(data: List[int]) -> int:
    count = 0
    prev = None
    for start_idx in range(len(data) - 2):
        depth = sum(data[start_idx:start_idx+3])

        if prev is None:
            prev = depth
            continue

        if depth > prev:
            count += 1

        prev = depth
    return count


if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        with open(input_file) as fin:
            print(count_depth_increases(list(map(int, (line.strip() for line in fin)))))


assert count_depth_increases(list(map(int, "199 200 208 210 200 207 240 269 260 263".split()))) == 5


