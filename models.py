from dataclasses import dataclass
from typing import List, Union, Set, Tuple
from collections import defaultdict


@dataclass
class Edge:
    start: int
    end: int

    def to_tuple(self) -> Tuple[str, str]:
        return str(self.start), str(self.end)


@dataclass
class WeightedEdge(Edge):
    weight: int

    def to_tuple(self) -> Tuple[str, str, float]:
        return str(self.start), str(self.end), float(self.weight)


class BaseGraph:
    def __init__(self):
        self.num_edges = 0
        self.outgoing_adj_list = defaultdict(list)
        self.incoming_adj_list = defaultdict(list)

    def get_all_edges_of(self, v: int) -> List[Union[Edge, WeightedEdge]]:
        """Get all edges connected v"""
        return self.outgoing_adj_list[v]

    def get_all_edges(self) -> List[Union[Edge, WeightedEdge]]:
        """Get all edges of this graph"""
        return [e for i in self.outgoing_adj_list.keys() for e in self.outgoing_adj_list[i]]

    def get_all_vertices(self) -> Set[int]:
        return set(self.outgoing_adj_list.keys()).union(set(self.incoming_adj_list.keys()))


class DirectedGraph(BaseGraph):
    def add_edge(self, _from: int, _to: int) -> None:
        edge = Edge(_from, _to)
        self.outgoing_adj_list[_from].append(edge)
        self.incoming_adj_list[_to].append(edge)
        self.num_edges += 1


class UndirectedGraph(BaseGraph):
    def add_edge(self, _from: int, _to: int) -> None:
        self.outgoing_adj_list[_from].append(Edge(_from, _to))
        self.outgoing_adj_list[_to].append(Edge(_to, _from))
        self.num_edges += 2


class WeightedDirectedGraph(BaseGraph):
    def add_edge(self, _from: int, _to: int, _weight: int) -> None:
        edge = WeightedEdge(_from, _to, _weight)
        self.outgoing_adj_list[_from].append(edge)
        self.incoming_adj_list[_to].append(edge)

        self.num_edges += 1


class UndirectedWeightedGraph(BaseGraph):
    def add_edge(self, _from: int, _to: int, _weight: int) -> None:
        self.outgoing_adj_list.setdefault(_from, list()).append(WeightedEdge(_from, _to, _weight))
        self.outgoing_adj_list.setdefault(_to, list()).append(WeightedEdge(_from, _to, _weight))
        self.num_edges += 2
