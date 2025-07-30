# Prepare the Melanoma Skin Cancer Dataset of 10000 Images dataset (the original one)

import os, shutil, random, pandas as pd

RAW_ROOT = "data/melanoma_cancer_dataset"

SRC_BENIGN = os.path.join(RAW_ROOT, "benign")
SRC_MELANO = os.path.join(RAW_ROOT, "malignant")

OUT = RAW_ROOT  # reuse same root for train/test splits

#Create train/test dirs
for split in ("train","test"):
    for label in ("benign","malignant"):
        os.makedirs(os.path.join(OUT, split, label), exist_ok=True)

#Split and copy
for src, label in [(SRC_BENIGN, "benign"), (SRC_MELANO, "malignant")]:
    imgs = [f for f in os.listdir(src) if f.lower().endswith((".jpg",".png"))]
    random.shuffle(imgs)
    cut = int(0.8 * len(imgs))

    for split, subset in [("train", imgs[:cut]), ("test", imgs[cut:])]:
        for f in subset:
            shutil.copy(os.path.join(src, f),
                        os.path.join(OUT, split, label, f))

print("Original dataset train/test ready under", OUT)
