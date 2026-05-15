# 获取一张样例图片
import os
import json
import shutil

TRAIN_DIR = "data/dataset/train"
OUTPUT_DIR = "flowers102"
JSON_PATH = "ai_model/cat_to_name.json"

os.makedirs(OUTPUT_DIR, exist_ok=True)

with open(JSON_PATH, "r", encoding="utf-8") as f:
    cat_to_name = json.load(f)

count = 0

for class_id in os.listdir(TRAIN_DIR):
    class_path = os.path.join(TRAIN_DIR, class_id)

    if not os.path.isdir(class_path):
        continue

    if class_id not in cat_to_name:
        continue

    images = [
        img for img in os.listdir(class_path)
        if img.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    if not images:
        continue

    img_path = os.path.join(class_path, images[0])

    # ⭐关键修改：用ID命名
    save_name = f"{class_id}.jpg"
    save_path = os.path.join(OUTPUT_DIR, save_name)

    shutil.copy(img_path, save_path)

    count += 1
    print(f"processed: {class_id}")

print(f"done, total: {count}")