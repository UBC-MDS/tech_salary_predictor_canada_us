# author: Sanchit Singh
# date: 2021-11-24

"Cleans, splits and pre-processes the Tech Salary Predictor. Writes the training and test data to separate files.

Usage: src/pre_process_wisc.R --input=<input> --out_dir=<out_dir>

Options:
--input=<input>       Path (including filename) to raw data (csv file)
--out_dir=<out_dir>   Path to directory where the processed data should be written
" -> doc

library(tidyverse)
library(caret)
library(docopt)

opt = docopt(doc)
#getwd()

main <- function(input, out_dir){
  # read data and convert class to factor
  raw_data <- read.csv(input) 
  # Pre Processing steps
  raw_data <- raw_data |> 
    select(Country, EdLevel, YearsCodePro, LanguageHaveWorkedWith, DevType, ConvertedCompYearly, Employment) |> 
    filter(Country=="Canada" & Employment == 'Employed full-time') |> 
    select(-Country) |> 
    separate_rows(DevType, sep=";")
  
  raw_data$YearsCodePro <- as.numeric(raw_data$YearsCodePro)
  quantile <- quantile(raw_data$ConvertedCompYearly, 0.92)
  raw_data <- raw_data |> filter(ConvertedCompYearly < quantile)
  
  # split into training and test data sets
  sample_size <- floor(0.8*nrow(raw_data))
  set.seed(123)
  picked <- sample(seq_len(nrow(raw_data)),size = sample_size)
  training_data <- raw_data[picked,]
  test_data <- raw_data[-picked,]
  
  # write training and test data to csv files
  write_csv(training_data, paste0(out_dir, "/training.csv"))
  write_csv(test_data, paste0(out_dir, "/test.csv"))
}

main(opt[["--input"]], opt[["--out_dir"]])

main("data/raw/survey_results_ca_usa.csv",
    "data/raw/")
