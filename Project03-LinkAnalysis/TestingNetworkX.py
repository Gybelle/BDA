import networkx as nx
import matplotlib.pyplot as plt
import itertools



testing = frozenset({1,2,3})
combitesting = itertools.combinations(testing, 2)
for test in combitesting:
    print(test)

G = nx.Graph()
G.add_node("Michelle")
G.add_edge("Anaïs", "Lenny")
G.add_edge("Anaïs", "Lenny")
G.add_edge("Anaïs", "Audric")
print(list(G.nodes()))

G["Anaïs"]["Lenny"]['weight'] = 1

G.add_edge("Anaïs", "Lenny")
G["Anaïs"]["Lenny"]['weight'] += 1

print(G.get_edge_data("Anaïs", "Lenny"))


pos = nx.spring_layout(G)
nx.draw_networkx_labels(G, pos)
nx.draw(G, pos)
plt.show()




