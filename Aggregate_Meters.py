"""Class that aggregates list of meters and plots the aggregate's energy usage as well as its spikes"""
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import math
import numpy as np


class AggregatedMeters:

    def __init__(self, dataframe, aggregate_list):
        self.df = dataframe
        self.aggregate_list = aggregate_list

    def aggregate(self, id_attribute, energy_attribute):
        cumulative_usage = [0] * 1439
        checked_list = []

        for IDs in self.df[id_attribute]:

            if IDs in self.aggregate_list and IDs not in checked_list:

                checked_list.append(IDs)
                temp_df = self.df[(self.df[id_attribute] == IDs)]
                energy_df = (temp_df[energy_attribute]).reset_index(drop=True)

                for index in range(len(energy_df) - 1):
                    cumulative_usage[index] += energy_df[index]

        aggregate_usage = []

        for index in range(1, len(cumulative_usage) - 1):
            rounded = cumulative_usage[index] - cumulative_usage[index - 1]
            aggregate_usage.append(self.round(rounded))

        return aggregate_usage

        # determines percentage contribution of each meter in the list to the overall aggregate
        # energy consumption at each interval

    def find_total_contribution(self, meter_list, id_attribute, energy_attribute, aggregate_usage):
        usage_percentages = {}
        total_usage = sum(self.remove_outliers(aggregate_usage))

        for IDs in self.df[id_attribute]:

            if IDs in meter_list:
                temp_df = self.df[(self.df[id_attribute] == IDs)]
                energy_df = (temp_df[energy_attribute]).reset_index(drop=True)
                individual_usage = energy_df[len(energy_df) - 1] - energy_df[0]
                usage_percentages[IDs] = (individual_usage / total_usage)

        print(usage_percentages)

    def aggregate_plot(self, meter_list, aggregate_usage, interval):
        plt.title("Aggregate Energy Usage for Meters: " +
                  ','.join([str(i) for i in meter_list]))
        plt.xlabel(str(interval) + ' Minute Intervals')
        plt.ylabel("Average KW/Min Usage")
        plt.show()

    """Rounds argument value to 4 digits"""
    def round(self, value):
        return math.ceil(value * 1000) / 1000
