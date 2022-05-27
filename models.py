import copy
import random
from dataclasses import dataclass
from typing import List, Union, Set, Tuple, Iterable, Dict
from collections import defaultdict


@dataclass
class Edge:
    __slots__ = ["start", "end"]
    start: int
    end: int

    def to_tuple(self) -> Tuple[str, str]:
        return str(self.start), str(self.end)

    def __hash__(self):
        if self.start > self.end:
            return hash(f"{self.start} {self.end}")
        else:
            return hash(f"{self.end} {self.start}")

    def __eq__(self, other):
        return (
            self.start == other.start
            and self.end == other.end
            or self.end == other.start
            and self.start == other.end
        )


@dataclass
class WeightedEdge(Edge):
    weight: int
    __slots__ = ["start", "end", "weight"]

    def to_tuple(self) -> Tuple[str, str, float]:
        return str(self.start), str(self.end), float(self.weight)

    def __hash__(self):
        if self.start > self.end:
            return hash(f"{self.start} {self.end}")
        else:
            return hash(f"{self.end} {self.start}")

    def __eq__(self, other):
        return (
            self.start == other.start
            and self.end == other.end
            or self.end == other.start
            and self.start == other.end
        )


class BaseGraph:
    __slots__ = ("num_edges", "outgoing_adj_list", "incoming_adj_list", "neighbors")

    def __init__(self):
        self.num_edges = 0
        self.outgoing_adj_list = defaultdict(list)
        self.incoming_adj_list = defaultdict(list)
        self.neighbors = defaultdict(list)

    def get_all_edges_of(self, v: int) -> Set[Union[Edge, WeightedEdge]]:
        """Get all edges connected v"""
        return self.outgoing_adj_list[v]

    def get_all_edges(self) -> List[Union[Edge, WeightedEdge]]:
        """Get all edges of this graph"""
        return [
            e for i in self.outgoing_adj_list.keys() for e in self.outgoing_adj_list[i]
        ]

    def get_all_vertices(self) -> Set[int]:
        return set(self.outgoing_adj_list.keys()).union(
            set(self.incoming_adj_list.keys())
        )

    def is_weighted(self):
        raise NotImplementedError()

    def is_directed(self):
        raise NotImplementedError()

    def delete_vertex(self, v: int) -> None:
        if not self.is_directed():
            del self.outgoing_adj_list[v]
            return

        end_vertices = []
        while self.outgoing_adj_list[v]:
            end_vertices.append(self.outgoing_adj_list[v][0].end)
            self.outgoing_adj_list[v].pop(0)

        for end in end_vertices:
            idx = [
                idx for idx, x in enumerate(self.incoming_adj_list[end]) if x.start == v
            ][0]
            self.incoming_adj_list[end].pop(idx)

        start_vertices = []
        while self.incoming_adj_list[v]:
            start_vertices.append(self.incoming_adj_list[v][0].start)
            self.incoming_adj_list[v].pop(0)

        for start in start_vertices:
            idx = [
                idx for idx, x in enumerate(self.outgoing_adj_list[start]) if x.end == v
            ][0]
            self.outgoing_adj_list[start].pop(idx)

    def delete_vertices(self, vertices_to_delete: List[int]):
        for v in vertices_to_delete:
            self.delete_vertex(v)

    def out_vertices_by_priority(self, v: int, priority: Dict[int, int] = None):
        new_edges = sorted(
            filter(lambda x: priority.get(x.end), self.outgoing_adj_list[v].copy()),
            key=lambda x: priority[x.end],
            reverse=True,
        )
        for i in new_edges:
            if priority.get(i.end):
                yield i.end

    def __repr__(self):
        return f"<{self.__class__.__name__} Outgoing: {self.outgoing_adj_list}; Incoming: {self.incoming_adj_list}"

    @property
    def num_vertices(self):
        return len(self.get_all_vertices())

    def __getitem__(self, key):
        return set(self.outgoing_adj_list[key]).update(self.incoming_adj_list[key])

    def __deepcopy__(self, memodict={}):
        graph_copy = self.__class__()
        for s in self.__slots__:
            setattr(graph_copy, s, copy.deepcopy(getattr(self, s)))
        return graph_copy


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


class UndirectedWeightedGraph(BaseGraph):
    def add_edge(self, _from: int, _to: int, _weight: int) -> None:
        self.outgoing_adj_list.setdefault(_from, set()).append(
            WeightedEdge(_from, _to, _weight)
        )
        self.outgoing_adj_list.setdefault(_to, set()).append(
            WeightedEdge(_to, _from, _weight)
        )
        self.num_edges += 2

        self.neighbors[_from].append(_to)
        self.neighbors[_to].append(_from)

    def is_weighted(self) -> bool:
        return True

    def is_directed(self) -> bool:
        return False
