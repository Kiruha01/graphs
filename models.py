from dataclasses import dataclass
from typing import List


@dataclass
class Edge:
    start: int
    end: int


@dataclass
class WeightedEdge(Edge):
    weight: int


class DirectedGraph:
    def __init__(self, num):
        self.num_vertices = num
        self.num_edges = 0
        self.adj_list = [[] for _ in range(num)]

    def add_edge(self, _from: int, _to: int) -> None:
        self.adj_list[_from].append(Edge(_from, _to))
        self.num_edges += 1

    def get_all_edges_of(self, v: int) -> List[Edge]:
        """Get all edges connected v"""
        return self.adj_list[v]

    def get_all_edges(self) -> List[Edge]:
        """Get all edges of this graph"""
        return [e for i in range(self.num_vertices) for e in self.adj_list[i]]


class UndirectedGraph(DirectedGraph):
    def add_edge(self, _from: int, _to: int) -> None:
        self.adj_list[_from].append(Edge(_from, _to))
        self.adj_list[_to].append(Edge(_to, _from))
        self.num_edges += 2


class WeightedDirectedGraph:
    def __init__(self, num):
        self.num_vertices = num
        self.num_edges = 0
        self.adj_list = [[] for _ in range(num)]

    def add_edge(self, _from: int, _to: int, _weight: int) -> None:
        self.adj_list[_from].append(WeightedEdge(_from, _to, _weight))
        self.num_edges += 1

    def get_all_edges_of(self, v: int) -> List[WeightedEdge]:
        """Get all edges connected v"""
        return self.adj_list[v]

    def get_all_edges(self) -> List[WeightedEdge]:
        """Get all edges of this graph"""
        return [e for i in range(self.num_vertices) for e in self.adj_list[i]]


class UndirectedWeightedGraph(WeightedDirectedGraph):
    def add_edge(self, _from: int, _to: int, _weight: int) -> None:
        self.adj_list[_from].append(WeightedEdge(_from, _to, _weight))
        self.adj_list[_to].append(WeightedEdge(_from, _to, _weight))
        self.num_edges += 2
