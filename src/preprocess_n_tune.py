# author: Gautham Pughazhendhi
# date: 2021-Nov-24

"""Reads in the train and test data, and outputs a tuned model and cross-validation results

Usage: preprocess_n_tune.py --train_data=<train_data> --results_path=<results_path>
 
Options: 
--train_data=<train_data>        Training data path 
--results_path=<results_path>    Output path for tuned  model and CV results
"""

import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import dataframe_image as dfi

from sklearn.compose import (
    make_column_transformer, ColumnTransformer
)
from sklearn.svm import SVR
from sklearn.metrics import (
    make_scorer,
    mean_squared_error,
    mean_absolute_error
)
from sklearn.model_selection import (
    RandomizedSearchCV,
    cross_validate,
)
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.preprocessing import (
    OneHotEncoder,
    StandardScaler
)
from scipy.stats import loguniform
from statsmodels.stats.outliers_influence import OLSInfluence
from docopt import docopt

# Attribution: adopted from 573 course material
def mean_std_cross_val_scores(model, X_train, y_train, **kwargs):
    """
    Returns mean and std of cross validation

    Parameters
    ----------
    model :
        scikit-learn model
    X_train : numpy array or pandas DataFrame
        X in the training data
    y_train :
        y in the training data

    Returns
    ----------
        Series: pandas Series with mean scores from cross_validation
    """

    scores = cross_validate(model, X_train, y_train, **kwargs)

    mean_scores = pd.DataFrame(scores).mean()
    std_scores = pd.DataFrame(scores).std()
    out_col = []

    for i in range(len(mean_scores)):
        out_col.append((f"%0.3f (+/- %0.3f)" % (mean_scores[i], std_scores[i])))

    return pd.Series(data=out_col, index=mean_scores.index)


def root_mean_squared_error(y_true, y_pred, **kwargs): 
    """
    Returns root mean squared error of the predictions

    Parameters
    ----------
    y_true : numpy array
        y in the test data
    y_pred :
        predictions for y_true

    Returns
    ----------
        ndarray: root mean squared error of the predictions
    """

    return np.sqrt(mean_squared_error(y_true, y_pred, **kwargs))


def read_data(path):
    """
    Reads and returns the data from path

    Parameters
    ----------
    path : str
        Path of the data

    Returns
    ----------
        tuple: pandas DataFrame of the data split by predictors and target
    """
    
    df = pd.read_csv(path)

    return df.drop("area", axis=1), df["area"]

def create_column_transformer():
    """
    Creates a column transformer object
    
    Returns
    ----------
        ColumnTransformer: a column transformer object for the pipeline
    """
    
    numeric = ['FFMC','DMC', 'DC', 'ISI', 'temp', 'RH','wind']
    categorical = ["X", "Y", "season"]
    drop = ["rain", "day", "month"]

    column_transformer = make_column_transformer(
        (StandardScaler(), numeric),
        (OneHotEncoder(sparse=False, handle_unknown="ignore"), categorical),
        ("drop", drop)
    )
    
    return column_transformer


def filter_outliers(X_train, y_train, column_transformer, plot_path_prefix):
    """
    Detects outliers and filters it from the data

    Parameters
    ----------
    X_train : numpy array or pandas DataFrame
        X in the training data
    y_train : numpy array
        y in the training data
    column_transformer: ColumnTransformer
        ColumnTransformer object for the pipeline
    plot_path_prefix: str
        output path prefix for the plot

    Returns
    ----------
        tuple: filtered X_train and y_train
    """
    
    filtered_X_train = X_train[y_train > 0]
    filtered_y_train = y_train[y_train > 0]
    transformed = column_transformer.fit_transform(filtered_X_train)

    preprocessed_X_train = pd.DataFrame(transformed,
                                        index=filtered_X_train.index)
    preprocessed_X_train = sm.add_constant(preprocessed_X_train)

    model = sm.OLS(filtered_y_train, preprocessed_X_train)
    model = model.fit()

    cooks_distance = OLSInfluence(model).cooks_distance

    plt.scatter(preprocessed_X_train.index, cooks_distance[0])
    plt.axhline(y=4 / filtered_X_train.shape[0], color="r", linestyle="-")
    plt.xlabel("Training data index")
    plt.ylabel("Cook's distance")
    plt.savefig(f"{plot_path_prefix}outlier_detection.png")

    outliers = pd.DataFrame(cooks_distance[0], index=filtered_X_train.index)
    outliers_index = outliers[outliers[0] > 4 / filtered_X_train.shape[0]].index

    X_train, y_train = X_train.drop(outliers_index), y_train.drop(outliers_index)
    
    return X_train, y_train

def create_scorers():
    """
    Creates scorers for the cross_validation
    
    Returns
    ----------
        dict: dictionary of scorers
    """
    
    mae_scorer = make_scorer(mean_absolute_error)
    rmse_scorer = make_scorer(root_mean_squared_error)

    return {
        "mae": mae_scorer,
        "rmse": rmse_scorer
    }

def cross_validate_n_tune(X_train, y_train, column_transformer, scorers):
    """
    Cross-validates and tunes a model for the data

    Parameters
    ----------
    X_train : numpy array or pandas DataFrame
        X in the training data
    y_train : numpy array
        y in the training data
    column_transformer: ColumnTransformer
        ColumnTransformer object for the pipeline
    scorers: dict
        dictionary of scorers

    Returns
    ----------
        tuple: best fit model, results dataframe
    """
    
    results= {}
    cv = 10
    
    svr_pipe = make_pipeline(
        column_transformer,
        SVR()
    )

    for name, scorer in scorers.items():
        results[f"SVR_{name.upper()}"] = mean_std_cross_val_scores(
            svr_pipe,
            X_train,
            y_train,
            cv=cv,
            scoring=scorer,
            return_train_score=True,
        )

    params = {
        "svr__C": loguniform(0.9, 2),
        "svr__gamma": loguniform(0.01, 1)
    }

    random_search = RandomizedSearchCV(
        svr_pipe,
        params,
        cv=cv,
        n_jobs=-1,
        n_iter=50,
        random_state=123,
        scoring=scorers["mae"]
    )

    random_search.fit(X_train, y_train)

    for name, scorer in scorers.items():

        results[f"SVR_Optimized_{name.upper()}"] = mean_std_cross_val_scores(
            random_search,
            X_train,
            y_train,
            cv=cv,
            scoring=scorer,
            return_train_score=True
        )
        
    return random_search.best_estimator_, pd.DataFrame(results)

def store_model_n_results(model, results, path_prefix):
    """
    Saves the model and results as an image

    Parameters
    ----------
    model : Pipeline
        the best fit model
    results : DataFrame
        CV results dataframe
    path_prefix: str
        output path prefix
    """
    
    with open(f"{path_prefix}tuned_model.pickle", "wb") as f:
        pickle.dump(model, f)
        
    dfi.export(results, f"{path_prefix}cv_results.png", table_conversion='matplotlib')

def main(opt):
    
    X_train, y_train = read_data(opt["--train_data"])
    column_transformer = create_column_transformer()
    X_train, y_train = filter_outliers(X_train,
                                       y_train,
                                       column_transformer,
                                       opt['--results_path'])
    scorers = create_scorers()
    model, results = cross_validate_n_tune(X_train,
                                           y_train,
                                           column_transformer,
                                           scorers)
    store_model_n_results(model, results, opt['--results_path'])

if __name__ == "__main__":
    opt = docopt(__doc__)
    main(opt)
