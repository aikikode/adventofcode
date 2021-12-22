import sys
from typing import List


def get_power_consumption(data: List[str]) -> int:
    def get_common_bits(records, idx):
        total = len(records)
        ones = sum(1 for r in records if r[idx] == "1")
        most_common = "1" if ones >= total / 2 else "0"
        return most_common, "0" if most_common == "1" else "1"

    # Find oxygen
    oxygen, idx = data, 0
    while len(oxygen) > 1:
        bit, _ = get_common_bits(oxygen, idx)
        oxygen = [record for record in oxygen if record[idx] == bit]
        idx += 1
    # print(oxygen)

    # Find co2
    co2, idx = data, 0
    while len(co2) > 1:
        _, bit = get_common_bits(co2, idx)
        co2 = [record for record in co2 if record[idx] == bit]
        idx += 1
    # print(co2)

    return int("".join(oxygen[0]), 2) * int("".join(co2[0]), 2)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        with open(input_file) as fin:
            print(get_power_consumption(list(line.strip() for line in fin)))


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
01010""".split()) == 230
