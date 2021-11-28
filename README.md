# Forest fire area prediction - Group 2  

In this project, we aim to predict the burned area of forest fires in the northeast region of Portugal, using meteorological and soil moisture data. Forest fires are major environmental concerns with the potential of endangering human lives (Cortez and Morais, 2007). Particularly, here in BC, millions of acres of forests are burned annually, damaging the environment and posing significant financial challenges. Being able to predict the size of burned area of future forest fires may help fire monitoring and fire mitigation efforts. 

We will be recreating a study performed in Cortez and Morais (2007), which looked at forest fire burn sizes in Montesinho natural park in northeast Portugal. This study provides us data that consists of meteorological observations (such as temperature, wind, relative humidity etc.), soil moisture indices, and locational data. The dataset contains 517 observations, with each row representing one fire monitoring instance, with the column area as our target (showing the burned area), and 12 other measurements and indexes as features (including `month`, `day`, `RH`, `rain`, `DC`, `ISI` etc.). 

To predict the size of wildfires, we will build a predictive regression model. First, we split our data set into train and test splits by 20:80 ratio. Our EDA analysis includes some preliminary information of the data set (such as type of features, value counts etc.) and plotting the dependent variables (area) as a function of predictors (features). We found that our target variable, `fire area` is highly skewed to small values so we will be using the log-transformed of the target variable to address this issue. We observe that one of the features (`day`) is not significantly impacting the output (the burned area is almost equally distributed across different days of the week), so we drop that feature but keep the rest. We also note that `month` (another feature) is unbalanced and we have fewer observations for some specific months. In order to avoid overfitting on this unbalanced feature, we define a new variable `season`, and plot the burned are versus this new variable. Surprisingly and contrary to our expectations, the summer fires are not significantly larger than other seasons. We also plot the size of the burned area as a function of spatial locations of the forest, where it shows that two particular locations with (X,Y)=(6,5) and (X,Y)=(8,6) have the largest burnt area. The pairplot between numerical variables shows that there are some outliers in the data that we have to be aware of when building the regression model. Finally, the correlation table (or heatmap) of all features shows that some features such as (`ISI` and `FFMC`), (`temp` and `FMC`), (`DC` and `DMC`) are quite associated with high correlation coefficients. On the other hand, some features such as (`DC` and `rain`), (`RH` and `DMC`) has almost zero correlation. 

Moving forward, we plan to explore several regression models such as SVM, k-NN, and linear regression to find the best-performing model. We use RMSE as a score metric and perform cross-validation with 20 folds to tune the hyperparameters. Once we find our best model, we evaluate that on the test set and report the scores and confusion matrix. In our final report, we will have a table of the training metrics from each model to highlight which performed best with our dataset. We will also have a line plot showing the predicted burned area from our best model versus the real burned area to highlight how well our model performs. The final report will also include a comparison between our findings and those reported in Cortex and Morais (2007). They highlight the performance of different models and it will be interesting to see if we find similar results.


**References:**  
P. Cortez and A. Morais. A Data Mining Approach to Predict Forest Fires using Meteorological Data. In J. Neves, M. F. Santos and J. Machado Eds., New Trends in Artificial Intelligence, Proceedings of the 13th EPIA 2007 - Portuguese Conference on Artificial Intelligence.

Data is publically avaliable at https://archive.ics.uci.edu/ml/datasets/Forest+Fires.



## Usage
To replicate our analysis install the dependenciese that are listed below and run the following commands in order in your terminal from the root directory of the project:

```
#Cleaning and splitting
python src/clean_n_split.py --file_path = data/raw/forestfires.csv --test_data_file = test_data --train_data_file= train_data

#EDA plots
python src/EDA.py --file_path="data/processed/train_data.csv" --out_folder=reports

#Preprocess, Cross-validate, and Tune model
python src/preprocess_n_tune_model.py --train_data=data/processed/<filename>.csv --results_path=results/

#Evaluate model
python src/evaluate.py --test_data=data/processed/<filename>.csv --results_path=results/

# render final report
Rscript -e "rmarkdown::render('doc/Final_report.Rmd', output_format = 'github_document')"

```

