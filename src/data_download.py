# author: Margot Vore
# date: Nov 19, 2021

""" This script reads in CSV from a given URL and saves it to your local machine.
Usage: python data_download.py <url> <path>    

Options:
<url>      Take the URL of the CSV you want to download
<path>     Takes the path where you want the data to be saved to
"""


from docopt import docopt
import pandas as pd

opt = docopt(__doc__)

def main(opt):
    df = pd.read_csv(opt["<url>"])
    df.to_csv(opt["<path>"])

if __name__ == "__main__":
    main(opt)
