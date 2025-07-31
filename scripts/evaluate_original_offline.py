# Evaluate the performance solely on the original dataset 

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

    # Extract features for ORIGINAL test split
    TEST_DIR = "data/melanoma_cancer_dataset/test"
    X_orig, y_orig = extract_split(TEST_DIR)

    preds = rf.predict(X_orig)
    probs = rf.predict_proba(X_orig)[:, 1]

    print("Original melanoma test set evaluation:")
    print(f"  # samples : {len(y_orig)}")
    print(f"  Accuracy   : {accuracy_score(y_orig, preds):.4f}")
    print(f"  ROC AUC    : {roc_auc_score(y_orig, probs):.4f}")

    report = classification_report(
        y_orig, preds,
        target_names=["benign", "malignant"],
        digits=4
    )
    print(f"\n{report}")

if __name__ == "__main__":
    main()
