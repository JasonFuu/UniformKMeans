"""Test client for KMeans++ and Equal Cluster K-Means"""
from KMeansPlus import K_Means_Plus_Plus
from Equal_Cluster_K_Means import Equal_K_Means
import matplotlib.pyplot as plt
import random

"""Tests K-means++ with 50 randomly generated 2-var data points in various ranges"""
def KMeansPlusPlus_Test():
    points = []
    xs = []
    ys = []

    for a in range(50):
        a = 100*random.random()
        b = 50*random.random()
        xs.append(a)
        ys.append(b)
        points.append([a, b])

    test = K_Means_Plus_Plus(points, 7)

    centroidx = []
    centroidy = []

    for points in test.final_centroids():
        centroidx.append(points[0])
        centroidy.append(points[1])

    plt.scatter(xs, ys, color = 'red')
    plt.scatter(centroidx, centroidy, color = 'black')

    plt.show()
    print(test.final_centroids())

def main():
    points = []
    xs = []
    ys = []

    for a in range(50):
        a = 100 * random.random()
        b = 50 * random.random()
        xs.append(a)
        ys.append(b)
        points.append([a, b])
    test = K_Means_Plus_Plus(points, 6)
    centroids = test.final_centroids()
    nexttest = Equal_K_Means(points, centroids, 6, 50)
    print(nexttest.final_clusters())

main()