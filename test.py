from tree import Tree
import networkx as nx

sequence = [3, 3, 3, 4]
tree = Tree(sequence)
my_set = tree.find_leaves_of()
print("The leaves of my tree are :", my_set)