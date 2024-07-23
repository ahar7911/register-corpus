#! /bin/bash

module load python/python-3.11.4
source /home2020/home/lilpa/harbison/experiences/env/bin/activate

mkdir -p corpus/train
mkdir -p corpus/test
mkdir -p summaries
echo "directories made, or already exist"

rm -f corpus/*.tsv
echo "removed all pre-existing corpus data"

source utils_core/standardize_core.sh

echo
python utils_alsacien/standardize_alsacien.py
echo "completed alsatian standardization"

echo
python analyze_dist.py

echo
source train_test_split.sh