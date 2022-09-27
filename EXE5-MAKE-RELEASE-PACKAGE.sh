#! /bin/bash

# make a release package
mkdir -p release/e2e_refined_dataset
cp -p release/README.md release/e2e_refined_dataset
cp -p out/e2e_train.json release/e2e_refined_dataset
cp -p out/e2e_valid.json release/e2e_refined_dataset
cp -p out/e2e_test.json release/e2e_refined_dataset
zip -r release/e2e_refined_dataset_v0_9_0.zip release/e2e_refined_dataset
