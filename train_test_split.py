from argparse import ArgumentParser
import sys
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split

def main(train_size : int = None):
    corpus_dir = Path("corpus")
    if not corpus_dir.exists():
        print("corpus directory does not exist, please run standardize.sh", file=sys.stderr)
        sys.exit(1)

    filepaths = list(corpus_dir.glob("*.tsv"))
    if len(filepaths) == 0:
        print("corpus directory is empty, please run standardize.sh", file=sys.stderr)
        sys.exit(1)

    for filepath in filepaths:
        lang = filepath.stem
        print(f"starting {lang} train test split")

        dataset = pd.read_csv(filepath, sep='\t')
        X = dataset.iloc[:,1].tolist()
        y = dataset.iloc[:,0].tolist()

        corpus_len = len(X)
        split_args = {"train_size":None, "test_size":None, "random_state":42, "stratify":y}

        if train_size is not None:
            if corpus_len >= train_size * 2:
                split_args["train_size"] = train_size
                split_args["test_size"] = train_size
                print("50/50 split with specified train size")
            elif corpus_len >= train_size * 1.25:
                split_args["train_size"] = train_size
                split_args["test_size"] = train_size // 4
                print("80/20 split with specified train size")
            else:
                split_args["test_size"] = 0.5
                print("50/50 split of entire corpus (too small for specified train size)")
        else:
            if corpus_len > 10000:
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
        except ValueError:
            split_args["stratify"] = None
            print("original stratified split failed, retrying without stratification")
            X_train, X_test, y_train, y_test = train_test_split(X, y, **split_args)

        print(f"split {len(X_train)} train, {len(X_test)} test")

        train_dir = corpus_dir / "train"
        test_dir = corpus_dir / "test"
        if not train_dir.exists() or not test_dir.exists():
            train_dir.mkdir(exist_ok=True)
            test_dir.mkdir(exist_ok=True)

        train_df = pd.DataFrame(zip(y_train, X_train))
        train_df.to_csv(train_dir / f"{lang}.tsv", sep="\t", header=False, index=False) 
        test_df = pd.DataFrame(zip(y_test, X_test))
        test_df.to_csv(test_dir / f"{lang}.tsv", sep="\t", header=False, index=False)

        print(f"completed {lang} train test split\n")

if __name__ == "__main__":
    parser = ArgumentParser(prog="Train test split",
                            description="Splits all corpus in folder 'corpus' into a train and test split")
    parser.add_argument("--train_size", type=int,
                        help="Size of the training set (if possible, otherwise will do a 50/50 split)")
    args = parser.parse_args()

    main(args.train_size)