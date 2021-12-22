import sys
from typing import List, Dict, Set, Iterable

"""
  0:      1:      2:      3:      4:
 aaaa    ....    aaaa    aaaa    ....
b    c  .    c  .    c  .    c  b    c
b    c  .    c  .    c  .    c  b    c
 ....    ....    dddd    dddd    dddd
e    f  .    f  e    .  .    f  .    f
e    f  .    f  e    .  .    f  .    f
 gggg    ....    gggg    gggg    ....

  5:      6:      7:      8:      9:
 aaaa    aaaa    aaaa    aaaa    aaaa
b    .  b    .  .    c  b    c  b    c
b    .  b    .  .    c  b    c  b    c
 dddd    dddd    ....    dddd    dddd
.    f  e    f  .    f  e    f  .    f
.    f  e    f  .    f  e    f  .    f
 gggg    gggg    ....    gggg    gggg
"""


def get_digit_sum(data: List[str]) -> int:
    total = 0
    for line in data:
        if not line:
            continue
        input_data, output_data = map(lambda x: x.strip().split(), line.split("|"))
        all_encoded_numbers = set(input_data) | set(output_data)
        mapping = get_mapping(all_encoded_numbers)
        total += decode_number(output_data, mapping)
    return total


def decode_number(encoded_number: List[str], mapping: Dict[str, int]) -> int:
    index_to_num = {
        '012456': 0,
        '25': 1,
        '02346': 2,
        '02356': 3,
        '1235': 4,
        '01356': 5,
        '013456': 6,
        '025': 7,
        '0123456': 8,
        '012356': 9,
    }
    n = 0
    for number in encoded_number:
        n = n * 10 + index_to_num[''.join(map(str, sorted([mapping[ch] for ch in number])))]
    return n


def get_mapping(encoded_numbers: Set[str]) -> Dict[str, int]:
    all_chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    possible_options = [set(all_chars) for _ in range(7)]
    """
          [0]
         dddd
    [1] e    a [2]
        e    a
         ffff  [3]
        g    b
    [4] g    b [5]
         cccc
          [6]
    """

    def remove_options(idxs: Iterable[int], chars: List[str]):
        for idx in idxs:
            possible_options[idx] -= set(chars)

    def allowed_options(idxs: Iterable[int], chars: List[str]):
        all_idxs = set(range(7))
        remove_options(all_idxs - set(idxs), chars)
        remove_options(idxs, list(set(all_chars) - set(chars)))

    def cleanup():
        found_items = []
        for char_set in possible_options:
            if len(char_set) == 1:
                found_items.append(list(char_set)[0])

        reprocess = False
        for char_set in possible_options:
            if len(char_set) > 1:
                char_set -= set(found_items)
                if len(char_set) == 1:
                    reprocess = True
        if reprocess:
            cleanup()

    while sum([len(x) for x in possible_options]) != 7:
        ns = list(encoded_numbers)
        for encoded_number in ns:
            # e.g. encoded_number = "bfc"
            if len(encoded_number) == 2:
                # Number 1: only [2] and [5] are allowed
                allowed_options([2, 5], list(encoded_number))
            elif len(encoded_number) == 3:
                # Number 7
                allowed_options([0, 2, 5], list(encoded_number))
            elif len(encoded_number) == 4:
                # Number 4
                allowed_options([1, 2, 3, 5], list(encoded_number))
            elif len(encoded_number) == 5:
                # Either number 2, or 3, or 5
                one = possible_options[2] | possible_options[5]
                if len(one) == 2:
                    if set(encoded_number) & one == one:
                        # It is 3:
                        allowed_options([0, 2, 3, 5, 6], list(encoded_number))
                    # If we know 1 positions, we can distinguish between 2 and 5
                    elif len(possible_options[2]) == 1 and len(possible_options[5]) == 1:
                        if set(encoded_number) & possible_options[2] == possible_options[2]:
                            # It is 2
                            allowed_options([0, 2, 3, 4, 6], list(encoded_number))
                        else:
                            # It is 5
                            allowed_options([0, 1, 3, 5, 6], list(encoded_number))
            elif len(encoded_number) == 6:
                # Either number 0, or 6, or 9
                #
                # If 1 is not present inside - it's 6
                one = possible_options[2] | possible_options[5]
                if len(one) == 2 and set(encoded_number) & one != one:
                    uniq = one - set(encoded_number)
                    allowed_options([2], list(uniq))

            elif len(encoded_number) == 7:
                # Number 8
                pass
            cleanup()

    return {char: idx for idx, char in enumerate([x.pop() for x in possible_options])}


if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        with open(input_file) as fin:
            print(get_digit_sum([line.strip() for line in fin]))

assert get_digit_sum(["be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe"]) == 8394
assert get_digit_sum("""be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
""".split("\n")) == 61229
