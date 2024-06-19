#! /bin/bash

module load python/python-3.11.3
source /home2020/home/lilpa/harbison/experiences/env/bin/activate

mkdir -p corpus/train
mkdir -p corpus/test
mkdir -p summaries

source utils_CORE/standardize_core.sh

python analyze_dist.py

rm corpus/train/*
rm corpus/test/*
python train_test_split.py