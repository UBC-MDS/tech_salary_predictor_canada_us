# Project proposal —— Salary predictor for tech employees in US and Canada

### Aim

Graduates and seasoned tech employees may have a question about how much they should get paid from their employers for the reason that salary is never transparent information. Lack of enough information, graduates may feel lost and insecure and job seekers may be at disadvantage when having salary discussion with HRs. Hence, we come up with this idea to build up a model to predict the  pay that technicians can expect based on several explicit factors including education level, previous experience, location etc.

### Data

The data set used in this project is sourced from the survey, [Stack Overflow Annual Developer Survey](https://insights.stackoverflow.com/survey), which is conducted annually with nearly 80000 responses from different backgrounds. Based on the survey results, much useful features could be extracted such as education level, location, the language used, job type, all of which are potentially associated with the annual compensation.

### Usage

suggested way to download data:

1. Clone this Github repository
2. Go to [Stack Overflow Annual Developer Survey](https://insights.stackoverflow.com/survey)
3. Copy the link of the csv file, taking 2019 result as an example:
   https://info.stackoverflowsolutions.com/rs/719-EMH-566/images/stack-overflow-developer-survey-2019.zip
4. Use **./src/download_data.py** to download the data set
5. Save the data in the folder **./data/raw** under this project
6. Run the following command at the terminal from the root directory of this project:
```
# download data
python src/download_data.py --url=https://info.stackoverflowsolutions.com/rs/719-EMH-566/images/stack-overflow-developer-survey-2019.zip --out_dir=data/raw

# pre-process data
Rscript src/pre_process_wisc.R --input=data/raw/survey_results_public.csv --out_dir=data/processed

# run eda report
python src/eda.py --train=data/processed/training.csv --out_dir=results/

# modelling
python src/salary_prediction_model.py --train=data/processed/training.csv --out_dir=results --test=data/processed/test.csv

# render report
jupyter-book build /doc/tech_salary_predictor_report/
```

### Modelling

This project intents to predict the payment level of individuals according to their own personal situations, so the linear regression model is chosen to present users a continuous prediction result. Additionally, the linear regression model can also provide other important information such as the weight of each feature.

The research question is:
> To predict the expected salary of a tech employee in US or Canada.

This topic is a predictive question, also extending to following sub-questions:
1. Which features have significantly statistical effect on the response (inference)?
2. Whether the model is robust (model estimation, a predictive problem)
3. The confidence interval of predictions (predictive)

### Exploratory data analysis

Based on the data corresponding to the five features in the survey, we can see the most frequently used languages in developer's work are JavaScript, HTML/CSS, SQL, Python and Bash/Shell. And the five most frequent coding experience years of those developers who took the survey are 10,5,6,8,4 years respectively.  

### Results sharing
We have done some exploratory data analysis so far which can be found in the literate document [here](https://github.com/UBC-MDS/tech_salary_predictor_canada_us/blob/main/src/EDA.ipynb).
