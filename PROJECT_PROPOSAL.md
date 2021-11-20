# Project proposal —— Salary predictor for technicians in US and Canada

### Aim

Graduates and seasoned programmers may have a question about how much they should get paid from their employers due to that salary is never transparent information. Lack of enough information, graduates may feel lost and insecure and job hunters may be at disadvantage when having salary discussion with HRs. Hence, we come up with this idea to build up a model to predict the  pay that programmers can expect based on several factors including eduction level, previous experience, location etc.

### Data

The data set used in this project is sourced from the survey, [Stack Overflow Annual Developer Survey](https://insights.stackoverflow.com/survey), which is conducted annually with nearly 80000 responses from different backgrounds. Based on the survey results, much useful features could be extracted such as education level, location, the language used, job type, all of which are potentially associated with the annual compensation.

### Modelling

This project intents to predict the payment level of individuals according to their own personal situations, so the linear regression model is chosen to present users a continuous prediction result. Additionally, the linear regression model can also provide other important information such as the weight of each feature.

The research question is:
> To predict the expected salary of a programmer either in US or Canada.

This topic is a predictive question, also extending to following sub-questions:
1. Which features have significantly statistical effect on the response (inference)
2. If the model is robust (model estimation, a predictive problem)
3. The confidence interval of predictions (predictive)

### Exploratory data analysis

Based on the data corresponding to the five features in the survey, we can see the most frequently used languages in developer's work are JavaScript, HTML/CSS, SQL, Python and Bash/Shell. And the five most frequent coding experience years of those developers who took the survey are 10,20,15,8,6 years respectively.  

### Results sharing

The project result will show the fitness of the model, including the significance test of feature coefficients and regression metrics on the test set.