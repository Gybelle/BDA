# Assignment 3: Importance of researches
# Authors: Michelle Gybels & Anaïs Ools

import itertools
import networkx as nx
import matplotlib.pyplot as plt

bigDataset = True
authorMap = {}
authorGraph = nx.Graph()

if not bigDataset:
    file = open("../Input/pods.txt", "r", encoding="utf8")
    results = open("../Output/authorImportance.txt", "w", encoding="utf8")
else:
    file = open("../Input/podsBIG.txt", "r", encoding="utf8")
    results = open("../Output/authorImportance_BIG.txt", "w", encoding="utf8")

def printAuthorGraph():
    pos = nx.spring_layout(authorGraph)
    nx.draw_networkx_labels(authorGraph, pos)
    nx.draw(authorGraph, pos)
    plt.show()

def createNetwork():
    for line in file:
        paperAuthors = frozenset(line.replace("[", "").replace("]", "").strip().split(","))
        for author in paperAuthors:
            #results.write("%s\n" % author)
            if author in authorMap:
                authorMap[author] += 1
            else:
                authorMap[author] = 1

        authorCombinations = itertools.combinations(paperAuthors, 2)
        for combination in authorCombinations:
            authorGraph.add_edge(combination[0], combination[1])

def printAuthorMap():
    for author in authorMap:
        results.write("%s: %d\n" % (author, authorMap[author]))


#testing
createNetwork()
printAuthorGraph()
printAuthorMap()

