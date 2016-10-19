# Assignment 2: Clustering
# Authors: Michelle Gybels & Anaïs Ools

from stemming.porter2 import stem
import re

file = open("../Input/titles.txt", "r")
# results = open("../Output/results.txt", "a")

index = 0
for line in file:
    if index < 20:
        line = line.strip().replace("[", "").replace("]", "")
        for word in line.split(" "):
            word = re.sub(r'\W+', '', word).lower()
            if word:
                print(stem(word), end=" ")
        print()
    index += 1


file.close()
# results.close()