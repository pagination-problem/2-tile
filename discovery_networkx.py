import json
import random
import networkx as nx
from networkx.algorithms import bipartite
from networkx.readwrite import json_graph
import matplotlib.pyplot as plt

from goodies import data_to_json

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


def test_add_vertices_to_set(g):
    g_save = g.copy(False)
    M1 = set()
    M1.add(g_save.nodes[1])

def random_graph_generation_and_dump_in_json():
    nb_sommets = 15
    d = 0.5
    m = (d * nb_sommets * (nb_sommets - 1)) / 2
    seed = 29
    graph_type = "normal"

    g = nx.gnm_random_graph(nb_sommets, m, seed)

    graph_in_data = dict()
    graph_in_data = {
        "seed" : seed,
        "graph_type" : graph_type,
        "total_node_count" : len(g.nodes),
        "edge_count" : len(list(g.edges)),
        "nodes" : sorted(g.nodes),
        "edges" : list(g.edges)
    }

    name = "test_dumps/random_graph_"+str(nb_sommets)+"_vertices.json"

    with open(name, 'w', encoding ='utf8') as json_file: 
        json_file.write(data_to_json(graph_in_data))

def random_bipartite_graph_generation():
    nb_sommets = 10
    seed = 29

    n1 = random.randint(1, nb_sommets-1)
    n2 = nb_sommets - n1
    p = 0.85

    print("n1 = ", n1)
    print("n2 = ", n2)

    g = bipartite.random_graph(n1, n2, p, seed, directed=False)
    #V1, V2 = nx.bipartite.sets(g)

    #print("V1 : ", V1)
    #print("V2 : ", V2)

    if (nx.is_connected(g)):
        print("The graph is connected")
    else:
        print("The graph is not connected")

def random_bipartite_graph_generation_and_dump_in_json():
    nb_sommets = 10
    seed = 29

    n1 = random.randint(1, nb_sommets-1)
    n2 = nb_sommets - n1
    p = 0.85

    print("n1 = ", n1)
    print("n2 = ", n2)

    g = bipartite.random_graph(n1, n2, p, seed, directed=False)
    V1, V2 = nx.bipartite.sets(g)

    graph_for_json = dict()
    graph_for_json = {
        "seed" : seed,
        "graph_type" : "bipartite",
        "total_node_count" : len(g.nodes),
        "V1_node_count" : len(V1),
        "V2_node_count" : len(V2),
        "edge_count" : len(list(g.edges)),
        "nodes" : sorted(g.nodes),
        "edges" : list(g.edges)
    }

    with open('test_dumps/random_bipartite_1.json', 'w', encoding ='utf8') as json_file: 
        json_file.write(data_to_json(graph_for_json))

def test_connectivity():
    nb_sommets = 15
    seed = 29

    n1 = random.randint(1, nb_sommets-1)
    n2 = nb_sommets - n1
    p = 0.5

    g = bipartite.random_graph(n1, n2, p, seed, directed=False)
    return nx.is_connected(g)

def stat_connectivity():
    false_count = 0
    true_count = 0
    for i in range(1000):
        if test_connectivity():
            true_count = true_count + 1
        else:
            false_count = false_count + 1
    
    print("There are ", true_count ,"connected graphs => ", 100 * true_count/1000, "%.")
    print("There are ", false_count ,"not connected graphs => ", 100 * false_count/1000, "%.")

def complete_bipartite_graph_generation_and_dump_in_json():
    nb_sommets = 15
    seed = 29

    n1 = random.randint(1, nb_sommets-1)
    n2 = nb_sommets - n1
    p = 0.5

    g = bipartite.complete_bipartite_graph(n1, n2)
    V1, V2 = bipartite.sets(g)
    graph_for_json = dict()
    graph_for_json = {
        "seed" : seed,
        "graph_type" : "bipartite",
        "total_node_count" : len(g.nodes),
        "V1_node_count" : len(V1),
        "V2_node_count" : len(V2),
        "edge_count" : len(list(g.edges)),
        "nodes" : sorted(g.nodes),
        "edges" : list(g.edges)
    }

    with open('test_dumps/complete_bipartite_1.json', 'w', encoding ='utf8') as json_file: 
        json.dump(graph_for_json, json_file, indent=4) # Ugly indents

    with open('test_dumps/complete_bipartite_2.json', 'w', encoding ='utf8') as json_file: 
        json_file.write(data_to_json(graph_for_json)) # Nice indents

def test_read_arbitrary_graph_from_json():
    with open('test_dumps/random_graph_5_vertices.json') as json_file:
        print(json_file)
        data = json.load(json_file)

    #nodes = data[nodes]
    print("nodes: ", data["nodes"])
    print("edges: ", data["edges"])
    g = nx.Graph()
    g.add_nodes_from(data["nodes"])
    g.add_edges_from(data["edges"])

    nx.draw_networkx (g)
    plt.savefig("Illustrations/graph_that_was_loaded.pdf")
    plt.close()

 
if __name__ == "__main__":
    #complete_bipartite_graph_generation_and_dump_in_json()
    #stat_connectivity()
    #test_read_graph_from_json()
    # random_graph_generation_and_dump_in_json()
    # random_bipartite_graph_generation_and_dump_in_json()
    # complete_bipartite_graph_generation_and_dump_in_json()
    test_read_classic_graph_from_json()
    