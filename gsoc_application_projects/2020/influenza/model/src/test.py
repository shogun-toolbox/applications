from pathlib import Path

import pandas as pd
from scipy.stats import skew
from sklearn.preprocessing import PowerTransformer, StandardScaler

import process

COUNTRIES = ['austria', 'belgium', 'germany', 'italy', 'netherlands']


def power_transform():
    path = Path.cwd()
    cleaned_data_path = path.parent / 'data' / 'cleaned'

    df = {}
    lmbda = {'austria'    : {}, 'belgium': {}, 'germany': {}, 'italy': {},
             'netherlands': {}}

    for country in COUNTRIES:
        print('For ' + country + ':')
        print()
        # read file
        file_path = cleaned_data_path / (country + '.csv')
        df[country] = pd.read_csv(file_path)

        process.add_polynomial_features(country, df, 10)

        numerical_features = df[country].select_dtypes(
                exclude=["object"]).columns
        numerical_features = numerical_features.drop('incidence')
        skewness = df[country][numerical_features].apply(lambda x: skew(x))
        skewness = skewness[abs(skewness) > 0.5]
        skewed_features = skewness.index

        process.hot_encode_weeks(country, df)

        train = df[country].sample(frac=0.8, random_state=200)
        test = df[country].drop(train.index)

        train = train.sort_values(by="date")
        test = test.sort_values(by="date")
        train = train.drop(columns=['week', 'date'])
        test = test.drop(columns=['week', 'date'])

        y_train = pd.Series(train['incidence']).to_frame('incidence')
        y_test = pd.Series(test['incidence']).to_frame('incidence')
        X_train = train.drop(columns=['incidence'])
        X_test = test.drop(columns=['incidence'])

        pt = PowerTransformer()
        pt.fit_transform(X_train, y_train.values)
        params = pt.get_params()
        pt.fit_transform(X_test)

        print('params are: '+str(params))
        # print("y_train : " + str(y_train))
        means = {}
        std_deviations = {}
        process.train_std_normal(X_train, numerical_features, means,
                                 std_deviations)

        process.apply_std_normal(X_test, numerical_features, means,
                                 std_deviations)

        print("X_train : " + str(X_train.shape))
        print("X_test : " + str(X_test.shape))

        test_data_path = path.parent / 'data' / 'test' / country

        x_train_file_path = test_data_path / 'X_train.csv'
        y_train_file_path = test_data_path / 'y_train.csv'
        x_test_file_path = test_data_path / 'X_test.csv'
        y_test_file_path = test_data_path / 'y_test.csv'

        X_train.to_csv(x_train_file_path, index=False)
        y_train.to_csv(y_train_file_path, index=False)
        X_test.to_csv(x_test_file_path, index=False)
        y_test.to_csv(y_test_file_path, index=False)

        print()
        print()


def test_train_split():
    path = Path.cwd()
    cleaned_data_path = path.parent / 'data' / 'cleaned'

    df = {}
    lmbda = {'austria'    : {}, 'belgium': {}, 'germany': {}, 'italy': {},
             'netherlands': {}}

    for country in COUNTRIES:
        print('For ' + country + ':')
        print()
        # read file
        file_path = cleaned_data_path / (country + '.csv')
        df[country] = pd.read_csv(file_path)

        process.add_polynomial_features(country, df, 10)

        numerical_features = df[country].select_dtypes(
                exclude=["object"]).columns
        numerical_features = numerical_features.drop('incidence')
        skewness = df[country][numerical_features].apply(lambda x: skew(x))
        skewness = skewness[abs(skewness) > 0.5]
        skewed_features = skewness.index

        process.hot_encode_weeks(country, df)

        train = df[country].sample(frac=0.8, random_state=200)
        test = df[country].drop(train.index)

        train = train.sort_values(by="date")
        test = test.sort_values(by="date")
        train = train.drop(columns=['week', 'date'])
        test = test.drop(columns=['week', 'date'])

        y_train = pd.Series(train['incidence']).to_frame('incidence')
        y_test = pd.Series(test['incidence']).to_frame('incidence')
        X_train = train.drop(columns=['incidence'])
        X_test = test.drop(columns=['incidence'])

        # print("skewed_features is : " + str(skewed_features))

        X_train, lmbda[country] = process.train_leo_johnson(X_train,
                                                            lmbda[country],
                                                            skewed_features)
        y_train, lmbda[country] = process.train_leo_johnson(y_train,
                                                            lmbda[country],
                                                            ['incidence'])

        # print("lamda is : " + str(lmbda[country]))
        print("y_train : " + str(y_train))
        means = {}
        std_deviations = {}
        process.train_std_normal(X_train, numerical_features, means,
                                 std_deviations)

        process.apply_leo_johnson(X_test, lmbda[country], skewed_features)
        process.apply_leo_johnson(y_test, lmbda[country], ['incidence'])

        process.apply_std_normal(X_test, numerical_features, means,
                                 std_deviations)

        print("X_train : " + str(X_train.shape))
        print("X_test : " + str(X_test.shape))

        # print("y_test : " + str(y_test))

        X_train['bias'] = 1
        X_test['bias'] = 1

        # save to file.
        test_data_path = path.parent / 'data' / 'test' / country

        x_train_file_path = test_data_path / 'X_train.csv'
        y_train_file_path = test_data_path / 'y_train.csv'
        x_test_file_path = test_data_path / 'X_test.csv'
        y_test_file_path = test_data_path / 'y_test.csv'

        X_train.to_csv(x_train_file_path, index=False)
        y_train.to_csv(y_train_file_path, index=False)
        X_test.to_csv(x_test_file_path, index=False)
        y_test.to_csv(y_test_file_path, index=False)

        print()
        print()


power_transform()
