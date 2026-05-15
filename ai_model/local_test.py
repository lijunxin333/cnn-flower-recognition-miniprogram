# ai_model/local_test.py
import os
import matplotlib.pyplot as plt
from PIL import Image
import random

from predict import load_model, predict_flower  

# 1. 路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
train_dir = os.path.join(BASE_DIR, "../data/dataset/train")

# 2. 加载模型（只加载一次）
model = load_model()

# 3. 示例图片
def get_example_image(class_id):
    class_folder = os.path.join(train_dir, class_id)

    if not os.path.exists(class_folder):
        return None

    images = [
        f for f in os.listdir(class_folder)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    if not images:
        return None

    img_path = os.path.join(class_folder, random.choice(images))
    return Image.open(img_path).convert("RGB")

# 4. 可视化
def visualize(image_path, result):

    img = Image.open(image_path).convert("RGB")

    classes = result["classes"]
    names = result["names"]
    probs = result["probs"]

    example_img = get_example_image(classes[0])

    # 输入图 + 示例图
    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.imshow(img)
    plt.axis("off")
    plt.title("Input Image")

    if example_img:
        plt.subplot(1, 2, 2)
        plt.imshow(example_img)
        plt.axis("off")
        plt.title(f"Predicted: {names[0]}")

    plt.show()

    # 概率图
    plt.figure(figsize=(8, 4))
    plt.barh(names[::-1], probs[::-1])
    plt.xlabel("Probability")
    plt.title("Top Predictions")
    plt.xlim(0, 1)
    plt.show()


# 5. 测试入口
if __name__ == "__main__":

    image_path = input("Enter image path: ").strip()

    if not os.path.exists(image_path):
        print("Image not found!")
        exit()

    result = predict_flower(image_path, model)

    print("\nTop predictions:")
    for cls, name, prob in zip(result["classes"], result["names"], result["probs"]):
        print(f"{cls} -> {name}: {prob:.4f}")

    visualize(image_path, result)