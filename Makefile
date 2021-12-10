# tech salary predictor canada data pipe
# author: Sanchit Singh
# date: 2021-12-01

all: docs/_build/report.html

# download data
data/raw/survey_results_public.csv: src/download_data.py
	python src/download_data.py --url=https://info.stackoverflowsolutions.com/rs/719-EMH-566/images/stack-overflow-developer-survey-2019.zip --out_dir=data/raw

# pre-process data
data/processed/training.csv: src/preprocessing.R data/raw/survey_results_public.csv
	Rscript src/preprocessing.R --input=data/raw/survey_results_public.csv --out_dir=data/processed 

# run eda report
results/edu_plot.png: src/eda.py data/processed/training.csv
	python src/eda.py --train=data/processed/training.csv --out_dir=results/
results/role_plot.png: src/eda.py data/processed/training.csv
	python src/eda.py --train=data/processed/training.csv --out_dir=results/
results/language_plot.png: src/eda.py data/processed/training.csv
	python src/eda.py --train=data/processed/training.csv --out_dir=results/
results/code_years_plot.png: src/eda.py data/processed/training.csv
	python src/eda.py --train=data/processed/training.csv --out_dir=results/
results/salary_density_plot.png: src/eda.py data/processed/training.csv
	python src/eda.py --train=data/processed/training.csv --out_dir=results/
results/language_codeyears_plot.png: src/eda.py data/processed/training.csv
	python src/eda.py --train=data/processed/training.csv --out_dir=results/

# modelling
results/best_model_pipe.joblib: src/salary_prediction_model.py data/processed/training.csv data/processed/test.csv
	python src/salary_prediction_model.py --train=data/processed/training.csv --out_dir=results --test=data/processed/test.csv
results/test_result.joblib: src/salary_prediction_model.py data/processed/training.csv data/processed/test.csv
	python src/salary_prediction_model.py --train=data/processed/training.csv --out_dir=results --test=data/processed/test.csv
results/alpha-tuning.png: src/salary_prediction_model.py data/processed/training.csv data/processed/test.csv
	python src/salary_prediction_model.py --train=data/processed/training.csv --out_dir=results --test=data/processed/test.csv

# render report
docs/_build/report.html: docs/report.ipynb docs/references.bib results/best_model_pipe.joblib results/test_result.joblib results/alpha-tuning.png results/edu_plot.png results/role_plot.png results/language_plot.png results/code_years_plot.png results/salary_density_plot.png results/language_codeyears_plot.png
	jupyter-book build docs

clean: 
	rm -f data/raw/*
	rm -f data/processed/*
	rm -f results/*
	rm -rf docs/_build