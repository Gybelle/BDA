# Assignment 1: Collaboration Groups
# Authors: Michelle Gybels & Anaïs Ools

index = 0
buckets = {}
threshold = 10

with open("../Input/authorsperpublication.txt", "r") as file:
    for line in file:
        for author in line.replace("[","").replace("]","").strip().split(","):
            key = frozenset({author})
            if key in buckets:
                buckets[key] += 1
            else:
                buckets[key] = 1


for author in buckets:
    if(buckets[author] >= threshold):
        print("%s -> %s" % (author, buckets[author]))

file.close()