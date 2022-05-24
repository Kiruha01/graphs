import io
import sys

from import_dataset import google_directed, ca_undirected, vk_undirected
from utils import *
from landmarks import *
import loguru

# =========== Google =============

loguru.logger.add("log.log", format="{level} {message}", level="DEBUG")


@loguru.logger.catch
def main():
    print("\nGoogle!!\n\n")

    google_graph = ca_undirected("test_datasets/web-Google.txt")
    comps = weak_conns(google_graph)

    google_land = LandmarksBasic(google_graph, 5, SelectLandmarksMethod.MANUAL)

    print(google_land._landmarks)

    print(google_land.distance(5, 3))

    exit()

    total_v = google_graph.num_vertices
    total_e = google_graph.num_edges
    print(f"v: {total_v}, e: {total_e}")
    print("part:", total_e / (2 * (total_v**2 - total_v)))

    print("Слабая связность", comps)
    max_weak_comp = max(comps, key=len)
    print("Доля вершин:", len(max_weak_comp) / total_v)

    comps = strong_conns(google_graph)
    print("Сильная связность: ", comps)
    max_strong_comp = max(comps, key=len)
    print("Доля вершин:", len(max_strong_comp) / total_v)

    radius, diameter, percentile = evaluate_main_characteristics(
        google_graph, max_weak_comp
    )
    print("Радиус: ", radius)
    print("Диаметр: ", diameter)
    print("90 процентиль расстояния: ", percentile)

    # ============ CA =============

    print("\nCA!!\n\n")

    ca_graph = ca_undirected("ca.txt")
    total_v = ca_graph.num_vertices
    total_e = ca_graph.num_edges
    print(f"v: {total_v}, e: {total_e}")
    print("part:", total_e / (2 * (total_v**2 - total_v)))

    comps = weak_conns(ca_graph)
    print("Слабая связность", comps)
    max_comp = max(comps, key=len)
    print("Доля вершин:", len(max_comp) / total_v)

    radius, diameter, percentile = evaluate_main_characteristics(ca_graph, max_comp)
    print("Радиус: ", radius)
    print("Диаметр: ", diameter)
    print("90 процентиль расстояния: ", percentile)

    # ============== VK =================

    print("\nVK!!\n\n")

    vk_graph = vk_undirected("vk.csv")

    total_v = vk_graph.num_vertices
    total_e = vk_graph.num_edges
    print(f"v: {total_v}, e: {total_e}")
    print("part:", total_e / (2 * (total_v**2 - total_v)))

    comps = weak_conns(vk_graph)
    print("Слабая связность", comps)
    max_weak_comp = max(comps, key=len)
    print("Доля вершин:", len(max_weak_comp) / total_v)

    comps = strong_conns(vk_graph)
    print("Сильная связность: ", comps)
    max_strong_comp = max(comps, key=len)
    print("Доля вершин:", len(max_strong_comp) / total_v)

    radius, diameter, percentile = evaluate_main_characteristics(
        vk_graph, max_weak_comp
    )
    print("Радиус: ", radius)
    print("Диаметр: ", diameter)
    print("90 процентиль расстояния: ", percentile)


if __name__ == "__main__":
    main()
