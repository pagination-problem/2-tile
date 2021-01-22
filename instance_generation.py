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
#        densites = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
# 
# 
#------------------------------------------------------

import networkx as nx
import json
from networkx.algorithms import bipartite
import random

from goodies import data_to_json

def tree_generation(tailles, nb_instances, chemin_pour_stockage):
    for nb_sommets in tailles:
            for i in range (1, nb_instances):
                g = nx.random_tree(nb_sommets, seed)
                graph_for_json = dict()
                graph_for_json = {
                    "seed" : seed,
                    "graph_type" : graph_type,
                    "total_node_count" : len(g.nodes),
                    "edge_count" : len(list(g.edges)),
                    "nodes" : sorted(g.nodes),
                    "edges" : list(g.edges)
                }

                name = chemin_pour_stockage + graph_type + "__n=" + str(nb_sommets) + "__" + '{:03}'.format(i) + ".json"
                with open(name, 'w', encoding ='utf8') as json_file: 
                    json_file.write(data_to_json(graph_for_json))

def complete_generation(tailles, nb_instances, chemin_pour_stockage):
    for nb_sommets in tailles:
            for i in range (1, nb_instances):
                g = nx.complete_graph(nb_sommets)
                graph_for_json = dict()
                graph_for_json = {
                    "seed" : seed,
                    "graph_type" : graph_type,
                    "total_node_count" : len(g.nodes),
                    "edge_count" : len(list(g.edges)),
                    "nodes" : sorted(g.nodes),
                    "edges" : list(g.edges)
                }

                name = chemin_pour_stockage + graph_type + "__n=" + str(nb_sommets) + "__" + '{:03}'.format(i) + ".json"
                with open(name, 'w', encoding ='utf8') as json_file: 
                    json_file.write(data_to_json(graph_for_json))

def bipartite_generation(tailles, nb_instances, chemin_pour_stockage):
    #We need to create a dict to count the number of bipartite graphs for each density
    print("!!! WORK IN PROGRESS !!!")

    for nb_sommets in tailles:
        for i in range (1, nb_instances):
            n1 = random.randint(1, nb_sommets-1)
            n2 = nb_sommets - n1
            p = 0.5 ################################################## WE HAVE TO DEFINE THIS VALUE
            g = bipartite.random_graph(n1, n2, p, seed, directed=False)

            if (nx.is_connected(g) == False): #the bipartite graph is not connected, we will have to add edges
                print("YOU STILL HAVE WORK TO DO")

            V1, V2 = bipartite.sets(g)
            graph_for_json = dict()
            graph_for_json = {
                "seed" : seed,
                "graph_type" : graph_type,
                "total_node_count" : len(g.nodes),
                "V1_node_count" : len(V1),
                "V2_node_count" : len(V2),
                "edge_count" : len(list(g.edges)),
                "nodes" : sorted(g.nodes),
                "edges" : list(g.edges)
            }
            
            #Computes the density
            d = 0

            #arrondi de la densité

            #Update the a counter linked to the density

            name = chemin_pour_stockage + graph_type + "__n=" + str(nb_sommets) + "__d=" + str(d) + "__" + '{:03}'.format(i) + ".json"
            with open(name, 'w', encoding ='utf8') as json_file: 
                json_file.write(data_to_json(graph_for_json))

def arbitrary_generation(tailles, densites, nb_instances, chemin_pour_stockage): #arbitrary ?
    graph_type = "classic"
    for nb_sommets in tailles:
            for d in densites:
                m = (d * nb_sommets * (nb_sommets - 1)) / 2
                for i in range (1, nb_instances):
                    g = nx.gnm_random_graph(nb_sommets, m, seed=None)
                    
                    graph_for_json = dict()
                    graph_for_json = {
                        "seed" : seed,
                        "graph_type" : graph_type,
                        "total_node_count" : len(g.nodes),
                        "edge_count" : len(list(g.edges)),
                        "nodes" : sorted(g.nodes),
                        "edges" : list(g.edges)
                    }
                    name = chemin_pour_stockage + graph_type + "__n=" + str(nb_sommets) + "__d=" + str(d) + "__" + '{:03}'.format(i) + ".json"
                    with open(name, 'w', encoding ='utf8') as json_file: 
                        json_file.write(data_to_json(graph_for_json))

if __name__ == "__main__":
    ########################################################################################################
    ############################################# Parameters ###############################################
    ########################################################################################################

    graph_type = "arbitrary" #Can be tree, planar, bipartite or arbitrary (= a random graph)
    nb_instances = 10
    tailles = [25, 50, 75, 100, 200, 500, 1000] #nombre de sommets
    densites = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

    ########################################################################################################
    ############################################# Generation ###############################################
    ########################################################################################################


    ################################################## 
    ##I still have to handle the name of the inputs ##
    ################################################## 

    ################################################################## 
    ## When we precise the path, we have to end it with a final '/' ##
    ##################################################################

    if (graph_type == "tree"):
        tree_generation(tailles, nb_instances, "instances/tree/")

    elif (graph_type == "complete"):
        complete_generation(tailles, nb_instances, "instances/complete/")
                
    elif (graph_type == "bipartite"):
        bipartite_generation(tailles, nb_instances, "instances/bipartite/")

    elif (graph_type == "planar"):
        print("CASE: TO DO")

    else:
        arbitrary_generation(tailles, densites, nb_instances, "instances/arbitrary/")

