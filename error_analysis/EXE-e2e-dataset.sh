#! /bin/bash

# analyse insertion/deletion/substitution errors
mkdir -p result
mkdir -p result/org
dataset=(train valid test)
for d in ${dataset[@]}; do
    python3 m_error_analysis.py -org ../data/e2e_"$d"_tmp.json -new ../out/e2e_"$d".json -o result/org/e2e_"$d".txt -v > result/org/RES-"$d".txt
done
