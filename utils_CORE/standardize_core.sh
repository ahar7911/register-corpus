#! /bin/bash

langs=("en" "fi" "fr" "sw")

for lang in "${langs[@]}"
do
    echo "standardizing CORE $lang"
    python utils_CORE/standardize_core.py --lang $lang
    echo "CORE $lang completed standardization"
done

echo "CORE completed standardization"