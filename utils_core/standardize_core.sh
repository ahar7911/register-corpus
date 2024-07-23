#! /bin/bash

langs=("en" "fi" "fr" "sv" "multi")
for lang in "${langs[@]}"; do
    echo
    echo "standardizing CORE $lang"
    python utils_core/standardize_core.py --lang $lang
done
echo "completed CORE standardization"