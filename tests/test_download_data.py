# author : Gautham Pughazhendhi
# date : 2021-12-08

import pandas as pd

def test_download_data():
    """
    Tests whether the raw data is correctly downloaded
    """

    path = "data/raw/forestfires.csv"

    try:
        data = pd.read_csv(path)
    except:
        assert False, "Cannot read the raw data file"

    assert isinstance(data, pd.DataFrame), "Data file cannot be converted into a dataframe"