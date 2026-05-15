# ai_model\predict.py,只用于加载模型和推测
import torch
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image
import json
import os
from .model import create_model

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "flower_model.pth")

# 加载 mapping
with open(os.path.join(BASE_DIR, "class_to_idx.json"), "r") as f:
    class_to_idx = json.load(f)

idx_to_class = {v: k for k, v in class_to_idx.items()}

# 加载花名
with open(os.path.join(BASE_DIR, "cat_to_name.json"), "r") as f:
    cat_to_name = json.load(f)

transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485,0.456,0.406],
                         [0.229,0.224,0.225])
])


def load_model():
    model = create_model(num_classes=102)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()
    return model


def predict_flower(image_path, model, topk=5):

    img = Image.open(image_path).convert("RGB")
    x = transform(img).unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(x)
        probs = F.softmax(outputs, dim=1)

        top_probs, top_idxs = torch.topk(probs, topk)

        top_probs = top_probs.cpu().numpy().flatten()
        top_idxs = top_idxs.cpu().numpy().flatten()

        classes = [idx_to_class[i] for i in top_idxs]
        names = [cat_to_name[c] for c in classes]

    return {
        "classes": classes,
        "names": names,
        "probs": top_probs.tolist()
    }