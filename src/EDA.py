# author : Hatef Rahmani
# date : 2021-11-24

""""Reads in cleaned data, does the EDA, and outputs images for the report"

Usage: EDA.py --file_path=<file_path> --season_plot=<season_plot> --pair_plot=<pair_plot>

Options:
--file_path=<file_path>             The path to read the cleaned/preprocessed data
--season_plot=<season_plot>         The path to where it locally saves the season plot
--pair_plot=<pair_plot>             The path to where it locally saves the pair plot of all numeric values
"""

import os
import numpy as np
import pandas as pd
import altair as alt
import pickle
from sklearn.model_selection import train_test_split
from docopt import docopt

opt = docopt(__doc__)

def main(file_path, season_plot, pair_plot):
    with open(file_path, 'rb') as f:
      cleaned_train_set = pickle.load(f)

    plot_1 = alt.Chart(cleaned_train_set).mark_bar(size = 15).encode(
    x = alt.X("season", 
              scale = alt.Scale(type = "sqrt"),
              title = "Season"),
    y = alt.Y("count()", stack=False,
              title = "Count")
              ).properties(
                height = 250,
                width = 450
                ).facet('fire') 
    
    plot_1.save(season_plot, scale_factor = 3)

    plot_2 = alt.Chart(cleaned_train_set).mark_circle().encode(
      x = alt.X(alt.repeat("row"), type = "quantitative"),
      y = alt.Y(alt.repeat("column"), type = "quantitative"),
      color = "fire"
      ).properties(
        width = 110,
        height = 110
        ).repeat(
          column = ["FFMC", "DMC", "DC", "ISI", "temp", "RH", "wind", "rain"],
          row = ["FFMC", "DMC", "DC", "ISI", "temp", "RH", "wind", "rain"]
          ).configure_mark(
            opacity = 1
            ).interactive()
  
    plot_2.save(pair_plot, scale_factor = 3)


if __name__ == "__main__":
  main(opt["--file_path"], opt["--season_plot"],opt["--pair_plot"])