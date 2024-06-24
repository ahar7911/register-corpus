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
    echo
    echo "standardizing CORE $lang"
    python utils_CORE/standardize_core.py --lang $lang
    echo "CORE $lang completed standardization"
done
echo "CORE completed standardization"

echo
python analyze_dist.py

echo
source train_test_split.sh