"""Parses through electrical metering data in .xlsx format. Finds all spikes and their respective times
for each meter ID."""
import pandas as pd
import math
import datetime
import numpy as np


class MeteringSpikes:

    def __init__(self, dataframe, intended_interval):
        self.df = dataframe
        self.intended_interval = intended_interval

    """Finds spikes in each meter's usage (spike is defined as energy usage 15% greater than
    the meter's average over the time period). Returns dictionary with keys representing meter IDs
    and values representing a 2D list containing each spike and its time"""
    def find_all_spikes(self, id_attribute, energy_attribute, date_attribute):
        spikes = {}

        for IDs in self.df[id_attribute]:

            if IDs not in spikes:
                temp_df = self.df[(self.df[id_attribute] == IDs)]
                energy_df = temp_df[energy_attribute].reset_index(drop=True)
                date_df = temp_df[date_attribute].reset_index(drop=True)
                differences = self.find_differences(energy_df)
                spikes[IDs] = self.find_outlier(differences, date_df)

        return spikes

    """Returns list of a meter's energy usage at each interval"""
    def find_differences(self, energy_df):
        differences = []

        for index in range(1, len(energy_df)):
            differences.append(self.round(energy_df[index] - energy_df[index - 1]))

        return differences

    """Finds outliers (15% higher than average) from a meter's energy usage list"""
    def find_outlier(self, differences, date_df):
        average = np.mean(differences)
        spike_limit = 2.55 * average
        outlier_list = []

        for index in range(len(differences)):
            initial = self.timestamp_to_datetime(date_df[index])
            final = self.timestamp_to_datetime(date_df[index + 1])

            if differences[index] > spike_limit and self.check_interval(initial, final):

                outlier_list.append([self.round(differences[index]), self.timestamp_to_datetime(date_df[index])])

        return outlier_list

    """Converts a pandas timestamp object to datetime object"""
    def timestamp_to_datetime(self, timestamp):
        return timestamp.to_datetime()

    """Checks if interval between two argument times are within the intended interval
    +/- 1 (some leeway for minor irregularities)"""
    def check_interval(self, time1, time2):
        outcome = False

        if time1 + datetime.timedelta(minutes=self.intended_interval - 1) <= time2 <= \
                time1 + datetime.timedelta(minutes=self.intended_interval + 1):
            outcome = True

        return outcome

    """Rounds argument value to 4 digits"""
    def round(self, value):
        return math.ceil(value * 1000) / 1000
