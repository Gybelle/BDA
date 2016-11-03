# Assignment 3: Importance of researches
# Authors: Michelle Gybels & Anaïs Ools
import networkx as nx
import matplotlib.pyplot as plt

def printAuthorGraph(G):
    pos = nx.spring_layout(G)
    nx.draw_networkx_labels(G, pos)
    nx.draw(G, pos)
    plt.show()

