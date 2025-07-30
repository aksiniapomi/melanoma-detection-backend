
import os
import requests
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report

#Configure to log in 
BASE_URL   = "http://127.0.0.1:8000"
USERNAME   = "xenia"
PASSWORD   = "Admin1"
PATIENT_ID = 2

def get_token():
    """Log in and grab JWT access token."""
    resp = requests.post(
        f"{BASE_URL}/auth/login",
        json={"username": USERNAME, "password": PASSWORD},
    )
    if resp.status_code != 200:
        print("Login failed:", resp.status_code, resp.text)
        resp.raise_for_status()
    return resp.json()["access_token"]

def main():
    token   = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    y_true = []
    y_prob = []
    y_pred = []

    for label_name, label_val in [("benign", 0), ("malignant", 1)]:
        folder = os.path.join("data", "melanoma_cancer_dataset", "test", label_name)
        if not os.path.isdir(folder):
            print(f"[!] Test folder not found: {folder}")
            continue

        for fname in os.listdir(folder):
            if not fname.lower().endswith((".jpg", ".jpeg", ".png", ".bmp")):
                continue
            path = os.path.join(folder, fname)

            # POST the image with authentication
            with open(path, "rb") as f:
                files = {"image": (fname, f, "image/jpeg")}
                r = requests.post(
                    f"{BASE_URL}/patients/{PATIENT_ID}/predictions/",
                    headers=headers,
                    files=files,
                )

            if r.status_code != 200:
                print(f"[!] Skipping {fname}: HTTP {r.status_code} → {r.text!r}")
                continue

            data = r.json()
            if "probability" not in data:
                print(f"[!] Skipping {fname}: no 'probability' in response {data!r}")
                continue

            prob = data["probability"]
            y_true.append(label_val)
            y_prob.append(prob)
            y_pred.append(1 if prob >= 0.5 else 0)

    if not y_true:
        print("\nNo successful predictions collected; check your login or endpoint.")
        return

    # Final metrics
    print("\n=== BULK CHECK OVER TEST SET ===")
    print("Accuracy:", accuracy_score(y_true, y_pred))
    print("ROC AUC:", roc_auc_score(y_true, y_prob))
    print("\n" + classification_report(
        y_true, y_pred,
        target_names=["benign", "malignant"],
        digits=4
    ))

if __name__ == "__main__":
    main()
