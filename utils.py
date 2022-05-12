import copy
import math
import random
from typing import List, Tuple, Optional, Dict
from collections import deque, defaultdict

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
        for edge in graph.outgoing_adj_list[min_v]:
            lengths[edge.end] = min(lengths[edge.end], lengths[min_v] + 1)
        for edge in graph.incoming_adj_list[min_v]:
            lengths[edge.start] = min(lengths[edge.start], lengths[min_v] + 1)
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


def evaluate_vertices_degree(graph: BaseGraph) -> Dict[int, list]:
    """
    Подсчёт вершин с определённой степенью
    """
    degree = defaultdict(list)
    for v in graph.get_all_vertices():
        degree[len(tuple(graph.neighbors(v)))].append(v)
    return degree


def num_of_triangles(graph: BaseGraph) -> int:
    """
    Подсчёт количества треугольников (полных подграфов на 3-х вершинах)
    """
    marked_a = set()
    triangles = 0
    for a in graph.get_all_vertices():
        marked_b = set()
        for b in filter(lambda x: x not in marked_a, graph.neighbors(a)):
            for c in filter(lambda x: x not in marked_a | marked_b | {a},
                            graph.neighbors(b)):
                if a in graph.neighbors(c):
                    triangles += 1
            marked_b.add(b)
        marked_a.add(a)
    return triangles


def _edges_between_n(graph: BaseGraph, v: int) -> int:
    """
    Подсчёт количества рёбер между соседями вершины v
    """
    edges = set()
    neigh = set(graph.neighbors(v))
    for n in neigh:
        for n_edge in graph.outgoing_adj_list[n]:
            if n_edge.end in neigh:
                edges.add(n_edge)
        for n_edge in graph.incoming_adj_list[n]:
            if n_edge.start in neigh:
                edges.add(n_edge)
    return len(edges)


def _local_cluster_coefficient(graph: BaseGraph, v: int) -> float:
    """
    Вычисление локального кластерного коэффициента графа на вершине v
    """
    degree = len(tuple(graph.neighbors(v)))
    if degree < 2:
        return 0

    e = _edges_between_n(graph, v)
    return 2 * e / (degree * (degree - 1))


def average_and_global_cluster_coefficients(graph: BaseGraph) -> Tuple[float, float]:
    """
    Вычисление среднего и глобального кластерного коэффициента графа
    """
    sum_for_avg, sum_for_global, sum_of_comb = 0, 0, 0
    vertices = graph.get_all_vertices()
    for v in vertices:
        local_coef = _local_cluster_coefficient(graph, v)
        n = len(tuple(graph.neighbors(v)))
        comb = math.comb(n, 2)

        sum_for_avg += local_coef
        sum_for_global += comb*local_coef
        sum_of_comb += comb

    average = sum_for_avg/len(vertices)
    glob = sum_for_global/sum_of_comb
    return average, glob
