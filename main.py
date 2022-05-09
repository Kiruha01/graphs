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

v = len(google_graph.get_all_vertices())
e = google_graph.num_edges
print(f"v: {v}, e: {e}")
print("part:", e/(2*(v**2-v)))

# Слабая связность
unvisited = set(google_graph.get_all_vertices())
num_of_comps = 0

while unvisited:
    start = unvisited.pop()
    num_of_comps += 1
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

print("Сдабая св", num_of_comps)



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
