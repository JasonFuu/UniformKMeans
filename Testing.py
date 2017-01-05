"""Test client for KMeans++ and Equal Cluster K-Means"""
from KMeansPlus import K_Means_Plus_Plus
from Equal_Cluster_K_Means import Equal_K_Means
import matplotlib.pyplot as plt
import random


def main():
    points = []
    xs = []
    ys = []

    for a in range(80):
        c = 100 * random.random()
        b = 50 * random.random()
        xs.append(a)
        ys.append(b)
        points.append([c, b])


    test = K_Means_Plus_Plus(points, 4)
    centroids = test.final_centroids()

    nexttest = Equal_K_Means(points, centroids, 4)
    clusters = nexttest.final_clusters()
    centroids = nexttest.final_centroids()
    group0x = []
    group0y = []
    group1x = []
    group1y = []
    group2x = []
    group2y = []
    group3x = []
    group3y = []
    centroidsx = []
    centroidsy = []

    for points in clusters[0]:
        group0x.append(points[0])
        group0y.append(points[1])
    for points in clusters[1]:
        group1x.append(points[0])
        group1y.append(points[1])
    for points in clusters[2]:
        group2x.append(points[0])
        group2y.append(points[1])
    for points in clusters[3]:
        group3x.append(points[0])
        group3y.append(points[1])
    for points in centroids:
        centroidsx.append(points[0])
        centroidsy.append(points[1])

    plt.scatter(group0x, group0y, color = 'red')
    plt.scatter(group1x, group1y, color = 'yellow')
    plt.scatter(group2x, group2y, color = 'blue')
    plt.scatter(group3x, group3y, color = 'green')

    plt.scatter(centroidsx, centroidsy, color = 'black')
    plt.show()

main()