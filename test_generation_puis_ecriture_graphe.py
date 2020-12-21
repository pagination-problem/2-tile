
import networkx as nx
import json

nb_instances = 1
nb_sommets = 10
d = 0.3

m = (d * nb_sommets * (nb_sommets - 1)) / 2
g = nx.gnm_random_graph(nb_sommets, m)
graph_in_data = nx.readwrite.json_graph.node_link_data(g)

with open('test.json', 'w', encoding ='utf8') as json_file: 
    json.dump(graph_in_data json_file, ensure_ascii = True)