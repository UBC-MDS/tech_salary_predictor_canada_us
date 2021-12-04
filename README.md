
# Salary predictor for tech employees in Canada

### Authors

-   Jiwei Hu
-   Sanchit Singh
-   Khalid Abdilahi
-   Vera Cui

Demo of a data analysis project for DSCI 522 (Data Science workflows); a
course in the Master of Data Science program at the University of
British Columbia.

### About

The aim of this project is to allow tech employees in Canada to get a
reasonable estimation of how much they will potentially earn given their
skill set and years of experience. Fresh graduates and seasoned
employees would benefit from an analysis tool that allows them to
predict their earning potential. While the Human Resources (HR)
department of companies has access to this market information, tech
employees are mostly clueless about what their market value is.
Therefore, a salary predictor tool could assist them in the negotiation
process.

Using the [Stack Overflow Annual Developer
Survey](https://insights.stackoverflow.com/survey) (Overflow 2021) data,
we did Exploratory Data analysis (EDA) and came up with some features
that we think help predict the expected yearly compensation of tech
employees. We describe the data, selected features, and the modeling
process which you should be able to reproduce following the usage steps.

### Data

The data set used in this project is from the [Stack Overflow Annual
Developer Survey](https://insights.stackoverflow.com/survey), which is
conducted annually. The survey data set has nearly 80,000 responses.
Several useful features could be extracted from this survey such as
education level, location, the language used, job type, all of which are
potentially associated with annual compensation.

### Usage

### Dependencies

The R dependencies are listed below:

-   R version 3.6.1 and R packages:
    -   tidyverse==1.3.1
    -   caret==6.0.90
    -   docopt==0.7.1
    -   testthat=3.0.4

The Python dependencies can be found in the tech_salary_pred_env.yaml
file. However, you don’t have to manually install these dependencies.
You need to install conda (v4.10.3) and then follow the installation
instructions described below.

Suggested way to download data:

1.  Clone this Github repository
2.  Go to [Stack Overflow Annual Developer
    Survey](https://insights.stackoverflow.com/survey)
3.  Copy the link of the csv file, taking 2019 result as an example:
    <https://info.stackoverflowsolutions.com/rs/719-EMH-566/images/stack-overflow-developer-survey-2019.zip>
4.  Run the following command at the terminal from the root directory of
    this project:

#### Option 1 - Using makefile

To replicate the analysis, clone this GitHub repository, install the
dependencies listed above, and run the following command at the command
line/terminal from the root directory of this project:

    make all

To reset the repo to a clean state, with no intermediate or results
files, run the following command at the command line/terminal from the
root directory of this project:

    make clean

#### Option 2 - Executing the scripts individually

    # create conda environment
    conda env create -f tech_salary_pred_env.yaml
    conda activate tech_salary_pred_env

    # download data
    python src/download_data.py --url=https://info.stackoverflowsolutions.com/rs/719-EMH-566/images/stack-overflow-developer-survey-2019.zip --out_dir=data/raw

    # pre-process data
    Rscript src/preprocessing.R --input=data/raw/survey_results_public.csv --out_dir=data/processed

    # run eda report
    python src/eda.py --train=data/processed/training.csv --out_dir=results/

    # modelling
    python src/salary_prediction_model.py --train=data/processed/training.csv --out_dir=results --test=data/processed/test.csv

    # render report
    jupyter-book build docs

### Report

The final report can be found
[here](https://github.com/UBC-MDS/tech_salary_predictor_canada_us/tree/main/docs/index.html)

### Exploratory data analysis

After carrying out EDA, we realize that the following features might
help us predict the salary of tech workers: years of experience,
education level, programming languages used, and their role (full-stack
developer, front-end developer, etc.)

Based on the data corresponding to the four features in the survey, we
created plots to visualize how the four features impact on the annual
compensation of developers. As we can see from the plots, a large
professional coding years and certain programming language
skills(Bash,C,SQL,HTML,Java) would have positive influence on the
average annual compensation. Then we dig a little deeper by visualizing
the combination of these two features in a heatmap, which shows the
average annual compensation given the number of professional coding
years and combination of programming language skills.

### Modelling

We built a multiple linear regression model to see the relationship
between these features and the annual compensation. To simplify our
analysis, we focused on Canada. We initially thought of building the
model on Canada and USA data. However, we learned from our EDA that
there is pay disparity and currency conversion involved. In the future,
we plan to include USA in the model and handle those discrepancies.

Additionally, the regression model can also provide other important
information such as the weight of each feature or how much each of those
features we picked contributes to the overall predicted annual
compensation.

To evaluate our model and selected features, we plan to use R squared
score as the score metric and see how well the tuned model can
generalize on the test data. For the purpose of visualizing the
performance of our prediction, we will plot the regression line on the
scattered data points to infer whether the relationship between features
and response is linear or not.

The research question is: \> To predict the expected salary of a tech
employee in Canada given their number of years of experience, education
level, programming languages used, and role

This topic is a predictive question, also extending to the following
sub-questions: 1. Which features have a significant statistical effect
on the response (inference)? 2. Whether the model is robust (model
estimation, a predictive problem) 3. The confidence interval of
predictions (predictive)

### LICENSE

This database - The Public 2019 Stack Overflow Developer Survey Results
- is made available under the Open Database License (ODbL):
<http://opendatacommons.org/licenses/odbl/1.0/>. Any rights in
individual contents of the database are licensed under the Database
Contents License: <http://opendatacommons.org/licenses/dbcl/1.0/>

# References

<div id="refs" class="references csl-bib-body hanging-indent">

<div id="ref-stack_overflow_survey" class="csl-entry">

Overflow, Stack. 2021. “2021 Developer Survey.” 2021.
<https://insights.stackoverflow.com/survey/2021>.

</div>

</div>
