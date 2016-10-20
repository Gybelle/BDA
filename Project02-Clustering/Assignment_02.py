# Assignment 2: Clustering
# Authors: Michelle Gybels & Anaïs Ools

from stemming.porter2 import stem
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

bigDataset = False
k = 2
startYear = 2000
endYear = startYear + 5
overlap = 2
topicPrintRange = 20

if not bigDataset:
    file = open("../Input/titles.txt", "r", encoding="utf8")
    resultsFile = "../Output/titlesResult_%d_%d-%d.txt" % (k, (startYear-overlap), (endYear+overlap))
    results = open(resultsFile, "w", encoding="utf8")
else:
    file = open("../Input/titlesBIG.txt", "r", encoding="utf8")
    resultsFile = "../Output/titlesResult_%d_%d-%d_BIG.txt" % (k, (startYear - overlap), (endYear + overlap))
    results = open(resultsFile, "w", encoding="utf8")

def stemLines(lines):
    result = []
    for line in lines:
            line = line.strip().replace("[", "").replace("]", "")
            year = int(line.split("\t")[0])
            if year >= (startYear-overlap) and year <= (endYear+overlap):
                line = line.split("\t")[1]
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

def printClustersToFile(topicRange, clusterList, k):
    results.write("Top topics per cluster:\n")
    order_centroids = clusterList.cluster_centers_.argsort()[:, ::-1]
    topics = vectorizer.get_feature_names()
    for i in range(k):
        results.write("Cluster %d:\n" % (i+1))
        for j in order_centroids[i, :topicRange]:
            results.write(' %s\n' % topics[j])
        results.write("\n")

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

printClusters(topicPrintRange, kmeans, k)
printClustersToFile(topicPrintRange, kmeans, k)

file.close()
results.close()

plotClusters(titleVectors, kmeans)