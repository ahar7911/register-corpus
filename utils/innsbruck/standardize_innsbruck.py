import sys
from pathlib import Path
import json
import csv

innsbruck_path = Path("corpus-original/innsbruck/GermInnC/1901-1950")

def main():
    with open(Path("mappings/innsbruck.json")) as mapping_file: # loads mapping as a dict
        mapping = json.load(mapping_file)
    
    corpus_dir = Path("corpus")
    if not corpus_dir.exists(): # make corpus dir if does not exist
        corpus_dir.mkdir()
    
    de_tsv_path = corpus_dir / "de.tsv"
    de_tsv_path.unlink(missing_ok=True) # removes corpus/de.tsv if already exists

    # remove empty lines, combine it all into one string (no new lines?)
    for text_path in innsbruck_path.iterdir():
        if not text_path.is_file():
            print(f"{text_path} is not a text file")
        old_reg = text_path.name.split("_")[0] # form REGISTER_P1_REGION_YEAR_NAME.txt
        new_reg = mapping[old_reg]

        text_lines = []
        with open(text_path, "r", encoding="latin1") as textfile:
            for line in textfile:
                line = line.strip()
                if line:
                    text_lines.append(line)
        
        if not text_lines:
            print(f"file {text_path} is empty")
            continue

        text = " ".join(text_lines)

        with open(de_tsv_path, "a+", encoding="utf-8", newline="") as corpus_file:
            text_writer = csv.writer(corpus_file, delimiter="\t")
            text_writer.writerow([new_reg, text])

if __name__ == "__main__":
    print("standardizing german innsbruck")

    if not innsbruck_path.exists() or not innsbruck_path.is_dir() or not any(innsbruck_path.iterdir()):
        print(f"current filepath to german innsbruck corpus ({innsbruck_path}) does not exist, is not a directory, or is empty", file=sys.stderr)
        print("edit the corpus_path variable in utils/innsbruck/standardize_innsbruck.py to the proper german innsbruck corpus directory", file=sys.stderr)
        sys.exit(1)

    main()
    print("completed german innsbruck standardization")