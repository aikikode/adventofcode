import sys
from typing import List


def convert_input(data: List[str]) -> List[str]:
    return data


def get_remaining_brackets(line: str) -> List[str]:
    closed_brackets_to_open = {
        ")": "(",
        "]": "[",
        "}": "{",
        ">": "<",
    }
    open_brackets_to_close = {
        "(": ")",
        "[": "]",
        "{": "}",
        "<": ">",
    }
    stack = []
    for char in line:
        if char in ["(", "[", "{", "<"]:
            stack.append(char)
        else:
            if stack and stack[-1] == closed_brackets_to_open[char]:
                stack.pop()
            else:
                return []
    return list(map(lambda br: open_brackets_to_close[br], stack[::-1]))


def get_error_score(data: List[str]) -> int:
    scores = {
        ")": 1,
        "]": 2,
        "}": 3,
        ">": 4,
    }
    line_scores = []
    for line in data:
        brackets = get_remaining_brackets(line)
        if brackets:
            s = 0
            for bracket in brackets:
                s = s * 5 + scores[bracket]
            line_scores.append(s)
    line_scores.sort()
    return line_scores[len(line_scores) // 2]


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
<{([{{}}[<[[[<>{}]]]>[]]""".split("\n"))) == 288957
