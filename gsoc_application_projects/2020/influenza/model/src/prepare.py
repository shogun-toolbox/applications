'''
  @file prepare.py
  @author Tej Sukhatme

  Prepare the dataset for regression
'''

from pathlib import Path

import pandas as pd


def prepare_data():
    path = Path.cwd()
    combined_data_path = path.parent / 'data' / 'combined'
    final_data_path = path.parent / 'data' / 'final'
    countries = ['austria', 'belgium', 'germany', 'italy', 'netherlands']
    for country in countries:
        combined_file_path = combined_data_path / (country + '.csv')
        df_country = pd.read_csv(combined_file_path)

        if 'cases' in df_country.columns:
            df_country = df_country.drop(columns=['cases'])

        if 'date' in df_country.columns:
            df_country = df_country.drop(columns=['date'])

        if 'week' in df_country.columns:
            df_country = df_country.drop(columns=['week'])

        final_file_path = final_data_path / (country + '.csv')
        df_country.to_csv(final_file_path, index=False)


prepare_data()
