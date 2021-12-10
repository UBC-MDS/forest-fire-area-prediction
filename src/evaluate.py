# author: Gautham Pughazhendhi
# date: 2021-Nov-24

"""Reads in the train and test data, and outputs a tuned model and cross-validation results

Usage: evaluate.py --test_data=<test_data> --results_path=<results_path>
 
Options: 
--test_data=<test_data>          Testing data path
--results_path=<results_path>    Output path for test data evaluation results
"""

import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import dataframe_image as dfi

from sklearn.metrics import mean_absolute_error
from sklearn.pipeline import Pipeline
from preprocess_n_tune import root_mean_squared_error, read_data
from docopt import docopt

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

    return predictions, pd.DataFrame(test_scores, index=["Test Score"])

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
    
    dfi.export(results, f"{path_prefix}test_results.png",table_conversion='matplotlib')
    

def plot_predictions(y_true, y_pred, path_prefix):
    """
    Saves the comparison plot of actual vs predicted values as an image

    Parameters
    ----------
    y_true : numpy array
        actual values
    y_pred : numpy array
        predicted values
    path_prefix: str
        output path prefix
    """
    
    plt.scatter(y_true, y_pred)
    plt.yscale('log')
    plt.xscale('log')

    p1 = max(max(y_pred), max(y_true))
    p2 = min(min(y_pred), min(y_true))
    plt.plot([p1, p2], [p1, p2], 'b-')
    plt.axis('equal')

    plt.xlabel("Log True Area(ha)")
    plt.ylabel("Log Predicted Area(ha)")
    plt.savefig(f"{path_prefix}predictions.png")


def main(opt):
    
    model = load_model(opt["--results_path"])
    X_test, y_test = read_data(opt["--test_data"])
    
    predictions, results = evaluate_model(model, X_test, y_test)
    assert(isinstance(results, pd.DataFrame))

    store_results(results, opt["--results_path"])
    plot_predictions(y_test, predictions, opt["--results_path"])
    
if __name__ == "__main__":
    opt = docopt(__doc__)
    main(opt)