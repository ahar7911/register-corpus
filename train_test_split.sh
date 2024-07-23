#! /bin/bash

module load python/python-3.11.4
source /home2020/home/lilpa/harbison/experiences/env/bin/activate

rm -f corpus/train/*
rm -f corpus/test/*
echo "cleared train and test folders"

echo
python train_test_split.py
echo "completed train test splits"