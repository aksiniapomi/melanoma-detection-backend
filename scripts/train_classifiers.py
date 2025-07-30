# Train each on ResNet Features and point out accuracy, ROC AUC and full classification report
# 5 classifiers to test 
import argparse
import numpy as np
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report

def load_data(npz_path="data/cnn_features.npz"):
    data = np.load(npz_path)
    return (
        data["X_train"], data["y_train"],
        data["X_val"],   data["y_val"],
        data["X_test"],  data["y_test"],
    )
    
def evaluate_split(name, model, X, y):
    """
    Print accuracy, ROC AUC and full report
    for the given (X, y) split under the label `name`.
    """
    preds = model.predict(X)
    probs = model.predict_proba(X)[:,1] if hasattr(model, "predict_proba") else None

    print(f"\n=== {name} set ===")
    print("Accuracy :", accuracy_score(y, preds))
    if probs is not None:
        print("ROC AUC  :", roc_auc_score(y, probs))
    print(classification_report(
        y, preds,
        target_names=["benign", "malignant"],
        digits=4
    ))
    
#  map command‑line names to actual model instances
MODEL_MAP = {
    "logistic": LogisticRegression(max_iter=1000),
    "svm":      SVC(kernel="linear", probability=True),
    "rf":       RandomForestClassifier(n_estimators=100),
    "knn":      KNeighborsClassifier(n_neighbors=5),
    "dt":       DecisionTreeClassifier(),
}

def main():
    # argument parsing 
    p = argparse.ArgumentParser(description="Train & save one classifier")
    p.add_argument("--model",
                   choices=MODEL_MAP.keys(),
                   required=True,
                   help="Which model to train: " + ", ".join(MODEL_MAP.keys()))
    p.add_argument("--save-path",
                   required=True,
                   help="Where to add the trained model (e.g. ml_models/logistic_final.joblib)")
    args = p.parse_args()

    #Load all splits
    X_train, y_train, X_val, y_val, X_test, y_test = load_data()
    
    clf = MODEL_MAP[args.model]
    
    #fit on the trainning split
    print(f"Training {args.model} on {X_train.shape[0]} samples…")
    clf.fit(X_train, y_train)
    
    # train + print metrics
    evaluate_split("Validation", clf, X_val, y_val)
    evaluate_split("Test", clf, X_test,  y_test)
    
    # save the trained classifier
    print(f"Saving trained {args.model} model to {args.save_path}…")
    joblib.dump(clf, args.save_path)
 
if __name__ == "__main__":
    main()

