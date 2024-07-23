#! /bin/bash

source load_env.sh

echo "START STANDARDIZATION"
rm -f -r corpus
mkdir corpus
echo "created directories and/or removed all pre-existing corpus data"

# standardization

# CORE standardization
source utils_core/standardize_core.sh

# alsatian standardization
echo
python utils_alsatian/standardize_alsatian.py

# corpus analysis
echo
echo "START CORPUS ANALYSIS"
source analyze_dist.sh

# train test split
echo
echo "START TRAIN TEST SPLIT"
source train_test_split.sh