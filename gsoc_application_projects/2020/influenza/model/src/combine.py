"""
  @file combine.py
  @author Tej Sukhatme

  Combining the dataset
"""

import pandas as pd
from pathlib import Path


def combine_data():
    path = Path.cwd()
    raw_data_path = path.parent / 'data' / 'raw'
    combined_data_path = path.parent / 'data' / 'combined'
    countries = ['austria', 'belgium', 'germany', 'italy', 'netherlands']
    years = [2007 + i for i in range(13)]
    for country in countries:
        frames = []
        for year in years:
            incidence_path = (raw_data_path / country / 'complete'
                              / (str(year) + '_' + str(year + 1) + '.csv'))

            if incidence_path.exists() and incidence_path.is_file():
                df_incidence = pd.read_csv(incidence_path)

                wiki_path1 = raw_data_path / ('wikipedia_' +
                                              country) / 'complete' / (
                                     str(year) + '.csv')
                wiki_path2 = raw_data_path / ('wikipedia_' +
                                              country) / 'complete' / (
                                     str(year + 1) + '.csv')

                if wiki_path1.exists() and wiki_path1.is_file():
                    df_wiki1 = pd.read_csv(wiki_path1)
                    df_wiki1 = df_wiki1.rename(columns={'Week': 'week'})
                    df_incidence = pd.merge(
                            df_wiki1, df_incidence, on='week', how='right')

                if wiki_path2.exists() and wiki_path2.is_file():
                    df_wiki2 = pd.read_csv(wiki_path2)
                    df_wiki2 = df_wiki2.rename(columns={'Week': 'week'})
                    df_incidence = pd.merge(
                            df_wiki2, df_incidence, on='week', how='right')

                for col_name in df_incidence.columns:
                    if col_name[-1] == 'x':
                        if col_name[:-2] + '_y' in df_incidence.columns:
                            df_incidence[col_name[:-2]] = df_incidence[
                                col_name].fillna(
                                    df_incidence[col_name[:-2] + '_y'])
                            df_incidence = df_incidence.drop(
                                    columns=[col_name, col_name[:-2] + '_y'])

                frames.append(df_incidence)

        df_country = pd.concat(frames)
        df_country['date'] = pd.to_datetime(
                df_country.week.add('-0'), format='%Y-%W-%w')
        df_country = df_country.sort_values(by="date")

        if 'cases' in df_country.columns:
            df_country.drop(columns=['cases'])

        file_path = combined_data_path / (country + '.csv')

        df_country.to_csv(file_path, index=False)


combine_data()