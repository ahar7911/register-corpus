#! /bin/bash

module load python/python-3.11.3
source /home2020/home/lilpa/harbison/experiences/env/bin/activate

mkdir -p corpus/train
mkdir -p corpus/test
mkdir -p summaries
echo "directories made, or already exist"

rm -f corpus/*.tsv
echo "removed all pre-existing corpus data"

langs=("en" "fi" "fr" "sv" "multi")
for lang in "${langs[@]}"
do
    echo "standardizing CORE $lang"
    python utils_CORE/standardize_core.py --lang $lang
    echo "CORE $lang completed standardization"
done
echo "CORE completed standardization"

python analyze_dist.py

rm -f corpus/train/*
rm -f corpus/test/*
echo "cleared train and test folders"
python train_test_split.py