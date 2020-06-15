"""
  @file model.py
  @author Tej Sukhatme

  Linear Ridge Regression.
"""
import logging
import numpy as np
import shogun as sg
from .. import config
from . import util


class Model:
    def __init__(self):
        self.random_forest = {}

    def train(self):

        logging.info('training model')
        for country in config.COUNTRIES:
            logging.info('training '+country)
            x_train_file_path = config.processed_data_path / (
                    country + '_features.csv')
            y_train_file_path = config.processed_data_path / (
                        country + '_labels.csv')
            features_train = sg.create_features(util.load(x_train_file_path).T)
            labels_train = sg.create_labels(
                    util.load(y_train_file_path, is_labels=True))

            mean_rule = sg.create_combination_rule("MeanRule")
            rand_forest = sg.create_machine("RandomForest",
                                            labels=labels_train,
                                            num_bags=5, seed=1,
                                            combination_rule=mean_rule)

            rand_forest.train(features_train)

            self.random_forest[country] = rand_forest

    def apply(self, country, df):
        # apply trained model on data
        # create features
        logging.info('Applying model.')
        X = df.values.astype(float)
        sg_features = sg.create_features(X.T)

        # apply Random Forest Model
        sg_labels = self.random_forest[country].apply_regression(sg_features)
        logging.info('Model applied')
        estimate = sg_labels.get("labels")
        logging.info('predicted value for '+country+' is '+str(estimate))
        return estimate

