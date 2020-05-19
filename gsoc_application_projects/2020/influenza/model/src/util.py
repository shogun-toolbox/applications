"""


"""

import pandas as pd


def load_features(path):
    if path.exists() and path.is_file():
        df = pd.read_csv(path)
        features = df.drop(columns=['incidence'])
        return features.values


def load_labels(path):
    if path.exists() and path.is_file():
        df = pd.read_csv(path)
        labels = pd.Series(df['incidence'])
        return labels.values
