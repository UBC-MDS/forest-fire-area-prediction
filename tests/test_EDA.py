# author : Gautham Pughazhendhi
# date : 2021-12-08

import os

def test_eda():
    """
    Tests whether the EDA plots are created successfully
    """

    files = [
        "EDA_day_plot.png",
        "EDA_season_plot.png",
        "EDA_pair_plot.png"
    ]

    for file in files:
        assert os.path.isfile(f"results/{file}"), f"EDA output {file} is missing"
