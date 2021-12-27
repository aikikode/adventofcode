import heapq
import math
import sys
from typing import List, Tuple


def convert_input(data: List[str]) -> List[List[int]]:
    return [list(map(int, line)) for line in data if line]


def get_neighbours(x, y: int, limit: int) -> List[Tuple[int, int]]:
    return [
        (i, j)
        for i, j in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        if not (i < 0 or j < 0 or i >= limit or j >= limit)
    ]


def get_shortest_path_len(data: List[List[int]]) -> int:
    """ Use Dijkstra's Shortest Path Algorithm """
    limit = len(data)
    assert len(data) == len(data[0])  # data is square
    visited = [[False] * limit for _ in range(limit)]
    distance = [[math.inf] * limit for _ in range(limit)]
    distance[0][0] = 0
    heap = []
    heapq.heappush(heap, (0, (0, 0)))
    while heap:
        dist, (x, y) = heapq.heappop(heap)
        if visited[x][y]:
            continue
        visited[x][y] = True
        for i, j in get_neighbours(x, y, limit):
            distance[i][j] = min(distance[i][j], distance[x][y] + data[i][j])
            heapq.heappush(heap, (distance[i][j], (i, j)))
    return int(distance[-1][-1])


if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        with open(input_file) as fin:
            data = [line.strip() for line in fin]
            print("part 1:", get_shortest_path_len(convert_input(data)))

assert get_shortest_path_len(convert_input("""1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581""".split("\n"))) == 40
