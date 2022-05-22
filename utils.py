import copy
from scipy.special import comb
import random
from typing import List, Tuple, Optional, Dict, Union, Callable, Any, Set
from collections import deque, defaultdict, OrderedDict

from models import BaseGraph, UndirectedGraph, UndirectedWeightedGraph


def weak_conns(graph: BaseGraph) -> List[Set[int]]:
    """Поиск компонент слабой связности"""

    unvisited = copy.deepcopy(graph.get_all_vertices())
    comps = []

    while unvisited:
        start = unvisited.pop()
        comps.append(set())
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
                    comps[-1].add(v)
    return comps


def strong_conns(graph: BaseGraph) -> List[Set[int]]:
    """Поиск компонент сильной связности"""

    unvisited = copy.deepcopy(graph.get_all_vertices())
    time = len(unvisited)
    ver_priority = OrderedDict()
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
                ver_priority[v] = time
                time -= 1

    # DFS on normal graph with new order
    comps = []
    while ver_priority:
        start = ver_priority.popitem()[0]
        stack = deque([[start, graph.out_vertices_by_priority(start, ver_priority)]])
        comps.append(set())
        while stack:
            v, next_vertex_gen = stack[-1]
            if ver_priority.get(v):
                ver_priority.pop(v)

            for out in next_vertex_gen:
                stack.append([out, graph.out_vertices_by_priority(out, ver_priority)])
                break
            else:
                stack.pop()
                comps[-1].add(v)
    return comps


def _get_shortest_path_lengths(graph: BaseGraph, source: int, vertices: Optional[List[int]]) -> Dict[int, int]:
    """Кротчайшее расстояние от v до вершин vertices поиском в ширину"""

    unvisited_target_vertices = set(vertices)
    unvisited_target_vertices.discard(source)
    lengths = {source: 0}
    queue = deque([(source, 0)])
    while unvisited_target_vertices:
        v, length = queue.popleft()
        for n in graph.neighbors[v]:
            if n not in lengths:
                queue.append((n, length + 1))
                lengths[n] = length + 1
                unvisited_target_vertices.discard(n)

    return {v: lengths[v] for v in vertices}


def evaluate_main_characteristics(graph: BaseGraph, max_weak_comp: List[int], k: int = 500) -> Tuple[int, int, int]:
    """
    Оценка значения радиуса, диаметра сети, 90 процентиля расстояния (геодезического) между вершинами графа
    на k случайных вершинах
    """

    random_vertices = random.sample(max_weak_comp, k=k) if len(max_weak_comp) > k else max_weak_comp

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
        degree[len(graph.neighbors[v])].append(v)
    return degree


def num_of_triangles(graph: BaseGraph) -> int:
    """
    Подсчёт количества треугольников (полных подграфов на 3-х вершинах)
    """
    marked_a = set()
    triangles = 0
    for a in graph.get_all_vertices():
        marked_b = set()
        marked_b.add(a)
        for b in graph.neighbors[a]:
            if b not in marked_a:
                for c in graph.neighbors[b]:
                    if c not in marked_b and c not in marked_a and a in graph.neighbors[c]:
                        triangles += 1
            marked_b.add(b)
        marked_a.add(a)
    return triangles


def _edges_between_n(graph: BaseGraph, v: int) -> int:
    """
    Подсчёт количества рёбер между соседями вершины v
    """
    edges = set()
    neigh = graph.neighbors[v]
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
    degree = len(graph.neighbors[v])
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
        n = len(graph.neighbors[v])
        combi = comb(n, 2, exact=True)

        sum_for_avg += local_coef
        sum_for_global += combi*local_coef
        sum_of_comb += combi

    average = sum_for_avg/len(vertices)
    glob = sum_for_global/sum_of_comb
    return average, glob


def split_graph(
    graph: Union[UndirectedGraph, UndirectedWeightedGraph],
    weak_conns: List[List[int]],
) -> List[Union[UndirectedGraph, UndirectedWeightedGraph]]:
    """
    Разделить граф по компонентам слабой связности

    :param graph:
    :param weak_conns:
    """
    graphs = []

    for component in weak_conns:
        new_graph = UndirectedGraph() if isinstance(graph, UndirectedGraph) else UndirectedWeightedGraph()
        for vertex in component:
            new_graph.outgoing_adj_list[vertex] = graph.outgoing_adj_list[vertex]
        graphs.append(new_graph)

    return graphs


def run_on_graphs(
        func: Callable[[BaseGraph, Any], Any],
        graphs: List[Union[UndirectedGraph, UndirectedWeightedGraph]],
        adder: Callable[[Any, Any], Any],
        *args,
        **kwargs,
) -> Any:
    """
    Запуск функции на множестве графов с последующим суммированием результата

    :param func: Целевая функция, результат которой необходимо узнать
    :param graphs: Множество графов, полученное функцией split_graph
    :param adder: Функция суммирования результата. Должна иметь сигнатуру

    def adder(result: Any, value: Any=None) -> Any:
        ...
    """
    result = None
    for index, graph in enumerate(graphs):
        print(f">graph {index+1} of {len(graphs)}, size {graph.num_vertices}...", end=' ')
        val = func(graph, *args, **kwargs)
        if result is not None:
            result = adder(result, val)
        else:
            result = val
        print(f"Pre-result: {result}")
    return result


def get_proportions_after_vertices_removal(
        graph: BaseGraph, step: float = 1.0, del_only_max_degree: bool = False
) -> Tuple[List[float], List[float]]:
    assert 0 < step < 100

    graph_copy = copy.deepcopy(graph)

    result_x = []
    result_y = []
    x = 0.0
    while x < 100:
        all_vertices = list(graph_copy.get_all_vertices())

        # delete needed number of vertices
        percent_to_delete = 0.0 if x == 0.0 else 1 - (1 - x / 100) / (1 - (x - step) / 100)
        vertices_num_to_delete = int(len(all_vertices) * percent_to_delete)
        if del_only_max_degree:
            sorted_all_vertices = sorted(all_vertices, key=lambda v: len(graph_copy.neighbors[v]), reverse=True)
            vertices_to_delete = sorted_all_vertices[:vertices_num_to_delete]
        else:
            vertices_to_delete = random.sample(all_vertices, k=vertices_num_to_delete)
        graph_copy.delete_vertices(vertices_to_delete)

        # add proportion
        comps = weak_conns(graph_copy)
        max_weak_comp = max(comps, key=len)
        result_x.append(x)
        result_y.append(len(max_weak_comp) / graph_copy.num_vertices)

        x += step

    result_x.append(100.0)
    result_y.append(0.0)

    return result_x, result_y
