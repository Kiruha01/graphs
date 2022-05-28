from models.graphs.base_graph import BaseGraph
from models.edges import Edge, WeightedEdge


class UndirectedGraph(BaseGraph):
    def add_edge(self, _from: int, _to: int) -> None:
        self.outgoing_adj_list[_from].append(Edge(_from, _to))
        self.outgoing_adj_list[_to].append(Edge(_to, _from))
        self.num_edges += 2

        self.neighbors[_from].append(_to)
        self.neighbors[_to].append(_from)

    def is_weighted(self) -> bool:
        return False

    def is_directed(self) -> bool:
        return False


class UndirectedWeightedGraph(BaseGraph):
    def add_edge(self, _from: int, _to: int, _weight: int) -> None:
        self.outgoing_adj_list[_from].append(
            WeightedEdge(_from, _to, _weight)
        )
        self.outgoing_adj_list[_to].append(
            WeightedEdge(_to, _from, _weight)
        )
        self.num_edges += 2

        self.neighbors[_from].append(_to)
        self.neighbors[_to].append(_from)

    def is_weighted(self) -> bool:
        return True

    def is_directed(self) -> bool:
        return False
