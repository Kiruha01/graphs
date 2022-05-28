from typing import List, Dict, Set

from algoritms.landmarks.basic import LandmarksBasic
from algoritms.landmarks.utils import get_lca_tree
from models import BaseGraph


class LandmarksLCA(LandmarksBasic):
    def _prepare(self, graph: BaseGraph) -> None:
        for landmark in self._landmarks:
            self._distances[landmark] = get_lca_tree(graph, landmark)

    def distance(self, start: int, end: int) -> int:
        upper_bounder = float("inf")
        for landmark in self._landmarks:
            lca_path = self._calculate_distance_over_by_landmark(landmark, start, end)
            upper_bounder = min(upper_bounder, len(lca_path) - 1)

        return upper_bounder

    def _calculate_distance_over_by_landmark(
        self, landmark: int, start: int, end: int
    ) -> List[int]:
        SPT = self._distances[landmark]
        path_from_start_to_landmark = self.get_path_to_set(SPT, start, {landmark})
        path_from_end_to_path_start_landmark = self.get_path_to_set(
            SPT, end, set(path_from_start_to_landmark)
        )

        LCA = path_from_end_to_path_start_landmark[-1]

        path = []
        for node in path_from_start_to_landmark:
            if node != LCA:
                path.append(node)

        path.extend(reversed(path_from_end_to_path_start_landmark))
        return path

    @staticmethod
    def get_path_to_set(
        SPT_tree: Dict[int, int], _from: int, _target: Set[int]
    ) -> List[int]:
        next_node = _from
        path = [next_node]
        while next_node not in _target:
            next_node = SPT_tree[next_node]
            path.append(next_node)
        return path
