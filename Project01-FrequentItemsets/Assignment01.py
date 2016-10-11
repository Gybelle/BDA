# Assignment 1: Collaboration Groups
# Authors: Michelle Gybels & Anaïs Ools

import itertools
import datetime

threshold = 20
file = open("../Input/authorsperpublication.txt", "r")
results = open("../Output/results.txt", "a")


def aPriori():
    print("------------- STEP 1 ------------- ", end="")
    print(datetime.datetime.now().time().strftime('%H:%M:%S'))
    list = applyThreshold(firstStep())

    size = len(list)
    print(size)
    printList(list, 1)

    i = 2
    while list:
        print("------------- STEP %d ------------- " % i, end="")
        print(datetime.datetime.now().time().strftime('%H:%M:%S'))
        list = step(i, list)
        list = applyThreshold(list)

        size = len(list)
        print(size)
        printList(list, i)
        i += 1

    print("------------- ENDED -------------- ", end="")
    print(datetime.datetime.now().time().strftime('%H:%M:%S'))

def printList(list, k):
    results.write("Threshold: %d\n" % threshold)
    results.write("Groupsize: %d\n" % k)
    results.write("Results: %d\n" % len(list))
    if not list:
        results.write("\n")
        return
    for authors in list:
        results.write("\t%s : %s\n" % (list[authors], printFrozenset(authors)))
    results.write("\n")

def printFrozenset(set):
    result = "{"
    size = len(set)
    for item in set:
        result += "'" + item + "'"
        size -= 1
        if size != 0:
            result += ", "
    result += "}"
    return result

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
    candidates = {}
    file.seek(0, 0)
    for line in file:
        authors = line.replace("[", "").replace("]", "").strip().split(",")
        frequentAuthors = []
        for author in authors:
            found = False
            for listItem in list:
                if not found and author in listItem and author not in frequentAuthors:
                    frequentAuthors.append(author)
                    found = True
        authorCombinations = itertools.combinations(frequentAuthors, k)
        for combination in authorCombinations:
            for authorSet in list:
                if authorSet.issubset(frozenset(combination)):
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
results.close()