from tree import Tree
import networkx as nx

def test_creation_from_prufer():
    sequence = [3, 3, 3, 4]
    t1 = Tree(sequence)
    t2 = nx.from_prufer_sequence(sequence)
    assert set(t1.tree.nodes) == set(t2.nodes)
    assert set(t1.tree.edges) == set(t2.edges)

def test_find_leaves():
    sequence = [3, 3, 3, 4]
    t = Tree(sequence)
    assert t.find_leaves() == {0, 1, 2, 5}
