# cnn-flower-recognition-miniprogram
# 开发日志 - 花卉识别系统

## 2026-01-21 Day 1: 项目启动
### 步骤流程
1.  **环境搭建**：在终端中用“python -m venv venv”成功创建虚拟环境 `(venv)`；用“venv\Scripts\activate”激活环境
2.  **依赖安装**：使用 `pip` 安装 Flask 3.1.2 等核心库，创建app.py。
3.  **服务开发**：完成最小 Flask 应用 (`app.py`)，包含：
    - 根路径 `/` 健康检查
    - **核心接口** `POST /predict`：接收图片文件并返回模拟识别结果
4.  **集成测试通过**：使用 `curl.exe` 调用 `/predict` 接口成功，收到预期JSON响应；通过本地访问http://127.0.0.1:5000模拟客户端用户
5.  **项目结构（一步一步完善的）**:

        project
        ├── ai_model/（AI模型）
            └── uploads/    :存放测试图片
            └── cat_to_name.json/    : 花卉映射关系
            └── class_to_idx.json    ：存储类别和下标的关系
            └── split_dataset.py     ：1.Oxford划分数据集，比例8：1：1
            └── data_preprocess.py   ：2.数据预处理
            └── model.py             ：3.创建模型
            └── train.py             : 4.训练模型
            └── predict.py           ：5.封装调用模型接口
            └── local_test.py        ：6.本地第一次测试模型是否可以调用
            └── flower_model.pth     ：7.训练好保存的模型
            └── training_curve.png   ：8 训练的曲线图
        ├── backend/（后端）
           └── static/              ：1.存放需要展示的示例花卉
            └── uploads/             ：2.暂时存放用户上传的花卉
            └── app.py               ：3.后端启动服务
            └── init_db.py           ：4.初始化数据库
            └── import_flower.py     ：5.导入102条花卉信息
            └── insert_flower.py     ：6.导入102花卉的部分详细信息
            └── flowers.db           ：7.数据库
            └── get_102flowers.py    ：8.获取102花卉的示例图片
        ├──  data/（数据）
        │   └── dataset/             ：1.存放所有图片文件
                └── test
                └── val
                └── train         
            └── raw                  ：2.未处理的原始文数据
        ├── miniprogram（前端）
            └── images/              ：1.存储前端展示需要的部分图片
            └── pages/               ：2.存储各种页面开发代码
            └── utils/               ：3.数据和外面通路需要的配置，包括IP
        ├── venv/           ：虚拟环境
        └── requirements.txt：记录依赖关系
        ├── progress.md ：记录文档

### 技术快照
- **项目路径**：`C:\Users\86159\Desktop\flower_ai_project`
- **虚拟环境**：已激活，依赖完全隔离
- **关键命令**：
    ```bash
    # 激活环境
    .\venv\Scripts\Activate.ps1
    ```

## 2026-04-06 Day 2: 获取数据集✅
### 步骤流程
1. **获取数据集：** 官网下载数据集并自行完成分类任务，按照8：1：1比例完成用split_dataset.py分类


## 2026-04-07 Day 3: 规范写法，训练模型一次 
### 步骤流程
1.  **预处理图像：** data_preprocess.py完成
2.  **训练模型：**train.py完成一次训练，保存模型（前期本机上面运行，后期在服务器上面进行）
3.  **训练评估值的学习**Train Acc，Val Acc，Test Acc，loss
4.  **完成一次测试**测试向日葵（下面是输出）：
            - Using device: cpu
            - Enter image path to predict: test.jpg
            - Top predictions (编号 -> 花名 -> 概率):
            - 54 -> sunflower: 0.9171
            - 41 -> barbeton daisy: 0.0341
            - 49 -> oxeye daisy: 0.0265
            - 5 -> english marigold: 0.0074
            - 63 -> black-eyed susan: 0.0043
4.  **确定模型框架：**完成项目框架

## 2026-04-08 Day 4: 规范写法，开始进行后端操作
### 具体
1. **重新写训练代码：** 可以画出loss和accuracy曲线并保存
2. **Flask API接口调试：** 完成本地调试，可以以JSON格式返回结果

## 2026-04-12 Day 5: 阅读代码查缺补漏
### 成果
1. **读代码：** 划分数据集的代码
2. **阅读理解训练代码：** 修改路径
3. **后续优化✅：** 数据预处理，之后可以增加一条数据增强，可以加强模型的泛化能力

## 2026-04-13 Day 6: 阅读代码查缺补漏
### 成果
1. **代码优化：** 在train.py中添加一个mapping映射，后面调用模型的时候可以不用训练集
2. **代码优化：** 将模型预测和本地测试可视化分开为predict.py和local_test.py，predict.py可以供本地使用，也可以供Flask使用
3.  **跑通所做过的整个流程：**  运行app.py,使用curl.exe -X POST http://127.0.0.1:5000/predict -F "image=@C:/Users/86159/Desktop/flower_ai_project/ai_model/uploads/carnation.jpg"完成测试
4.  **后续可优化1（本人没有完成）✅：** 学习了微调+冻结，目前我的是修改了分类层+全局微调，之后可以冻结卷积层+微调后面的参数
5.  **后续可优化2（已经完成）✅：** train.py的绘图曲线可以标注数据，更加方便直接；除了在训练集上面的loss曲线，还要有在验证集上的loss曲线

## 2026-04-14 Day 7: 搭建前端

## 2026-04-15 Day 8: JavaScript函数优化，还有IP地址
### 重要点：
1. **关于域名：** 微信开发者工具 → 详情 → 本地设置 → 不校验合法域名（仅仅用于本地测试）
2. **使用SQLite数据库:** 方便，仅仅需要3个表

## 2026-04-16 Day 9:决定连接数据库
###
1. 先用backend\get_102flowers.py生成示例图片
2. 再用backend\init_db.py创建数据库，是SQLite
3. 后用backend\import_flower插入花卉数据
4. 将app.py补充完整，并完成前端的修改
5. **这个没有经过测试（本人没有成功使用，所以放弃了）：** 真机测验但是要https格式，下载工具 “ngrok”，在cmd输入：ngrok config add-authtoken 3CRMhQ9QPn16o2TxYYe1lZZk4rK_4mrRuxwm6LoHU49CWWafP,运行app.py,另外在cmd输入ngrok http 5000，找到给的https地址，更改路径

## 2026-04-16 Day 10:利用SQLite数据库
1. 正式全线跑通，用ngrok无果，无法解决https的问题

## 2026-04-18 Day 11:决定用域名服务器（结果失败）
1. 用阿里云免费服务器创建实例，进入之后：
sudo apt update && sudo apt upgrade -y（更新资源）
2. 选择：keep the local version currently installed
（保留当前本地配置）
3. 继续输入sudo apt install python3-pip nginx -y
4. 下载WinSCP，输入IP和密码，进入home/admin建立项目
5. 全选将本地的文件拖入到服务器中
进入目录：cd /home/admin/flower_ai_project
6. 更新设置
sudo apt update && sudo apt upgrade -y（更新资源）
sudo apt install python3-pip -y
7. 安装虚拟环境sudo apt install python3-venv -y
8. 清除旧的虚拟环境sudo rm -rf venv
9. 创建python3 -m venv venv虚拟环境
10. 激活虚拟环境source venv/bin/activate
deactivate退出虚拟环境
11. 安装之前的库，pip install flask numpy pillow torch torchvision
12. sudo $(which python) app.py
## 2026-04-19 Day 12:用域名服务器（结果失败）


## 2026-04-20 Day 13:买GPU服务器
1. 购买阿里云免费的服务器DSW创建实例，选择镜像，不要再安装torch库了，选择适合的Pytorch镜像，还要选择GPU，选择2.5.0版本  
2. 创建Notebook 把文件拖进来，将数据打包为data.zip,  
        apt-get update  
        apt-get install unzip -y安装unzip用于解压.zip文件  
        unzip data.zip -d data解压文件
3. 进入cd /mnt/workspace/flower_ai_project
4. 进行训练train.py,并且手动安装需要的依赖  

## 2026-04-21 Day 14:训练一下，基本没干什么
## 2026-04-22 Day 15:使用 overleaf（本人没有学会），可以用于画图、写代码的工具，但可以用viso代替用来画图，很方便
去github下载库https://github.com/HarisIqbal88/PlotNeuralNet/tree/master/pycore

## 2026-05-15 Day ？:所有毕业结束，整理内容
![展示](result_show\1登录.png)
<center> 图1 用户注册登录界面 </center>

![展示](result_show\2导航.png)
<center> 图2 页面导航 </center>

![展示](result_show\3花卉识别展示.png)
<center> 图3 花卉识别展示1 </center>

![展示](result_show\4花卉识别展示.png)
<center> 图4 花卉识别展示2 </center>

![展示](result_show\5收藏展示.png)
<center> 图5 收藏功能展示 </center>

![展示](ai_model\training_curve.png)
<center> 图6 模型训练结果展示 </center>
