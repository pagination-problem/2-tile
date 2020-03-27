"""
    This class will be based on networkx Graph class.
    We are going to add a few methods needed for our experimentations.
"""

import networkx as nx
import random
import sys
import string
import cplex #https://anaconda.org/IBMDecisionOptimization/cplex
from pathlib import Path

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
            prufer_sequence = [random.randint(0,n-1) for i in range(n-2)]
        else:
            sys.exit("Incorrect input in the creation of a Tree.")

        T = nx.from_prufer_sequence(prufer_sequence)
        d = dict(enumerate(string.ascii_lowercase, 0))
        self.tree = nx.relabel_nodes(T, d)

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

    def to_cplex_input(self):
        # https://gist.github.com/WPettersson/287de1e739d4d7869d555fd28ac587cf
        # https://medium.com/opex-analytics/optimization-modeling-in-python-pulp-gurobi-and-cplex-83a62129807a

        # https://www.ibm.com/support/knowledgecenter/SSSA5P_12.7.0/ilog.odms.cplex.help/refpythoncplex/html/cplex.Cplex-class.html?pos=2
        # https://www.ibm.com/support/knowledgecenter/SSSA5P_12.7.0/ilog.odms.cplex.help/refpythoncplex/html/cplex._internal._subinterfaces.VariablesInterface-class.html
        
        problem = cplex.Cplex()
        problem.objective.set_sense(problem.objective.sense.minimize)

        var_names = list()
        constraints = list()

        # For each node u in the tree, we create two variables: x_1u et x_2u
        for u in self.tree.nodes():
            var_names.append("x_1"+str(u))
            var_names.append("x_2"+str(u))

        problem.variables.add(names = var_names)

        # Variables needed to describe the constraints:
        constraints = list()
        constraint_senses = list()
        rhs = list()

        # The first constraint says that Cmax = number of symbols on P2
        vars_on_p1 = list()
        vars_on_p2 = list()
        coefficients_for_p1 = list() #this list will be used to create the first constraint of the lp model
        coefficients_for_p2 = list() #this list will be used to create the first constraint of the lp model

        for u in self.tree.nodes():
            vars_on_p1.append("x_1"+str(u))
            vars_on_p2.append("x_2"+str(u))
            coefficients_for_p1.append(1.0)
            coefficients_for_p2.append(-1.0)

        lin_expr = [ vars_on_p1 + vars_on_p2, coefficients_for_p1 + coefficients_for_p2]
        constraints.append(lin_expr)
        constraint_senses.append("L")
        rhs.append(0)
        
        # Second constraint (which is actually a group of constraint):
        # A tile is fully assigned to one of the pages.
        for edge in self.tree.edges:
            u = edge[0]
            v = edge[1]
            
            constraints.append( [ ["x_1"+str(u), "x_2"+str(v)], [1.0, 1.0] ] )
            constraint_senses.append("L")
            rhs.append(1.0)

            constraints.append( [ ["x_1"+str(v), "x_2"+str(u)], [1.0, 1.0] ] )
            constraint_senses.append("L")
            rhs.append(1.0)

        # Third constraint (which is actually a group of constraint):
        # A vertex cannot belong to V1 and V2: it belongs either to V1 (x_1u = 1), to V2 (x_2u = 1) or
        # to C (x_1u = 0 AND x_2u = 0).
        for u in self.tree.nodes():
            constraints.append( [ ["x_1"+str(u), "x_2"+str(u)], [1.0, 1.0] ] )
            constraint_senses.append("L")
            rhs.append(1.0)
        
        # We build the set of contraints of our model
        problem.linear_constraints.add(lin_expr = constraints,
                                    senses = constraint_senses,
                                    rhs = rhs,)
        
        return problem

