import os, shutil, random

SRC = "Garbage classification"
DEST = "dataset"

mapping = {
    "cardboard": "paper",
    "metal": "metal",
    "plastic": "plastic",
    "glass": "other",
    "trash": "other"
}

# Create folders
for c in ["paper", "metal", "plastic", "other"]:
    os.makedirs(f"{DEST}/train/{c}", exist_ok=True)
    os.makedirs(f"{DEST}/val/{c}", exist_ok=True)

# Copy & split images
for src, dst in mapping.items():
    files = os.listdir(f"{SRC}/{src}")
    random.shuffle(files)

    split = int(0.8 * len(files))   # 80% train, 20% val

    for i, f in enumerate(files):
        subset = "train" if i < split else "val"
        src_path = f"{SRC}/{src}/{f}"
        dst_path = f"{DEST}/{subset}/{dst}/{f}"
        shutil.copy(src_path, dst_path)

print("Dataset prepared successfully!")
