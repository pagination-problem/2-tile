from tree import Tree
import cplex
import math
import networkx as nx
import matplotlib.pyplot as plt
import random

"""
    This script generates random trees
    (with a number of nodes between a lower and an upper born),
    finds the optimal solution using CPLEX
    and checks two conditions: one about the number of
    duplicated symbols in the optimal solution and
    one about the optimal value.

    If a tree doesn't verify one of the condition,
    it is stored in a specific folder: saved_trees
"""

MIN_NODE_NUMBER = 5
MAX_NODE_NUMBER = 26

while(True):
    n = random.randint(MIN_NODE_NUMBER, MAX_NODE_NUMBER)
    t = Tree(n)
    cplex_input = t.to_cplex_input()
    cplex_input.solve()

    cpt = 0

    for u in t.tree.nodes():
        (val_1, val_2) = cplex_input.solution.get_values( ["x_1"+str(u), "x_2"+str(u)] )

        if val_1 == 0 and val_2 == 0:
            cpt = cpt + 1

    OPT = cplex_input.solution.get_objective_value() + len(t.tree)

    if cpt > 2 or OPT > math.ceil( (len(t.tree)+1) / 2 ):
        print(t.prufer_sequence)
        name = "model_" + "-".join(str(i) for i in t.prufer_sequence)
        cplex_input.write("saved_models/"+name+".lp", "lp")

        plt.figure(figsize=(5,5))
        nx.draw_networkx (t.tree)
        plt.savefig("saved_models/"+name+".pdf")
    else:
        print("nope")

