# author: Margot Vore
# date: 2021-Nov-23

"""Reads in data the forest fire csv file, preprocesses the data, and outputs the training and test datasets

Usage: clean_n_split.py --file_path=<file_path> --test_data_file=<test_data_file> --train_data_file=<train_data_file> 
 
Options:
--file_path=<file_path>     The path to the forest fire dataset 
--test_data_file=<test_data_file>   The file name of the created test data set 
--train_data_file=<train_data_file>   The file name of the created training data set
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from docopt import docopt

def get_seasons(df):
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
    return seasons
    
def main(file_path,  test_data_file, train_data_file):
    ff_data = pd.read_csv(file_path)

    s = get_seasons(ff_data)

    ff_data["season"] = s

    train_df, test_df = train_test_split(ff_data, test_size=0.2, random_state=123)
     
    test_df.to_csv('data/processed/%s.csv'%(test_data_file),index=False)
    train_df.to_csv('data/processed/%s.csv'%(train_data_file), index=False)


if __name__ == "__main__":
    opt = docopt(__doc__)
    main(opt["--file_path"], opt["--test_data_file"],opt["--train_data_file"])
