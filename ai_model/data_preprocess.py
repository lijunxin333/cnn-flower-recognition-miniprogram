# ai_model\data_preprocess.py，利用pytorch完成

from torchvision import datasets, transforms
from torch.utils.data import DataLoader

# 代码功能：图片数据处理，并为模型提供张量输入

# 数据路径
train_dir = "../data/dataset/train"
val_dir = "../data/dataset/val"
test_dir = "../data/dataset/test"

# 训练集数据增强（数据增强）
train_transform = transforms.Compose([
    transforms.Resize((256, 256)),              # 先放大一点
    transforms.RandomResizedCrop(
        224,
        scale=(0.75, 1.0)),                      # 随机裁剪(但不能剪裁太多)
    transforms.RandomHorizontalFlip(),          # 随机水平翻转
    transforms.RandomRotation(10),              # 随机旋转
    transforms.ColorJitter(                     # 颜色扰动
        brightness=0.1,
        contrast=0.1,
        saturation=0.1,
        hue=0.02
    ),
    transforms.ToTensor(),
    transforms.Normalize(
        [0.485, 0.456, 0.406],
        [0.229, 0.224, 0.225]
    )
])

# 验证集，测试集（不能增强）
val_transform = transforms.Compose([
    transforms.Resize((224, 224)),  # 或 Resize + CenterCrop
    transforms.ToTensor(),
    transforms.Normalize(
        [0.485, 0.456, 0.406],
        [0.229, 0.224, 0.225]
    )
])
test_transform = val_transform

# # 图像预处理，transform是图片处理工具
# transform = transforms.Compose([          #保存处理参数
#         transforms.Resize((224,224)),     #将图片改成224x224 大小
#         transforms.ToTensor(),            #把图片转成模型能看懂的张量
#         transforms.Normalize(             #标准化，将像素数值压缩到-1~1之间
#              [0.485,0.456,0.406],         #ImageNet 数据集均值、标准差
#                [0.229,0.224,0.225])         
# ])

# 读取后自动预处理、加上标签（从0开始的，相当于建立了一个对应的标签表）
# 格式为(图片, 标签)
train_dataset = datasets.ImageFolder(train_dir, transform=train_transform)
val_dataset = datasets.ImageFolder(val_dir, transform=val_transform)
test_dataset = datasets.ImageFolder(test_dir, transform=test_transform)

# 将数据集打包，一次32张图片                              打乱顺序
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=32)
test_loader = DataLoader(test_dataset, batch_size=32)

print("Train samples:", len(train_dataset))
print("Val samples:", len(val_dataset))
print("Test samples:", len(test_dataset))

print("Number of classes:", len(train_dataset.classes))

# 测试训练
for images, labels in train_loader:
    print("Batch shape:", images.shape)
    print("Labels:", labels.shape)
    break