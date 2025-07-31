# Melanoma Detection Backend

This FastAPI-based backend extracts ResNet50 features from three skin-cancer datasets, trains multiple classical classifiers, and serves predictions via HTTP.

---

## 📁 Repository Structure

```text
.
├── .gitignore
├── .env
├── alembic/                          # DB migrations
├── app/                              # FastAPI application
│   ├── main.py                       # entrypoint
│   ├── config.py
│   ├── database.py
│   ├── auth/                         # authentication routes & models
│   ├── patient/                      # patient CRUD
│   ├── predict/                      # prediction endpoints
│   └── utils/                        # shared utilities
├── data/                             # datasets & generated features
│   ├── melanoma_cancer_dataset/      # original 10k images (pre-split)
│   ├── ham_binary/                   # HAM10000 binary train/test/val
│   ├── skin9_binary/                 # ISIC-9 binary train/test
│   └── cnn_features.npz              # ResNet features for train/val/test
├── ml_models/                        # saved .joblib classifiers
├── scripts/                          # CLI tools
│   ├── data_prep/                    # prepare_ham10000.py, prepare_skin9_binary.py
│   ├── feature_extraction/           # extract_features.py
│   ├── training/                     # train_classifiers.py
│   ├── evaluation/                   # evaluate_original_offline.py, evaluate_ham_offline.py, evaluate_skin9_offline.py, evaluate_api.py
│   └── utils/                        # check_splits.py, count_classes.py
├── tests/                            # pytest suites
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md                         # ← this file
```

---

## 🔧 Prerequisites

- Python 3.13  
- `git`, `curl` (for manual API checks)

---

## 🚀 Setup

```bash
# 1. Clone & enter
git clone https://github.com/your-org/melanoma-detection-backend.git
cd melanoma-detection-backend

# 2. Create & activate venv
python -m venv .venv
# Windows (PowerShell)
. .\.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## 📊 Data Preparation

```bash
# HAM10000 binary split
python scripts/data_prep/prepare_ham10000.py

# ISIC-9 binary split
python scripts/data_prep/prepare_skin9_binary.py
```

> The original 10 000-image dataset is already split into `train/` and `test/`, so no prep script is needed.

---

## 🛠 Feature Extraction

```bash
python scripts/feature_extraction/extract_features.py
```

Produces `data/cnn_features.npz` containing:  
- `X_train`, `y_train`  
- `X_val`,   `y_val`  
- `X_test`,  `y_test`

---

## 🤖 Model Training & Evaluation

```bash
python scripts/training/train_classifiers.py \
  --model rf \
  --save-path ml_models/rf_final.joblib
```

Swap `--model` for `logistic`, `svm`, `knn`, or `dt` to train a different classifier.

---

## 📈 Offline Evaluation (Per Dataset)

```bash
python scripts/evaluation/evaluate_original_offline.py
python scripts/evaluation/evaluate_ham_offline.py
python scripts/evaluation/evaluate_skin9_offline.py
```

---

## 🌐 Live API Smoke-Tests

```bash
# Start API
uvicorn app.main:app --reload

# Health check
curl http://127.0.0.1:8000/health

# Bulk evaluation
python scripts/evaluation/evaluate_api.py
```

---

## 🧪 Additional Utilities

- `scripts/utils/check_splits.py` — verify folder structure  
- `scripts/utils/count_classes.py` — count images per class  

---

## 💾 Pushing to GitHub

```bash
git add README.md
git commit -m "docs: add full backend README"
git push origin your-branch
```
