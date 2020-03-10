from tree import Tree
import networkx as nx

def test_creation_from_prufer():
    sequence = [3, 3, 3, 4]
    t1 = Tree(sequence)
    t2 = nx.from_prufer_sequence(sequence)
    assert t1 == t2

def test_find_leaves():
    sequence = [3, 3, 3, 4]
    t = Tree(sequence)
    assert t.find_leaves_of() == {0, 1, 2, 5}