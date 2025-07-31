#Evaluate the API performance for the predictions 
import os
import requests
import numpy as np
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report

# Configuration 
BASE_URL   = "http://127.0.0.1:8000"
USERNAME   = "xenia"    
PASSWORD   = "Admin1"    
PATIENT_ID = 2

API_PRED   = f"{BASE_URL}/patients/{PATIENT_ID}/predictions"
AUTH_LOGIN = f"{BASE_URL}/auth/login"

# The three test-set roots
TEST_DIRS = {
    "original":  "data/melanoma_cancer_dataset/test",
    "ham10000":  "data/ham_binary/test",
    "skin9":     "data/skin9_binary/test",
}

def main():
    # Authenticate and get a JWT
    resp = requests.post(
        AUTH_LOGIN,
        json={"username": USERNAME, "password": PASSWORD},
        headers={"Content-Type": "application/json"},
    )
    resp.raise_for_status()
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    y_true, y_pred, y_prob = [], [], []

    # Loop through each test folder, POST to API, collect predictions
    for ds_name, base in TEST_DIRS.items():
        for cls in ("benign", "malignant"):
            cls_path = os.path.join(base, cls)
            for fname in os.listdir(cls_path):
                img_path = os.path.join(cls_path, fname)
                with open(img_path, "rb") as f:
                    resp = requests.post(
                        API_PRED,
                        files={"image": f},    # matches `image: UploadFile`
                        headers=headers,       # include Bearer token
                    )
                resp.raise_for_status()
                data = resp.json()
                prob = data["probability"] 
                pred = 1 if prob >= 0.5 else 0

                y_true.append(1 if cls == "malignant" else 0)
                y_pred.append(pred)
                y_prob.append(prob)

    #Compute and print overall live-API metrics
    print("\n=== LIVE API EVALUATION ===\n")
    print("Accuracy:", accuracy_score(y_true, y_pred))
    print("ROC-AUC :", roc_auc_score(y_true, y_prob))
    report = classification_report(
        y_true, y_pred,
        target_names=["benign", "malignant"],
        digits=4
    )
    print(f"\n{report}")

if __name__ == "__main__":
    main()
