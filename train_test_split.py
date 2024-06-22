import glob
import pandas as pd
from sklearn.model_selection import train_test_split

filepaths = glob.glob("corpus/*.tsv")

for filepath in filepaths:
    lang = filepath[7:-4]
    dataset = pd.read_csv(filepath, sep='\t')

    X = dataset.iloc[:,1].tolist()
    y = dataset.iloc[:,0].tolist()

    train_size = None
    if len(X) > 10000:
        train_size = 8000
        test_size = 2000
    elif len(X) > 500:
        test_size = 0.2
    else:
        test_size = 0.5
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=train_size, test_size=test_size, random_state=42)

    train_df = pd.DataFrame(zip(y_train, X_train))
    train_df.to_csv(f"corpus/train/{lang}.tsv", sep="\t", header=False, index=False) 
    test_df = pd.DataFrame(zip(y_test, X_test))
    test_df.to_csv(f"corpus/test/{lang}.tsv", sep="\t", header=False, index=False) 

    print(f"completed {lang} train test split")

print("completed train test splits")