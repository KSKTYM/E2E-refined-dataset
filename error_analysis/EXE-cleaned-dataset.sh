#! /bin/bash

# get cleaned dataset
git clone https://github.com/tuetschek/e2e-cleaning

# convert csv dataset to json format
mkdir -p data
mkdir -p data/cleaned
python3 m_convert_cleaned.py -i e2e-cleaning/cleaned-data/train-fixed.no-ol.csv -o data/cleaned/e2e_cleaned_train_org.json
python3 m_convert_cleaned.py -i e2e-cleaning/cleaned-data/devel-fixed.no-ol.csv -o data/cleaned/e2e_cleaned_valid_org.json
python3 m_convert_cleaned.py -i e2e-cleaning/cleaned-data/test-fixed.csv -o data/cleaned/e2e_cleaned_test_org.json

# correct text data
dataset=(train valid test)
for d in ${dataset[@]}; do
    python3 ../m_correct_txt.py -i data/cleaned/e2e_cleaned_"$d"_org.json -o data/cleaned/e2e_cleaned_"$d"_tmp.json
done

# make "MR value" list for MR correction
python3 ../m_make_valuelist.py -itrain data/cleaned/e2e_cleaned_train_tmp.json -ivalid data/cleaned/e2e_cleaned_valid_tmp.json -itest data/cleaned/e2e_cleaned_test_tmp.json -o data/cleaned/e2e_cleaned_mr_value.json -mix

# correct MR data
for d in ${dataset[@]}; do
    python3 ../m_correct_mr.py -i data/cleaned/e2e_cleaned_"$d"_tmp.json -iv data/cleaned/e2e_cleaned_mr_value.json -o data/cleaned/e2e_cleaned_"$d".json
done

# analyse insertion/deletion/substitution errors
mkdir -p result
mkdir -p result/cleaned
for d in ${dataset[@]}; do
    python3 m_error_analysis.py -org data/cleaned/e2e_cleaned_"$d"_tmp.json -new data/cleaned/e2e_cleaned_"$d".json -o result/cleaned/e2e_cleaned_"$d".txt -v > result/cleaned/RES-cleaned-"$d".txt
done
