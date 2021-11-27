#!/usr/bin/env python
# coding: utf-8

# # Results

# In[1]:


from joblib import dump, load
import pandas as pd
from myst_nb import glue
import altair as alt
from altair_saver import save
alt.data_transformers.enable('data_server')
alt.renderers.enable('mimetype')


pipe_loaded = load('../../results/best_model_pipe.joblib')
alpha = round(pipe_loaded.best_params_['ridge__alpha'], 3)
rsquare = round(pipe_loaded.best_score_, 3)
glue("alpha_coef", alpha);
glue("R2", rsquare);

test_result_loaded = load('../../results/test_result.joblib')
rsquare_test = round(test_result_loaded["r_sq_test"], 3)
glue("R2_test", rsquare_test);

test_df = pd.read_csv("../../data/processed/test.csv")
y_test = test_df.ConvertedComp.tolist()
y_predict = test_result_loaded["predict_y"].tolist()
result = {"true_y": y_test, "predicted_y": y_predict}
df_result = pd.DataFrame(data=result)
df_result.head(5)

df_diag = pd.DataFrame(data={"true_y": [0, max(df_result.true_y)+500],
                             "predicted_y":[0, max(df_result.true_y)+500]})

plt1 = alt.Chart(df_result).mark_point(opacity=0.5).encode(
    alt.X("predicted_y", title="Predicted salary"),
    alt.Y("true_y", title="True salary")
) + alt.Chart(df_diag).mark_line(color='red').encode(
    alt.X("predicted_y", title="Predicted salary"),
    alt.Y("true_y", title="True salary")
)


# The hyperparameter tunning result shows that the model is at the best performance when alpha = {glue:text}`alpha_coef` with a training $R^2$  of {glue:text}`R2` as shown in the figure below.
# 
# ```{figure} ../../results/alpha-tuning.png
# ---
# height: 400px
# name: alpha-tuning
# ---
# Hyperparameter searching
# ```
# Applying the fitted model to the test data set, we get  a testing $R^2$ of {glue:text}`R2_test`.

# In[ ]:




