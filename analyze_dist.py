import sys
import csv
import json
from pathlib import Path

def main():
    # https://stackoverflow.com/questions/15063936/csv-error-field-larger-than-field-limit-131072
    maxInt = sys.maxsize
    while True: # decrease the maxInt value by factor 10 as long as the OverflowError occurs
        try:
            csv.field_size_limit(maxInt)
            break
        except OverflowError:
            maxInt = int(maxInt/10)
    
    with open(Path("info/reg_abbv.json")) as reg_abbv_file: # load as dict
        reg_abbv2name = json.load(reg_abbv_file)

    corpus_dir = Path("corpus")
    if not corpus_dir.exists() or not corpus_dir.is_dir():
        print("corpus directory does not exist or is not a directory, please run standardize.sh", file=sys.stderr)
        sys.exit(1)

    filepaths = list(corpus_dir.glob("*.tsv"))
    if len(filepaths) == 0:
        print("corpus directory has no tsv files, please run standardize.sh", file=sys.stderr)
        sys.exit(1)

    for filepath in filepaths:
        lang = filepath.stem
        print(f"start analysis of {lang}")

        counter = {k : 0 for k in reg_abbv2name.keys()}
        with open(filepath, "rt", encoding="utf-8") as src_file:
            src_reader = csv.reader(src_file, delimiter="\t", quoting=csv.QUOTE_NONE)
            for row in src_reader:
                register = row[0]
                counter[register] += 1

        counts = dict(counter)
        total = sum(counter.values())
        percentages = {k : v / total * 100 for k, v in counts.items()}

        summary_dir = Path("summaries")
        if not summary_dir.exists(): # make summary dir if does not exist
            summary_dir.mkdir()
        
        with open(summary_dir / f"{lang}.json", "w") as file:
            json.dump({"counts" : counts, "percentages" : percentages}, file, indent=4)
        
        print(f"completed analysis of {lang}")

if __name__ == "__main__":
    main()