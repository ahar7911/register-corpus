#! /bin/bash

source load_env.sh

rm -rf corpus
mkdir corpus
echo "created directories and/or removed all pre-existing corpus data"

# STANDARDIZATION
echo "START STANDARDIZATION"

# CORE standardization
source utils/core/standardize_core.sh
# alsatian standardization
echo
python utils/alsatian/standardize_alsatian.py
# German Innsbruck standardization
echo
python utils/innsbruck/standardize_innsbruck.py

echo "END STANDARDIZATION"

# corpus analysis
echo
echo "START CORPUS ANALYSIS"
rm -rf summaries
python analyze_dist.py
echo "END CORPUS ANALYSIS"

# train test split
echo
echo "START TRAIN TEST SPLIT"
rm -rf corpus/train
rm -rf corpus/test
python train_test_split.py
echo "END TRAIN TEST SPLIT"

# create distributed register corpus
echo
echo "START CREATION OF DISTRIBUTED REGISTER CORPUS"
python distr_corpus.py