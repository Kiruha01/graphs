from models import DirectedGraph, UndirectedGraph, WeightedDirectedGraph
import csv


def google_directed(filename: str, num_of_nodes: int) -> DirectedGraph:
    graph = DirectedGraph(num_of_nodes)

    with open(filename, 'r') as file:
        for l in file.readlines():
            if l[0] == '#':
                continue
            new_line = l.strip()
            u, v = new_line.split('\t')
            graph.add_edge(int(u), int(v))
    return graph


def ca_undirected(filename: str, num_of_nodes: int) -> UndirectedGraph:
    graph = UndirectedGraph(num_of_nodes)

    with open(filename, 'r') as file:
        for l in file.readlines():
            if l[0] == '#':
                continue
            new_line = l.strip()
            u, v = new_line.split('\t')
            graph.add_edge(int(u), int(v))
    return graph


def vk_directed(filename: str, num_of_nodes: int):
    graph = WeightedDirectedGraph(num_of_nodes)

    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        next(reader)
        for row in reader:
            u, v, t, h = "".join(row).split(",")
            if t != '0':
                graph.add_edge(int(u), int(v), int(t))
            if h != '0':
                graph.add_edge(int(v), int(u), int(h))

    return graph

