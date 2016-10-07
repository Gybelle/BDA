# Assignment 1: Collaboration Groups
# Authors: Michelle Gybels & Anaïs Ools
# Process the results from "A Priori" algorithm.

results = open("../Output/results.txt", "r")
processResults = open("../Output/processResults.txt", "w")

currentThreshold = -1
currentK = -1
max = -1
listMax = []
size = -1

for line in results:
    if currentThreshold == -1:
        currentThreshold = int(line.split(":")[1])
    elif currentK == -1:
        currentK = int(line.split(":")[1])
    elif size == -1:
        size = int(line.split(":")[1])
    elif size == 0:
        if max is not -1:
            processResults.write("T:%d, K:%d, Max = %d %s\n" % (currentThreshold, currentK, max, ''.join(listMax)))
        currentThreshold = -1
        currentK = -1
        listMax = []
        size = -1
        max = -1
    else:
        line = line.strip()
        currentCount = int(line.split(":")[0].strip())
        list = line.split(":")[1].strip()
        if currentCount > max:
            max = currentCount
            listMax = [list]
        elif currentCount == max:
            listMax.append(list)
        size -= 1
if max is not -1:
    processResults.write("T:%d, K:%d, Max = %d %s\n" % (currentThreshold, currentK, max, ''.join(listMax)))
