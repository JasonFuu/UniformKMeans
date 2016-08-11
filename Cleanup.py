""""Finds potential errors in metering data that could interfere with aggregation process or cause
erroneous results. Input is the metering dataframe as well as attributes for ID, energy usage, time,
and the intended time interval between each measurement."""
import pandas as pd
import datetime


class Clean_csv:

    def __init__(self, dataframe, id_attribute, energy_attribute, time_attribute, intended_interval):
        self.df = dataframe
        self.id_attribute = id_attribute
        self.energy_attribute = energy_attribute
        self.time_attribute = time_attribute
        self.intended_interval = intended_interval
        self.non_increasing_list = []
        self.massive_spike_list = []
        self.wrong_interval_list = []

    "Prints IDs and times of meters with potentially erroneous energy usage values"
    def check_energy_usage(self):
        checked_list = []

        for IDs in self.df[self.id_attribute]:

            if IDs not in checked_list:

                temp_df = self.df[(self.df[self.id_attribute] == IDs)]
                energy_df = temp_df[self.energy_attribute].reset_index(drop=True)
                date_df = temp_df[self.time_attribute].reset_index(drop=True)
                self.check_increasing(energy_df, date_df, IDs)
                self.check_massive_jump(energy_df, date_df, IDs)
                checked_list.append(IDs)

        print("Non-increasing values:", self.non_increasing_list)
        print("Intervals with extremely high usage:", self.massive_spike_list)

    """Checks to see that energy usage values for an ID are monotonically increasing"""
    def check_increasing(self, energy_df, date_df, ID):

        for index in range(1, len(energy_df)):

            if energy_df[index-1] > energy_df[index]:
                self.non_increasing_list.append([ID, self.str_to_datetime(date_df[index]), energy_df[index-1] - energy_df[index]])
                break

    """Checks for large power spikes that could indicate errors in the data such as skipped times, etc."""
    def check_massive_jump(self, energy_df, date_df, ID):

        for index in range(1, len(energy_df)):
            difference = energy_df[index] - energy_df[index - 1]

            if difference > 5:
                self.massive_spike_list.append([ID, self.str_to_datetime(date_df[index]), difference])
                break

    """Performs checks on timestamp column; prints potentially erroneous IDs and times"""
    def check_times(self):
        checked_IDs = []

        for IDs in self.df[self.id_attribute]:

            if IDs not in checked_IDs:
                temp_df = self.df[(self.df[self.id_attribute] == IDs)]
                date_df = temp_df[self.time_attribute].reset_index(drop=True)
                self.check_interval(date_df, IDs)
                checked_IDs.append(IDs)

        print("Wrong intervals:", self.wrong_interval_list)

    """Determines if times in the timestamp column are all the intended interval apart"""
    def check_interval(self, date_df, IDs):

        for index in range(1, len(date_df)):

            if not self.is_in_intended_interval(self.str_to_datetime(date_df[index-1]), self.str_to_datetime(date_df[index])):
                self.wrong_interval_list.append([IDs, self.str_to_datetime(date_df[index])])
                break

    """Checks if two times are in the intended interval +/- 1 minute"""
    def is_in_intended_interval(self, time1, time2):
        outcome = False

        if time1 + datetime.timedelta(minutes = self.intended_interval - 1) <= time2 <= \
            time1 + datetime.timedelta(minutes = self.intended_interval + 1):

            outcome = True

        return outcome

    """Converts date in format 'M/D/Y X:XX' to datetime format for comparison"""
    def str_to_datetime(self, timestamp):
        return timestamp.to_datetime()

