# Prepare HAM10000 dataset 

import os
import shutil
import random
import pandas as pd

# paths
SRC_DIRS = [
    "data/ham10000/HAM10000_images_part_1",
    "data/ham10000/HAM10000_images_part_2",
]
META    = "data/ham10000/HAM10000_metadata.csv"
OUT     = "data/ham_binary"

# make output folders
for split in ("train", "test"):
    for cls in ("benign", "malignant"):
        os.makedirs(os.path.join(OUT, split, cls), exist_ok=True)

# load and filter metadata
df = pd.read_csv(META)
df = df[df.dx.isin(["nv", "mel"])]
mapping = {"nv": "benign", "mel": "malignant"}

# 80/20 train/test split per class
for dx, group in df.groupby("dx"):
    image_ids = group["image_id"].tolist()
    random.shuffle(image_ids)
    cut = int(len(image_ids) * 0.8)

    for split_name, subset in [("train", image_ids[:cut]), ("test", image_ids[cut:])]:
        for image_id in subset:
            # find the image in one of the source directories
            for src_dir in SRC_DIRS:
                src_path = os.path.join(src_dir, image_id + ".jpg")
                if os.path.exists(src_path):
                    dst_dir = os.path.join(OUT, split_name, mapping[str(dx)])
                    dst_path = os.path.join(dst_dir, image_id + ".jpg")
                    shutil.copy(src_path, dst_path)
                    break
            else:
                print(f"[!] WARNING: {image_id}.jpg not found in any source folder")

print("HAM10000 binary train/test ready in", OUT)
