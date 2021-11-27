# author: Khalid Abdilahi
# date: 2021-11-28

"""Builds multiple regression model to predict salary based on features

Usage: src/salary_prediction_model.py --train=<train> --out_dir=<out_dir>
  
Options:
--train=<train>     Path (including filename) to training data (which needs to be saved as a csv file)
--out_dir=<out_dir> Path to directory where the serialized model should be written

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
train = "data/preprocessed/training.csv"
out_dir = "results"

def main(train, out_dir):

#     try:
        train_df = pd.read_csv(train)
        build_model(train_df, out_dir)
#     except:
#         print("A problem ocurred when building the model")
#         print(e)

def build_model(train_df, out_dir):
    X_train = train_df.drop(columns=["ConvertedComp"])
    y_train = train_df["ConvertedComp"]
    results = {}
    numeric_features = ["YearsCodePro"]
    categorical_features = ["DevType", "EdLevel", "LanguageWorkedWith"]

    print("Creating column transformer")
    numeric_transformer = make_pipeline(SimpleImputer(), StandardScaler())
    categorical_transformer = make_pipeline(SimpleImputer(strategy="constant", fill_value="missing"),
                                           OneHotEncoder(sparse=False, handle_unknown="ignore"))

    preprocessor = make_column_transformer(
        (numeric_transformer, numeric_features),
        (categorical_transformer, categorical_features)
    )

    pipe = make_pipeline(preprocessor, DummyRegressor())
    results["Dummy"] = mean_std_cross_val_scores(pipe, X_train, y_train, cv=5,
                                                 return_train_score=True)

    # Carry out hyper-parameter tuning
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

    best_model = random_search.best_estimator_

    print(f"Saving best model to {out_dir}")
    dump(best_model, f'{out_dir}/best_model_pipe.joblib')

# Code snippet copied from https://gist.github.com/jlln/338b4b0b55bd6984f883
def splitDataFrameList(df, target_column, separator):
    ''' df = dataframe to split,
    target_column = the column containing the values to split
    separator = the symbol used to perform the split
    returns: a dataframe with each entry for the target column separated, with each element moved into a new row. 
    The values in the other columns are duplicated across the newly divided rows.
    '''
    def splitListToRows(row,row_accumulator, target_column, separator):
        split_row = row[target_column].split(separator)
        for s in split_row:
            new_row = row.to_dict()
            new_row[target_column] = s
            row_accumulator.append(new_row)
    new_rows = []
    df.apply(splitListToRows,axis=1,args = (new_rows,target_column,separator))
    new_df = pd.DataFrame(new_rows)
    return new_df

# Code copied from 573 lecture notes
def mean_std_cross_val_scores(model, X_train, y_train, **kwargs):
    """
    Returns mean and std of cross validation

    Parameters
    ----------
    model :
        scikit-learn model
    X_train : numpy array or pandas DataFrame
        X in the training data
    y_train :
        y in the training data

    Returns
    ----------
        pandas Series with mean scores from cross_validation
    """

    scores = cross_validate(model, X_train, y_train, **kwargs)

    mean_scores = pd.DataFrame(scores).mean()
    std_scores = pd.DataFrame(scores).std()
    out_col = []

    for i in range(len(mean_scores)):
        out_col.append((f"%0.3f (+/- %0.3f)" % (mean_scores[i], std_scores[i])))

    return pd.Series(data=out_col, index=mean_scores.index)


if __name__ == "__main__":
    main(opt["--train"], opt["--out_dir"])
