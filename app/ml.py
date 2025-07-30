import io
import joblib
import torch
import numpy as np
from PIL import Image
from torchvision import models, transforms

# Load trained classifier
CLF_PATH = "ml_models/rf_final.joblib"
clf = joblib.load(CLF_PATH)

# Prepare the ResNet50 feature extractor
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
resnet = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V1)
resnet.fc = torch.nn.Identity()   # chop off the final layer
resnet = resnet.to(device).eval()

#Same transforms as in scripts/extract_features.py
tfm = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

def predict_melanoma(img_bytes: bytes) -> float:
    # Load image
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    # Transform & add batch dim
    x = tfm(img).unsqueeze(0).to(device)    # shape [1,3,224,224]
    # Extract features
    with torch.no_grad():
        feats = resnet(x).cpu().numpy().squeeze()  # [2048]
    # Classify
    prob = clf.predict_proba([feats])[0, 1]      # p(malignant)
    return float(prob)
