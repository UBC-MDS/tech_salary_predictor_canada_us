# Methods
## Data
The data set used in this project is sourced from the survey, [Stack Overflow Annual Developer Survey](https://insights.stackoverflow.com/survey), which is conducted annually with nearly 80000 responses from different backgrounds. Based on the survey results {cite:p}`stack_overflow_survey`, much useful features could be extracted such as education level, location, the language used, job type, all of which are potentially associated with the annual compensation.

## Exploratory Data Analysis
After performing EDA on the training data set, there several points worth mention. The distribution of the response variable, salary, is positive skewed with a fat tail, as shown in Fig. 1 {cite:p}`vanderplas2018altair`. This attribute is undesirable, which makes the model less robust. So, extremely high salary (top 8%) in our training data set will be defined as outliers which are removed in the preprocessing step.<br>

```{figure} ../../results/salary_density_plot.png
---
height: 400px
name: salary_density
---
Density plot of salary
```

Among all the features investigated, it can be found that the salary is strongly correlated to the number of professional coding years. Fig.2 clearly shows that there is a linear relation between the number of professional coding years and the salary.

```{figure} ../../results/code_years_plot.png
---
height: 400px
name: code_years_plot
---
Number of coding years Vs. salary
```

Figures below present how other 3 features we selected have significant effects on the income level.
```{figure} ../../results/edu_plot.png
---
height: 150px
name: edu_plot
---
Education levels related to salary
```
```{figure} ../../results/language_plot.png
---
height: 150px
name: lang_plot
---
Programming languages related to salary
```
```{figure} ../../results/role_plot.png
---
height: 150px
name: role_plot
---
Roles related to salary
```
## Model
In light of EDA and recommendations from Stack Overflow, 4 features are extracted that are duration for being a profession, education level, programming language worked with and job position. Then, the regression equation can be obtained:<br>

$$ 
    Y_{salary} = w^T X + b
$$

*where w is the weight vector, X is the feature vector, b is the error term, $Y_{salary}$ is predicted variable.* <br>

Within the training data set, randomized hyperparameter searching {cite:p}`scikit-learn` was also carried out based on the scoring matrix, $R^2$.