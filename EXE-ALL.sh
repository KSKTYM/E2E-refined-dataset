#! /bin/bash

./EXE0-GET-E2E-DATASET.sh
./EXE1-CONV-CSV2JSON.sh
./EXE2-CORRECT-TXT.sh
./EXE3-CORRECT-MR.sh
./EXE4-CONV-JSON2CSV.sh
./EXE5-MAKE-RELEASE-PACKAGE.sh