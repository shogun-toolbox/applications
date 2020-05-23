from datetime import timedelta, date, datetime
from pathlib import Path

import pageviewapi
import pandas as pd


class DataGateway:
    def __init__(self):
        countries = ['austria', 'belgium', 'germany', 'italy', 'netherlands']
        self.data_path = Path.cwd() / 'data'
        self.df_dict = {}
        self.wiki = WikiGateway()
        self.model = Model()
        for country in countries:
            file_path = self.data_path / (country + '.csv')
            df_country = pd.read_csv(file_path)

            if 'cases' in df_country.columns:
                df_country = df_country.drop(columns=['cases'])

            df_country = df_country.set_index('week')
            self.df_dict[country] = df_country

    def get_incidence(self, **filters):
        ans = {}
        countries = ['austria', 'belgium', 'germany', 'italy', 'netherlands']
        week = 'current'
        category = 'estimate'
        if 'countries' in filters:
            countries = [filters['countries']]
        if 'year' in filters:
            week = filters['year'] + '-' + filters['week']
        if 'category' in filters:
            category = [filters['category']]
        for country in countries:
            estimate = self.df_dict[country].getvalue(week, category)
            if estimate is None or week is 'current':
                query = self.query(countries=[country], week=week)
                estimate = query[country]['estimate']
            ans[country] = estimate
        return ans

    def query(self, **filters):
        countries = ['austria', 'belgium', 'germany', 'italy', 'netherlands']
        ans = {}
        if 'countries' in filters:
            countries = [filters['countries']]
        if 'week' in filters:
            week = filters['week']
            for country in countries:
                ans[country] = self.get_old_data(country, week)
        else:
            for country in countries:
                ans[country] = self.get_live_data(country)

        return ans

    def get_live_data(self, country):
        yesterday = date.today() - timedelta(days=1)
        last_checked = datetime.strptime(
                self.df_dict[country].getvalue('current', date), '%Y-%m-%d')
        if last_checked < yesterday:
            # query data
            features = self.wiki.get_pageviews(country, yesterday)
            features['date'] = str(yesterday)
            features['week'] = 'current'
            features['estimate'] = str(self.model.predict(country, features))

            # store data
            self.df_dict[country] = self.df_dict[country].drop('current')
            self.df_dict[country] = self.df_dict[country].append(features)
            file_path = self.data_path / (country + '.csv')
            self.df_dict[country].to_csv(file_path, index=False)

        # return data
        return self.df_dict[country].loc['current'].to_dict()

    def get_old_data(self, country, week):
        if week not in self.df_dict[country]:
            # query data
            current_date = pd.to_datetime(
                    self.df_dict[country].week.add('-0'), format='%Y-%W-%w')
            features = self.wiki.get_pageviews(country, current_date)
            features['date'] = str(current_date)
            features['week'] = str(week)
            features['estimate'] = str(self.model.predict(country, features))

            # store data
            self.df_dict[country] = self.df_dict[country].append(features)
            file_path = self.data_path / (country + '.csv')
            self.df_dict[country].to_csv(file_path, index=False)

        # return data
        return self.df_dict[country].loc[week].to_dict()


class WikiGateway:
    def __init__(self):
        self.language = {'austria'    : 'german',
                         'belgium'    : 'dutch',
                         'germany'    : 'german',
                         'italy'      : 'italian',
                         'netherlands': 'dutch'}

        self.prefix = {'german': 'de', 'dutch': 'nl', 'italian': 'it'}

        self.keywords_path = Path.cwd() / 'keywords'

    def get_pageviews(self, country, current_date):
        project = self.prefix[self.language[country]] + '.wikipedia'
        filepath = self.keywords_path / ('keywords_' + country + '.txt')

        current_date = current_date - timedelta(days=1)
        end = current_date.strftime('%Y%m%d')
        start_date = current_date - timedelta(days=6)
        start = start_date.strftime('%Y%m%d')

        features = {}

        with open(filepath, 'r') as file:
            for line in file:
                count = 0
                res = pageviewapi.per_article(project, line.strip(), start,
                                              end,
                                              access='all-access',
                                              agent='all-agents',
                                              granularity='daily')
                for item in res['items']:
                    count += int(item['views'])
                features[line] = str(count)

        return features


class Model:
    def __init__(self):
        self.wiki = WikiGateway()

    def predict(self, country, features):
        estimate = 0
        # apply model, predict and store in estimate
        return estimate
