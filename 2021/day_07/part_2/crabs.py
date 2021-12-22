import sys
from collections import Counter
from typing import List


def get_single_distance(pos_a, pos_b):
    delta = max(pos_a - pos_b, pos_b - pos_a)
    return delta * (delta + 1) // 2


assert get_single_distance(0, 5) == 15
assert get_single_distance(6, 2) == 10


def get_distance(pos: int, counter) -> int:
    d = 0
    for el, count in counter.items():
        d += count * get_single_distance(pos, el)
    return d


def get_least_fuel(data: List[int]) -> int:
    counter = Counter(data)
    # points = sorted(counter.keys())
    start_pos = sum(data) // len(data)
    while True:
        # print(start_pos)
        left = get_distance(start_pos - 1, counter)
        cur = get_distance(start_pos, counter)
        right = get_distance(start_pos + 1, counter)
        if cur <= left and cur <= right:
            # print(cur)
            return cur

        if cur > left:
            start_pos -= 1
        else:
            start_pos += 1
    # print(min_pos)
    # return min_sum


if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        with open(input_file) as fin:
            print(get_least_fuel(list(map(int, fin.readline().strip().split(",")))))

# assert get_least_fuel([1, 3, 5, ]) == 6
assert get_least_fuel([16, 1, 2, 0, 4, 2, 7, 1, 2, 14]) == 168
