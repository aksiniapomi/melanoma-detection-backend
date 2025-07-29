import argparse
import numpy as np
import joblib
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report

def main(model_path, features_path="data/cnn_features.npz"):
    # load trained model
    model = joblib.load(model_path) #loads serialised model 

    # load held‑out features
    data = np.load(features_path)
    X_test, y_test = data["X_test"], data["y_test"] #reads features 

    # predict & score
    preds = model.predict(X_test)
    probs = model.predict_proba(X_test)[:,1]

    # print metrics
    print("=== EVALUATION ON:", features_path, "===\n")
    print("Accuracy:", accuracy_score(y_test, preds))
    print("ROC AUC:", roc_auc_score(y_test, probs))
    print("\n" + classification_report(
        y_test, preds,
        target_names=["benign","malignant"],
        digits=4
    ))

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--model-path",  required=True,
                   help="Path to a .joblib model file")
    p.add_argument("--features-path", default="data/cnn_features.npz",
                   help=".npz file with X_test/y_test arrays")
    args = p.parse_args()
    main(args.model_path, args.features_path)
