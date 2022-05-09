from models import DirectedGraph, UndirectedGraph, WeightedDirectedGraph
import csv


def google_directed(filename: str) -> DirectedGraph:
    graph = DirectedGraph()

    with open(filename, 'r') as file:
        for l in file.readlines():
            if l[0] == '#':
                continue
            new_line = l.strip()
            u, v = new_line.split('\t')
            graph.add_edge(int(u), int(v))
    return graph


def ca_undirected(filename: str) -> UndirectedGraph:
    graph = UndirectedGraph()

    with open(filename, 'r') as file:
        for l in file.readlines():
            if l[0] == '#':
                continue
            new_line = l.strip()
            u, v = new_line.split('\t')
            graph.add_edge(int(u), int(v))
    return graph


def vk_directed(filename: str):
    graph = WeightedDirectedGraph()

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

