import sys
from collections import Counter
from typing import List, Optional


def get_zero_fish_count(steps: Optional[int] = 80) -> List[List[int]]:
    fishes_by_day = [[0], ]
    for _ in range(steps):
        tmp = fishes_by_day[-1]
        fishes = tmp[:]
        for idx in range(len(fishes)):
            if fishes[idx] == 0:
                fishes[idx] = 6
                fishes.append(8)
            else:
                fishes[idx] -= 1
        fishes_by_day.append(fishes)
    return fishes_by_day


def get_fish_count_part_1(data: List[int], days_passed=80) -> int:
    """ Sufficient for part 1, but will take too much time for part 2. """
    result = 0
    fishes_by_day = get_zero_fish_count(days_passed)
    for days, count in Counter(data).items():
        result += len(fishes_by_day[days_passed - int(days)]) * int(count)
    return result


def get_fish_count_part_2(input_data: List[int], days_passed=80) -> int:
    data = dict()

    def get_count(count, days):
        # (3, 100) -> (0, 97)
        # (6, 2) -> (4, 0) -> (0, 0)
        days = max(days - count, 0)
        if days in data:
            return data[days]
        if days == 0:
            data[0] = 1
        else:
            # (0, 100) -> (6, 99) + (8, 99)
            data[days] = get_count(6, days - 1) + get_count(8, days - 1)
        return data[days]

    result = 0
    for days, count in Counter(input_data).items():
        result += get_count(days, days_passed) * count
    return result


if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        with open(input_file) as fin:
            print(get_fish_count_part_2(list(map(int, fin.readline().strip().split(","))), 256))


assert get_fish_count_part_2([5], 2) == 1
assert get_fish_count_part_2([1], 2) == 2
assert get_fish_count_part_2(list(map(int, "3,4,3,1,2".split(","))), 80) == 5934
assert get_fish_count_part_2(list(map(int, "3,4,3,1,2".split(","))), 256) == 26984457539
