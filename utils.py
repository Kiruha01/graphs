import copy
import random
from typing import List, Tuple, Optional, Dict
from collections import deque

from models import BaseGraph


def weak_conns(graph: BaseGraph) -> List[List[int]]:
    """Поиск компонент слабой связности"""

    unvisited = copy.deepcopy(graph.get_all_vertices())
    comps = []

    while unvisited:
        start = unvisited.pop()
        comps.append([])
        stack = deque([start])
        while stack:
            v = stack[-1]
            unvisited.discard(v)
            for out_edge in graph.outgoing_adj_list[v]:
                if out_edge.end in unvisited:
                    stack.append(out_edge.end)
                    break
            else:
                for in_edge in graph.incoming_adj_list[v]:
                    if in_edge.start in unvisited:
                        stack.append(in_edge.start)
                        break
                else:
                    stack.pop()
                    comps[-1].append(v)
    return comps


def strong_conns(graph: BaseGraph) -> List[List[int]]:
    """Поиск компонент сильной связности"""

    ver_order = []
    unvisited = copy.deepcopy(graph.get_all_vertices())
    while unvisited:
        # DFS on inverted graph
        start = unvisited.pop()
        stack = deque([start])
        while stack:
            v = stack[-1]
            unvisited.discard(v)
            for in_edge in graph.incoming_adj_list[v]:
                if in_edge.start in unvisited:
                    stack.append(in_edge.start)
                    break
            else:
                stack.pop()
                ver_order.append(v)
    ver_order.reverse()

    # DFS on normal graph with new order
    unvisited = set(graph.get_all_vertices())
    comps = []
    while unvisited:
        start = sorted(unvisited, key=lambda x: ver_order.index(x))[0]
        stack = deque([start])
        comps.append([])
        while stack:
            v = stack[-1]
            unvisited.discard(v)
            for out_edge in sorted(graph.outgoing_adj_list[v], key=lambda edge: ver_order.index(edge.end)):
                if out_edge.end in unvisited:
                    stack.append(out_edge.end)
                    break
            else:
                stack.pop()
                comps[-1].append(v)
    return comps


def _get_shortest_path_lengths(graph: BaseGraph, source: int, vertices: Optional[List[int]] = None) -> Dict[int, int]:
    """Кротчайшее расстояние от v до вершин vertices (все если None) алгоритмом Дейкстры"""

    all_vertices = graph.get_all_vertices()

    lengths = {v: float('inf') for v in all_vertices}
    lengths[source] = 0

    unvisited = copy.deepcopy(all_vertices)
    while unvisited:
        min_v = min(unvisited, key=lambda item: lengths[item])
        for edge in graph.get_all_edges_of(min_v):
            weight = edge.weight if graph.is_weighted() else 1
            lengths[edge.end] = min(lengths[edge.end], weight + lengths[min_v])
        unvisited.discard(min_v)

    if vertices is None:
        return lengths
    else:
        return {v: lengths[v] for v in vertices}


def evaluate_main_characteristics(graph: BaseGraph, max_weak_comp: List[int], k: int = 500) -> Tuple[int, int, int]:
    """
    Оценка значения радиуса, диаметра сети, 90 процентиля расстояния (геодезического) между вершинами графа
    на k случайных вершинах
    """

    random_vertices = random.choices(max_weak_comp, k=k) if len(max_weak_comp) > k else max_weak_comp

    eccentricity = {}
    for v in random_vertices:
        path_lengths = _get_shortest_path_lengths(graph, v, random_vertices)
        eccentricity[v] = max(path_lengths.values())

    radius = min(eccentricity.values())
    diameter = max(eccentricity.values())
    percentile = sorted(eccentricity.values())[int(len(eccentricity) * 0.9)]

    return radius, diameter, percentile
