# author: Khalid Abdilahi
# date: 2021-11-28

"""Builds multiple regression model to predict salary based on features

Usage: src/salary_prediction_model.py --train=<train> --out_dir=<out_dir> --test=<test>
  
Options:
--train=<train>     Path (including filename) to training data (which needs to be saved as a csv file)
--out_dir=<out_dir> Path to directory where the serialized model should be written
[--test=<test>]     Path (including filename) to test data (which needs to be saved as a csv file)
"""

import os
import sys
from hashlib import sha1

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import datasets
from sklearn.compose import ColumnTransformer, make_column_transformer
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    make_scorer,
    precision_score,
    recall_score,
    average_precision_score, 
    auc
)
from sklearn.model_selection import (
    GridSearchCV,
    RandomizedSearchCV,
    cross_val_score,
    cross_validate,
    train_test_split,
)
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler
from sklearn.svm import SVC, SVR
from sklearn.impute import SimpleImputer
from sklearn.metrics import ConfusionMatrixDisplay
from scipy.stats import expon, lognorm, loguniform, randint, uniform
from sklearn.metrics import PrecisionRecallDisplay, RocCurveDisplay
import altair as alt
from joblib import dump, load

from docopt import docopt
import zipfile
import requests
from io import BytesIO

opt = docopt(__doc__)
train = "data/processed/training.csv"
test = "data/processed/test.csv"
out_dir = "results"

def main(train, out_dir, test=None):
    train_df = pd.read_csv(train)
    if test:
        test_df = pd.read_csv(test)
    else:
        test_df = None
    build_model(train_df, out_dir, test_df)

"""
    Build a regression model to predict salaries

    Parameters
    ----------
    train_df : dataframe
       the training set as a dataframe
    out_dir: str
        the directory in which the results will be saved
    test_df: dataframe
        the testing data that the final selected model will be tested on

"""
def build_model(train_df, out_dir, test_df=None):
    X_train = train_df.drop(columns=["ConvertedComp"])
    y_train = train_df["ConvertedComp"]
    results = {}
    numeric_features = ["YearsCodePro"]
    categorical_features = ["DevType", "EdLevel", "LanguageWorkedWith"]

    numeric_transformer = make_pipeline(SimpleImputer(), StandardScaler())
    categorical_transformer = make_pipeline(SimpleImputer(strategy="constant", fill_value="missing"),
                                           OneHotEncoder(sparse=False, handle_unknown="ignore"))

    preprocessor = make_column_transformer(
        (numeric_transformer, numeric_features),
        (categorical_transformer, categorical_features)
    )

    # Carry out hyper-parameter tuning
    print("Carrying out hyper-parameter tuning")
    pipe = make_pipeline(preprocessor, Ridge())

    param_grid = {
        "ridge__alpha": np.logspace(-3, 5)
    }

    random_search = RandomizedSearchCV(
        pipe,
        param_distributions=param_grid,
        n_jobs=-1,
        n_iter=50,
        cv=5,
        random_state=123,
        return_train_score=True
    )
    random_search.fit(X_train, y_train)

    # Create hyper-parameter tuning plot and save
    cv_df = pd.DataFrame(random_search.cv_results_)[["param_ridge__alpha", 
                                                     "mean_test_score", "mean_train_score"]]
    cv_df.set_index("param_ridge__alpha").plot(logx=True)
    plt.title('Train score and test score as alpha parameter increases')
    plt.xlabel("Alpha")
    plt.ylabel("Score")
    plt.savefig(f"{out_dir}/alpha-tuning.png")

    best_model = random_search

    print(f"Saving best model to {out_dir}")
    dump(best_model, f'{out_dir}/best_model_pipe.joblib')

    # for test data set
    if len(test_df) > 0:
        X_test = test_df.drop(columns=["ConvertedComp"])
        y_test = test_df["ConvertedComp"]
        r_test = random_search.score(X_test, y_test)
        y_predict = random_search.predict(X_test)

        dummy_result = {}
        dummy_result["r_sq_test"] = r_test
        dummy_result["predict_y"] = y_predict
        print(f"Saving test result to {out_dir}")
        dump(dummy_result, f'{out_dir}/test_result.joblib')

    print("Done")


if __name__ == "__main__":
    main(opt["--train"], opt["--out_dir"], opt["--test"])
