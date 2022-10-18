# E2E refined dataset
This is an refined dataset of the [E2E dataset](https://github.com/tuetschek/e2e-dataset/releases/download/v1.0.0/e2e-dataset.zip).

_Authors: Keisuke Toyama, Katsuhito Sudoh, and Satoshi Nakamura_

## Download Link
https://github.com/KSKTYM/E2E-refined-dataset/blob/main/release/e2e_refined_dataset_v1_0_0.zip

## Description
The original E2E dataset is one of the most popular datasets for MR-to-text. However, the relationship between the MR and the sentences is not strict so that some MR-text pairs have "deletion(the MR is not reflected in the sentences)", "substitution(the MR value is substituted in the sentences)", and/or "insertion(the MR whose value is empty is appeared in the sentences with an unintended value)" errors.
Thus, we developed python programs to refine the E2E dataset.

We also developed three new MR features as follows:
1) "order": the order of the mention of MR values in the sentences
2) "num_sen": the number of sentences in "text"
3) "idx_sen": the index of the sentence which includes the MR value.

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
2) convert csv file to json file
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
5) convert json file to csv file
```
$ ./EXE4-CONV-JSON2CSV.sh
```
6) collect the generated dataset and pack them in zip
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
K. Toyama, K. Sudoh, and S. Nakamura, "E2E Refined Dataset," arXiv preprint arXiv:22XX.XXXXX, 2022

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
2022/10/??   version 1.0.0 (initial version)

## License
Distributed under the [Creative Common 4.0 Attribution-ShareAlike License (CC4.0-BY-SA)](https://creativecommons.org/licenses/by-sa/4.0/).
