from argparse import ArgumentParser
import sys
from pathlib import Path
import json
import csv
import random
import pandas as pd


def combine_lists(text_lists : list[list[str]], target_len : int) -> list[str]:
    total_length = sum(len(text_list) for text_list in text_lists)
    if target_len > total_length:
        return [text for text_list in text_lists for text in text_list]

    for text_list in text_lists:
        random.shuffle(text_list)
    
    combined_list = []
    while len(combined_list) < target_len:
        for text_list in text_lists:
            if len(text_list) > 0:
                combined_list.append(text_list.pop(0))
            if len(combined_list) >= target_len:
                break

    return combined_list


def get_distr_reg2texts(filepaths : list[Path], 
                        max_size : int, 
                        cutoff : int
                        ) -> dict[str, list[str]]:
    with open(Path("info/reg_abbv.json")) as reg_abbv_file:
        reg_abbv2name = json.load(reg_abbv_file)

    print("starting distributed register corpus creation")
    reg2texts = {k : [] for k in reg_abbv2name.keys()}
    for filepath in filepaths:
        if not filepath.exists() or not filepath.is_file():
            print(f"filepath {filepath} taken from specified language {filepath.stem} does not exist or is not a file", file=sys.stderr)
            sys.exit(1)
        
        lang_reg2texts = {k : [] for k in reg_abbv2name.keys()}
        with open(filepath, "rt", encoding="utf-8") as src_file:
            src_reader = csv.reader(src_file, delimiter="\t", quoting=csv.QUOTE_NONE)
            for row in src_reader:
                register, text = row[0], row[1]
                lang_reg2texts[register].append(text)
        for reg, texts in lang_reg2texts.items():
            reg2texts[reg].append(texts)
    
    reg2len = {}
    for reg, text_lists in reg2texts.items():
        reg2len[reg] = sum([len(texts) for texts in text_lists])
    if max_size is None:
        max_size = min([num for num in reg2len.values() if num > cutoff])
    print(f"number of texts found per register:\n" + "\n".join([f"{reg}: {num}" for reg, num in reg2len.items()]))

    for reg, text_lists in reg2texts.items():
        reg2texts[reg] = combine_lists(text_lists, max_size)
    
    print("number of texts put in new distr corpus per register:" + "\n".join([f"{reg}: {len(texts)}" for reg, texts in reg2texts.items()]))
    return reg2texts


def main(langs : list[str], max_size : int, cutoff : int) -> None:
    # https://stackoverflow.com/questions/15063936/csv-error-field-larger-than-field-limit-131072
    maxInt = sys.maxsize
    while True: # decrease the maxInt value by factor 10 as long as the OverflowError occurs
        try:
            csv.field_size_limit(maxInt)
            break
        except OverflowError:
            maxInt = int(maxInt/10)

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
    
    distr_train_path = train_dir / "distr.tsv"
    if distr_train_path in filepaths:
        filepaths.remove(distr_train_path)
        print("distr.tsv included in original filepaths, now removed")
    
    print(f"languages used in making distr corpus: {', '.join(sorted([filepath.stem for filepath in filepaths]))}")
    
    reg2texts = get_distr_reg2texts(filepaths, max_size, cutoff)
    distr_regs = []
    distr_texts = []
    for reg, texts in reg2texts.items():
        distr_texts.extend(texts)
        distr_regs.extend([reg] * len(texts))
    
    distr_df = pd.DataFrame(zip(distr_regs, distr_texts))
    distr_df.to_csv(corpus_dir / "distr.tsv", sep="\t", header=False, index=False) # also save to corpus so that distributions can be analyzed
    distr_df.to_csv(train_dir / "distr.tsv", sep="\t", header=False, index=False) 
    print("saved distributed register corpus to corpus/distr.tsv and corpus/train/distr.tsv")


if __name__ == "__main__":
    parser = ArgumentParser(prog="Distributed register corpus",
                            description="Creates a corpus distr.tsv in the corpus folder which has equal amounts of text in each register from the specified languages")
    parser.add_argument("--langs", nargs="+",
                        help="Languages to create distributed register corpus from. If unspecified, all train corpus from corpus/train are used")
    parser.add_argument("--max_size", type=int,
                        help="""If specified, used as the maximum number of examples allowed per register. 
                        Otherwise, this number will be the minimum size of all registers with a number of texts greater than the cutoff""")
    parser.add_argument("--cutoff", type=int, default=100,
                        help="""Minimum cutoff for the number of examples allowed for each register (default: 100). 
                        All registers with more examples than this number will use the minimum length of that set of registers;
                        all registers with less examples will use all of their examples (creates slightly imbalanced corpus).
                        If max_size is specified, this number is ignored.""")
    args = parser.parse_args()

    main(**vars(args))