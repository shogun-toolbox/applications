"""
  @file model.py
  @author Tej Sukhatme

  Linear Ridge Regression.
"""

import pickle
from pathlib import Path

import util
from shogun import *
from shogun import LinearRidgeRegression as LRR


def apply_regression():
    path = Path.cwd()
    final_data_path = path.parent / 'data' / 'final'
    countries = ['austria', 'belgium', 'germany', 'italy', 'netherlands']
    models = {}
    for country in countries:
        file_path = final_data_path / (country + '.csv')

        features_train = RealFeatures(util.load_features(file_path).T)
        labels_train = RegressionLabels(util.load_labels(file_path))

        tau = 2
        bias = 0
        solver = ST_AUTO
        """ 
        options are:
            ST_AUTO,
            ST_CPLEX,
            ST_GLPK,
            ST_NEWTON,
            ST_DIRECT,
            ST_ELASTICNET,
            ST_BLOCK_NORM
        """
        # creating and training a model
        model = LRR(tau, features_train, labels_train)
        model.set_bias(bias)
        model.set_solver_type(solver)

        model.train()

        models[country] = model

    # serializing our dict of models to a file called models/model.pkl
    model_path = path.parent / 'models' / 'model.pkl'
    pickle.dump(models, open(str(model_path.absolute()), "wb"))


apply_regression()
