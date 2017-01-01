"""Takes initial centroid inputs from K-Means++. Divides given list of n points into clusters sized
(floor(n/k), floor(n/k)+1). Returns 2d list of final aggregates"""
import numpy as np
import math

class Equal_K_Means():

    """Input is a 2d list of initial seed clusters obtained from K-means++"""
    def __init__(self, points_list, seeds, k):
        self.centroids = seeds
        self.cluster_count = k
        self.check_seeds()
        self.points_list = points_list
        self.points_count = len(points_list)
        self.cluster_size = math.floor(self.points_count/k)
        self.iterations = 0
        self.max_iterations = 128
        self.assign_initial_clusters()
        self.compute_clusters()

    """Checks if seeds are valid"""
    def check_seeds(self):
        if len(self.centroids) != self.cluster_count:
            raise ValueError("Invalid seed length!")

    """Assigns points to initial seeds. almost_full_clusters keeps track of clusters that reach
    floor(n/k) capacity so they are not selected for point addition"""
    def assign_initial_clusters(self):
        self.clusters = [[] for i in range(self.cluster_count)]
        almost_full_clusters = []

        for j in range(self.points_count):
            if len(almost_full_clusters) == self.cluster_count:
                self.overflow_clusters(j)
                break
            index = self.nearest_centroid(self.points_list[j], almost_full_clusters)
            self.clusters[index].append(j)
            if self.is_almost_full(index):
                almost_full_clusters.append(index)

    """Finds nearest centroid to given point, denoted by its index in the points_list"""
    def nearest_centroid(self, point, full_clusters):
        best_centroid = -1
        min_distance = math.inf

        for i in range(self.cluster_count):
            distance = self.euclidean_distance(self.centroids[i], point)
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
            self.clusters[index].append(i)
            if self.is_full(index):
                full_clusters.append(index)

    """computes N-d euclidean distance between two points represented as lists:
       (x1, x2, ..., xn) and (y1, y2, ..., yn)"""
    def euclidean_distance(self, point1, point2):
        point1 = np.asarray(point1)
        point2 = np.asarray(point2)

        return np.linalg.norm(point2 - point1)

    """Computes the +/- equally sized clusters. Swap proposals {cluster_index[points wanting to join,...]}
    closest_cluster is destination, i is current"""
    def compute_clusters(self):
        self.compute_new_centroids()
        swap_proposals = [[] for i in range(self.cluster_count)]
        if self.iterations > 1000:
            return

        for i in range(self.cluster_count):
            for j in range(len(self.clusters[i])):
                closest_cluster = self.nearest_centroid(self.clusters[i][j], [])
                if closest_cluster != i:
                    if len(self.clusters[closest_cluster]) < len(self.clusters[i]):
                        swap_point = self.clusters[i].pop(j)
                        self.clusters[closest_cluster].append(swap_point)
                        self.iterations += 1
                        break
                    elif self.check_swap(swap_proposals, i, closest_cluster) != -1:
                        point_to_swap = self.check_swap(swap_proposals, i, closest_cluster)
                        swap_point_1 = self.clusters[i].pop(j)
                        self.clusters[closest_cluster].remove(point_to_swap)
                        self.clusters[closest_cluster].append(swap_point_1)
                        self.clusters[i].append(point_to_swap)
                        self.iterations += 1
                        break
                    else:
                        swap_proposals[closest_cluster].append(self.clusters[i][j])
                        self.iterations += 1

        self.compute_clusters()

    """Checks if there is a swap proposal from one argument cluster to another. CHANGE LATER TO ACCOMODATE """
    def check_swap(self, swap_proposals, destination, current):
        value = -1
        for points in swap_proposals[destination]:
            if current == self.cluster_number(points):
                value = points

        return value

    """Returns cluster number that the given point belongs to"""
    def cluster_number(self, point):
        index = -1

        for cluster in self.clusters:
            if point in cluster:
                index = self.clusters.index(cluster)

        return index


    """Finds new centroids for given clusters"""
    def compute_new_centroids(self):
        new_centroids = []

        for i in range(self.cluster_count):
            l = []
            for point_index in self.clusters[i]:
                l.append(self.points_list[point_index])
            l = np.asarray(l)
            new_centroids.append(np.mean(l, axis=0).tolist())

        self.centroids = new_centroids

    """Returns cluster lists"""
    def final_clusters(self):
        l = []

        for clusters in self.clusters:
            appending = []
            for point_index in clusters:
                appending.append(self.points_list[point_index])
            l.append(appending)

        return l

    """Returns final centroids"""
    def final_centroids(self):
        return self.centroids


