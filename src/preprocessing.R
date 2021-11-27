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
library(testthat)

opt = docopt(doc)

main <- function(input, out_dir){
  # read data and convert class to factor
  raw_data <- read.csv(input) 
  # Pre Processing steps
  pre_processing <- function(df){
    df <- df |> 
      select(Country, EdLevel, YearsCodePro, LanguageWorkedWith, DevType, ConvertedComp, Employment, Student) |> 
      filter(Country=="Canada" & 
               Employment == 'Employed full-time' & 
               Student=='No' & 
               YearsCodePro != 'Less than 1 year' &
               YearsCodePro != 'More than 50 years') |> 
      select(-Country, -Student) |> 
      separate_rows(DevType, sep=";")
    
    df$YearsCodePro <- as.numeric(df$YearsCodePro)
    quantile <- quantile(df$ConvertedComp, 0.92, na.rm=TRUE)
    df <- df |> filter(ConvertedComp < quantile)
    
  }
  
  raw_data <- pre_processing(raw_data)
  
  # Testing the pre processed data
  test_that("Testing if country column is removed and employment type is Full time", {
    
    testing_data_1 <- data.frame(Country=c("Canada", "Canada", "Canada"),
                                 EdLevel=c("a", "b", "c"), 
                                 YearsCodePro=c(1, 2, 3),
                                 LanguageWorkedWith=c("h", "y", "k"),
                                 DevType=c("g", "t", "l"),
                                 ConvertedComp=c(20, 30, 40), 
                                 Employment=c("Employed full-time", "Employed full-time", "Employed full-time"),
                                 Student=c("No", "No", "No"))
    
    expect_equal(data.frame(pre_processing(testing_data_1))$Country, NULL)
    
    expect_equal(unique(data.frame(pre_processing(testing_data_1))$Employment), "Employed full-time")  
    
  })
  
  # Selecting the number of rows to split
  splitting <- function(df){
    
    sample_size <- floor(0.8*nrow(df))
    set.seed(123)
    picked <- sample(seq_len(nrow(df)),size = sample_size)
  }
  
  # Testing the split function
  test_that("Testing if number of rows picked is 80% of the total rows ", {
    
    testing_data_2 <- data.frame(Country=replicate(10, "Canada"),
                                 EdLevel=c("a", "b", "c", "d", "e", "f", "g", "h", "i", "j"), 
                                 YearsCodePro=seq(1, 10, 1),
                                 LanguageWorkedWith=c("a", "b", "c", "d", "e", "f", "g", "h", "i", "j"),
                                 DevType=c("a", "b", "c", "d", "e", "f", "g", "h", "i", "j"),
                                 ConvertedComp=seq(10, 100, 10), 
                                 Employment=replicate(10, "Employed full-time"),
                                 Student=replicate(10, "No"))
    
    expect_that(nrow(data.frame(splitting(testing_data_2))), equals(8))})
  
  
  # split into training and test data sets
  training_data <- raw_data[splitting(raw_data),]
  test_data <- raw_data[-splitting(raw_data),]
  
  # write training and test data to csv files
  write_csv(training_data, paste0(out_dir, "/training.csv"))
  write_csv(test_data, paste0(out_dir, "/test.csv"))
}

main(opt[["--input"]], opt[["--out_dir"]])