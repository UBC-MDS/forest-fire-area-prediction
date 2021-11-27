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
from preprocess_n_tune_model import root_mean_squared_error
from scipy.stats import loguniform
from statsmodels.stats.outliers_influence import OLSInfluence
from docopt import docopt


opt = docopt(__doc__)

def main():

    with open(opt["--test_data"], "rb") as f:
        test_df = pickle.load(f)

    with open(f"{opt['--results_path']}tuned_model.pickle", "rb") as f:
        model = pickle.load(f)

    X_test, y_test = test_df.drop("area", axis=1), test_df["area"]

    test_scores = {}

    predictions = model.predict(X_test)
    test_scores[f"SVR_Optimized_MAE"] = mean_absolute_error(y_test, predictions)
    test_scores[f"SVR_Optimized_RMSE"] = root_mean_squared_error(y_test, predictions)

    result_df = pd.DataFrame(test_scores, index=["Test Score"])
    dfi.export(result_df, f"{opt['--results_path']}test_results.png")
    
if __name__ == "__main__":
    main()