"""
    This class will be based on networkx Graph class.
    We are going to add a few methods needed for our experimentations.
"""

import networkx as nx

class Tree(nx.Graph):
    def __init__(self, prufer_sequence):
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

    def find_diameter_in(self, T, length):
        """
            Goal: this function finds one of the possible diameters in the tree T
            Inputs: the tree and the length of the diameter
            Output: a list of vertices that forms a diameter.
            
            Remarks: There can be several paths long enough to
                be diameters but this function will return only one.
        """
        print("I'm not finished!")