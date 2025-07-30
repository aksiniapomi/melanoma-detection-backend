#Prepare the Skin Cancer ISIC dataset for trainning and testing 

import os
import shutil

# Paths to the raw SKIN‑9 folders
SKIN9_ROOT = "data/skin9/Skin cancer ISIC The International Skin Imaging Collaboration"
RAW_TRAIN  = os.path.join(SKIN9_ROOT, "Train")
RAW_TEST   = os.path.join(SKIN9_ROOT, "Test")

# Where to write binary split
OUT_ROOT = "data/skin9_binary"

# Only keep these two classes 
CLASS_MAP = {
    "nevus":    "benign",     # keep only nevus as benign
    "melanoma": "malignant",  # keep only melanoma as malignant
}

# output directories
for split in ("train", "test"):
    for label in CLASS_MAP.values():
        os.makedirs(os.path.join(OUT_ROOT, split, label), exist_ok=True)

def copy_split(src_dir, split_name):
    """
    Copy only the 'nevus' and 'melanoma' folders from src_dir into
    OUT_ROOT/split_name/{benign,malignant}.
    """
    for folder_name, label in CLASS_MAP.items():
        src_folder = os.path.join(src_dir, folder_name)
        if not os.path.isdir(src_folder):
            print(f"[!] Missing folder: {src_folder}")
            continue

        for fname in os.listdir(src_folder):
            if not fname.lower().endswith((".jpg", ".jpeg", ".png")):
                continue
            src_path = os.path.join(src_folder, fname)
            dst_path = os.path.join(OUT_ROOT, split_name, label, fname)
            shutil.copy(src_path, dst_path)

# Copy train and test
print("Copying SKIN‑9 TRAIN images…")
copy_split(RAW_TRAIN, "train")

print("Copying SKIN‑9 TEST images…")
copy_split(RAW_TEST, "test")

print("SKIN‑9 binary split ready in", OUT_ROOT)
