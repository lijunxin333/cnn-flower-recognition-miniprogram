# train.py
import torch
import torch.nn as nn
import torch.optim as optim
from tqdm import tqdm
import matplotlib.pyplot as plt
import os
import json

from data_preprocess import train_loader, val_loader, test_loader
from model import create_model

# 模型存储路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "flower_model.pth")


# 1. 设备
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)

# 2. 创建模型
model = create_model(num_classes=102)
model = model.to(device)

# 3. 损失函数和优化器
criterion = nn.CrossEntropyLoss(label_smoothing=0.1)
optimizer = optim.Adam(model.parameters(), 1e-4, weight_decay=1e-4)

# 4. 训练轮数
epochs = 10

# 5. 训练记录
train_losses = []
val_losses = []
train_accs = []
val_accs = []

best_val_acc = 0.0

# 6. 训练循环,从0开始
for epoch in range(epochs):
    print(f"\n===== Epoch {epoch+1}/{epochs} =====")
    model.train()     #通知模型开始训练
   
   # 训练集
    running_loss = 0.0
    correct = 0
    total = 0

    # 多了一个进度条的功能，仍然是train_loader
    progress_bar = tqdm(train_loader, desc="Training")
    for images, labels in progress_bar:
        # 将图片送入device中计算，因为模型也在device里面
        images, labels = images.to(device), labels.to(device)

        optimizer.zero_grad()             #清空旧的梯度
        outputs = model(images)           #预测结果
        loss = criterion(outputs, labels) #算loss值，张量形式
        loss.backward()                   #计算梯度，告诉模型错在哪里
        optimizer.step()                  #修改参数

        running_loss += loss.item()          #取出增长量中的数
        _, predicted = torch.max(outputs, 1) #返回概率最大值，最大值的位置

        total += labels.size(0)                       #总共数量
        correct += (predicted == labels).sum().item() #猜对的数量

        progress_bar.set_postfix(loss=loss.item(),acc=100 * correct / total) 

    train_loss = running_loss / len(train_loader)
    train_acc = 100 * correct / total

    train_losses.append(train_loss)  #存进列表中
    train_accs.append(train_acc)

    print(f"Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.2f}%")


    # 验证集
    model.eval()
    val_loss = 0.0
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in val_loader:
            images, labels = images.to(device), labels.to(device)
            
            outputs = model(images)
            loss = criterion(outputs, labels)
            val_loss += loss.item()

            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    
    val_loss = val_loss / len(val_loader)
    val_acc = 100 * correct / total
    val_accs.append(val_acc)
    val_losses.append(val_loss)

    print(f"Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.2f}%")

    # 保存最优模型
    if val_acc > best_val_acc:
        best_val_acc = val_acc
        torch.save(model.state_dict(), model_path)
        print("Saved best model with val acc: {:.2f}%".format(best_val_acc))


# 保存映射
class_to_idx = train_loader.dataset.class_to_idx
with open(os.path.join(BASE_DIR, "class_to_idx.json"), "w") as f:
    json.dump(class_to_idx, f)

# 7. 测试集评估
print("\n===== Testing Best Model =====")
model.load_state_dict(torch.load(model_path, map_location=device))
model.eval()

correct = 0
total = 0
with torch.no_grad():
    for images, labels in test_loader:
        images, labels = images.to(device), labels.to(device)
        outputs = model(images)
        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

test_acc = 100 * correct / total
print(f"Test Accuracy: {test_acc:.2f}%")

# 8. 绘制 Loss & Accuracy 曲线
# 绘制数据的关键点
def annotate_key_points(x, y):
    import numpy as np

    y = np.array(y)
    x = list(x)

    # 找关键点索引
    max_idx = y.argmax()
    min_idx = y.argmin()
    last_idx = len(y) - 1

    key_indices = set([max_idx, min_idx, last_idx])

    for idx in key_indices:
        plt.text(
            x[idx], y[idx],
            f"{y[idx]:.2f}",
            ha='center',
            va='bottom',
            fontsize=9,
            color='red'
        )

plt.figure(figsize=(12,5))

# Loss曲线
plt.subplot(1,2,1)
epochs_range = range(1, epochs+1)

plt.plot(epochs_range, train_losses, marker='o', label='Train Loss')
plt.plot(epochs_range, val_losses, marker='o', label='Val Loss')

annotate_key_points(epochs_range, train_losses)
annotate_key_points(epochs_range, val_losses)

plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Training Loss vs Validation Loss')
plt.grid(True)
plt.legend()

# Accuracy曲线
plt.subplot(1,2,2)
plt.plot(epochs_range, train_accs, marker='o', label='Train Acc')
plt.plot(epochs_range, val_accs, marker='o', label='Val Acc')

annotate_key_points(epochs_range, train_accs)
annotate_key_points(epochs_range, val_accs)

plt.xlabel('Epoch')
plt.ylabel('Accuracy (%)')
plt.title('Accuracy')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.savefig("training_curve.png")
plt.show()

print("\nTraining finished. Best model saved as flower_model.pth")