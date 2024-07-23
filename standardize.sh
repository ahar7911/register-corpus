#! /bin/bash

module load python/python-3.11.4
source /home2020/home/lilpa/harbison/experiences/env/bin/activate

rm -f -r corpus
mkdir corpus
echo "created directories and/or removed all pre-existing corpus data"

# standardization

# CORE standardization
source utils_core/standardize_core.sh

# alsatian standardization
echo
python utils_alsatian/standardize_alsatian.py
echo "completed alsatian standardization"

# corpus analysis
echo
source analyze_dist.sh

# train test split
echo
source train_test_split.sh