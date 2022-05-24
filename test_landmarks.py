import pytest
from random import seed

from import_dataset import ca_undirected
from utils import split_graph, weak_conns
from landmarks import SelectLandmarksMethod, LandmarksBasic


@pytest.fixture
def google():
    g = ca_undirected("test_datasets/web-Google.txt")
    wc = weak_conns(g)
    return split_graph(g, wc)[0]


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
