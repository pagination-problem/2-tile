import networkx as nx

n = 40
#Rappel: densite = m / [n(n - 1)/2]
m = 6
g1 = nx.gnm_random_graph(n, m)

if nx.is_connected(g1):
    print("This messages should not be printed.")
else:
    print("g1 is not connected.")

m = 350
g2 = nx.gnm_random_graph(n, m)
cpt=0
while (not nx.is_connected(g2)):
    cpt=cpt+1
    g2 = nx.gnm_random_graph(n, m)

print(f"g2 is a connected graph and it took {cpt} iterations to find a connected graph.")
print(f"The density of g2 is {m/(n*(n-1)/2)}.")