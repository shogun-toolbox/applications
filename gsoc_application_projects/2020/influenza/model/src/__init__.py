from clean import *
from combine import *
from model import *
from prepare import *

if __name__ == '__main__':
    combine_data()
    clean_data()
    prepare_data()
    apply_regression()
