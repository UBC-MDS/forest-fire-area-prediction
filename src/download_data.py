# author : Hatef Rahmani
# date : 2021-11-19

""""Downloads data csv data from a url and save it to a local filepath as csv format"

Usage: download_data.py --url=<url> --out_file=<out_file>

Options:
--url=<url>             URL  where to download the data (must be in standard csv format)
--out_file=<out_file>   Path where to locally write the file
"""

import pandas as pd
import os
from docopt import docopt

opt = docopt(__doc__)

def main(url, out_file):
  data = pd.read_csv(url)
  try:
    data.to_csv(out_file, index = False)
  except:
     os.makedirs(os.path.dirname(out_file))
     data.to_csv(out_file, index = False)

if __name__ == "__main__":
  main(opt["--url"], opt["--out_file"])