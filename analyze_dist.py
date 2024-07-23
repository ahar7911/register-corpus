import sys
import csv
import json
from pathlib import Path
from collections import Counter

# https://stackoverflow.com/questions/15063936/csv-error-field-larger-than-field-limit-131072
maxInt = sys.maxsize
while True: # decrease the maxInt value by factor 10 as long as the OverflowError occurs
    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)

corpus_dir = Path("corpus")
filepaths = corpus_dir.glob("*.tsv")

for filepath in filepaths:
    lang = filepath.stem
    print(f"start analysis of {lang}")

    counter = Counter()
    with open(filepath, "rt", encoding="utf-8") as src_file:
        src_reader = csv.reader(src_file, delimiter="\t", quoting=csv.QUOTE_NONE)
        for row in src_reader:
            register, text = row[0], row[-1]
            counter[register] += 1

    counts = dict(counter)
    total = sum(counter.values())
    percentages = {k : v / total * 100 for k, v in counts.items()}
    counts["total"] = total

    summary_dir = Path("summaries")
    if summary_dir.exists():
        with open(summary_dir / f"{lang}.json", "w") as file:
            json.dump({"counts" : counts, "percentages" : percentages}, file, indent=4)
    else:
        print("\nsummary folder does not exist, please run analyze_dist.sh instead")
        sys.exit(1)
    
    print(f"completed analysis of {lang}")