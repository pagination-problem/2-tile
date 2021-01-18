import json
import random
import networkx as nx
from networkx.algorithms import bipartite
from networkx.readwrite import json_graph

from goodies import data_to_json

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

    with open('test_dumps/random_graph.json', 'w', encoding ='utf8') as json_file: 
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


if __name__ == "__main__":
    #complete_bipartite_graph_generation_and_dump_in_json()
    #stat_connectivity()
    #test_read_graph_from_json()
    random_graph_generation_and_dump_in_json()
    random_bipartite_graph_generation_and_dump_in_json()
    complete_bipartite_graph_generation_and_dump_in_json()