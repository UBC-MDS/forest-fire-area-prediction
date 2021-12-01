# author: Gautham Pughazhendhi
# date: 2021-Nov-24

"""Reads in the train and test data, and outputs a tuned model and cross-validation results

Usage: evaluate.py --test_data=<test_data> --results_path=<results_path>
 
Options: 
--test_data=<test_data>          Testing data path
--results_path=<results_path>    Output path for test data evaluation results
"""

import pickle
import pandas as pd
import dataframe_image as dfi

from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_error
)
from sklearn.pipeline import make_pipeline, Pipeline
from preprocess_n_tune import root_mean_squared_error, read_data
from scipy.stats import loguniform
from statsmodels.stats.outliers_influence import OLSInfluence
from docopt import docopt


opt = docopt(__doc__)

def load_model(path_prefix):
    """
    Loads the model from the path prefix

    Parameters
    ----------
    path_prefix : str
        Path prefix of the model

    Returns
    ----------
        Pipeline: saved model
    """

    with open(f"{path_prefix}tuned_model.pickle", "rb") as f:
        model = pickle.load(f)
        
    return model

def evaluate_model(model, X_test, y_test):
    """
    Evaluates the best fit model on the test data

    Parameters
    ----------
    model: Pipeline
        the best fit model
    X_test : pandas DataFrame
        X in the test data
    y_test : numpy array
        y in the test data 

    Returns
    ----------
        DataFrame: best fi model's results on the test data
    """
    
    test_scores = {}

    predictions = model.predict(X_test)
    test_scores[f"SVR_Optimized_MAE"] = mean_absolute_error(y_test, predictions)
    test_scores[f"SVR_Optimized_RMSE"] = root_mean_squared_error(y_test, predictions)

    return pd.DataFrame(test_scores, index=["Test Score"])

def store_results(results, path_prefix):
    """
    Saves the test results as an image

    Parameters
    ----------
    results : DataFrame
        test results dataframe
    path_prefix: str
        output path prefix
    """
    
    dfi.export(results, f"{path_prefix}test_results.png")


def main(opt):
    
    model = load_model(opt["--results_path"])
    assert(isinstance(model, Pipeline))
    X_test, y_test = read_data(opt["--test_data"])
    assert(isinstance(X_test, pd.DataFrame))
    
    results = evaluate_model(model, X_test, y_test)
    assert(isinstance(results, pd.DataFrame))
    store_results(results, opt["--results_path"])
    
if __name__ == "__main__":
    main(opt)