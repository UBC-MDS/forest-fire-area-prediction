# author : Hatef Rahmani
# date : 2021-11-24

""""Reads in cleaned data, does the EDA, and outputs images for the report"

Usage: EDA.py --file_path=<file_path> --out_folder=<out_folder> 

Options:
--file_path=<file_path>             The path to read the cleaned/preprocessed data
--out_folder=<out_folder>           The folder name where locally save the plots
"""

import os
import numpy as np
import pandas as pd
import altair as alt
import pickle
from sklearn.model_selection import train_test_split
from docopt import docopt

opt = docopt(__doc__)

def main(file_path, out_folder):

    assert file_path.endswith(".csv"), "Input should be a .csv file as the <in_file>"
    
    cleaned_train_set = pd.read_csv(file_path)

    assert {'DC','DMC','FFMC','ISI','RH','X','Y','area','day','month','rain','season','temp',
    'wind'} == set(cleaned_train_set.columns), "Required columns are not available"

    day_plot = alt.Chart(cleaned_train_set).mark_boxplot(size = 15).encode(
      x = alt.X("area", 
              scale = alt.Scale(type = "sqrt"),
              title = "Burned area (ha)"),
      y = alt.Y("day", 
              sort = "x",
              title = "Day of Week"),
      color = alt.Color("day",
                      legend = None)
                      ).properties(
                        height = 250,
                        width = 450
                        )
    
    season_plot = alt.Chart(cleaned_train_set).mark_boxplot(size = 15).encode(
      x = alt.X("area", 
              scale = alt.Scale(type = "sqrt"),
              title = "Burned area (ha)"),
      y = alt.Y("season", 
              sort = "x",
              title = "Season"),
   #   color = alt.Color("day",
    #                  legend = None)
                    ).properties(
                        height = 250,
                        width = 450
                        )

    pair_plot = alt.Chart(cleaned_train_set).mark_circle().encode(
      x = alt.X(alt.repeat("row"), type = "quantitative"),
      y = alt.Y(alt.repeat("column"), type = "quantitative"),
      color = "season"
      ).properties(
        width = 110,
        height = 110
        ).repeat(
          column = ["FFMC", "DMC", "DC", "ISI", "temp", "RH", "wind", "rain"],
          row = ["FFMC", "DMC", "DC", "ISI", "temp", "RH", "wind", "rain"]
          ).configure_mark(
            opacity = 1
            ).interactive()
    
    # Outputing plots
    day_plot.save(f"{out_folder}/EDA_day_plot.png", scale_factor=5.0)
    season_plot.save(f"{out_folder}/EDA_season_plot.png", scale_factor=5.0)
    pair_plot.save(f"{out_folder}/EDA_pair_plot.png", scale_factor=5.0)


if __name__ == "__main__":
  main(opt["--file_path"], opt["--out_folder"])