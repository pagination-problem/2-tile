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

