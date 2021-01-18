#------------------------------------------------------
# Une instance est un graphe.
# Il faut générer nb_instances instances (nb_instances restent à définir).
# 
# Je pense prendre cette énumération comme taille (=nb de sommets) d'instances :
#       tailles = [25, 50, 75, 100, 200, 500, 1000] (les 2 dernières seulement si les premières instances sont réalisées relativement vite)
# 
# Rappel : la densité d'un graphe G=(n,m) est exprimée ainsi : d = m / ( n(n - 1) / 2 )
# 
# Je pense étudier en priorité les densités suivantes :
#        densites = [0.1, 0.2, 0.3, 0.4, 0.5]
# 
# 
#------------------------------------------------------

import networkx as nx
import json
from networkx.algorithms import bipartite
import random

########################################################################################################
############################################# Parameters ###############################################
########################################################################################################

graph_type = "tree" #Can be tree, planar, bipartite or None. If none, then an ordinary graph in generated
seed = None
nb_instances = 100
tailles = [25, 50, 75, 100, 200, 500, 1000] #nombre de sommets
densites = [0.1, 0.2, 0.3, 0.4, 0.5]

########################################################################################################
############################################# Generation ###############################################
########################################################################################################


################################################## 
##I still have to handle the name of the inputs ##
################################################## 

if (graph_type == "tree"):
    for nb_sommets in tailles:
        m = nb_sommets - 1
        for i in range (1, nb_instances):
            g = nx.random_tree(nb_sommets, seed)
            graph_for_json = dict()
            graph_for_json = {
                "seed" : seed,
                "node_count" : len(g.nodes),
                "edge_count" : len(list(g.edges)),
                "nodes" : sorted(g.nodes),
                "edges" : list(g.edges)
            }

            with open('myfile.json', 'w', encoding ='utf8') as json_file: 
                json.dump(graph_for_json, json_file, indent=4)
elif (graph_type == "bipartite"):
    print("bipartite")
    N1 = random.randint(1, nb_sommets-1)
    N2 = nb_sommets - N1
    p = 0.5 ################################################## WE HAVE TO DEFINE THIS VALUE

    for nb_sommets in tailles:
        for i in range (1, nb_instances):
            g = bipartite.random_graph(N1, N2, p, seed, directed=False)
            graph_for_json = dict()
            graph_for_json = {
                "seed" : seed,
                "graph_type" : graph_type,
                "node_count" : len(g.nodes), ################################################## A MODIFIER
                "edge_count" : len(list(g.edges)),
                "nodes" : sorted(g.nodes),
                "edges" : list(g.edges)
            }

            with open('myfile.json', 'w', encoding ='utf8') as json_file: 
                json.dump(graph_for_json, json_file, indent=4)
else:
    for nb_sommets in tailles:
        for d in densites:
            m = (d * nb_sommets * (nb_sommets - 1)) / 2
            for i in range (1, nb_instances):
                if (graph_type == "planar"):
                    print("CASE: TO DO")
                else:
                    g = nx.gnm_random_graph(nb_sommets, m, seed=None)
                graph_for_json = dict()
                graph_for_json = {
                    "seed" : seed,
                    "node_count" : len(g.nodes),
                    "edge_count" : len(list(g.edges)),
                    "nodes" : sorted(g.nodes),
                    "edges" : list(g.edges)
                }

                with open('myfile.json', 'w', encoding ='utf8') as json_file: 
                    json.dump(graph_for_json, json_file, indent=4)

