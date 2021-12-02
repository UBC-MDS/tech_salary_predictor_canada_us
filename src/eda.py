# author: Jiwei Hu
# date: 2021-11-24

#Usage # create exploratory data analysis figures and write to file 
#python src/eda.py --train=data/processed/training.csv --out_dir=results/

'''Creates eda charts and plots for the pre-processed training data from the Stack Overflow Annual Developer Survey 2019 data (from https://info.stackoverflowsolutions.com/rs/719-EMH-566/images/stack-overflow-developer-survey-2019.zip).
Saves the plots as a pdf and png file.
Usage: src/eda.py --train=<train> --out_dir=<out_dir>
  
Options:
--train=<train>     Path (including filename) to training data (which needs to be saved as a csv file)
--out_dir=<out_dir> Path to directory where the plots should be saved
'''

from docopt import docopt
import numpy as np
import pandas as pd
import altair as alt
from altair_saver import save
alt.data_transformers.enable('data_server')
alt.renderers.enable('mimetype')

opt = docopt(__doc__)

def main(train, out_dir):
    # read in data
    train_df = pd.read_csv(train)

    # visualize the annual compensation comparision by different education levels
    
    train_df = train_df.query('ConvertedComp < 200000')
    replace_dict = {'Bachelor’s degree (BA, BS, B.Eng., etc.)':'Bachelor',
            'Master’s degree (MA, MS, M.Eng., MBA, etc.)':'Master',
            'Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)':'Secondary_school'}
    edu_df = train_df[train_df["EdLevel"].astype(str).str.contains('Bachelor|Master|Secondary')].replace(replace_dict)


    edu_plot = alt.Chart(edu_df).mark_boxplot().encode(
        alt.Y('EdLevel', title='Education level'), 
        alt.X('ConvertedComp', title='Annual Compensation(USD)'),
        color='EdLevel',
        )
    
     # visualize the annual compensation comparision by different job types  
    role_df = train_df[train_df["DevType"].astype(str).str.contains('full-stack|front-end|back-end|desktop|mobile')]


    role_plot = alt.Chart(role_df).mark_boxplot().encode(
        alt.Y('DevType:N', title='Job type'), 
        alt.X('ConvertedComp:Q', title='Annual Compensation(USD)'),
        color='DevType:N',
        )

    # visualize the annual compensation comparision by different programming languages
    tech = ['C#;HTML/CSS;JavaScript;SQL', 'C#;HTML/CSS;JavaScript;SQL;TypeScript', 'HTML/CSS;JavaScript', 'HTML/CSS;JavaScript;PHP;SQL', 'Bash/Shell/PowerShell;C#;HTML/CSS;JavaScript;SQL']
    tech_df = train_df.query('LanguageWorkedWith == @tech')
    lang_replace_dict = {'C#;HTML/CSS;JavaScript;SQL':'C,SQL,HTML,Java',
            'C#;HTML/CSS;JavaScript;SQL;TypeScript':'TypeScript,C,SQL,HTML,Java',
            'HTML/CSS;JavaScript':'HTML,Java',
            'HTML/CSS;JavaScript;PHP;SQL':'HTML,Java,PHP,SQL',
            'Bash/Shell/PowerShell;C#;HTML/CSS;JavaScript;SQL':'Bash,C,SQL,HTML,Java',
               }
    tech_df = tech_df.replace(lang_replace_dict)
    language_plot = alt.Chart(tech_df).mark_boxplot().encode(
        alt.Y('LanguageWorkedWith:N', title='Languages worked with'), 
        alt.X('ConvertedComp:Q', title='Annual Compensation(USD)'),
        color='LanguageWorkedWith:N',
        )

    # visualize the annual compensation comparision by different codeing experience years

    # code_years_df = (train_df.query("YearsCodePro != 'Less than 1 year' and YearsCodePro != 'More than 50 years' ")
    #              .dropna(subset=["YearsCodePro", "ConvertedComp", "DevType"]).astype({"YearsCodePro": "int"})
    #              .query("YearsCodePro <= 30"))
    code_years_df = train_df.query("YearsCodePro <= 30")


    code_years_plot = alt.Chart(code_years_df).mark_point(
        ).encode(alt.X('YearsCodePro',title='Number of professional coding years'), 
         alt.Y('mean(ConvertedComp)', title='Annual Compensation(USD)'), 
        )
    
    # visualize the salary distribution 
    salary_density_plot = (alt.Chart(train_df)
        .transform_density(
        'ConvertedComp',
         as_=['ConvertedComp', 'Density'])  # Give the name "density" the KDE columns we just created
        .mark_area(opacity=0.8).encode(
        x=alt.X('ConvertedComp'),
        y='Density:Q'))
    
    # save all the plots in the out_dir
    
    save(edu_plot,out_dir + 'edu_plot.png')
    save(role_plot,out_dir + 'role_plot.png')
    save(language_plot,out_dir + 'language_plot.png')
    save(code_years_plot,out_dir + 'code_years_plot.png')
    save(salary_density_plot,out_dir + 'salary_density_plot.png')



if __name__ == "__main__":
    main(opt["--train"], opt["--out_dir"])