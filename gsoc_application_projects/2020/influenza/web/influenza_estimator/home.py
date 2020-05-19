from datetime import timedelta, date
from pathlib import Path

import pageviewapi
from flask import (
    Blueprint, render_template
)

bp = Blueprint('home', __name__, url_prefix='/home')

estimates = {}
countries = ['austria', 'belgium', 'germany', 'italy', 'netherlands']


def get_features(country_name, current_date):
    prefix = {'austria'    : 'de',
              'belgium'    : 'nl',
              'germany'    : 'de',
              'italy'      : 'it',
              'netherlands': 'nl'}

    project = prefix[country_name] + '.wikipedia'

    keywords_path = Path.cwd() / 'keywords'
    filepath = keywords_path / ('keywords_' + country_name + '.txt')

    current_date = current_date - timedelta(days=1)
    end = current_date.strftime('%Y%m%d')
    start_date = current_date - timedelta(days=6)
    start = start_date.strftime('%Y%m%d')

    features = []

    with open(filepath, 'r') as file:
        for line in file:
            count = 0
            res = pageviewapi.per_article(project, line.strip(), start, end,
                                          access='all-access',
                                          agent='all-agents',
                                          granularity='daily')
            for item in res['items']:
                count += int(item['views'])
            features.append(count)

    return features


def apply_model(features):
    ans = 0.0
    return ans


def predict():
    for country in countries:
        estimates[country] = 0.0
        # feats = get_features(country, date.today())
        # estimate = apply_model(feats)
        # estimates[country] = estimate


@bp.route('/')
def display():
    predict()
    return render_template('home.html', estimates=estimates)
