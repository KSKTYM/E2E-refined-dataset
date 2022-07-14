#! /bin/bash

mkdir -p out_shuffle
python3 m_shuffle_order.py -np 4 -nv 4 -seed 1234 -i out/e2e_test.json -d_out out_shuffle
