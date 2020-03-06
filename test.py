import networkx as nx

sequence = [4, 4, 4, 5]
tree = nx.from_prufer_sequence(sequence)
print (tree)
