import sys
import csv
import json
from pathlib import Path
from collections import Counter

corpus_dir = Path("corpus")
summary_dir = Path("summaries")
reg_abbv_path = Path("info", "reg_abbv.json")

def main():
    # https://stackoverflow.com/questions/15063936/csv-error-field-larger-than-field-limit-131072
    maxInt = sys.maxsize
    while True: # decrease the maxInt value by factor 10 as long as the OverflowError occurs
        try:
            csv.field_size_limit(maxInt)
            break
        except OverflowError:
            maxInt = int(maxInt/10)
    
    if reg_abbv_path.exists():
        with open(reg_abbv_path) as reg_abbv_file:
            reg_abbv2name = json.load(reg_abbv_file)
    else:
        print(f"register abbreviation json file not found at {reg_abbv_path}, please reload from original repo")

    if not corpus_dir.exists():
        print("corpus directory does not exist, please run standardize.sh", file=sys.stderr)
        sys.exit(1)

    filepaths = list(corpus_dir.glob("*.tsv"))
    if len(filepaths) == 0:
        print("corpus directory is empty, please run standardize.sh", file=sys.stderr)
        sys.exit(1)

    for filepath in filepaths:
        lang = filepath.stem
        print(f"start analysis of {lang}")

        counter = {k : 0 for k, _ in reg_abbv2name.items()}
        with open(filepath, "rt", encoding="utf-8") as src_file:
            src_reader = csv.reader(src_file, delimiter="\t", quoting=csv.QUOTE_NONE)
            for row in src_reader:
                register = row[0]
                counter[register] += 1

        counts = dict(counter)
        total = sum(counter.values())
        percentages = {k : v / total * 100 for k, v in counts.items()}

        if summary_dir.exists():
            with open(summary_dir / f"{lang}.json", "w") as file:
                json.dump({"counts" : counts, "percentages" : percentages}, file, indent=4)
        else:
            print("\nsummary folder does not exist, please run analyze_dist.sh instead", file=sys.stderr)
            sys.exit(1)
        
        print(f"completed analysis of {lang}")

if __name__ == "__main__":
    main()