from argparse import ArgumentParser
import sys
from pathlib import Path
from random import sample
import json
import csv
import pandas as pd

def main(langs : list[str] = None):
    # https://stackoverflow.com/questions/15063936/csv-error-field-larger-than-field-limit-131072
    maxInt = sys.maxsize
    while True: # decrease the maxInt value by factor 10 as long as the OverflowError occurs
        try:
            csv.field_size_limit(maxInt)
            break
        except OverflowError:
            maxInt = int(maxInt/10)
    
    with open(Path("info/reg_abbv.json")) as reg_abbv_file:
        reg_abbv2name = json.load(reg_abbv_file)

    corpus_dir = Path("corpus")
    if not corpus_dir.exists() or not corpus_dir.is_dir():
        print("corpus directory does not exist or is not a directory, please run standardize.sh", file=sys.stderr)
        sys.exit(1)
    
    train_dir = corpus_dir / "train"
    if not train_dir.exists() or not train_dir.is_dir() or not any(train_dir.iterdir()):
        import train_test_split
        train_test_split.main()

    if langs is None:
        filepaths = list(train_dir.glob("*.tsv"))
        if len(filepaths) == 0:
            print("corpus directory has no tsv files, please run standardize.sh", file=sys.stderr)
            sys.exit(1)
    else:
        filepaths = [train_dir / f"{lang}.tsv" for lang in langs]

    print("starting distributed register corpus creation")
    reg2texts = {k : [] for k in reg_abbv2name.keys()}
    for filepath in filepaths:
        with open(filepath, "rt", encoding="utf-8") as src_file:
            src_reader = csv.reader(src_file, delimiter="\t", quoting=csv.QUOTE_NONE)
            for row in src_reader:
                register, text = row[0], row[1]
                reg2texts[register].append(text)
    
    print([len(texts) for texts in reg2texts.values()])
    min_len = min([len(texts) for texts in reg2texts.values() if len(texts) > 100])
    distr_regs = []
    distr_texts = []
    for reg, texts in reg2texts.items():
        try:
            distr_texts += sample(texts, min_len)
            distr_regs += [reg] * min_len
        except ValueError:
            print(f"allocation size {min_len} too large for {reg} dataset of size {len(texts)}, using register dataset size")
            distr_texts += texts
            distr_regs += [reg] * len(texts)
    
    distr_df = pd.DataFrame(zip(distr_regs, distr_texts))
    distr_df.to_csv(train_dir / "distr.tsv", sep="\t", header=False, index=False) 
    print("saved distributed register corpus to corpus/train/distr.tsv")


if __name__ == "__main__":
    parser = ArgumentParser(prog="Distributed register corpus",
                            description="Creates a corpus distr.tsv in the corpus folder which has equal amounts of text in each register from the specified languages")
    parser.add_argument("--langs", nargs="+",
                        help="Languages to create distributed register corpus from")
    args = parser.parse_args()

    main(args.langs)