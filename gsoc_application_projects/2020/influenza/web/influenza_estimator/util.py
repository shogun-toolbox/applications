import pickle
import shogun as sg
from datetime import timedelta, date, datetime
from pathlib import Path

import numpy as np
import pageviewapi
import pandas as pd
from pageviewapi.client import ZeroOrDataNotLoadedException

from . import config
from .random_forest import model


class DataGateway:
    def __init__(self):
        self.data_path = Path.cwd() / 'influenza_estimator' / 'data'
        self.df = {}
        self.wiki = WikiGateway()
        self.estimator = ModelGateway()
        self.current_file_path = self.data_path / 'current.csv'
        self.current_df = pd.read_csv(self.current_file_path)
        self.current_df = self.current_df.reset_index().set_index('country')
        for country in config.COUNTRIES:
            file_path = self.data_path / (country + '.csv')
            self.df[country] = pd.read_csv(file_path)

            # for index, row in self.df[country].iterrows():
            #     if row['week'] != 'current':
            #         date = datetime.strptime(str(row['date']), '%Y-%m-%d')
            #         week = str(date.isocalendar()[0])+'-'+str(
            #         date.isocalendar()[1])
            #         self.df[country].at[index, 'week'] = week
            self.df[country] = self.df[country].reset_index().set_index('week')
            print(self.df[country].columns.values)

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
            print('country: ' + str(country))
            if week != 'current':
                incidence = self.df[country].at[week, category]
            if pd.isna(incidence) or week == 'current':
                query = self.query(country, week)
                incidence = query['estimate']
            ans[country] = incidence
        return ans

    def query(self, country, week):
        if week != 'current':
            ans = self.get_old_data(country, week)
        else:
            ans = self.get_live_data(country)
        return ans

    def get_live_data(self, country):
        yesterday = date.today() - timedelta(days=1)
        print(yesterday)
        last_checked = self.current_df.get_value(country, 'last_checked')

        if isinstance(last_checked, str):
            last_checked = datetime.strptime(last_checked, '%Y-%m-%d').date()
        print('\tlast checked at ' + str(last_checked))
        if last_checked < yesterday:
            print('\tmaking API calls again')
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
        print(self.df[country].columns.values)
        current_date = pd.to_datetime(self.df[country].at[week, 'week'].add('-0'),
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
        print('getting pageviews for ' + country)
        project = config.PREFIX[config.LANGUAGE[country]] + '.wikipedia'
        filepath = config.keywords_path / (country + '.txt')

        current_date = current_date - timedelta(days=1)
        end = current_date.strftime('%Y%m%d')
        start_date = current_date - timedelta(days=6)
        start = start_date.strftime('%Y%m%d')

        features = pd.Series()
        print('from ' + str(start) + ' to ' + str(end))
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
                    count = 0
                features[line] = count
                print('\tpageviews for ' + line + ' are ' + str(count))

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
        # print(data)
        data = self.hot_encode_weeks(data)
        if 'date' in data.columns:
            data = data.drop(columns=['date'])
        if 'week' in data.columns:
            data = data.drop(columns=['week'])
        if 'cases' in data.columns:
            data = data.drop(columns=['cases'])
        # if 'week_number' in data.columns:
        # data = data.drop(columns=['week_number'])
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
