"""
  @file model.py
  @author Tej Sukhatme

  Linear Ridge Regression.
"""
import pickle
import shogun as sg
import numpy as np
from pathlib import Path

# from config import COUNTRIES
import util

COUNTRIES = ['austria', 'belgium', 'germany', 'italy', 'netherlands']


def apply_regression():
    path = Path.cwd()
    processed_data_path = path.parent / 'data' / 'processed'
    model = {}
    for country in COUNTRIES:
        x_train_file_path = processed_data_path / (country + '_features.csv')
        y_train_file_path = processed_data_path / (country + '_labels.csv')

        features_train = sg.create_features(util.load(x_train_file_path).T)
        labels_train = sg.create_labels(
            util.load(y_train_file_path, is_labels=True))

        mean_rule = sg.create_combination_rule("MeanRule")
        rand_forest = sg.create_machine("RandomForest", labels=labels_train,
                                        num_bags=5, seed=1,
                                        combination_rule=mean_rule)

        rand_forest.train(features_train)

        model[country] = rand_forest

    # serializing our dict of models to a file called models/model.pkl
    model_path = path.parent / 'models' / 'model.pkl'
    pickle.dump(model, open(str(model_path.absolute()), "wb"))


apply_regression()
