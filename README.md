# E2E refined dataset
This is an refined dataset of the [E2E dataset](https://github.com/tuetschek/e2e-dataset/releases/download/v1.0.0/e2e-dataset.zip).

## Description
The original E2E dataset is one of the most popular datasets for MR-to-text. However, the relationship betwenn the MR and the sentence is not strict so that some MR-text pairs have "deletion(the MR is not reflected in the sentence)", "substitution(the MR value is substituted in the sentence)", and/or "insertion(the MR whose value is empty is appeared in the sentence with an unintended value)" errors.
Thus, we refined the E2E dataset by manually annotating the MR values.

_Authors: Anonymous_

## Process
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
6) extend test data
```
$ ./EXE5-SHUFFLE-ORDER.sh
```
7) collect the generated dataset and pack them in zip
```
$ ./EXE6-MAKE-RELEASE-PACKAGE.sh
```

You can execute these process with one command as
```
$ ./EXE-ALL.sh
```
These programs are written in python 3.

## Citing
If you use this dataset in your work, please cite the following papers:
```
@inproceedings{(Anonymous),
  title={(Anonymous)},
  author={(Anonymous)},
  booktitle={(Anonymous)},
  address={(Anonymous)},
  year={(Anonymous)},
  note={(Anonymous)},
  url={(Anonymous)},
}

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
2022/7/15   version 0.8.0 (initial version)

## License
Distributed under the [Creative Common 4.0 Attribution-ShareAlike License (CC4.0-BY-SA)](https://creativecommons.org/licenses/by-sa/4.0/).
