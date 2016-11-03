# Assignment 3: Importance of researches
# Authors: Michelle Gybels & Anaïs Ools

import itertools
import networkx as nx
import matplotlib.pyplot as plt
import csv

bigDataset = True
labelThreshold = 10
authorMap = {}
authorGraph = nx.Graph()

if not bigDataset:
    file = open("../Input/pods.txt", "r", encoding="utf8")
    outputFile = "../Output/authorImportance.csv"
else:
    file = open("../Input/podsBIG.txt", "r", encoding="utf8")
    outputFile = "../Output/authorImportance_BIG.csv"

def printAuthorGraph():
    d = {}
    lab = {}
    for node in authorGraph.nodes():
        size = authorMap[node][0]  # set size of node
        d[node] = size
        if size > labelThreshold:
            lab[node] = node  # set label
        else:
            lab[node] = ""
    nx.draw_random(authorGraph, nodelist=d.keys(), node_size=[v * 100 for v in d.values()], labels=lab, with_labels=True, node_color='c', edge_color='#7F7F7F', font_weight='bold')
    plt.show()

def createNetwork():
    for line in file:
        paperAuthors = frozenset(line.replace("[", "").replace("]", "").strip().split(","))
        for author in paperAuthors:
            if author in authorMap:
                authorMap[author] = (authorMap[author][0] + 1, authorMap[author][1], authorMap[author][2])
            else:
                authorMap[author] = (1, 0, 0)  #Tuple: ("Publication count", "PageRank", "Authority Score"
        authorCombinations = itertools.combinations(paperAuthors, 2)
        for combination in authorCombinations:
            if(authorGraph.has_node(combination[0]) and authorGraph.has_node(combination[1]) and
                   combination[0] in authorGraph.neighbors(combination[1])):
                authorGraph.add_edge(combination[0], combination[1])
                authorGraph[combination[0]][combination[1]]["weight"] += 1
            else:
                authorGraph.add_edge(combination[0], combination[1])
                authorGraph[combination[0]][combination[1]]["weight"] = 0

def calculatePageRank():
    pRank = nx.pagerank(authorGraph)
    for author in pRank:
        authorMap[author] = (authorMap[author][0], pRank[author], authorMap[author][2])

def printResults():
    with open(outputFile, 'w', newline='') as csvfile:
        csvWriter = csv.writer(csvfile, delimiter=';', quotechar=';', quoting=csv.QUOTE_MINIMAL)
        csvWriter.writerow(['Author', 'Publication count', 'PageRank', 'Authority score'])
        for author in authorMap:
            csvWriter.writerow([author, authorMap[author][0], authorMap[author][1], authorMap[author][2]])


#testing
createNetwork()
calculatePageRank()
#printAuthorMap()
printResults()
printAuthorGraph()

