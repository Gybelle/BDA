# Assignment 2: Clustering
# Authors: Michelle Gybels & Anaïs Ools

from stemming.porter2 import stem
import re

bigDataset = False
if not bigDataset:
    file = open("../Input/titles.txt", "r", encoding="utf8")
    # results = open("../Output/titlesResult.txt", "a", encoding="utf8")
else:
    file = open("../Input/titlesBIG.txt", "r", encoding="utf8")
    # results = open("../Output/titlesResultBIG.txt", "a", encoding="utf8")

def stemLines(lines):
    result = []
    for line in lines:
            line = line.strip().replace("[", "").replace("]", "")
            stemmedLine = ""
            for word in line.split(" "):
                word = re.sub(r'\W+', '', word).lower() # to alphanumeric lowercase
                stemmedLine += stem(word)
                stemmedLine += " "
            result.append(stemmedLine.strip())
    return result

print(stemLines(file))
file.close()
# results.close()