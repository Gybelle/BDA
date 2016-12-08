# Assignment 4: Graph Mining
# Authors: Michelle Gybels & Anaïs Ools

import itertools
import networkx as nx
import matplotlib.pyplot as plt
import csv
import community
import igraph

bigDataset = True
authorGraph = nx.Graph()
otherGraph = igraph.Graph(directed=False)
startYear = 2006
endYear = 2016

if not bigDataset:
    file = open("../Input/pods.txt", "r", encoding="utf8")
    # outputFile = "../Output/authorImportance.csv"
else:
    file = open("../Input/podsBIG.txt", "r", encoding="utf8")
    # outputFile = "../Output/authorImportance_BIG.csv"


def createGraph():
    """
    Generate a network of the authors. A hashmap will also be created containing the publication count per author.
    """
    for line in file:
        year = int(line[:line.find(" ")])
        if year >= startYear and year <= endYear:
            authors = line[line.find(" ")+1:]
            paperAuthors = frozenset(authors.replace("[", "").replace("]", "").strip().split(","))
            # print(year, end=" ")
            # print(paperAuthors)
            authorCombinations = itertools.combinations(paperAuthors, 2)
            for combination in authorCombinations:
                if(authorGraph.has_node(combination[0]) and authorGraph.has_node(combination[1]) and
                       combination[0] in authorGraph.neighbors(combination[1])):
                    authorGraph.add_edge(combination[0], combination[1])
                    authorGraph[combination[0]][combination[1]]["weight"] += 1
                else:
                    authorGraph.add_edge(combination[0], combination[1])
                    authorGraph[combination[0]][combination[1]]["weight"] = 1

                addNode(combination[0])
                addNode(combination[1])
                otherGraph.add_edge(combination[0], combination[1])


def addNode(node):
    """
    Add a node to the global graph if it does not exist yet.
    :param node: the node to add
    """
    # Graph has no nodes
    if len(otherGraph.vs) == 0:
        otherGraph.add_vertex(node)
        return
    # Graph does not have node
    if node not in otherGraph.vs["name"]:
        otherGraph.add_vertex(node)


def flattenGraph(graph):
    """
    Merges multiple edges into one edge with the count as weight.
    """
    graph.es["width"] = 1
    graph.simplify(combine_edges={"width": "sum"})
    graph.simplify()


def fix_dendrogram(graph, cl):
    """
    Takes a graph and an incomplete dendrogram and completes the dendrogram by merging the remaining nodes in arbitrary
    order.
    Source: https://lists.nongnu.org/archive/html/igraph-help/2014-02/msg00067.html
    :param graph: original graph
    :param cl: dendrogram
    """
    already_merged = set()
    for merge in cl.merges:
        already_merged.update(merge)

    num_dendrogram_nodes = graph.vcount() + len(cl.merges)
    not_merged_yet = sorted(set(range(num_dendrogram_nodes)) - already_merged)
    if len(not_merged_yet) < 2:
        return

    v1, v2 = not_merged_yet[:2]
    cl._merges.append((v1, v2))
    del not_merged_yet[:2]

    missing_nodes = range(num_dendrogram_nodes,
            num_dendrogram_nodes + len(not_merged_yet))
    cl._merges.extend(zip(not_merged_yet, missing_nodes))
    cl._nmerges = graph.vcount()-1


def calculateBetweenness():

    result = nx.betweenness_centrality(authorGraph)
    for item in result:
        print(item, end=" --> ")
        print(result[item])
    # draw with highlighted belangrijke nodes
    # http://glowingpython.blogspot.be/2013/02/betweenness-centrality.html


def calculateCommunities():
    # calculate dendrogram
    dendrogram = otherGraph.community_edge_betweenness()
    fix_dendrogram(otherGraph, dendrogram)
    print(dendrogram)

    # convert it into a flat clustering
    clusters = dendrogram.as_clustering()
    print(clusters)

    # print memberships
    # membership = clusters.membership
    # for name, membership in zip(g.vs["name"], membership):
    #     print([name, membership])


#####################################
#       Run the program:            #
#       Execute functions           #
#####################################
createGraph()

# calculateBetweenness()

flattenGraph(otherGraph)

calculateCommunities()