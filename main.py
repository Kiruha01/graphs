from import_dataset import google_directed, ca_undirected, vk_directed
from utils import weak_conns, strong_conns

# =========== Google =============

print('\nGoogle!!\n\n')

google_graph = google_directed('google.txt')

total_v = len(google_graph.get_all_vertices())
total_e = google_graph.num_edges
print(f"v: {total_v}, e: {total_e}")
print("part:", total_e/(2*(total_v**2-total_v)))

comps = weak_conns(google_graph)
print("Слабая связность", comps)
max_comp = max(comps, key=lambda x: len(x))
print("Доля вершин:", len(max_comp)/total_v)

comps = strong_conns(google_graph)
print('Strong: ', comps)
max_comp = max(comps, key=lambda x: len(x))
print("Доля вершин:", len(max_comp)/total_v)

# ============ CA =============

print('\nCA!!\n\n')

ca_graph = ca_undirected('ca.txt')
total_v = len(ca_graph.get_all_vertices())
total_e = ca_graph.num_edges
print(f"v: {total_v}, e: {total_e}")
print("part:", total_e/(2*(total_v**2-total_v)))

comps = weak_conns(ca_graph)
print("Слабая связность", comps)
max_comp = max(comps, key=lambda x: len(x))
print("Доля вершин:", len(max_comp)/total_v)

# ============== VK =================

print('\nVK!!\n\n')


vk_graph = vk_directed('vk.csv')

total_v = len(vk_graph.get_all_vertices())
total_e = vk_graph.num_edges
print(f"v: {total_v}, e: {total_e}")
print("part:", total_e/(2*(total_v**2-total_v)))

comps = weak_conns(vk_graph)
print("Слабая связность", comps)
max_comp = max(comps, key=lambda x: len(x))
print("Доля вершин:", len(max_comp)/total_v)

comps = strong_conns(vk_graph)
print('Strong: ', comps)
max_comp = max(comps, key=lambda x: len(x))
print("Доля вершин:", len(max_comp)/total_v)

