"""
    This class will be based on networkx Graph class.
    We are going to add a few methods needed for our experimentations.
"""

import networkx as nx
import random
import sys

class Tree(nx.Graph):
    """
        input: a integer or a sequence of integer
        output: initialization of a Tree

        Remarks: if the input is a sequence, then it means that the user directly gives the Prufer sequence
        describing a tree. However, if the input is an integer, it means the user wants to generate a
        random tree. The number of nodes inside the tree is the value of the input.

    """
    def __init__(self, my_input):
        if isinstance(my_input, list):
            prufer_sequence = my_input
        elif isinstance(my_input, int):
            n = my_input
            prufer_sequence = [random.randint(0,n) for i in range(n-2)]
        else:
            sys.exit("Incorrect input in the creation of a Tree.")

        T = nx.from_prufer_sequence(prufer_sequence)
        self.tree = T

    def degree(self, node):
        return self.tree.degree(node)

    def find_leaves(self):
        """
            This function put all the leaves (every node with a degree = 1) of the tree in a set
            Input: a tree
            Output: a set
        """
        leaves_set = set()
        [leaves_set.add(x) for x in self.tree.nodes if self.degree(x) == 1]
        return leaves_set

    def find_a_diameter(self):
        """
            Goal: this function finds one of the possible diameters in the tree T
            Input: self
            Output: a list of vertices that forms a diameter. The order will be important
            
            Remarks: There can be several paths long enough to
                be diameters but this function will return only one.
        """
        length = nx.diameter(self.tree) #length = number of edges in the diameter
        leaves_set = self.find_leaves()
        
        for leaf_1 in leaves_set :
            leaves_set_temp = set(leaves_set)
            leaves_set_temp.remove(leaf_1)
            for leaf_2 in leaves_set_temp :
                path = nx.shortest_path(self.tree, leaf_1, leaf_2)
                if len(path) == length + 1: #len(path) = number of vertices in the list 'path'
                                            #that's why we need the "+1"
                    return path

        return None #for tests

