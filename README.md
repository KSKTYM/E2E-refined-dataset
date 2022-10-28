# E2E refined dataset
This is an refined dataset of the [E2E dataset](https://github.com/tuetschek/e2e-dataset/releases/download/v1.0.0/e2e-dataset.zip).

_Authors: Keisuke Toyama, Katsuhito Sudoh, and Satoshi Nakamura_

## Download Link
https://github.com/KSKTYM/E2E-refined-dataset/blob/main/release/e2e_refined_dataset_v1_0_0.zip

## Description
The E2E dataset is a very popular dataset for MR-to-text.
However, some of the MR-text pairs suffer from the following errors: "deletion" (an MR is not reflected in the text), "insertion" (an MR whose value is empty appears in the text with an unintended value), and "substitution" (an MR value is replaced in the text).
Since such errors affet the quality of MR-to-text systems, they must be fixed as much as possible.
Therefore, we developed a refined dataset and some python programmes that convert the original E2E dataset into a refined dataset.

We also provided the following additional annotations:
1) "MR order" (order): the order of the mentions of MR values in corresponding sentences
2) "Number of sentences" (num_sen): the number of sentences included in the text part
3) "Sentence indexes" (idx_sen): an index of sentences that include the corresponding MR values

## Development Environment
- OS
  + Ubuntu 20.04
- Python
  + 3.8.10

## Usage
1) download the E2E dataset
```
$ ./EXE0-GET-E2E-DATASET.sh
```
2) convert csv files to json files
```
$ ./EXE1-CONV-CSV2JSON.sh
```
3) correct text data
```
$ ./EXE2-CORRECT-TXT.sh
```
4) correct MR data
```
$ ./EXE3-CORRECT-MR.sh
```
5) convert json files to csv files
```
$ ./EXE4-CONV-JSON2CSV.sh
```
6) collect the generated dataset and pack them in a zip file
```
$ ./EXE5-MAKE-RELEASE-PACKAGE.sh
```

You can execute these process with one command as
```
$ ./EXE-ALL.sh
```

## Error Analysis
```
$ cd error_analysis
$ ./EXE-e2e-dataset.sh
$ ./EXE-cleaned-dataset.sh
$ ./EXE-enriched-dataset.sh
```

## Citing
If you use this dataset in your work, please cite the following papers:
```
K. Toyama, K. Sudoh, and S. Nakamura, "E2E Refined Dataset," arXiv preprint arXiv:22XX.XXXXX, 2022 (to be appeared)

@inproceedings{novikova2017e2e,
  title={The {E2E} Dataset: New Challenges for End-to-End Generation},
  author={Novikova, Jekaterina and Du{\v{s}}ek, Ondrej and Rieser, Verena},
  booktitle={Proceedings of the 18th Annual Meeting of the Special Interest 
             Group on Discourse and Dialogue},
  address={Saarbr\"ucken, Germany},
  year={2017},
  note={arXiv:1706.09254},
  url={https://arxiv.org/abs/1706.09254},
}
```

## Version
2022/09/28   version 0.9.0 (prerelease version)
2022/11/??   version 1.0.0 (initial version)

## License
Distributed under the [Creative Common 4.0 Attribution-ShareAlike License (CC4.0-BY-SA)](https://creativecommons.org/licenses/by-sa/4.0/).
