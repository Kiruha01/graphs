# Слабая связность
from typing import List

from models import BaseGraph


def weak_conns(graph: BaseGraph) -> List[List[int]]:
    unvisited = set(graph.get_all_vertices())
    comps = []

    while unvisited:
        start = unvisited.pop()
        comps.append([])
        stack = [start]
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
                    stack.pop(-1)
                    comps[-1].append(v)
    return comps


# Сильная связность
def strong_conns(graph: BaseGraph) -> List[List[int]]:
    ver_order = []
    unvisited = set(graph.get_all_vertices())
    while unvisited:
        # DFS on inverted graph
        start = unvisited.pop()
        stack = [start]
        while stack:
            v = stack[-1]
            unvisited.discard(v)
            for in_edge in graph.incoming_adj_list[v]:
                if in_edge.start in unvisited:
                    stack.append(in_edge.start)
                    break
            else:
                stack.pop(-1)
                ver_order.append(v)
    ver_order.reverse()

    # DFS on normal graph with new order
    unvisited = set(graph.get_all_vertices())
    comps = []
    while unvisited:
        start = sorted(unvisited, key=lambda x: ver_order.index(x))[0]
        stack = [start]
        comps.append([])
        while stack:
            v = stack[-1]
            unvisited.discard(v)
            for out_edge in sorted(graph.outgoing_adj_list[v], key=lambda edge: ver_order.index(edge.end)):
                if out_edge.end in unvisited:
                    stack.append(out_edge.end)
                    break
            else:
                stack.pop(-1)
                comps[-1].append(v)
    return comps
