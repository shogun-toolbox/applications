"""Start function for the entire model.

This module simply imports all the functions needed to apply the model on
the data and calls them one by one.

"""

import combine
import clean
import process
import prepare
import model


if __name__ == '__main__':
    combine.combine_data()
    clean.clean_data()
    prepare.prepare_data()
    process.process_data()
    model.apply_regression()
