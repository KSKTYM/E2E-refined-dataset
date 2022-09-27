#! /bin/bash

# correct text data
dataset=(train valid test)
for d in ${dataset[@]}; do
    python3 m_correct_txt.py -i data/e2e_"$d"_org.json -o data/e2e_"$d"_tmp.json
done
