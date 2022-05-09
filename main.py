from typing import Set

from import_dataset import google_directed, ca_undirected, vk_directed
from models import DirectedGraph


def dfs(graph: DirectedGraph, unvisited: Set[int], start: int):
    for edge in graph.outgoing_adj_list[start]:
        if edge.end in unvisited:
            unvisited.remove(edge.end)
            dfs(graph, unvisited, edge.end)




google_graph = google_directed('.google.txt')
# ca_graph = ca_undirected('.ca.txt')
# vk_graph = vk_directed('.test.csv')

total_v = len(google_graph.get_all_vertices())
total_e = google_graph.num_edges
print(f"v: {total_v}, e: {total_e}")
print("part:", total_e/(2*(total_v**2-total_v)))

# Слабая связность

unvisited = set(google_graph.get_all_vertices())
comps = []

while unvisited:
    start = unvisited.pop()
    comps.append([])
    stack = [start]
    while stack:
        v = stack[-1]
        unvisited.discard(v)
        for out_edge in google_graph.outgoing_adj_list[v]:
            if out_edge.end in unvisited:
                stack.append(out_edge.end)
                break
        else:
            for in_edge in google_graph.incoming_adj_list[v]:
                if in_edge.start in unvisited:
                    stack.append(in_edge.start)
                    break
            else:
                stack.pop(-1)
                comps[-1].append(v)

print("Сдабая св", comps)
max_comp = max(comps, key=lambda x: len(x))
print("Доля вершин:", len(max_comp)/total_v)

# Сильная связность

ver_order = []
unvisited = set(google_graph.get_all_vertices())
while unvisited:
    # DFS on inverted graph
    start = unvisited.pop()
    stack = [start]
    while stack:
        v = stack[-1]
        unvisited.discard(v)
        for in_edge in google_graph.incoming_adj_list[v]:
            if in_edge.start in unvisited:
                stack.append(in_edge.start)
                break
        else:
            stack.pop(-1)
            ver_order.append(v)
ver_order.reverse()

# DFS on normal graph with new order
unvisited = set(google_graph.get_all_vertices())
comps = []
while unvisited:
    start = sorted(unvisited, key=lambda x: ver_order.index(x))[0]
    stack = [start]
    comps.append([])
    while stack:
        v = stack[-1]
        unvisited.discard(v)
        s = sorted(google_graph.outgoing_adj_list[v], key=lambda edge: ver_order.index(edge.end))
        for out_edge in sorted(google_graph.outgoing_adj_list[v], key=lambda edge: ver_order.index(edge.end)):
            if out_edge.end in unvisited:
                stack.append(out_edge.end)
                break
        else:
            stack.pop(-1)
            comps[-1].append(v)

print('Strong: ', comps)
max_comp = max(comps, key=lambda x: len(x))
print("Доля вершин:", len(max_comp)/total_v)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
