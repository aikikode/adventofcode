import sys
from typing import Iterable


def count_depth_increases(data: Iterable[int]) -> int:
    count = 0
    prev = None
    for depth in data:
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
            print(count_depth_increases(map(int, (line.strip() for line in fin))))


assert count_depth_increases([199, 198]) == 0
assert count_depth_increases([199, 200]) == 1
assert count_depth_increases([199, 210, 100, 210]) == 2
assert count_depth_increases([199, 200, 208, 210, 200, 207, 240, 269, 260, 263]) == 7
assert count_depth_increases(map(int, "188 192 196 198 199 202 208 225 231 219 226 232 265 267 268 287".split())) == 14
