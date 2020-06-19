"""
  @file process.py
  @author Tej Sukhatme

  Data pre-processing.
"""

from src import config
import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import skew


class Processor:
    def __init__(self):
        self.df = {}
        self.lmbda = {'austria'    : {}, 'belgium': {}, 'germany': {},
                      'italy'      : {},
                      'netherlands': {}}
        self.numerical_features = {'austria': [], 'belgium': [], 'germany': [],
                                   'italy'  : [], 'netherlands': []}
        self.skewed_features = {'austria': [], 'belgium': [], 'germany': [],
                                'italy'  : [], 'netherlands': []}

        self.means = {'austria'    : {}, 'belgium': {}, 'germany': {},
                      'italy'      : {},
                      'netherlands': {}}
        self.std_deviations = {'austria'    : {}, 'belgium': {}, 'germany': {},
                               'italy'      : {},
                               'netherlands': {}}

        for country in config.COUNTRIES:
            # read file
            file_path = config.cleaned_data_path / (country + '.csv')
            self.df[country] = pd.read_csv(file_path)

    def process_vector(self, pageviews, country):
        data = pd.DataFrame.from_dict(pageviews)
        data, self.lmbda[country] = self.apply_leo_johnson(data,
                                                           self.lmbda[country],
                                                           self.skewed_features[
                                                               country])

        self.apply_std_normal(data,
                              self.numerical_features[country],
                              self.means[country],
                              self.std_deviations[country])

        return data

    def process_data(self):
        for country in config.COUNTRIES:

            self.hot_encode_weeks(country)

            labels = pd.Series(self.df[country].incidence).to_frame(
                    'incidence')

            features = self.df[country].drop(
                columns=['incidence', 'week', 'date', 'week_number'])
            if 'cases' in features.columns:
                features = features.drop(columns=['cases'])

                # save to file.
            features_file_path = config.processed_data_path / (
                    country + '_features.csv')
            labels_file_path = config.processed_data_path / (
                    country + '_labels.csv')
            features.to_csv(features_file_path, index=False)
            labels.to_csv(labels_file_path, index=False)

    # perform one hot encoding for week numbers
    def hot_encode_weeks(self, country):
        week_number = []
        for index, row in self.df[country].iterrows():
            week_number.append(row['week'][-2:])
        self.df[country]['week_number'] = week_number
        one_hot_encoded_weeks = pd.get_dummies(self.df[country]['week_number'],
                                               prefix='week')
        self.df[country] = pd.concat([self.df[country], one_hot_encoded_weeks],
                                     axis=1)
        self.df[country].drop(columns=['week_number'])

    # we transform features so that mean is 0 and std deviation is 1.
    def apply_std_normal(self, df, numerical_features, means, std_deviations):
        for feature in numerical_features:
            column = df[feature]
            column -= means[feature]
            column /= std_deviations[feature]
            df[feature] = column

    # we transform features so that mean is 0 and std deviation is 1.
    def train_std_normal(self, df, numerical_features, means, std_deviations):
        for feature in numerical_features:
            column = df[feature]
            means[feature] = column.mean()
            std_deviations[feature] = column.std()
            column -= means[feature]
            column /= std_deviations[feature]
            df[feature] = column

    # we apply the Yeo Johnson Transformation.
    def apply_leo_johnson(self, df, lmbda, skewed_features):
        for feature in skewed_features:
            column = df[feature] + 1
            column = stats.boxcox(column.values, lmbda=lmbda[feature])
            column = pd.Series(column)
            df[feature] = column
        return df

    # we train AND apply the Yeo Johnson Transformation.
    def train_leo_johnson(self, df, lmbda, skewed_features):
        for feature in skewed_features:
            column = df[feature] + 1
            column, lmbda[feature] = stats.boxcox(column.values)
            column = pd.Series(column)
            df[feature] = column
        return df, lmbda

    # add 3 polynomial features each for the most important features.
    def add_polynomial_features(self, country, df, num):
        # find the correlation matrix.
        correlation_matrix = df[country].corr()
        correlation_matrix.sort_values(['incidence'], ascending=False,
                                       inplace=True)

        count = 0
        for column, correlation in correlation_matrix['incidence'].items():
            if count > num:
                break
            if column == 'incidence' or column == 'week' or column == 'date':
                continue
            df[country][column + '-s2'] = df[country][column] ** 2
            df[country][column + '-s3'] = df[country][column] ** 3
            df[country][column + '-sq'] = np.sqrt(df[country][column])
            count += 1
