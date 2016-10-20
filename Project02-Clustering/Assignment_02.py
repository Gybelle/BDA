# Assignment 2: Clustering
# Authors: Michelle Gybels & Anaïs Ools

from stemming.porter2 import stem
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

bigDataset = True
k = 2

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

def executeKMeans(k, titleVectors):
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(titleVectors.toarray())
    return kmeans

def printClusters(topicRange, clusterList, k):
    print("Top topics per cluster:")
    order_centroids = clusterList.cluster_centers_.argsort()[:, ::-1]
    topics = vectorizer.get_feature_names()
    for i in range(k):
        print("Cluster %d:" % (i+1))
        for j in order_centroids[i, :topicRange]:
            print(' %s' % topics[j])
        print()

def plotClusters(titleVectors, clusterList):
    # Plot: data
    pca = PCA(n_components=2).fit(titleVectors.toarray())
    data = pca.transform(titleVectors.toarray())
    plt.scatter(data[:, 0], data[:, 1], c=clusterList.labels_)

    # Plot: centers
    centers = pca.transform(clusterList.cluster_centers_)
    plt.hold(True)
    plt.scatter(centers[:, 0], centers[:, 1], marker='x', s=200, linewidths=2, c='r')
    plt.show()



stemmedTitles = stemLines(file)

# vectorize
vectorizer = TfidfVectorizer(stop_words='english')
titleVectors = vectorizer.fit_transform(stemmedTitles)

kmeans = executeKMeans(k, titleVectors)

# printClusters(topicRange, clusterList, k):
printClusters(10, kmeans, k)
plotClusters(titleVectors, kmeans)

file.close()
# results.close()