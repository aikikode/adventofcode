import copy
import sys
from collections import defaultdict
from typing import List, Tuple, Dict, Set


def convert_input(data: List[str]) -> List[Tuple[str, str]]:
    return [tuple(line.split("-")) for line in data]


def create_connections(data: List[Tuple[str, str]]) -> Dict[str, List[str]]:
    connections = defaultdict(list)
    for a, b in data:
        connections[a].append(b)
        connections[b].append(a)
    return connections


def get_paths(node: str, connections: Dict[str, List[str]], visited: Set[str]):
    if node in visited:
        return 0
    if node.islower():
        visited.add(node)
    if node == "end":
        return 1
    # Paths count is the sum of all pathes from all children
    paths = 0
    for neighbour in connections[node]:
        paths += get_paths(neighbour, connections, copy.deepcopy(visited))
    return paths


def count_paths(data: List[Tuple[str, str]]) -> int:
    """ May visit small caves only once """
    connections = create_connections(data)
    visited = set()
    return get_paths("start", connections, visited)


def get_complex_paths(node: str, connections: Dict[str, List[str]], visited: Set[str], visited_twice: str):
    if node == visited_twice:
        return 0  # we already processed it twice
    if node == "start" and node in visited:
        return 0  # do not process start again
    if node in visited and visited_twice:
        return 0  # we already processed some small node twice

    if node.islower():
        if node in visited:
            visited_twice = node
        visited.add(node)
    if node == "end":
        return 1
    # Paths count is the sum of all pathes from all children
    paths = 0
    for neighbour in connections[node]:
        paths += get_complex_paths(neighbour, connections, copy.deepcopy(visited), visited_twice)
    return paths


def count_complex_paths(data: List[Tuple[str, str]]) -> int:
    """ May visit one small cave twice """
    connections = create_connections(data)
    visited = set()
    return get_complex_paths("start", connections, visited, "")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        with open(input_file) as fin:
            data = [line.strip() for line in fin]
            print("part 1:", count_paths(convert_input(data)))
            print("part 2:", count_complex_paths(convert_input(data)))

assert count_paths(convert_input("""start-A
start-b
A-c
A-b
b-d
A-end
b-end""".split("\n"))) == 10

assert count_paths(convert_input("""dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc""".split("\n"))) == 19

assert count_paths(convert_input("""fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW""".split("\n"))) == 226

assert count_complex_paths(convert_input("""start-A
start-b
A-c
A-b
b-d
A-end
b-end""".split("\n"))) == 36

assert count_complex_paths(convert_input("""dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc""".split("\n"))) == 103

assert count_complex_paths(convert_input("""fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW""".split("\n"))) == 3509
