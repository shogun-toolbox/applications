"""Start function for the entire model.

This module simply imports all the functions needed to apply the model on
the data and calls them one by one.

"""

import model


if __name__ == '__main__':

    influenza_estimator = model.Model()
    influenza_estimator.train()
    influenza_estimator.serialize()

