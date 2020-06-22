"""
  @file util.py
  @author Tej Sukhatme

  some functions to be used
"""

import pandas as pd


def load_features(path):
    if path.exists() and path.is_file():
        df = pd.read_csv(path)
        features = df.drop(columns=['incidence'])
        return features.values
    return None


def load_labels(path):
    if path.exists() and path.is_file():
        df = pd.read_csv(path)
        labels = pd.Series(df['incidence'])
        return labels.values
    return None

def load(path, is_labels=False):
    if path.exists() and path.is_file():
        df = pd.read_csv(path)
        if is_labels:
            df = pd.Series(df['incidence'])
        return df.values
    return None