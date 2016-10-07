# Assignment 1: Collaboration Groups
# Authors: Michelle Gybels & Anaïs Ools

import itertools
import datetime

threshold = 2
file = open("../Input/authorsperpublication.txt", "r")

def aPriori():
    print("------------- STEP 1 ------------- ", end="")
    print(datetime.datetime.now().time().strftime('%H:%M:%S'))
    list = applyThreshold(firstStep())

    size = len(list)
    print(size)
    if size < 20:
        printList(list)

    i = 2
    while list:
        print("------------- STEP %d ------------- " % i, end="")
        print(datetime.datetime.now().time().strftime('%H:%M:%S'))
        list = step(i, list)
        list = applyThreshold(list)

        size = len(list)
        print(size)
        if size < 20:
            printList(list)
        i += 1

    print("-------------- ENDED -------------- ", end="")
    print(datetime.datetime.now().time().strftime('%H:%M:%S'))

def printList(list):
    if not list:
        print("List is empty")
        return
    for authors in list:
        print("%s -> %s" % (authors, list[authors]))

def firstStep():
    candidates = {}
    for line in file:
        for author in line.replace("[", "").replace("]", "").strip().split(","):
            key = frozenset({author})
            if key in candidates:
                candidates[key] += 1
            else:
                candidates[key] = 1
    return candidates

def applyThreshold(candidates):
    list = {}
    for authors in candidates:
        if(candidates[authors] >= threshold):
            list[authors] = candidates[authors]
    return list

def step(k, list):
    # candidates = createNewCandidates(list, k)
    # print("\t Candidates created.")
    candidates = {}
    file.seek(0, 0)
    for line in file:
        authors = line.replace("[", "").replace("]", "").strip().split(",")
        authorCombinations = itertools.combinations(authors, k)
        for combination in authorCombinations:
            for author in list:
                if author.issubset(frozenset(combination)):
                    key = frozenset(combination)
                    if key in candidates:
                        candidates[key] += 1
                    else:
                        candidates[key] = 1
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
file.close()