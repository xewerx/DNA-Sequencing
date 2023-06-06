import networkx as nx
import matplotlib.pyplot as plt

# Tworzenie grafu
G = nx.Graph()
G.add_edge(1, 2, weight=3)
G.add_edge(2, 3, weight=4)
G.add_edge(3, 4, weight=2)
G.add_edge(4, 1, weight=1)

# Rysowanie grafu
pos = nx.circular_layout(G)
nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray')

# Rysowanie etykiet wag na krawędziach
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

# Wyświetlanie grafu
plt.show()
