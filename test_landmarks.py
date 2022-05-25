import sys

import loguru
import pytest
from random import seed
import io

from import_dataset import ca_undirected
from utils import split_graph, weak_conns
from landmarks import SelectLandmarksMethod, LandmarksBasic, LandmarksLCA
from models import UndirectedGraph


@pytest.fixture
def google():
    g = ca_undirected("test_datasets/web-Google.txt")
    wc = weak_conns(g)
    return split_graph(g, wc)[0]


@pytest.fixture
def SPT():
    d = {
        2: 1,
        6: 1,
        3: 1,
        4: 3,
        5: 3
    }
    return d


@pytest.fixture
def simple_graph(SPT):
    g = UndirectedGraph()
    for u, v in SPT.items():
        g.add_edge(u, v)
    return g


@pytest.mark.parametrize("num_of_landmarks", [i for i in range(1, 9)])
@pytest.mark.parametrize(
    "method",
    [
        SelectLandmarksMethod.RANDOM,
        SelectLandmarksMethod.MAX_DEGREE,
        pytest.param(SelectLandmarksMethod.BEST_COVERAGE, marks=pytest.mark.xfail),
    ],
)
def test__google_landmarks(google, num_of_landmarks, method):
    seed(0)
    land = LandmarksBasic(google, num_of_landmarks, method)
    if num_of_landmarks == 1 and method == SelectLandmarksMethod.RANDOM:
        assert land.distance(10, 5) == 5
    else:
        assert land.distance(10, 5) == 3


def test__get_path_to_set(SPT):
    path = LandmarksLCA.get_path_to_set(SPT, 4, {2, 1, 6})
    assert path == [4, 3, 1]


def test__lca_simple(simple_graph):
    sys.stdin = io.StringIO("1")
    land = LandmarksLCA(simple_graph, 1, SelectLandmarksMethod.MANUAL)

    assert land._calculate_distance_over_by_landmark(1, 4, 2) == [4, 3, 1, 2]


@pytest.mark.parametrize("num_of_landmarks", [i for i in range(1, 9)])
@pytest.mark.parametrize(
    "method",
    [
        SelectLandmarksMethod.RANDOM,
        SelectLandmarksMethod.MAX_DEGREE,
        SelectLandmarksMethod.BEST_COVERAGE,
    ],
)
def test__google_landmarks_lca(google, num_of_landmarks, method):
    seed(0)
    land = LandmarksLCA(google, num_of_landmarks, method)
    if num_of_landmarks == 1 and method == SelectLandmarksMethod.RANDOM:
        assert land.distance(10, 5) == 4
    else:
        assert land.distance(10, 5) == 3
