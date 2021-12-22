import sys
from collections import Counter
from typing import List


def get_least_fuel(data: List[int]) -> int:
    counter = Counter(data)
    points = sorted(counter.keys())
    # print(len(points), len(data))
    right_sum = total_sum = sum(data)
    right_points = total_points = len(data)
    # min_pos = None
    min_sum = None
    for el in points:
        cur_points_count = counter[el]
        cur_sum = cur_points_count * el
        right_sum -= cur_sum
        right_points -= cur_points_count
        left_sum = total_sum - right_sum - cur_sum
        left_points = total_points - right_points - cur_points_count
        s = right_sum + (left_points - right_points) * el - left_sum
        if min_sum is None or s < min_sum:
            min_sum = s
            # min_pos = el
    # print(min_pos)
    return min_sum


if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        with open(input_file) as fin:
            print(get_least_fuel(list(map(int, fin.readline().strip().split(",")))))


assert get_least_fuel([0, 1, 2, 2, 2, 4]) == 5
assert get_least_fuel([16, 1, 2, 0, 4, 2, 7, 1, 2, 14]) == 37
