from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

titles = ["Human machine interface for lab abc computer applications",
             "A survey of user opinion of computer system response time",
             "The EPS user interface management system",
             "System and human system engineering testing of EPS",
             "Relation of user perceived response time to error measurement",
             "The generation of random binary unordered trees",
             "The intersection graph of paths in trees",
             "Graph minors IV Widths of trees and well quasi ordering",
             "Graph minors A survey",
            "Graph survey tree"]


# Vectorize the titles
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(titles)

k = 3
kmeans = KMeans(n_clusters=k)
kmeans.fit(X.toarray())

test = vectorizer.get_feature_names()
for element in test:
    print(element)
print(X)

print("Top terms per cluster:")
order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
for i in range(k):
    print("Cluster %d:" % i)
    for ind in order_centroids[i, :10]:
        print (' %s' % terms[ind])
    print()

#Plotten
#Plot: data
pca = PCA(n_components=2).fit(X.toarray())
data2D = pca.transform(X.toarray())
plt.scatter(data2D[:,0], data2D[:,1], c=kmeans.labels_)
#plt.show()


# Plot: centers
centers2D = pca.transform(kmeans.cluster_centers_)
plt.hold(True)
plt.scatter(centers2D[:,0], centers2D[:,1], marker='x', s=200, linewidths=3, c='r')
plt.show()


## Functions based on the code above:
def vectorizeTitles(titles):
    vectorizer = TfidfVectorizer(stop_words='english')
    titleVectors = vectorizer.fit_transform(titles)
    return titleVectors

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

