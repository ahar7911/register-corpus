from argparse import ArgumentParser
import sys
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split

def main(langs : list[str], train_size : int) -> None:
    corpus_dir = Path("corpus")
    if not corpus_dir.exists() or not corpus_dir.is_dir():
        print("corpus directory does not exist or is not a directory, please run standardize.sh", file=sys.stderr)
        sys.exit(1)
    
    if langs is None: # if no langs specified, use all that are in corpus dir
        filepaths = list(corpus_dir.glob("*.tsv"))
        if len(filepaths) == 0:
            print("corpus directory has no tsv files, please run standardize.sh", file=sys.stderr)
            sys.exit(1)
    else:
        filepaths = []
        for lang in langs:
            lang_dir = corpus_dir / f"{lang}.tsv"
            if lang_dir.exists() and lang_dir.is_file():
                filepaths.append(lang_dir)
            else:
                print(f"specified language {lang} has no corresponding corpus tsv file in the corpus directory at {lang_dir}", file=sys.stderr)
                sys.exit(1)

    for filepath in filepaths:
        lang = filepath.stem # .../.../lang.tsv -> lang
        print(f"starting {lang} train test split")

        dataset = pd.read_csv(filepath, sep='\t')
        X = dataset.iloc[:,1].tolist() # X refers to texts
        y = dataset.iloc[:,0].tolist() # y refers to registers (classes/labels)

        corpus_len = len(X)
        split_args = {"train_size":None, "test_size":None, "random_state":42, "stratify":y} # args for sklearn's train_test_split

        if train_size is not None: # size of training corpus is specified
            if corpus_len >= train_size * 2: # enough for a 50/50 split
                split_args["train_size"] = train_size
                split_args["test_size"] = train_size
                print("50/50 split with specified train size")
            elif corpus_len >= train_size * 1.25: # not enough for 50/50 but enough for 80/20 split
                split_args["train_size"] = train_size
                split_args["test_size"] = train_size // 4
                print("80/20 split with specified train size")
            else: # not even enough for 80/20 split, just split corpus in half
                split_args["test_size"] = 0.5
                print("50/50 split of entire corpus (too small for specified train size)")
        else: # no training corpus size specified
            if corpus_len > 10000: # limit the size of examples used from corpora to 10000 max
                split_args["train_size"] = 8000
                split_args["test_size"] = 2000
                print("8000 training examples, 2000 test examples")
            elif corpus_len > 500:
                split_args["test_size"] = 0.2
                print("80/20 split")
            else:
                split_args["test_size"] = 0.5
                print("50/50 split")

        try:
            X_train, X_test, y_train, y_test = train_test_split(X, y, **split_args)
        except ValueError: # impossible to do a stratified split (not enough of one register)
            split_args["stratify"] = None
            print("original stratified split failed, retrying without stratification")
            X_train, X_test, y_train, y_test = train_test_split(X, y, **split_args)

        print(f"split {len(X_train)} train, {len(X_test)} test")

        train_dir = corpus_dir / "train"
        test_dir = corpus_dir / "test"
        if not train_dir.exists() or not test_dir.exists(): # make train and test dir if do not exist
            train_dir.mkdir(exist_ok=True)
            test_dir.mkdir(exist_ok=True)

        # save in same format as original tsv files
        train_df = pd.DataFrame(zip(y_train, X_train))
        train_df.to_csv(train_dir / f"{lang}.tsv", sep="\t", header=False, index=False) 
        test_df = pd.DataFrame(zip(y_test, X_test))
        test_df.to_csv(test_dir / f"{lang}.tsv", sep="\t", header=False, index=False)

        print(f"completed {lang} train test split\n")

if __name__ == "__main__":
    parser = ArgumentParser(prog="Train test split",
                            description="Splits all corpus in folder 'corpus' into a train and test split")
    parser.add_argument("--langs", nargs="+",
                        help="Languages for which to create train test splits. If unspecified, all corpus from corpus directory are used")
    parser.add_argument("--train_size", type=int,
                        help="Size of the training set (if possible, otherwise will do a 50/50 split)")
    args = parser.parse_args()

    main(**vars(args))