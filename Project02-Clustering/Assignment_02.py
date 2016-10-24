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
    """
    Convert each title to a string which contains only stemmed words.
    :param lines: File containing the titles.
    :return: List with converted titles.
    """
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
    """
    Execute the K-Means clustering algorith with specified parameters.
    :param k: Number of desired clusters.
    :param titleVectors: Vector containing the vectorized titles.
    :return: Resulting clusters.
    """
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(titleVectors.toarray())
    return kmeans

def printClusters(topicRange, clusterList, k):
    """
    Print a subset of the clusters to the console. This subset contains only the (stemmed) words with most occurrences.
    :param topicRange: Number of words of each cluster that will be printed to the console.
    :param clusterList: The generated clusters.
    :param k: Number of clusters.
    :return:
    """
    print("Top topics per cluster:")
    order_centroids = clusterList.cluster_centers_.argsort()[:, ::-1]
    topics = vectorizer.get_feature_names()
    for i in range(k):
        print("Cluster %d:" % (i+1))
        for j in order_centroids[i, :topicRange]:
            print(' %s' % topics[j])
        print()

def printClustersToFile(topicRange, clusterList, k):
    """
       Print a subset of the clusters to a file. This subset contains only the (stemmed) words with most occurrences.
       :param topicRange: Number of words of each cluster that will be printed to a file.
       :param clusterList: The generated clusters.
       :param k: Number of clusters.
       :return:
       """
    results.write("Top topics per cluster:\n")
    order_centroids = clusterList.cluster_centers_.argsort()[:, ::-1]
    topics = vectorizer.get_feature_names()
    for i in range(k):
        results.write("Cluster %d:\n" % (i+1))
        for j in order_centroids[i, :topicRange]:
            results.write(' %s\n' % topics[j])
        results.write("\n")

def plotClusters(titleVectors, clusterList):
    """
    Plot the clusters for a visual representation.
    :param titleVectors: Vector containing the vectorized titles.
    :param clusterList: The generated clusters.
    :return:
    """
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

# vectorize the textual data
vectorizer = TfidfVectorizer(stop_words='english')
titleVectors = vectorizer.fit_transform(stemmedTitles)

# execute clustering algorithm
kmeans = executeKMeans(k, titleVectors)

# print the n words with most occurences within each cluster
printClusters(topicPrintRange, kmeans, k)
printClustersToFile(topicPrintRange, kmeans, k)

file.close()
results.close()

plotClusters(titleVectors, kmeans)