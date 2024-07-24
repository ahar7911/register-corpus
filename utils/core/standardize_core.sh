#! /bin/bash

source load_env.sh

langs=("en" "fi" "fr" "sv" "multi")
for lang in "${langs[@]}"; do
    echo
    echo "standardizing CORE $lang"
    python utils/core/standardize_core.py --lang $lang
done
echo "completed CORE standardization"