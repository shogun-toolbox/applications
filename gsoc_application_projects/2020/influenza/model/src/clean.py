"""
  @file clean.py
  @author Tej Sukhatme

  Data Cleaning.
"""

import config
import numpy as np
import pandas as pd


class Cleaner:

    def __init__(self):
        self.df = {}

    def clean_vector(self, pageviews):
        for article in pageviews:
            if pageviews[article] < 0 or np.isnan(pageviews[article]):
                pageviews[article] = 0

    def clean_data(self):
        for country in config.COUNTRIES:
            # read file
            combined_file_path = config.combined_data_path / (country + '.csv')
            self.df[country] = pd.read_csv(combined_file_path)

            # drop columns with all more than 20% data missing
            percent_missing = (self.df[country].isnull().sum() / self.df[
                country].isnull().count()).sort_values(ascending=False)

            for column, null_percent in percent_missing.items():
                if null_percent > 0.2:
                    self.df[country] = self.df[country].drop(columns=[column])

            # perform linear interpolation on remaining missing values
            self.df[country] = self.df[country].interpolate(method='linear',
                                                            limit_direction='forward',
                                                            axis=0)
            self.df[country] = self.df[country].interpolate(method='linear',
                                                            limit_direction='backward',
                                                            axis=0)

            # drop columns with all values as zeroes
            self.df[country] = self.df[country].loc[:,
                               (self.df[country] != 0).any(axis=0)]

            # save to file.
            cleaned_file_path = config.cleaned_data_path / (country + '.csv')
            self.df[country].to_csv(cleaned_file_path, index=False)
