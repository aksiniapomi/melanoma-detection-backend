# Two classes - "benign (nevus)" and "malignant (melanoma)" 

import os, shutil, random, pandas as pd

# paths
SRC_DIRS = [
    "data/ham10000/HAM10000_images_part_1",
    "data/ham10000/HAM10000_images_part_2",
]
META    = "data/ham10000/HAM10000_metadata.csv"
OUT     = "data/ham_binary"

# make folders
for split in ("train","test"):
    for cls in ("benign","malignant"):
        os.makedirs(os.path.join(OUT,split,cls), exist_ok=True)

# load metadata & filter
df = pd.read_csv(META)
df = df[df.dx.isin(["nv","mel"])]
mapping = {"nv":"benign","mel":"malignant"}

# for each dx group, shuffle+80/20 split
for dx, g in df.groupby("dx"):
    ids = g["image_id"].tolist()
    random.shuffle(ids)
    cut = int(len(ids)*0.8)
    
    for split, subset in [("train", ids[:cut]), ("test", ids[cut:])]:
        for image_id in subset:
            src = None
            for d in SRC_DIRS:
             candidate = os.path.join(d, image_id + ".jpg")
             if os.path.exists(candidate):
               src = candidate
               break
            if not src:
               print(f"[!] WARNING: {image_id}.jpg not found in any part, skipping")
               continue
           
            dst = os.path.join(OUT, split, mapping[dx], image_id + ".jpg")

            if not os.path.exists(src):
                print(f"[!] WARNING: {src} not found, skipping")
                continue

            shutil.copy(src, dst)

print("HAM10000 binary train/test ready in", OUT)

# carve off 20% of train to data/ham_binary/val/{benign,malignant}

for cls in ("benign","malignant"):
    src_dir = os.path.join(OUT, "train", cls)
    dst_dir = os.path.join(OUT, "val",   cls)
    os.makedirs(dst_dir, exist_ok=True)

    all_imgs = os.listdir(src_dir)
    random.shuffle(all_imgs)
    n_val = int(0.2 * len(all_imgs))
    for img in all_imgs[:n_val]:
        shutil.move(
            os.path.join(src_dir, img),
            os.path.join(dst_dir, img)
        )
print("Validation split ready in", os.path.join(OUT, "val"))