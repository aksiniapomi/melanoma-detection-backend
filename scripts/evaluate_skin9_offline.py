# Evaluate the performance on the skin9 dataset 

import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

import numpy as np
from joblib import load
from scripts.extract_features import extract_split
from sklearn.metrics import accuracy_score, roc_auc_score

def main():
    # Loadtrained Random Forest classifier
    rf = load("ml_models/rf_final.joblib")

    # Extract features for the entire SKIN-9 test split
    TEST_DIR = "data/skin9_binary/test"
    X_skin9, y_skin9 = extract_split(TEST_DIR)

    # Predict & evaluate
    preds = rf.predict(X_skin9)
    probs = rf.predict_proba(X_skin9)[:, 1]

    print("Skin-9 test set evaluation:")
    print(f"  Number of samples : {len(y_skin9)}")
    print(f"  Accuracy          : {accuracy_score(y_skin9, preds):.4f}")
    print(f"  ROC AUC           : {roc_auc_score(y_skin9, probs):.4f}")

if __name__ == "__main__":
    main()
