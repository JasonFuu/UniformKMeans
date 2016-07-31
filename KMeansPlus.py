"""K-Means++ class made for two parameters (intensity and frequency) of energy spikes. Returns k centroids"""
import datetime
import numpy as np
import random
import math

class K_Means_Plus_Plus:

    """Input is meter dictionary from Anon_Metering_Data class(each ID corresponds to a 2d list
    containing the intensity of each spike and the time when it occurred; k refers to number of clusters
    meter dict is in the format: {ID1: [spike power(in kW), datetime of spike], [spike power....], ID2... etc.}"""
    def __init__(self, meter_dictionary, k):
        self.cluster_count = k
        self.meter_dict = meter_dictionary
        self.id_list = self.create_id_list()
        self.intensity_list = self.normalize_list(self.parse_intensities())
        self.frequency_list = self.normalize_list(self.parse_frequencies())
        self.initialize_centroid()
        self.centroid_count = 0

    """Creates a list of all meter IDs from the meter dictionary"""
    def create_id_list(self):
        id_list = []

        for values in self.meter_dict:
            id_list.append(values)

        return id_list

    """parses average spike intensities from dictionary"""""
    def parse_intensities(self):
        self.average_list = []
        temp_list = []

        for values in self.meter_dict:

            for index in range(len(self.meter_dict[values])):
                temp_list.append(self.meter_dict[values][index][0])

            self.average_list.append(np.mean(temp_list))

        return self.average_list

    """parses spike frequencies from dictionary"""
    def parse_frequencies(self):
        freq_list = []

        for values in self.meter_dict:
            freq_list.append(len(self.meter_dict[values]))

        return freq_list

    """Normalizes values in given list to range [0, 1]"""
    def normalize_list(self, list):
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
        index = random.randint(0, len(self.id_list)-1)
        self.centroid_list.append([self.id_list[index], self.intensity_list[index], self.frequency_list[index]])
        self.remove_ID(index)
        self.centroid_count += 1

    """Removes ID associated with given index so it cannot be picked as a future centroid"""
    def remove_ID(self, index):
        print(index)
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