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

nb_instances = 100
tailles = [25, 50, 75, 100, 200, 500, 1000] #nombre de sommets
densites = [0.1, 0.2, 0.3, 0.4, 0.5]

for nb_sommets in tailles:
    for d in densites:
        m = (d * nb_sommets * (nb_sommets - 1)) / 2
        for i in range (1, nb_instances):
            g = nx.gnm_random_graph(nb_sommets, m)
            graph_in_data = nx.readwrite.json_graph.node_link_data(g)

            with open('myfile.json', 'w', encoding ='utf8') as json_file: 
                json.dump(d, json_file, ensure_ascii = True) 
                #json.dump(graph_in_data)
