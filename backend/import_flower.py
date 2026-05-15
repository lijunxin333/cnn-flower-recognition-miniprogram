# 用于导入花卉数据
import sqlite3
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(BASE_DIR, "flowers.db")
JSON_PATH = os.path.join(BASE_DIR, "..", "ai_model", "cat_to_name.json")

with open(JSON_PATH, "r", encoding="utf-8") as f:
    cat_to_name = json.load(f)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

count = 0

for class_id, name in cat_to_name.items():

    class_id_int = int(class_id)

    img_path = f"/static/flowers102/{class_id_int}.jpg"

    cursor.execute("""
        INSERT OR REPLACE INTO flower
        (id, name, image_path, description,language, light, water, soil)
        VALUES (?, ?, ?, ?, ?, ?, ?,?)
    """, (
        class_id_int,
        name,
        img_path,
        "待补充",
        "待补充",
        "待补充",
        "待补充",
        "待补充"
    ))

    count += 1

conn.commit()
conn.close()

print(f"all done, {count} records!")