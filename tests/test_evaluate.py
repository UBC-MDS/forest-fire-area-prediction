# author : Gautham Pughazhendhi
# date : 2021-12-08

import os
import sys
import pandas as pd

sys.path.append("src/")
from evaluate import *

RESULTS_PATH = "results/"
TEST_DATA_PATH = "data/processed/test_data.csv"

def test_load_model():
    """
    Tests whether the load_model function returns the model correctly
    """

    model = load_model(RESULTS_PATH)

    assert isinstance(model, Pipeline), "Cannot load model"

def test_read_data():
    """
    Tests whether the read_data function reads the test data correctly
    """

    X_test, y_test = read_data(TEST_DATA_PATH)

    assert isinstance(X_test, pd.DataFrame), "Cannot obtain features of test data"
    assert isinstance(y_test, pd.Series), "Cannot obtain the target of test data"

def test_evaluate_model():
    """
    Tests whether the evaluate_model function correctly outputs the results
    """

    model = load_model(RESULTS_PATH)
    X_test, y_test = read_data(TEST_DATA_PATH)
    predictions, results = evaluate_model(model, X_test, y_test)

    assert isinstance(results, pd.DataFrame), "Type of results object is wrong"
    assert results.shape == (1, 2), "Test result dataframe shape is wrong"
    assert predictions.shape == y_test.shape, "Prediction array shape is wrong"

def test_store_results():
    """
    Tests whether the test result is correctly stored as an image
    """

    assert os.path.isfile(RESULTS_PATH + "test_results.png"), "Test results image not created"