#! /bin/bash

# get enriched dataset
git clone https://github.com/ThiagoCF05/EnrichedE2E

# convert xml dataset to json format
mkdir -p data
mkdir -p data/enriched
python3 m_convert_enriched.py -d_i EnrichedE2E/train -o data/enriched/e2e_enriched_train_org.json -all
python3 m_convert_enriched.py -d_i EnrichedE2E/dev -o data/enriched/e2e_enriched_valid_org.json -all
python3 m_convert_enriched.py -d_i EnrichedE2E/test -o data/enriched/e2e_enriched_test_org.json -all

# correct text data
dataset=(train valid test)
for d in ${dataset[@]}; do
    python3 ../m_correct_txt.py -i data/enriched/e2e_enriched_"$d"_org.json -o data/enriched/e2e_enriched_"$d"_tmp.json
done

# make "MR value" list for MR correction
python3 ../m_make_valuelist.py -itrain data/enriched/e2e_enriched_train_tmp.json -ivalid data/enriched/e2e_enriched_valid_tmp.json -itest data/enriched/e2e_enriched_test_tmp.json -o data/enriched/e2e_enriched_mr_value.json -mix

# correct MR data
for d in ${dataset[@]}; do
    python3 ../m_correct_mr.py -i data/enriched/e2e_enriched_"$d"_tmp.json -iv data/enriched/e2e_enriched_mr_value.json -o data/enriched/e2e_enriched_"$d".json
done

# analyse insertion/deletion/substitution errors
mkdir -p result
mkdir -p result/enriched
for d in ${dataset[@]}; do
    python3 m_error_analysis.py -org data/enriched/e2e_enriched_"$d"_tmp.json -new data/enriched/e2e_enriched_"$d".json -o result/enriched/e2e_enriched_"$d".txt -v > result/enriched/RES-enriched-"$d".txt
done
