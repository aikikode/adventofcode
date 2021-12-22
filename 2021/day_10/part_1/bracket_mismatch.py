import sys
from typing import List, Optional


def convert_input(data: List[str]) -> List[str]:
    return data


def get_mismatched_bracket(line: str) -> Optional[str]:
    closed_brackets_to_open = {
        ")": "(",
        "]": "[",
        "}": "{",
        ">": "<",
    }
    stack = []
    for char in line:
        if char in ["(", "[", "{", "<"]:
            stack.append(char)
        else:
            if stack and stack[-1] == closed_brackets_to_open[char]:
                stack.pop()
            else:
                return char
    return None


def get_error_score(data: List[str]) -> int:
    scores = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137,
    }
    total_score = 0
    for line in data:
        bracket = get_mismatched_bracket(line)
        total_score += scores.get(bracket, 0)
    return total_score


if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        with open(input_file) as fin:
            data = [line.strip() for line in fin]
            print(get_error_score(convert_input(data)))

assert get_error_score(convert_input("""[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]""".split("\n"))) == 26397
