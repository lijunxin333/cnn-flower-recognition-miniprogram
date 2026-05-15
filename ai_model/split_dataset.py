# ai_model\split_dataset.py
import os
import shutil
import scipy.io
import numpy as np
from sklearn.model_selection import train_test_split

# 代码功能：完成数据集的切分

# 设置文件路径
image_dir = "../data/raw/102flowers"       # 存储的图片文件夹
label_path = "../data/raw/imagelabels.mat" # 标签文件
output_dir = "../data/dataset"             # 分类后的输出文件夹


# 清空旧数据
if os.path.exists(output_dir):
    shutil.rmtree(output_dir)

# 1 加载标签
labels = scipy.io.loadmat(label_path)["labels"][0] # matlab存储标签，从字典里面取出来标签，并取得二维列表的的第一个

print("Total images:", len(labels))                #多少个数字就有多少个图片
print("Number of classes:", len(set(labels)))      #变为set（集合），可以自动去掉重复的，所以获取了种类个数


# 2 生成图像索引，从0开始给每一张图片编号
all_indices = np.arange(len(labels))    #返回列表[0,1,2...]


# 3 第一次划分 (80% 训练 + 20% 剩余)
train_idx, temp_idx = train_test_split(#返回两组图片编号
    all_indices,
    test_size=0.2,
    random_state=42,                   #固定随机
    stratify=labels                    #按类别均匀切割
)


# 4 二次划分 (10% 验证集 + 10% 测试集)
val_idx, test_idx = train_test_split(
    temp_idx,
    test_size=0.5,
    random_state=42,        
    stratify=labels[temp_idx]
)


print("\nDataset split result:")
print("Train:", len(train_idx))
print("Validation:", len(val_idx))
print("Test:", len(test_idx))


# 5 创建文件夹并复制图片
def save_split(idx_list, split_name):

    print(f"\nProcessing {split_name} set... ({len(idx_list)} images)")

    for idx in idx_list:

        img_name = f"image_{idx+1:05d}.jpg"  #生成图像名字，图像编号应该从1开始
        class_id = str(labels[idx])          #获取类别号，将数字转换成字符

        src_path = os.path.join(image_dir, img_name) #源图片位置
        dst_dir = os.path.join(output_dir, split_name, class_id) #拼接路径

        os.makedirs(dst_dir, exist_ok=True)

        dst_path = os.path.join(dst_dir, img_name) #目标路径

        shutil.copy(src_path, dst_path)            #复制图片


# 6 执行划分，分3次完成
save_split(train_idx, "train")
save_split(val_idx, "val")
save_split(test_idx, "test")


print("\nDataset split finished!")
print(f"Train set: {len(train_idx)}")
print(f"Validation set: {len(val_idx)}")
print(f"Test set: {len(test_idx)}")


# 7 检查数据结构
print("\nChecking dataset structure...")

for split in ["train", "val", "test"]:

    split_path = os.path.join(output_dir, split)

    class_num = len(os.listdir(split_path))

    print(f"{split} classes:", class_num)

print("\nCheck finished!")