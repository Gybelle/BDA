# Assignment 1: Collaboration Groups
# Authors: Michelle Gybels & Anaïs Ools

import itertools

threshold = 25

def aPriori():
    list = applyThreshold(firstStep())

    i = 2
    while list:
        list = applyThreshold(step(i, list))
        i += 1

def firstStep():
    candidates = {}
    with open("../Input/authorsperpublication.txt", "r") as file:
        for line in file:
            for author in line.replace("[", "").replace("]", "").strip().split(","):
                key = frozenset({author})
                if key in candidates:
                    candidates[key] += 1
                else:
                    candidates[key] = 1
    file.close()
    return candidates

def applyThreshold(candidates):
    list = []
    for authors in candidates:
        if(candidates[authors] >= threshold):
            list.append(authors)
    return list

def step(k, list):
    print("Step %d:" % (k))
    candidates = createNewCandidates(list, k)
    print("\t Candidates created.")
    with open("../Input/authorsperpublication.txt", "r") as file:
        for line in file:
            for authors in candidates:  #change this
                allPresent = True
                for author in authors:
                    if allPresent and author not in line:
                        allPresent = False
                if allPresent:
                    candidates[authors] += 1
    file.close()
    for authors in candidates:
        if candidates[authors] != 0:
            print("%s -> %s" % (authors, candidates[authors]))
    return candidates


def createNewCandidates(list, k):
    authorCollection = []
    for authors in list:
        authorCollection.extend(authors)
    keys = itertools.combinations(authorCollection, k)
    print("\t Candidates intialised.")
    candidates = {}
    for key in keys:
        candidates[key] = 0
    return candidates


aPriori()