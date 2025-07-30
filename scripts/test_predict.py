import os, sys
# add the project root (one level up) to Python’s import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.ml import predict_melanoma

# load one of held‑out test images
with open("data/melanoma_cancer_dataset/test/benign/melanoma_10000.jpg","rb") as f:
    img_bytes = f.read()

prob = predict_melanoma(img_bytes)
print("Predicted prob(malignant):", prob)
