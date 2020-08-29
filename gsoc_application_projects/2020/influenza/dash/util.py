# -*- coding: utf-8 -*-
"""Utility Functions for web application.

Author: Tej Sukhatme

"""

import copy
import logging
from datetime import timedelta, date, datetime
from pathlib import Path

import numpy as np
import pageviewapi
import pandas as pd
from pageviewapi.client import ZeroOrDataNotLoadedException, \
    ThrottlingException

import config
from random_forest import model


class DataGateway:
    def __init__(self):
        logging.basicConfig(filename=config.LOG_FILENAME, level=logging.INFO)

        self.data_path = Path.cwd() / 'data'
        self.df = {}
        self.wiki = WikiGateway()
        self.estimator = ModelGateway()
        self.current_file_path = self.data_path / 'current.csv'
        self.saved_file_path = self.data_path / 'saved.csv'
        self.current_df = pd.read_csv(self.current_file_path)
        self.current_df = self.current_df.set_index('country')
        self.saved_df = pd.read_csv(self.saved_file_path)
        self.saved_df = self.saved_df.set_index('date')
        for country in config.COUNTRIES:
            file_path = self.data_path / (country + '.csv')
            self.df[country] = pd.read_csv(file_path)
            self.df[country] = self.df[country].reset_index().set_index('week')
        logging.info('DataGateway Object Created.')

    def get_incidence(self, **filters):
        ans = {}
        countries = config.COUNTRIES
        week = 'current'
        category = 'estimate'
        incidence = None
        if 'countries' in filters:
            countries = filters['countries']
        if 'year' in filters:
            week = str(filters['year']) + '-' + str(filters['week'])
        if 'category' in filters:
            category = [filters['category']]
        for country in countries:
            if week != 'current':
                incidence = self.df[country].at[week, category]
            if pd.isna(incidence) or week == 'current':
                query = self.query(country, week)
                incidence = query['estimate']
            ans[country] = incidence
        if week == 'current':
            yesterday = date.today() - timedelta(days=1)
            self.saved_df = self.saved_df.append({'date': yesterday,
                                                'austria': ans['austria'],
                                                'belgium': ans['belgium'],
                                                'germany': ans['germany'],
                                                'italy': ans['italy'],
                                                'netherlands': ans['netherlands']},
                                                ignore_index=True)
            self.saved_df.to_csv(self.saved_file_path)
        return ans

    def query(self, country, week):
        if week != 'current':
            ans = self.get_old_data(country, week)
        else:
            ans = self.get_live_data(country)
        return ans

    def get_live_data(self, country):
        logging.info('Fetching live data.')
        yesterday = date.today() - timedelta(days=1)
        last_checked = self.current_df.get_value(country, 'last_checked')

        if isinstance(last_checked, str):
            last_checked = datetime.strptime(last_checked, '%Y-%m-%d').date()
        logging.info('\tlast checked at ' + str(last_checked))
        if last_checked < yesterday:
            logging.info('\tmaking API calls again.')
            # query data
            features = self.wiki.get_pageviews(country, yesterday)
            features['date'] = yesterday
            features['week'] = 'current'
            features['estimate'] = self.estimator.predict(country, features)

            # store data
            self.current_df.at[country, 'last_checked'] = yesterday
            self.current_df.at[country, 'estimate'] = features['estimate']
            self.current_df.to_csv(self.current_file_path)

        # return data
        return self.current_df.loc[country].to_dict()

    def get_old_data(self, country, week):
        # query data
        logging.info('Fetching old data.')
        current_date = pd.to_datetime(
                self.df[country].at[week, 'week'].add('-0'),
                format='%Y-%W-%w')
        features = self.wiki.get_pageviews(country, current_date)
        features['date'] = current_date
        features['week'] = week
        features['estimate'] = self.estimator.predict(country, features)

        # store data
        self.df[country].at[week, 'estimate'] = features['estimate']
        file_path = self.data_path / (country + '.csv')
        self.df[country].to_csv(file_path, index=False)

        # return data
        return self.df[country].loc[week].to_dict()


class WikiGateway:

    def get_pageviews(self, country, current_date):
        logging.info('getting pageviews for ' + country)
        project = config.PREFIX[config.LANGUAGE[country]] + '.wikipedia'
        filepath = config.keywords_path / (country + '.txt')

        current_date = current_date - timedelta(days=1)
        end = current_date.strftime('%Y%m%d')
        start_date = current_date - timedelta(days=6)
        start = start_date.strftime('%Y%m%d')

        features = pd.Series()
        logging.info('from ' + str(start) + ' to ' + str(end))
        with open(str(filepath.absolute()), 'r') as file:
            for line in file:
                line = line[:-1]
                count = 0
                try:
                    res = pageviewapi.per_article(project, line.strip(), start,
                                                  end,
                                                  access='all-access',
                                                  agent='all-agents',
                                                  granularity='daily')

                    for item in res['items']:
                        count += int(item['views'])
                except ZeroOrDataNotLoadedException:
                    logging.info(
                        'ZeroOrDataNotLoadedException returned, saving '
                        'pageviews as 0.')
                    count = 0
                except ThrottlingException:
                    logging.info(
                        'ThrottlingException returned, saving pageviews as 0.')
                    count = 0
                features[line] = count
                logging.info('\tpageviews for ' + line + ' are ' + str(count))

        return features


class ModelGateway:
    def __init__(self):
        self.random_forest = model.Model()
        self.random_forest.train()

    def predict(self, country, features):
        # prepare data
        self.clean_vector(features)
        df = self.process_vector(features)
        estimate = self.random_forest.apply(country, df)
        return estimate[0]

    def clean_vector(self, pageviews):
        for article, v in pageviews.items():
            if article == 'week' or article == 'date':
                continue
            if int(pageviews[article]) < 0 or np.isnan(
                    int(pageviews[article])):
                pageviews[article] = 0

    def process_vector(self, pageviews):
        data = pd.DataFrame([pageviews], columns=pageviews.index)
        data = self.hot_encode_weeks(data)
        if 'date' in data.columns:
            data = data.drop(columns=['date'])
        if 'week' in data.columns:
            data = data.drop(columns=['week'])
        if 'cases' in data.columns:
            data = data.drop(columns=['cases'])
        return data

    def hot_encode_weeks(self, df):
        week_number = []
        for index, row in df.iterrows():
            if row['week'] != 'current':
                week_number.append(row['week'][-2:])
            else:
                # FIXME
                yesterday = date.today() - timedelta(days=1)
                week_number.append(yesterday.isocalendar()[1])

        for i in range(16):
            if i == 0:
                continue
            if i == week_number:
                df['week_' + str(i)] = 1
            else:
                df['week_' + str(i)] = 0

        for i in range(11):
            if i + 42 == 0:
                continue
            if i + 42 == week_number:
                df['week_' + str(i + 42)] = 1
            else:
                df['week_' + str(i + 42)] = 0
        return df


def calculate_count(dict):
    estimates = copy.deepcopy(dict)
    estimates['total_count'] = 0
    for country in dict:
        estimates[country + '_count'] = int(
                estimates[country] * config.POPULATION[country] / 100000)
        estimates['total_count'] += estimates[country + '_count']
    return estimates
