"""K-Means++ class made for multiple parameters. Returns k initial seeds to be used in Equal_Cluster_K_Means"""
import numpy as np
import random
import math

class K_Means_Plus_Plus:

    """Input is a 2D list of n-dimensional points. Normalizes each parameter to minimize effect of outliers"""
    def __init__(self, points_list, n, k):
        self.centroid_count = 0
        self.dimensions = n
        self.cluster_count = k
        self.normalized_points = self.normalize_parameters(points_list)
        self.initialize_centroid()

    """Normalizes each of the n parameters in the initial list of points"""
    def normalize_parameters(self, points):
        normalized = []

        for a in range(self.dimensions):
            appending = []
            for point in points:
                appending.append(point[a])
            normalized.append(self.normalize(appending))

        return normalized

    """Normalizes values in given list to range [0, 1]"""
    def normalize(self, list):
        new_list = []
        max = np.max(list)
        min = np.min(list)

        for values in list:
            new_list.append((values - min)/(max-min))

        return new_list

    """Picks a random point to serve as the first centroid. Centroids are recorded in list form:
    [ID, spike frequency, spike intensity]"""
    def initialize_centroid(self):
        self.centroid_list = []
        index = random.randint(0, len(self.normalized_points)-1)

        self.remove_ID(index)
        self.centroid_count += 1

    """Removes ID associated with given index so it cannot be picked as a future centroid"""
    def remove_ID(self, index):
        del self.id_list[index]
        del self.frequency_list[index]
        del self.intensity_list[index]

    """Calculates distance from each point to its nearest cluster center. Then chooses new
    center based on the weighted probability of these distances"""
    def find_new_center(self):
        distance_list = []

        for index in range(len(self.id_list)):
            distance_list.append(self.find_nearest_centroid(index))

        new_center_index = self.choose_weighted(distance_list)
        self.centroid_list.append([self.id_list[new_center_index], self.intensity_list[new_center_index],
                                   self.frequency_list[new_center_index]])
        self.remove_ID(new_center_index)
        self.centroid_count += 1

    """Finds centroid nearest to the given ID, and returns its distance"""
    def find_nearest_centroid(self, index):
        min_distance = math.inf

        for values in self.centroid_list:
            distance = self.euclidean_distance(self.intensity_list[index], self.frequency_list[index],
                                               values[1], values[2])
            if distance < min_distance:
                min_distance = distance

        return min_distance

    """Chooses an index based on weighted probability"""
    def choose_weighted(self, distance_list):
        distance_list = [x**2 for x in distance_list]
        weighted_list = self.weight_values(distance_list)
        indices = [i for i in range(len(distance_list))]
        return np.random.choice(indices, p = weighted_list)

    """Weights values from [0,1]"""
    def weight_values(self, list):
        sum = np.sum(list)
        return [x/sum for x in list]

    """computes 2d euclidean distance between (x1, y1) and (x2, y2)"""
    def euclidean_distance(self, x1, y1, x2, y2):
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    """Checks to see if final condition has been satisfied (when K centroids have been created)"""
    def is_finished(self):
        outcome = False
        if self.centroid_count == self.cluster_count:
            outcome = True

        return outcome

    """Returns final centroid values"""
    def final_centroids(self):
        return self.centroid_list