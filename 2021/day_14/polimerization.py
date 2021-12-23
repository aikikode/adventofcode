import sys
from collections import Counter
from typing import List, Tuple, Dict


def convert_input(data: List[str]) -> Tuple[str, Dict[str, str]]:
    template = data[0]
    new_elements = dict()
    for line in data[2:]:
        if not line:
            continue
        k, v = line.split(" -> ")
        new_elements[k] = v
    return template, new_elements


def polimer_delta_len(template: str, new_elements: Dict[str, str], steps: int) -> int:
    """ Brute-force approach when steps count is small, use _dp version below for large (>20) steps """
    out = list(template)
    for _ in range(steps):
        for idx in range(len(out) - 2, -1, -1):
            key = "".join(out[idx:idx + 2])
            if key in new_elements:
                out.insert(idx + 1, new_elements[key])
    c = Counter("".join(out)).most_common()
    return c[0][1] - c[-1][1]


def get_elements_counter(key: str, steps: int, new_elements: Dict[str, str], memo: Dict[Tuple[str, int], Counter]):
    if (key, steps) in memo:
        return memo[(key, steps)]

    if key not in new_elements or steps == 0:
        memo[(key, steps)] = Counter(key)
    else:
        c = (
            get_elements_counter(f"{key[0]}{new_elements[key]}", steps - 1, new_elements, memo) +
            get_elements_counter(f"{new_elements[key]}{key[1]}", steps - 1, new_elements, memo)
        )
        c[new_elements[key]] -= 1
        memo[(key, steps)] = c

    return memo[(key, steps)]


def polimer_delta_len_dp(template: str, new_elements: Dict[str, str], steps: int) -> int:
    out = list(template)
    c = Counter()
    memo = dict()
    for idx in range(len(out) - 1):
        key = "".join(out[idx:idx + 2])
        c.update(get_elements_counter(key, steps, new_elements, memo))
        if idx > 0:
            # decrease middle element count by 1
            c[out[idx]] -= 1

    c = c.most_common()
    return c[0][1] - c[-1][1]


if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        with open(input_file) as fin:
            data = [line.strip() for line in fin]
            print("part 1:", polimer_delta_len(*convert_input(data), steps=10))
            print("part 2:", polimer_delta_len_dp(*convert_input(data), steps=40))

assert polimer_delta_len_dp(*convert_input("""NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C""".split("\n")), steps=10) == 1588

assert polimer_delta_len_dp(*convert_input("""NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C""".split("\n")), steps=40) == 2188189693529
