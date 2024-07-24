#! /bin/bash

source load_env.sh

rm -f -r corpus
mkdir corpus
echo "created directories and/or removed all pre-existing corpus data"

# STANDARDIZATION
echo "START STANDARDIZATION"

# CORE standardization
source utils/core/standardize_core.sh
# alsatian standardization
echo
python utils/alsatian/standardize_alsatian.py

echo "END STANDARDIZATION"

# corpus analysis
echo
echo "START CORPUS ANALYSIS"
rm -r -f summaries
python analyze_dist.py
echo "END CORPUS ANALYSIS"

# train test split
echo
echo "START TRAIN TEST SPLIT"
rm -r -f corpus/train
rm -r -f corpus/test
python train_test_split.py
echo "END TRAIN TEST SPLIT"