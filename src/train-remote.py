import argparse
import os
import pickle

import pandas as pd
import xgboost as xgb
from azureml.core import Run

run = Run.get_context()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data_path", type=str, default=".", help="Path to the training data"
    )
    parser.add_argument(
        "--learning_rate", type=float, default=0.01, help="Learning rate for XGBoost"
    )
    parser.add_argument(
        "--n_estimators", type=int, default=500, help="Estimators for XGBoost"
    )

    parser.add_argument(
        "--reg_alpha", type=float, default=0.5, help="Regularization parameter"
    )

    args = parser.parse_args()

    print("===== DATA =====")
    print("DATA PATH: " + args.data_path)
    print("LIST FILES IN DATA PATH...")
    print(os.listdir(args.data_path))
    print("================")

    # load data

    df_pos = pd.read_csv(args.data_path + "/pos.csv", index_col=0)
    df_neg = pd.read_csv(args.data_path + "/neg.csv", index_col=0)

    df = pd.concat([df_pos, df_neg])
    df.reset_index(drop=True)

    history = {}
    watchlist = [()]

    X = df.values[:, :-1]
    y = df.values[:, -1]

    # define convolutional network
    model = xgb.XGBClassifier(
        objective="binary:logistic",
        n_estimators=args.n_estimators,
        reg_alpha=args.reg_alpha,
        learning_rate=args.learning_rate,
        max_depth=6,
        subsample=0.8,
    )

    model.fit(X, y)
    pkl_filename = "outputs/xgboost_peptide_classifier.pkl"

    with open(pkl_filename, "wb") as file:
        pickle.dump(model, file)

    print("Finished Training")
