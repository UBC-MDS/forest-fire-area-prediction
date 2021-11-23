# author: Margot Vore
# date: 2021-Nov-23

"""Reads in data the forest fire csv  file, preprocesses the data, and outputs the training and test datasets

Usage: preprocessing.py --file_path=<file_path> --test_data_file=<test_data_file> --training_data_file=<training_data_file> 
 
Options:
--file_path=<file_path>     The path to the forest fire dataset
--test_data_file=<test_data_file>   The file name of the created test data set
--training_data_file=<training_data_file>   The file name of the created training data set
"""

import os
import numpy as np
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from docopt import docopt

opt = docopt(__doc__)

def main(file_path,  test_data_file, training_data_file):
    ff_data = pd.read_csv(file_path)
    ff_data["area_log"] = round(np.log(ff_data.area + 1), 3)
    seasons = ["NONE"] * len(ff_data)

    for x in range(0, len(ff_data)):
        m = ff_data.loc[x, "month"]
        if m in ["dec, jan, feb"]:
            seasons[x] = "winter"
        elif m in ["mar", "apr", "may"]:
            seasons[x] = "spring"
        elif m in ["jun", "jul", "aug"]:
            seasons[x] = "summer"
        elif m in ["sep", "oct", "nov"]:
            seasons[x] = "fall"

    ff_data["seasons"] = seasons

    train_df, test_df = train_test_split(ff_data, test_size=0.2, random_state=123)

    with open('data/processed/%s.pickle'%(test_data_file), 'wb') as f:
        pickle.dump(test_df, f)
        
    with open('data/processed/%s.pickle'%(training_data_file), 'wb') as f:
        pickle.dump(train_df, f)


if __name__ == "__main__":
    main(opt["--file_path"], opt["--test_data_file"],opt["--training_data_file"])
