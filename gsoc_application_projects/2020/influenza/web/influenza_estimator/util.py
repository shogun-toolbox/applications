import pickle
import shogun as sg
from datetime import timedelta, date, datetime
from pathlib import Path

import numpy as np
import pageviewapi
import pandas as pd
from pageviewapi.client import ZeroOrDataNotLoadedException

from . import config


class DataGateway:
    def __init__(self):
        self.data_path = Path.cwd() / 'influenza_estimator' / 'data'
        self.df = {}
        self.wiki = WikiGateway()
        self.estimator = Model()
        for country in config.COUNTRIES:
            file_path = self.data_path / (country + '.csv')
            self.df[country] = pd.read_csv(file_path)
            self.df[country] = self.df[country].set_index('week')

    def get_incidence(self, **filters):
        ans = {}
        countries = config.COUNTRIES
        week = 'current'
        category = 'estimate'
        incidence = None
        if 'countries' in filters:
            countries = [filters['countries']]
        if 'year' in filters:
            week = filters['year'] + '-' + filters['week']
        if 'category' in filters:
            category = [filters['category']]
        for country in countries:
            print('country: ' + str(country))
            if week != 'current':
                incidence = self.df[country].get_value(week, category)
            if incidence is None or week == 'current':
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
        last_checked = date(2005, 1, 1)
        if 'current' in self.df[country]:
            last_checked = datetime.strptime(
                    self.df[country].getvalue('current', date), '%Y-%m-%d')
        if last_checked < yesterday or 'current' not in self.df['country']:
            # query data
            features = self.wiki.get_pageviews(country, yesterday)
            features['date'] = yesterday
            features['week'] = 'current'
            features['estimate'] = self.estimator.predict(country, features)

            # store data
            if 'current' in self.df[country]:
                self.df[country] = self.df[country].drop('current')
            self.df[country] = self.df[country].append(features)
            file_path = self.data_path / (country + '.csv')
            self.df[country].to_csv(file_path, index=False)

        # return data
        return self.df[country].loc['current'].to_dict()

    def get_old_data(self, country, week):
        if week not in self.df[country].index:
            # query data
            current_date = pd.to_datetime(
                    self.df[country].week.add('-0'), format='%Y-%W-%w')
            features = self.wiki.get_pageviews(country, current_date)
            features['date'] = str(current_date)
            features['week'] = str(week)
            features['estimate'] = str(
                    self.estimator.predict(country, features))

            # store data
            self.df[country] = self.df[country].append(features)
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


class Model:
    def __init__(self):
        self.rf = {}

        for country in config.COUNTRIES:
            model_file_path = config.models_path / (country + '_model.pkl')
            with open(str(model_file_path.absolute()), 'rb') as _f:
                self.rf[country] = pickle.load(_f)

    def predict(self, country, features):
        # prepare data
        self.clean_vector(features)
        df = self.process_vector(features)

        # create features
        X = df.values
        print('features are ' + str(X.T))
        sg_features = sg.create_features(X.T)
        print('features created')

        # apply Random Forest Model
        sg_labels = self.rf[country].apply(sg_features)
        print('model applied')
        estimate = sg_labels.get("labels")
        return estimate

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
