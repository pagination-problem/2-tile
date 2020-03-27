import context
from tree import Tree
import networkx as nx
import string

def test_creation_from_prufer():
    sequence = [3, 3, 3, 4]
    t1 = Tree(sequence)
    t2 = nx.from_prufer_sequence(sequence)
    d = dict(enumerate(string.ascii_lowercase, 0))
    t2 = nx.relabel_nodes(t2, d)
    assert set(t1.tree.nodes) == set(t2.nodes)
    assert set(t1.tree.edges) == set(t2.edges)

def test_random_generation ():
    n = 10
    t = Tree(n)
    assert len(set(t.tree.nodes)) == n
    assert len(set(t.tree.edges)) == n-1

def test_find_leaves():
    sequence = [3, 3, 3, 4]
    t = Tree(sequence)
    assert t.find_leaves() == {'a', 'b', 'c', 'f'}

def test_find_a_diameter():
    sequence = [3, 3, 3, 4]
    t = Tree(sequence)

    set_of_all_possible_diameters = set()
    #This trick is necessary because I cannot make a set of lists
    # as lists are non-hashable elements.
    a = [['a', 'd', 'e', 'f'], ['b', 'd', 'e', 'f'], ['c', 'd', 'e', 'f']]
    for i in a:
        set_of_all_possible_diameters.add(tuple(i)) 

    computed_diameter = t.find_a_diameter()
    computed_diameter = tuple(computed_diameter)
    print(computed_diameter)
    print(set_of_all_possible_diameters)
    assert computed_diameter in set_of_all_possible_diameters

def test_to_cplex_input():
    print("lauch test_to_cplex_input")
    t = Tree(4)
    print("end of test_to_cplex_input")
