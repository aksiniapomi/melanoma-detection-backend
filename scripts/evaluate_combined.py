import argparse
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics       import accuracy_score, roc_auc_score, classification_report
from sklearn.linear_model  import LogisticRegression
from sklearn.svm           import SVC
from sklearn.ensemble      import RandomForestClassifier
from sklearn.neighbors     import KNeighborsClassifier
from sklearn.tree          import DecisionTreeClassifier

# map names to instances
MODEL_MAP = {
    "logistic": LogisticRegression(max_iter=1000, class_weight="balanced"),
    "svm"     : SVC(kernel="linear", probability=True, class_weight="balanced"),
    "rf"      : RandomForestClassifier(n_estimators=100, class_weight="balanced"),
    "knn"     : KNeighborsClassifier(n_neighbors=5),
    "dt"      : DecisionTreeClassifier(class_weight="balanced"),
}

def main():
    p = argparse.ArgumentParser(
        description="Overall eval of a classifier on combined ResNet features"
    )
    p.add_argument(
        "--model",
        choices=MODEL_MAP.keys(),
        required=True,
        help="Which classifier to fit/evaluate"
    )
    p.add_argument(
        "--test-size",
        type=float,
        default=0.2,
        help="Fraction of data to hold out as the unified test set"
    )
    args = p.parse_args()

    # load everything
    data = np.load("data/cnn_features.npz")
    X = np.vstack([data["X_train"], data["X_val"], data["X_test"]])
    y = np.concatenate([data["y_train"], data["y_val"], data["y_test"]])

    # stratified split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=args.test_size,
        stratify=y,
        random_state=42,
    )

    # fit the chosen model
    clf = MODEL_MAP[args.model]
    print(f"\nTraining {args.model!r} on {len(y_train)} samples…")
    clf.fit(X_train, y_train)

    # evaluate on unified test set
    preds = clf.predict(X_test)
    probs = clf.predict_proba(X_test)[:,1] if hasattr(clf, "predict_proba") else None

    print(f"\n=== Combined Test Metrics ({args.model}) ===")
    print("Accuracy:", accuracy_score(y_test, preds))
    if probs is not None:
        print("ROC‑AUC :", roc_auc_score(y_test, probs))
    print(classification_report(
        y_test, preds,
        target_names=["benign","malignant"],
        digits=4
    ))

if __name__ == "__main__":
    main()
