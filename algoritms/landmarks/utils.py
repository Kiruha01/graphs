import random
from collections import deque
from enum import Enum
from random import sample
from typing import Dict, Set, List

from models import BaseGraph


def get_lca_tree(graph: BaseGraph, vertex: int) -> Dict[int, int]:
    tree = {}
    stack = deque([vertex])
    while stack:
        node = stack.popleft()
        for n in graph.neighbors[node]:
            if n not in tree.keys():
                tree[n] = node
                stack.append(n)
    return tree


def compute_coverage(paths: Set[Set[int]], node: int) -> int:
    coverage = 0
    for path in paths:
        if node in path:
            coverage += 1

    return coverage


class SelectLandmarksMethod(Enum):
    RANDOM = "rnd"
    MAX_DEGREE = "max_deg"
    BEST_COVERAGE = "best_cov"

    # Dev mode
    MANUAL = "manual"


def select_landmarks(
    graph: BaseGraph,
    count_landmarks: int,
    method: SelectLandmarksMethod = SelectLandmarksMethod.RANDOM,
) -> List[int]:
    if method == SelectLandmarksMethod.RANDOM:
        return sample(tuple(graph.get_all_vertices()), count_landmarks)

    elif method == SelectLandmarksMethod.MAX_DEGREE:
        sorted_all_vertices = sorted(
            graph.get_all_vertices(),
            key=lambda v: len(graph.neighbors[v]),
            reverse=True,
        )
        return sorted_all_vertices[:count_landmarks]

    elif method == SelectLandmarksMethod.BEST_COVERAGE:
        all_vert = graph.get_all_vertices()
        count_shortest_path = len(all_vert) % 500
        all_paths = set()

        for _ in range(count_shortest_path):
            start, end = random.sample(tuple(all_vert), 2)
            tree = get_lca_tree(graph, start)
            path = {end}
            node = end
            while node != start:
                node = tree[node]
                path.add(node)

            all_paths.add(frozenset(path))

        landmarks = []
        while len(landmarks) < count_landmarks and all_paths:
            best_coverage = 0
            best_landmark = None

            for v in all_vert:
                v_coverage = compute_coverage(all_paths, v)
                if v_coverage > best_coverage:
                    best_coverage = v_coverage
                    best_landmark = v

            landmarks.append(best_landmark)
            all_paths = set(filter(lambda s: best_landmark not in s, all_paths))
            all_vert.remove(best_landmark)

        # if len(landmarks) < count_landmarks:
        #     landmarks.extend(random.sample(all_vert, count_landmarks - len(landmarks)))

        return landmarks

    elif method == SelectLandmarksMethod.MANUAL:
        return list(map(int, input("Landmarks: ").split()))

    raise NotImplementedError
