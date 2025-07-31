# Evaluate performance on HAM10000 dataset only 

import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

import numpy as np
from joblib import load
from scripts.extract_features import extract_split
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report

def main():
    # Load RF model
    rf = load("ml_models/rf_final.joblib")

    # Extract features for HAM10000 test split
    TEST_DIR = "data/ham_binary/test"
    X_ham, y_ham = extract_split(TEST_DIR)

    preds = rf.predict(X_ham)
    probs = rf.predict_proba(X_ham)[:, 1]

    print("HAM10000 test set evaluation:")
    print(f"  # samples : {len(y_ham)}")
    print(f"  Accuracy   : {accuracy_score(y_ham, preds):.4f}")
    print(f"  ROC AUC    : {roc_auc_score(y_ham, probs):.4f}")

    report = classification_report(
        y_ham, preds,
        target_names=["benign", "malignant"],
        digits=4
    )

    print(f"\n{report}")

if __name__ == "__main__":
    main()
