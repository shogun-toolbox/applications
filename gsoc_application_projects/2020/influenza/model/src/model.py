"""
  @file model.py
  @author Tej Sukhatme

  Linear Ridge Regression.
"""

import pickle
from pathlib import Path

import shogun as sg

import util


def apply_regression():
    path = Path.cwd()
    final_data_path = path.parent / 'data' / 'final'
    countries = ['austria', 'belgium', 'germany', 'italy', 'netherlands']
    models = {}
    for country in countries:
        file_path = final_data_path / (country + '.csv')

        features_train = sg.create_features(util.load_features(file_path).T)
        labels_train = sg.create_labels(util.load_labels(file_path))

        # creating and training a model
        lrr = sg.create_machine("LinearRidgeRegression", tau=0.001,
                                labels=labels_train)
        lrr.train(features_train)

        models[country] = lrr

    # serializing our dict of models to a file called models/model.pkl
    model_path = path.parent / 'models' / 'model.pkl'
    pickle.dump(models, open(str(model_path.absolute()), "wb"))


apply_regression()
