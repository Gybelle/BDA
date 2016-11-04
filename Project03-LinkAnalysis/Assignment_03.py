# Assignment 3: Importance of researches
# Authors: Michelle Gybels & Anaïs Ools

import itertools
import networkx as nx
import matplotlib.pyplot as plt
import csv

bigDataset = True
labelThreshold = 0.08
dataElement = 2  # 0 = publ. count, 1 = PageRank, 2 = authority
authorMap = {}
authorGraph = nx.Graph()
highlightNames = {"Frank Neven", "Jan Van den Bussche", "Marc Gyssens", "Stijn Vansummeren", "Bas Ketsman", "Tom J. Ameloot"}

if not bigDataset:
    file = open("../Input/pods.txt", "r", encoding="utf8")
    outputFile = "../Output/authorImportance.csv"
else:
    file = open("../Input/podsBIG.txt", "r", encoding="utf8")
    outputFile = "../Output/authorImportance_BIG.csv"

def printAuthorGraph():
    d = {}
    lab = {}
    labCol = {}
    calculatedThreshold = calculateThreshold()
    threshold = calculatedThreshold[0]
    factor = calculatedThreshold[1]
    for node in authorGraph.nodes():
        size = authorMap[node][dataElement] * factor  # set size of node
        d[node] = size
        if size > threshold:
            if node in highlightNames:
                labCol[node] = node  # set label
            else:
                lab[node] = node
        else:
            if node in highlightNames:
                labCol[node] = ""
            else:
                lab[node] = ""
    print(labCol)

    pos = nx.random_layout(authorGraph)
    nx.draw(authorGraph, pos=pos, nodelist=d.keys(), node_size=[v * 100 for v in d.values()], labels=lab, with_labels=True, node_color='c', edge_color='#9F9F9F', font_weight='bold')
    nx.draw_networkx_labels(authorGraph, pos=pos, labels=labCol, font_weight='bold', font_color='#E12707')
    plt.show()

def calculateThreshold():
    weights = []
    if dataElement == 0:
        factor = 1
    elif dataElement == 1:
        factor = 1000
    elif dataElement == 2:
        factor = 1000
    for node in authorGraph.nodes():
        weights.append(float(authorMap[node][dataElement]))
    weights.sort()
    labThreshold = int(round(len(weights)*(1.0-labelThreshold), 0))
    while labThreshold > 0 and labThreshold < len(weights)-1 and weights[labThreshold-1] == weights[labThreshold]:
        labThreshold += 1
    return weights[labThreshold] * factor, factor

def createNetwork():
    """
    Generate a network of the authors. A hashmap will also be created containing the publication count per author.
    """
    for line in file:
        paperAuthors = frozenset(line.replace("[", "").replace("]", "").strip().split(","))
        for author in paperAuthors:
            if author in authorMap:
                authorMap[author] = (authorMap[author][0] + 1, authorMap[author][1], authorMap[author][2])
            else:
                authorMap[author] = (1, 0, 0)  #Tuple: ("Publication count", "PageRank", "Authority Score")
        authorCombinations = itertools.combinations(paperAuthors, 2)
        for combination in authorCombinations:
            if(authorGraph.has_node(combination[0]) and authorGraph.has_node(combination[1]) and
                   combination[0] in authorGraph.neighbors(combination[1])):
                authorGraph.add_edge(combination[0], combination[1])
                authorGraph[combination[0]][combination[1]]["weight"] += 1
            else:
                authorGraph.add_edge(combination[0], combination[1])
                authorGraph[combination[0]][combination[1]]["weight"] = 1

def perfomLinkAnalysis():
    """
    For each author in the network, the 'PageRank' and 'Authority Score' will be calculated. The hashmap already
    containing all the authors and 'Publication Count' will also be updated with these values.
    """
    pRank = nx.pagerank(authorGraph)
    hubs, authorities = nx.hits(authorGraph)
    for author in authorMap:
        if (author in pRank):
            authorMap[author] = (authorMap[author][0], pRank[author], authorMap[author][2])
        if (author in authorities):
            authorMap[author] = (authorMap[author][0], authorMap[author][1], authorities[author])

def printResults():
    """
    Save the results in a CSV file. The file contains the following columns: Author, Publication count, PageRank and
    Authority Score.
    """
    with open(outputFile, 'w', newline='') as csvfile:
        csvWriter = csv.writer(csvfile, delimiter=';', quotechar=';', quoting=csv.QUOTE_MINIMAL)
        csvWriter.writerow(['Author', 'Publication count', 'PageRank', 'Authority score'])
        for author in authorMap:
            csvWriter.writerow([author, authorMap[author][0], authorMap[author][1], authorMap[author][2]])

createNetwork()
perfomLinkAnalysis()
printResults()
printAuthorGraph()

