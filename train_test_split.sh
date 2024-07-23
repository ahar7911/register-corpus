#! /bin/bash

source load_env.sh

rm -f -r corpus/train
rm -f -r corpus/test
mkdir corpus/train
mkdir corpus/test
echo "created train and test directories and/or removed pre-existing train and test splits"

echo
python train_test_split.py
echo "completed train test splits"