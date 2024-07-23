import sys
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split

corpus_dir = Path("corpus") # from running standardize.sh
filepaths = corpus_dir.glob("*.tsv")

for filepath in filepaths:
    lang = filepath.stem
    print(f"starting {lang} train test split")

    dataset = pd.read_csv(filepath, sep='\t')
    X = dataset.iloc[:,1].tolist()
    y = dataset.iloc[:,0].tolist()

    split_args = {"train_size":None, "test_size":None, "random_state":42, "stratify":y}
    if len(X) > 10000:
        split_args["train_size"] = 8000
        split_args["test_size"] = 2000
    elif len(X) > 500:
        split_args["test_size"] = 0.2
    else:
        split_args["test_size"] = 0.5
    
    try:
        X_train, X_test, y_train, y_test = train_test_split(X, y, **split_args)
    except ValueError as e:
        split_args["stratify"] = None
        print("original stratified split failed, retrying without stratification")
        X_train, X_test, y_train, y_test = train_test_split(X, y, **split_args)

    print(f"split {len(X_train)} train, {len(X_test)} test")

    if (corpus_dir / "train").exists() and (corpus_dir / "test").exists():
        train_df = pd.DataFrame(zip(y_train, X_train))
        train_df.to_csv(corpus_dir / "train" / f"{lang}.tsv", sep="\t", header=False, index=False) 
        test_df = pd.DataFrame(zip(y_test, X_test))
        test_df.to_csv(corpus_dir / "test" / f"{lang}.tsv", sep="\t", header=False, index=False)
    else:
        print("\ntrain and test folders do not exist, please run train_test_split.sh instead")
        sys.exit(1)

    print(f"completed {lang} train test split\n")