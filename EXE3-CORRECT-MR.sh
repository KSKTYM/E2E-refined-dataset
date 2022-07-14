#! /bin/bash

# make value list for MR correction
python3 m_make_valuelist.py -itrain data/e2e_train_tmp.json -ivalid data/e2e_valid_tmp.json -itest data/e2e_test_tmp.json -o data/e2e_mr_value.json -mix

# MR correction
mkdir -p out
data=(test train valid)
for d in ${data[@]}; do
    python3 m_correct_mr.py -i data/e2e_"$d"_tmp.json -iv data/e2e_mr_value.json -o out/e2e_"$d".json
done
