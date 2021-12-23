import sys
from typing import List, Tuple, Set


def convert_input(data: List[str]) -> Tuple[Set[Tuple[int, int]], List[Tuple[str, int]]]:
    dots = set()
    folds = []
    for line in data:
        if not line:
            continue
        if line.startswith("fold"):
            axis, number = line.split()[2].split("=")
            folds.append((axis, int(number)))
        else:
            dots.add(tuple(map(int, line.split(","))))
    return dots, folds


def get_dimenstions(data: Set[Tuple[int, int]]) -> Tuple[int, int]:
    X = Y = 0
    for x, y in data:
        X = max(x, X)
        Y = max(y, Y)
    return X + 1, Y + 1


def fold_paper(dots: Set[Tuple[int, int]], folds: List[Tuple[str, int]], limit_folds=None, with_draw=False) -> Set[Tuple[int, int]]:
    X, Y = get_dimenstions(dots)
    for axis, fold_idx in (folds[:limit_folds] if limit_folds else folds):
        if axis == "y":
            assert fold_idx < Y
            Y = max(fold_idx, Y - fold_idx - 1)
        else:
            assert fold_idx < X
            X = max(fold_idx, X - fold_idx - 1)

        new_dots = set()
        while dots:
            x, y = dots.pop()
            if axis == "y":
                y = Y - max(y - fold_idx, fold_idx - y)
            else:
                x = X - max(x - fold_idx, fold_idx - x)
            new_dots.add((x, y))
        dots = new_dots
    if with_draw:
        draw(dots, X, Y)
    return dots


def draw(dots: Set[Tuple[int, int]], X, Y: int):
    # X, Y = get_dimenstions(dots)
    canvas = [["."] * X for _ in range(Y)]
    for x, y in dots:
        canvas[y][x] = "#"
    print("\n".join(["".join(line) for line in canvas]))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        with open(input_file) as fin:
            data = [line.strip() for line in fin]
            print("part 1:", len(fold_paper(*convert_input(data), limit_folds=1)))
            print("part 2:", len(fold_paper(*convert_input(data), with_draw=True)))

assert len(fold_paper(*convert_input("""6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5""".split("\n")), limit_folds=1)) == 17

'''
fold_paper(*convert_input("""6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5""".split("\n")), with_draw=True)
'''
