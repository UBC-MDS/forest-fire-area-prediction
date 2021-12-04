# Forest Fire Area Prediction

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Research Question:** Can we accurately predict the size of a forest fire based on meteorological and soil moisture records?

In this project, we aim to predict the burned area of forest fires in the northeast region of Portugal. Forest fires are major environmental concerns with the potential of endangering human lives (Cortez and Morais, 2007). Here in BC, millions of acres of forests burn annually, damaging large swaths of forest and posing significant financial challenges. Being able to predict the size of the burned area of forest fires may significantly impact fire management and mitigation efforts.

### Data Set

We are basing our work on a study performed by Cortez and Morais (2007), which looks at forest fire burn sizes in Montesinho natural park in northeast Portugal. This study provides us data that consists of meteorological observations (such as temperature, wind, relative humidity etc.), soil moisture indices, and spatial data. The data set contains 517 observations with no missing data, where each row represents one fire monitoring instance. The column `area` is our target value containing the burned area and the other 12 measurements and indexes will be the features.

### EDA

Our EDA analysis includes preliminary information of the test data set (such as type of features, value counts etc.) and plots depicting the dependent variables (area) as a function of potential predicting features. From the EDA analysis, we found that our target variable, `fire area` is highly skewed to small values. We observe that the feature `day` is not significantly impacting the output as the burned area is equally distributed across different days of the week, thus we drop that feature from the analysis. We also note that the `month` feature is unbalanced with fewer observations for some specific months. In order to avoid overfitting on this unbalanced feature, we define a new variable `season`, and plot the burned are versus this new variable. Surprisingly and contrary to our expectations, the summer fires are not significantly larger than other seasons. We also plot the size of the burned area as a function of spatial locations of the forest, which shows that two particular locations with (`X`,`Y`)=(6,5) and (`X`,`Y`)=(8,6) have the largest burnt area. The pair plot between numerical variables shows that there are some outliers in the data that we have to be aware of when building the regression model. Finally, the correlation table (i.e. heatmap) of all features shows that some features such as \[`ISI` and `FFMC`\], \[`temp` and `FMC`\], \[`DC` and `DMC`\] are associated with high correlation coefficients. On the other hand, some features such as \[`DC` and `rain`\], \[`RH` and `DMC`\] has close to zero correlation.

### Analysis

To predict the size of wildfires, we are building a predictive regression model. First, we split our data set into train and test splits with an 80:20 ratio. Then, we use Cook’s Distance method with a threshold of 4/n to detect and remove outliers from the data set. We explore several regression models such as SVM, k-NN, and linear regression to find the best-performing model. We use MAE and RMSE as the scoring metrics and perform cross-validation with 10 folds to tune the hyperparameters. Once our best model is found, we will evaluate it on the test set and report the scores. Our final report will contain a table of error metrics for the selected model as well as a plot showing the predicted burned areas from our best model versus the observed burned areas to highlight the model's performance on unseen test data.

------------------------------------------------------------------------

## Report

The final report can be found [here](https://github.com/UBC-MDS/forest-fire-area-prediction-group-2/blob/dev/reports/forest_fire_analysis_report.md).

## Usage

**WINDOWS USERS:** The current workflow might not work on Windows due to a dependency support issue not in our control. This will be resolved in the next milestone with Docker containers.

To replicate our analysis install the dependencies that are listed below. Alternatively, you can create and activate a conda environment with all the dependencies using the following `conda` command.

``` bash
conda env create -f environment.yml
conda activate ffa_prediction
```

-   Run the following commands in order in your terminal from the root directory of the project.

``` bash
# Clean and Split Data
python src/clean_n_split.py --file_path=data/raw/forestfires.csv --test_data_file=test_data --train_data_file=train_data

# Exploratory Data Analysis
python src/EDA.py --file_path=data/processed/train_data.csv --out_folder=results

# Preprocess, Cross-validate, and Tune Model
python src/preprocess_n_tune.py --train_data=data/processed/train_data.csv --results_path=results/

# Evaluate Model
python src/evaluate.py --test_data=data/processed/test_data.csv --results_path=results/

# Render Final Report
Rscript -e "rmarkdown::render('reports/Final_report.Rmd', output_format = 'github_document')"
```

**Dependencies**

Python:

      - pandas[version='>=1.3.*']
      - altair_viewer
      - requests[version='>=2.24.0']
      - matplotlib[version='>=3.2.2']
      - python-graphviz
      - altair
      - jinja2
      - graphviz
      - scikit-learn[version='>=1.0']
      - ipykernel
      - altair_saver
      - pip
      - docopt
      - dataframe_image
      - statsmodels

R:

      - knitr==1.26
      - tidyverse==1.2.1
      - caret==6.0-84
      - ggthemes==4.2.0

## References

P. Cortez and A. Morais. A Data Mining Approach to Predict Forest Fires using Meteorological Data. In J. Neves, M. F. Santos and J. Machado Eds., New Trends in Artificial Intelligence, Proceedings of the 13th EPIA 2007 - Portuguese Conference on Artificial Intelligence.

Data is publicly available at <https://archive.ics.uci.edu/ml/datasets/Forest+Fires>.
