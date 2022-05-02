from models import DirectedGraph, UndirectedGraph


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
