"""Parses through cleansed metering data to find spikes. Then uses K-Means++ to find the
input centroid value for the K-Mean variant. This variant then aggregates the meters
into floor(n/k) +/- 1 sized clusters"""
import datetime
import numpy as np
from MeteringAnon.Parse_Metering_Data import MeteringSpikes
from MeteringAnon.KMeansPlus import K_Means_Plus_Plus

def parse_x_centroids(centroids):
    x_coords = []
    for index in range(len(centroids)):
        x_coords.append(centroids[index][0])

    return x_coords


def parse_y_centroids(centroids):
    y_coords = []
    for index in range(len(centroids)):
        y_coords.append(centroids[index][1])

    return y_coords


def consolidate_centroids(x_list, y_list):
    final = []
    for index in range(len(x_list)):
        final.append([x_list[index], y_list[index]])

    return final

"""Energy usage interval for this data-set is 15 minutes"""
initial_filename = '/Users/jason/Downloads/_january1through15.xlsx'
metering_data = MeteringSpikes(initial_filename, 15)
energy_use_dictionary = metering_data.find_all_spikes('Meter_ID', 'KW/MIN', 'time')
k_means = K_Means_Plus_Plus(energy_use_dictionary, 20)

"""Runs K-means++ to find K initial centers for input into the K-means variant"""
while not k_means.is_finished():
    k_means.find_new_center()

print('Final K centroids', k_means.final_centroids())
K_centroids = k_means.final_centroids()
