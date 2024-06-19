#! /bin/bash

rm corpus/*

langs=("en" "fi" "fr" "sv" "multi")

for lang in "${langs[@]}"
do
    echo "standardizing CORE $lang"
    python utils_CORE/standardize_core.py --lang $lang
    echo "CORE $lang completed standardization"
done

echo "CORE completed standardization"