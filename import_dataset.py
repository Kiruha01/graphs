from collections import defaultdict
from typing import Dict, List


def google_oriented(filename: str) -> Dict[int, List[int]]:
    graph = defaultdict(list)

    with open(filename, 'r') as file:
        for l in file.readlines():
            if l[0] == '#':
                continue
            new_line = l.strip()
            u, v = new_line.split('\t')
            graph[int(u)].append(int(v))
    return graph


def ca_not_oriented(filename: str) -> Dict[int, List[int]]:
    graph = defaultdict(list)

    with open(filename, 'r') as file:
        for l in file.readlines():
            if l[0] == '#':
                continue
            new_line = l.strip()
            u, v = new_line.split('\t')
            if int(v) not in graph[int(u)]:
                graph[int(u)].append(int(v))
            if int(u) not in graph[int(v)]:
                graph[int(v)].append(int(u))
    return graph
