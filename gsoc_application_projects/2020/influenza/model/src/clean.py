"""
  @file clean.py
  @author Tej Sukhatme

  Data Cleaning.
"""

from pathlib import Path

import pandas as pd


def clean_data():
    path = Path.cwd()
    combined_data_path = path.parent / 'data' / 'combined'
    cleaned_data_path = path.parent / 'data' / 'cleaned'

    countries = ['austria', 'belgium', 'germany', 'italy', 'netherlands']

    df = {}
    for country in countries:
        # read file
        combined_file_path = combined_data_path / (country + '.csv')
        df[country] = pd.read_csv(combined_file_path)

        # drop columns with all more than 20% data missing
        percent_missing = (df[country].isnull().sum() / df[
            country].isnull().count()).sort_values(ascending=False)

        for column, null_percent in percent_missing.items():
            if null_percent > 0.2:
                df[country] = df[country].drop(columns=[column])

        # perform linear interpolation on remaining missing values
        df[country] = df[country].interpolate(method='linear',
                                              limit_direction='forward',
                                              axis=0)
        df[country] = df[country].interpolate(method='linear',
                                              limit_direction='backward',
                                              axis=0)

        # drop columns with all values as zeroes
        df[country] = df[country].loc[:, (df[country] != 0).any(axis=0)]

        # save to file.
        cleaned_file_path = cleaned_data_path / (country + '.csv')
        df[country].to_csv(cleaned_file_path, index=False)


clean_data()
