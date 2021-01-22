import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter

DEBUG = False

def heuristic_one_and_two (g, H2):
    g_save = g.copy(False)
    M1 = set()
    M2 = set()
    C  = set ()

    while (len(g_save.nodes)):
        if (DEBUG):
            print("M1 = ", M1)
            print("M2 = ", M2)
            print("C = ", C)

        sorted_nodes = [node for (node, val) in sorted(g_save.degree(), key=lambda pair: pair[1], reverse=H2)] #Graph.degree = list of (degree, node number)
        v = sorted_nodes[0]
        if (DEBUG):
            print("Computing node ", v)

        if (len(M1) <= len(M2)):
            M1.add(v)
        else:
            M2.add(v)

        neighbourhood = set(g_save.neighbors(v))
        if (DEBUG):
            print("neighbourhood of", v, " : ", neighbourhood)
        C = C.union(neighbourhood)
        g_save.remove_nodes_from(neighbourhood)

        g_save.remove_node(v)

    return (M1, M2, C)

################################################################################################################
# I did not write the function colorGraph, I took it from https://www.techiedelight.com/greedy-coloring-graph/ #
# and I adapted it to fit my data structure.                                                                   #
################################################################################################################
def colour_graph(g):
 
    # stores color assigned to each vertex
    result = {}
 
    # assign color to vertex one by one
    for u in sorted(g.nodes):
 
        # set to store color of adjacent vertices of u
        # check colors of adjacent vertices of u and store in set
        assigned = set([result.get(nbr) for nbr in g[u] if nbr in result])
 
        # check for first free color
        color = 1
        for c in assigned:
            if color != c:
                break
            color = color + 1
 
        # assigns vertex u the first available color
        result[u] = color

    return result
 

def heuristic_three (g):
    g_save = g.copy(False)
    M1 = set()
    M2 = set()
    C  = set ()

    colours = colour_graph(g_save)

    counters = Counter(colours.values())
    c1 = list(counters.keys())[0]       # Most present colour in the graph
    vertices = [key for key, value in colours.items() if value == c1] # Vertices coloured by c1

    if (DEBUG):
        print("Counters : ", counters)
        print("Most present colour : ", c1)
        print("Vertices colours by c1 : ", vertices)

    split_idx = (len(vertices) +1) // 2 # Depending on the convention we want to follow, we may want to
    M1 = vertices[:split_idx]           # the formula for split_idx. If we want M2 to be the most 
    M2 = vertices[split_idx:]           # loaded machine, we should write : split_idx = len(vertices) // 2
    
    C = g.nodes - vertices

    return (M1, M2, C)

#TO DELETE WHEN CODING IS OVER
def test_remove_vertices (g):
    g_save = g.copy(False)
    g_save.remove_node(1)
    g_save.remove_node(2)
    g_save.remove_node(3)
    g_save.remove_node(4)
    g_save.remove_node(5)
    nx.draw_spring(g_save, with_labels = True)
    plt.savefig("Illustrations/my_graph_with_less_vertices.pdf")
    plt.close()

#TO DELETE WHEN CODING IS OVER
def test_add_vertices_to_set(g):
    g_save = g.copy(False)
    M1 = set()
    M1.add(g_save.nodes[1])

edges = [
    (1, 2),
    (2, 3), (2, 4), (2, 12),
    (3, 4), (3, 6), (3, 12),
    (4, 5),
    (5, 6),
    (6, 7), (6, 8),
    (7, 8), (7, 9),
    (8, 9),
    (9, 10), (9, 12),
    (10, 12),
    (11, 12)
]

g = nx.Graph()
g.add_edges_from(edges)

#test_remove_vertices (g)

#nx.draw_networkx (g)
#nx.draw_planar(g, with_labels = True)
#nx.draw_spring(g, with_labels = True)
#plt.savefig("Illustrations/my_graph_with_12_vertices.pdf")
#plt.close()

print("Results for H1 :")
(P1, P2, sep) = heuristic_one_and_two(g, False)
print("P1 = ", sorted(P1))
print("P2 = ", sorted(P2))
print("sep = ", sorted(sep))

print("\nResults for H2 :")
(P1, P2, sep) = heuristic_one_and_two(g, True)
print("P1 = ", sorted(P1))
print("P2 = ", sorted(P2))
print("sep = ", sorted(sep))

print("\nResults for H3 :")
(P1, P2, sep) = heuristic_three (g)
print("P1 = ", sorted(P1))
print("P2 = ", sorted(P2))
print("sep = ", sorted(sep))