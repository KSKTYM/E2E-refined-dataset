#! /bin/bash

mkdir -p out_csv
python3 m_conv_json2csv.py -i out/e2e_train.json -o out_csv/trainset.csv
python3 m_conv_json2csv.py -i out/e2e_valid.json -o out_csv/devset.csv
python3 m_conv_json2csv.py -i out/e2e_test.json  -o out_csv/testset_w_refs.csv
python3 m_conv_json2csv.py -i out/e2e_test.json  -o out_csv/testset.csv -nr
