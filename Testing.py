"""Test client for KMeans++ and Equal Cluster K-Means"""
from KMeansPlus import K_Means_Plus_Plus
import pandas
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random

"""Tests K-means++ with 50 randomly generated 3-var data points in various ranges"""
def KMeansPlusPlus_Test():
    points = []
    xs = []
    ys = []
    zs = []
    for a in range(50):
        a = 100*random.random()
        b = 50*random.random()
        c = 70*random.random()
        xs.append(a)
        ys.append(b)
        zs.append(c)
        points.append([a, b, c])

    test = K_Means_Plus_Plus(points, 7)

    centroidx = []
    centroidy = []
    centroidz = []

    for points in test.final_centroids():
        centroidx.append(points[0])
        centroidy.append(points[1])
        centroidz.append(points[2])

    fig = plt.figure()
    ax = fig.add_subplot(111, projection = '3d')
    scatterplot = ax.scatter(xs, ys, zs, color = 'yellow')
    scatterplot1 = ax.scatter(centroidx, centroidy, centroidz, color = 'black')

    plt.show()
    print(test.final_centroids())


KMeansPlusPlus_Test()