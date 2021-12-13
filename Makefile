# Margot Vore, Dec 1, 2021

# This make file runs the full analysis for 
# the forest fire size prediction process.

all: reports/forest_fire_analysis_report.md tests


# Inital cleaning of the data and split into train and test sets
data/processed/train_data.csv data/processed/test_data.csv: src/clean_n_split.py data/raw/forestfires.csv
	python src/clean_n_split.py --file_path=data/raw/forestfires.csv --test_data_file=test_data --train_data_file=train_data

# Creating EDA plots used in report
results/EDA_day_plot.png results/EDA_pair_plot.png results/EDA_season_plot.png: data/processed/train_data.csv
	 python src/EDA.py --file_path=data/processed/train_data.csv --out_folder=results

# Preprocessing, transforming features, and tuning model for analysis on training data
results/cv_results.png results/outlier_detection.png results/tuned_model.pickle : src/preprocess_n_tune.py data/processed/train_data.csv
	python src/preprocess_n_tune.py --train_data=data/processed/train_data.csv --results_path=results/

# Evaluates the best tuned model on test data
results/test_results.png results/predictions.png : src/evaluate.py results/tuned_model.pickle data/processed/test_data.csv
	python src/evaluate.py --test_data=data/processed/test_data.csv --results_path=results/

# Compile the results into a report
reports/forest_fire_analysis_report.md : results/EDA_day_plot.png results/EDA_pair_plot.png results/EDA_season_plot.png \
 										 results/cv_results.png results/outlier_detection.png results/test_results.png \
										 results/predictions.png reports/forest_fire_analysis_report.Rmd reports/report_sections/*
										
	Rscript -e "rmarkdown::render('reports/forest_fire_analysis_report.Rmd')"

# Test the functions and results
tests : tests/* src/clean_n_split.py src/download_data.py src/EDA.py src/evaluate.py src/preprocess_n_tune.py \
		data/processed/train_data.csv results/EDA_day_plot.png results/cv_results.png results/test_results.png
	pytest --disable-warnings tests/

clean: 
	rm -rf data/processed/*.csv results/* reports/forest_fire_analysis_report.md reports/forest_fire_analysis_report.html
