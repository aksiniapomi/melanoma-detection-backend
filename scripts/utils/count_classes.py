# Count benign vs malignant examples in the dataset to check the split 
# Checked - balanced dataset! 
# From: Melanoma Skin Cancer Dataset of 10000 Images 
# Dataset Author: Muhammad Hasnain Javid

import os
from collections import Counter

def count_images(base_path: str):
    """Return a dict mapping each sub‑folder name to its .jpg/.png count."""
    result = Counter()
    for cls_name in os.listdir(base_path):
        cls_dir = os.path.join(base_path, cls_name)
        if not os.path.isdir(cls_dir):
            continue
        # only count image files
        files = [f for f in os.listdir(cls_dir)
                 if f.lower().endswith((".jpg", ".png"))]
        result[cls_name] = len(files)
    return result

if __name__ == "__main__":
    train_folder = "data/melanoma_cancer_dataset/train"
    test_folder  = "data/melanoma_cancer_dataset/test"

    train_counts = count_images(train_folder)
    test_counts  = count_images(test_folder)

    print("=== TRAIN CLASS COUNTS ===")
    for cls, cnt in train_counts.items():
        print(f"  {cls:10s}: {cnt}")
    print("\n=== TEST  CLASS COUNTS ===")
    for cls, cnt in test_counts.items():
        print(f"  {cls:10s}: {cnt}")
