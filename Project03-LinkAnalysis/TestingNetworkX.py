import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
G.add_node("Michelle")
G.add_edge("Anaïs", "Lenny")
G.add_edge("Anaïs", "Audric")
print(list(G.nodes()))

pos = nx.spring_layout(G)
nx.draw_networkx_labels(G, pos)
nx.draw(G, pos)
plt.show()
