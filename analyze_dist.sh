#! /bin/bash

module load python/python-3.11.4
source /home2020/home/lilpa/harbison/experiences/env/bin/activate

rm -f -r summaries
mkdir summaries
echo "created summary directory and/or removed pre-existing summaries"

echo
python analyze_dist.py
echo "completed corpus analysis"