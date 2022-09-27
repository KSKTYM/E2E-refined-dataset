#! /bin/bash

# convert csv file to json file
mkdir -p data
python3 m_conv_csv2json.py -i e2e-dataset/trainset.csv -o data/e2e_train_org.json
python3 m_conv_csv2json.py -i e2e-dataset/devset.csv -o data/e2e_valid_org.json
python3 m_conv_csv2json.py -i e2e-dataset/testset_w_refs.csv -o data/e2e_test_org.json
