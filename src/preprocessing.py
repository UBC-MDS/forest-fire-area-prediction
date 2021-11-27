# author: Margot Vore
# date: 2021-Nov-23

"""Reads in data the forest fire csv file, preprocesses the data, and outputs the training and test datasets

Usage: preprocessing.py --file_path=<file_path> --test_data_file=<test_data_file> --train_data_file=<train_data_file> 
 
Options:
--file_path=<file_path>     The path to the forest fire dataset 
--test_data_file=<test_data_file>   The file name of the created test data set 
--train_data_file=<train_data_file>   The file name of the created training data set
"""

import os
import numpy as np
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from docopt import docopt

opt = docopt(__doc__)

def  seasons(df):
    """
    Changes months into season

    Parameters
    ----------
    df : dataframe
        the forest fire dataframe 

    Returns
    -------
    Array
       Seasons the months are associated with
    """


    seasons = ["NONE"] * len(df)
    for x in range(0, len(df)):
        m = df.loc[x, "month"]
        if m in ["dec", "jan", "feb"]:
            seasons[x] = "winter"
        elif m in ["mar", "apr", "may"]:
            seasons[x] = "spring"
        elif m in ["jun", "jul", "aug"]:
            seasons[x] = "summer"
        elif m in ["sep", "oct", "nov"]:
            seasons[x] = "fall"
    return (seasons)
    
def main(file_path,  test_data_file, train_data_file):
    ff_data = pd.read_csv(
        "C:/Users/margo.DESKTOP-T66VM01/Desktop/UBC_Program/522_workflows/forest-fire-area-prediction-group-2/data/raw/forestfires.csv"
        )
    s = seasons(ff_data)

    ff_data["season"] = s

    ff_data["fire"] = 0
    ff_data["rain_cat"] = 0

    ff_data.loc[ff_data.area > 0, "fire"] = 1
    ff_data.loc[ff_data.rain > 0, "rain_cat"] = 1

    ff_data = ff_data.drop("area", axis =1 )
    ff_data

    train_df, test_df = train_test_split(ff_data, test_size=0.2, random_state=123)


    with open('data/processed/%s.pickle'%(test_data_file), 'wb') as f:
        pickle.dump(test_df, f)
        
    with open('data/processed/%s.pickle'%(train_data_file), 'wb') as f:
        pickle.dump(train_df, f)


if __name__ == "__main__":
    main(opt["--file_path"], opt["--test_data_file"],opt["--train_data_file"])
