import glob
import pandas as pd
from sklearn.model_selection import train_test_split

filepaths = glob.glob("corpus/*.tsv")

for filepath in filepaths:
    lang = filepath[7:-4]
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
        print("original stratified split failed, retrying")
        X_train, X_test, y_train, y_test = train_test_split(X, y, **split_args)

    print(f"split {len(X_train)} train, {len(X_test)} test")

    train_df = pd.DataFrame(zip(y_train, X_train))
    train_df.to_csv(f"corpus/train/{lang}.tsv", sep="\t", header=False, index=False) 
    test_df = pd.DataFrame(zip(y_test, X_test))
    test_df.to_csv(f"corpus/test/{lang}.tsv", sep="\t", header=False, index=False) 

    print(f"completed {lang} train test split\n")