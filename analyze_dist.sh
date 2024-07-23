#! /bin/bash

source load_env.sh

rm -f -r summaries
mkdir summaries
echo "created summary directory and/or removed pre-existing summaries"

echo
python analyze_dist.py
echo "completed corpus analysis"