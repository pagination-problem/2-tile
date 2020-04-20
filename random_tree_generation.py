from tree import Tree
import math
import networkx as nx
import matplotlib.pyplot as plt
import random

"""
    This script generates number_of_desired_trees random trees
    (with a number of nodes between a lower and an upper born),
"""

MIN_NODE_NUMBER = 10
MAX_NODE_NUMBER = 10

def saves_a_tree(path, t, index):
    """
    inputs:
        path: relative or absolute path to the folder where we want to store the tree
        tree: the networkx graph we want to store

    outputs: a pdf file
        containing a graphic representation of the tree
        the name of the file will be "tree_" followed by the index and then the Prufer sequence of the tree
    """
    name = "tree_" + str(index) + "_" + str(t.prufer_sequence)

    plt.figure(figsize=(5,5))
    nx.draw_networkx (t.tree)
    plt.savefig(path+name+".pdf")


path = "saved_trees/"
number_of_desired_trees = 1

for input_count in range(0,number_of_desired_trees):
    n = random.randint(MIN_NODE_NUMBER, MAX_NODE_NUMBER)
    t = Tree(n)
    
    saves_a_tree(path, t, input_count)