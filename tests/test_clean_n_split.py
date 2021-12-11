# author : Gautham Pughazhendhi
# date : 2021-12-08

import os
import sys
import pandas as pd

sys.path.append("src/")
from clean_n_split import get_seasons

def test_get_seasons():
    """
    Tests whether the derived column seasons is created and added correctly
    """

    path = "data/processed"

    ff_data = pd.read_csv("data/raw/forestfires.csv")
    seasons = get_seasons(ff_data)
    ff_data["season"] = seasons

    assert \
        (len(ff_data.loc[ff_data.season == 'fall']) ==
         len(ff_data.loc[
            (ff_data.month =='sep') | 
            (ff_data.month =='oct') |
            (ff_data.month =='nov')
            ])), \
        "Seasons data not created correctly"

    assert os.path.isfile(path + "/train_data.csv"), "Training data not found"
    assert os.path.isfile(path + "/test_data.csv"), "Testing data not found"
    