from enum import Enum
from typing import Callable, List, Optional
from random import sample

from models import BaseGraph
from utils import get_shortest_path_lengths


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
        return sample(graph.get_all_vertices(), count_landmarks)

    elif method == SelectLandmarksMethod.MAX_DEGREE:
        sorted_all_vertices = sorted(
            graph.get_all_vertices(),
            key=lambda v: len(graph.neighbors[v]),
            reverse=True,
        )
        return sorted_all_vertices[:count_landmarks]

    elif method == SelectLandmarksMethod.MANUAL:
        return list(map(int, input("Landmarks: ").split()))

    elif method == SelectLandmarksMethod.BEST_COVERAGE:
        # TODO: Best Coverage
        raise NotImplementedError

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

    def _prepare(self, graph: BaseGraph):
        for landmark in self._landmarks:
            self._distances[landmark] = get_shortest_path_lengths(
                graph, landmark, graph.get_all_vertices()
            )

    def distance(self, start: int, end: int) -> int:
        upper_bounder = float("inf")
        for landmark in self._landmarks:
            landmark_distance = self._distances[landmark]
            upper_bounder = min(
                upper_bounder, landmark_distance[start] + landmark_distance[end]
            )

        return upper_bounder
