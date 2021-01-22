import networkx as nx

from heuristics import heuristic_one_and_two, heuristic_three


# A graphic representation of this graph and its different solutions
# is available in this Overlaf document :
# or in a power point.

edges = [
    (1, 2),
    (2, 3), (2, 4), (2, 12),
    (3, 4), (3, 6), (3, 12),
    (4, 5),
    (5, 6),
    (6, 7), (6, 8),
    (7, 8), (7, 9),
    (8, 9),
    (9, 10), (9, 12),
    (10, 12),
    (11, 12)
]

g = nx.Graph()
g.add_edges_from(edges)

def test_heuristic_one():
    expected_M1 = [1, 5, 10]
    expected_M2 = [3, 7, 11]
    expected_sep = [2, 4, 6, 8, 9, 12]

    (P1, P2, sep) = heuristic_one_and_two(g, False)

    assert sorted(P1) == expected_M1
    assert sorted(P2) == expected_M2
    assert sorted(sep) == expected_sep

def test_heuristic_two():
    expected_M1 = [1, 12]
    expected_M2 = [4, 6]
    expected_sep = [2, 3, 5, 7, 8, 9, 10, 11]

    (P1, P2, sep) = heuristic_one_and_two(g, True)

    assert sorted(P1) == expected_M1
    assert sorted(P2) == expected_M2
    assert sorted(sep) == expected_sep


def test_heuristic_three():
    expected_M1 = [1, 3, 5]
    expected_M2 = [7, 10, 11]
    expected_sep = [2, 4, 6, 8, 9, 12]

    (P1, P2, sep) = heuristic_one_and_two(g, True)

    assert sorted(P1) == expected_M1
    assert sorted(P2) == expected_M2
    assert sorted(sep) == expected_sep

