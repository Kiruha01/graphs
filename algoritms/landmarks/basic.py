from typing import Optional

from algoritms.landmarks.utils import SelectLandmarksMethod, select_landmarks
from models import BaseGraph


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
