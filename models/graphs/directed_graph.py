from models.graphs.base_graph import BaseGraph
from models.edges import Edge, WeightedEdge


class DirectedGraph(BaseGraph):
    def add_edge(self, _from: int, _to: int) -> None:
        edge = Edge(_from, _to)
        self.outgoing_adj_list[_from].append(edge)
        self.incoming_adj_list[_to].append(edge)
        self.num_edges += 1

        self.neighbors[_from].append(_to)
        self.neighbors[_to].append(_from)

    def is_weighted(self) -> bool:
        return False

    def is_directed(self) -> bool:
        return True


class WeightedDirectedGraph(BaseGraph):
    def add_edge(self, _from: int, _to: int, _weight: int) -> None:
        edge = WeightedEdge(_from, _to, _weight)
        self.outgoing_adj_list[_from].append(edge)
        self.incoming_adj_list[_to].append(edge)

        self.num_edges += 1

        self.neighbors[_from].append(_to)
        self.neighbors[_to].append(_from)

    def is_weighted(self) -> bool:
        return True

    def is_directed(self) -> bool:
        return True
