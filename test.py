import networkx as nx

sequence = [3, 3, 3, 4]
tree = nx.from_prufer_sequence(sequence)
nx.draw_networkx (tree)


    # >>> import networkx as nx
    # >>> G = nx.Graph()
    # >>> G.add_edge('A', 'B', weight=4)
    # >>> G.add_edge('B', 'D', weight=2)
    # >>> G.add_edge('A', 'C', weight=3)
    # >>> G.add_edge('C', 'D', weight=4)
    # >>> nx.shortest_path(G, 'A', 'D', weight='weight')
    # ['A', 'B', 'D']
    