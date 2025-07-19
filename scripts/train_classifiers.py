#Train each on ResNet Features and point out accuracy ROC AUC and full classification report 
# 5 classifiers to test 
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report

def load_data(npz_path="data/cnn_features.npz"):
    data = np.load(npz_path)
    X_train, y_train = data["X_train"], data["y_train"]
    X_test,  y_test  = data["X_test"],  data["y_test"]
    return X_train, y_train, X_test, y_test

def evaluate_model(model, X_train, y_train, X_test, y_test):
    model.fit(X_train, y_train) #the robot studies which fingerprint patterns go with “benign” vs “malignant”
    preds = model.predict(X_test)
    probs = model.predict_proba(X_test)[:,1] if hasattr(model, "predict_proba") else None

    print(f"— {model.__class__.__name__} —")
    print("Accuracy:", accuracy_score(y_test, preds))
    if probs is not None:
        print("ROC AUC: ", roc_auc_score(y_test, probs))
    print(classification_report(
        y_test, 
        preds,
        target_names=["benign", "malignant"], 
        digits=4
        ))
    print("="*40)

#in-built classifiers 
def main():
    X_train, y_train, X_test, y_test = load_data()
    models = [
        LogisticRegression(max_iter=1000),
        SVC(kernel="linear", probability=True),
        RandomForestClassifier(n_estimators=100),
        KNeighborsClassifier(n_neighbors=5),
        DecisionTreeClassifier(),
    ]

    for m in models:
        evaluate_model(m, X_train, y_train, X_test, y_test)

if __name__ == "__main__":
    main()
