from os import path

from pathlib import Path


class Config(object):
    DEBUG = True
    PORT = 5000
    HOST = '0.0.0.0'
    # URL_PREFIX = '/api'
    PROJECT_ROOT = path.abspath(path.dirname(__file__))
    TEMPLATE_FOLDER = path.join(PROJECT_ROOT, 'templates')
    # MYSQL_DATABASE_HOST = '127.0.0.1'
    # MYSQL_DATABASE_DB = 'default_db'
    # MYSQL_DATABASE_USER = 'default_user'
    # MYSQL_DATABASE_PASSWORD = 'password'


class Development(Config):
    DEBUG = True
    SECRET_KEY = 'development'


class Production(Config):
    pass


class Testing(Config):
    TESTING = True
    SECRET_KEY = 'testing'


COUNTRIES = ['austria', 'belgium', 'germany', 'italy', 'netherlands']
LANGUAGE = {'austria'    : 'german',
            'belgium'    : 'dutch',
            'germany'    : 'german',
            'italy'      : 'italian',
            'netherlands': 'dutch'}

PREFIX = {'german': 'de', 'dutch': 'nl', 'italian': 'it'}

POPULATION = {'austria'    : 9003354,
              'belgium'    : 11586640,
              'germany'    : 83768122,
              'italy'      : 60467045,
              'netherlands': 17132636}

processed_data_path = Path.cwd() / 'influenza_estimator' / 'data' / 'processed'
keywords_path = Path.cwd() / 'influenza_estimator' / 'revised_keywords'
models_path = Path.cwd() / 'influenza_estimator' / 'models'

years = [2007 + i for i in range(13)]

LOG_FILENAME = str(
    (Path.cwd() / 'influenza_estimator' / 'information.log').absolute())
