# author : Gautham Pughazhendhi
# date : 2021-12-08

import os
import sys
import pandas as pd

sys.path.append("src/")
from preprocess_n_tune import *

RESULTS_PATH = "results/"
TRAIN_DATA_PATH = "data/processed/train_data.csv"

def test_read_data():
    """
    Tests whether the read_data function reads the train data correctly
    """

    X_train, y_train = read_data(TRAIN_DATA_PATH)

    assert isinstance(X_train, pd.DataFrame), "Cannot obtain features of train data"
    assert isinstance(y_train, pd.Series), "Cannot obtain the target of train data"

def test_create_column_transformer():
    """
    Tests whether the create_column_transformer function returns a ColumnTransformer
    """

    column_transformer = create_column_transformer()
    assert isinstance(column_transformer, ColumnTransformer), "Cannot create a column transformer"

def test_filter_outliers():
    """
    Tests whether the filter_outliers function filters the identified outliers in the train data
    """

    X_train, y_train = read_data(TRAIN_DATA_PATH)
    column_transformer = create_column_transformer()
    X_train_f, y_train_f = filter_outliers(X_train,
                                       y_train,
                                       column_transformer,
                                       RESULTS_PATH)
    assert X_train.shape[0] != X_train_f.shape[0], "Outlier rows not removed in features"
    assert y_train.shape[0] != y_train_f.shape[0], "Outlier rows not removed in target"

def test_create_scorers():
    """
    Tests whether the create_scorers functions returns the expected result
    """

    scorers = create_scorers()

    assert len(scorers) == 2, "The number of scorers created is not correct"
    assert isinstance(scorers, dict), "Scorers dict not created correctly"
    assert list(scorers.keys()) == ["mae", "rmse"], "Scorers dict keys not correct"

def test_cross_validate_n_tune():
    """
    Tests whether the cross_validate_n_tune returns the best fit model and CV results
    """

    X_train, y_train = read_data(TRAIN_DATA_PATH)
    column_transformer = create_column_transformer()
    X_train, y_train = filter_outliers(X_train,
                                       y_train,
                                       column_transformer,
                                       RESULTS_PATH)
    scorers = create_scorers()
    model, results = cross_validate_n_tune(X_train,
                                           y_train,
                                           column_transformer,
                                           scorers)
    assert isinstance(model, Pipeline), "Pipeline not created correctly"
    assert results.shape == (4, 4), "CV results dataframe not created correctly"

def test_store_model():
    """
    Tests whether the best fit model is stored in the results directory
    """

    assert os.path.isfile(RESULTS_PATH + "tuned_model.pickle"), "Model not stored"