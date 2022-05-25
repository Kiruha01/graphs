import random
from enum import Enum
from typing import Callable, List, Optional, Set, Dict
from random import sample
from collections import deque

from models import BaseGraph
from utils import get_shortest_path_lengths


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
        count_shortest_path = round(random.random() * (len(all_vert) - count_landmarks) + count_landmarks)
        all_paths = set()
        print(count_shortest_path)

        for _ in range(count_shortest_path):
            start, end = random.sample(tuple(all_vert), 2)
            print(start, end)
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


class LandmarksBasic:
    def __init__(
        self,
        graph: BaseGraph,
        count_landmarks: int,
        select_landmarks_method: Optional[SelectLandmarksMethod] = None,
    ):
        self._landmarks = select_landmarks(
            graph, count_landmarks, select_landmarks_method
        )
        self._distances = {}
        self._prepare(graph)

    def _prepare(self, graph: BaseGraph) -> None:
        for landmark in self._landmarks:
            self._distances[landmark] = get_shortest_path_lengths(graph, landmark, graph.get_all_vertices()
            )

    def distance(self, start: int, end: int) -> int:
        upper_bounder = float("inf")
        for landmark in self._landmarks:
            landmark_distance = self._distances[landmark]
            upper_bounder = min(
                upper_bounder, landmark_distance[start] + landmark_distance[end]
            )

        return upper_bounder


class LandmarksLCA(LandmarksBasic):
    def _prepare(self, graph: BaseGraph) -> None:
        for landmark in self._landmarks:
            self._distances[landmark] = get_lca_tree(graph, landmark)

    def distance(self, start: int, end: int) -> int:
        upper_bounder = float("inf")
        for landmark in self._landmarks:
            lca_path = self._calculate_distance_over_by_landmark(landmark, start, end)
            upper_bounder = min(
                upper_bounder, len(lca_path) - 1
            )

        return upper_bounder

    def _calculate_distance_over_by_landmark(self, landmark: int, start: int, end: int) -> List[int]:
        SPT = self._distances[landmark]
        path_from_start_to_landmark = self.get_path_to_set(SPT, start, {landmark})
        path_from_end_to_path_start_landmark = self.get_path_to_set(SPT, end, set(path_from_start_to_landmark))

        LCA = path_from_end_to_path_start_landmark[-1]

        path = []
        for node in path_from_start_to_landmark:
            if node != LCA:
                path.append(node)

        path.extend(reversed(path_from_end_to_path_start_landmark))
        return path

    @staticmethod
    def get_path_to_set(SPT_tree: Dict[int, int], _from: int, _target: Set[int]) -> List[int]:
        next_node = _from
        path = [next_node]
        while next_node not in _target:
            next_node = SPT_tree[next_node]
            path.append(next_node)
        return path
