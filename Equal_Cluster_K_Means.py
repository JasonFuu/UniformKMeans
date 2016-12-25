"""Takes initial centroid inputs from K-Means++. Divides given dictionary of n meters into clusters sized
n/k +/- 1. Returns 2d list of final aggregates"""
import numpy as np
import math

class Equal_K_Means():

    """Input is a 2d list of initial seed clusters obtained from K-means++"""
    def __init__(self, points_list, seeds, k, iterations):
        self.centroids = seeds
        self.cluster_count = k
        self.points_list = points_list
        self.points_count = len(points_list)
        self.cluster_size = math.floor(self.points_count/k)
        self.interations = iterations
        self.assign_initial_clusters()

    """Assigns points to initial seeds. almost_full_clusters keeps track of clusters that reach
    floor(n/k) capacity so they are not selected for point addition"""
    def assign_initial_clusters(self):
        self.clusters = [[] for i in range(self.cluster_count)]
        almost_full_clusters = []

        for j in range(self.points_count):
            if len(almost_full_clusters) == self.cluster_count:
                self.overflow_clusters(j)
                break
            index = self.nearest_centroid(j, almost_full_clusters)
            self.clusters[index].append(self.points_list[j])
            if self.is_almost_full(index):
                almost_full_clusters.append(index)

    """Finds nearest centroid to given point, denoted by its index in the points_list"""
    def nearest_centroid(self, index, full_clusters):
        best_centroid = -1
        min_distance = math.inf

        for i in range(self.cluster_count):
            distance = self.euclidean_distance(self.centroids[i], self.points_list[index])
            if distance < min_distance and i not in full_clusters:
                best_centroid = i
                min_distance = distance

        return best_centroid

    """Checks if cluster defined by the given index reaches floor(n/k) capacity"""
    def is_almost_full(self, index):
        return len(self.clusters[index]) == self.cluster_size

    """Checks if cluster defined by the given index reaches floor(n/k)+1 capacity"""
    def is_full(self, index):
        return len(self.clusters[index]) == self.cluster_size+1

    """Fills the remaining clusters if they all reach floor(n/k) capacity starting at the given point index
    Involves new list containing clusters that have reached floor(n/k)+1 (ie max) capacity"""
    def overflow_clusters(self, index):
        full_clusters = []

        for i in range(index, self.points_count):
            index = self.nearest_centroid(i, full_clusters)
            self.clusters[index].append(self.points_list[i])
            if self.is_full(index):
                full_clusters.append(index)

    """computes N-d euclidean distance between two points represented as lists:
       (x1, x2, ..., xn) and (y1, y2, ..., yn)"""
    def euclidean_distance(self, point1, point2):
        point1 = np.asarray(point1)
        point2 = np.asarray(point2)

        return np.linalg.norm(point2 - point1)

    """Returns cluster lists"""
    def final_clusters(self):
        for a in range(self.cluster_count):
            print(a, len(self.clusters[a]))
        return self.clusters


