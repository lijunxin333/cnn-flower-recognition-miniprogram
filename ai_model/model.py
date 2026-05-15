# model.py
import torch
import torch.nn as nn
from torchvision import models

# 代码功能：完成模型测试

def create_model(num_classes=102):

    # 加载预训练好的模型 MobileNetV2
    model = models.mobilenet_v2(weights="DEFAULT")

    # 获取原分类层输入特征数,实际为1280
    in_features = model.classifier[1].in_features
    
    # 修改分类层为102类，微调，共计in_features个特征
    model.classifier[1] = nn.Linear(in_features, num_classes)

    return model


if __name__ == "__main__":

    model = create_model()

    print(model)

    # 测试前向传播
    x = torch.randn(1,3,224,224)

    y = model(x)

    print("Output shape:", y.shape)