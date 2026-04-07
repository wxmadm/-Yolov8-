# 基于Yolov8的汽车速度检测的设计与实现

> 🚀 本项目提供了一套完整的从零开始搭建 YOLOv8 GPU 加速环境的流程，涵盖了从驱动检测到 TensorRT 加速及项目依赖安装的全过程。

## 📋 目录
- [1. 基础环境准备](#1-基础环境准备)
- [2. TensorRT 加速配置](#2-tensorrt-加速配置)
- [3. 虚拟环境搭建](#3-虚拟环境搭建)

## 1. 基础环境准备

在开始安装前，请确认硬件兼容性并准备好相关安装包：

- **CUDA 兼容性**：前往 [PyTorch 官网](https://pytorch.org/) 检查您的显卡是否支持 **CUDA 11.8**。
- **Anaconda**：请参考相关教程完成 Anaconda 的安装。
- **资源包准备**：从网盘下载提供的 CUDA 和 cuDNN 压缩包。

⚠️ **注意**：按照视频安装完 CUDA/cuDNN 后，**请立即暂停**，不要盲目跟随视频执行 `pip install ultralytics`。

## 2. TensorRT 加速配置

为了进一步提升模型的推理速度，我们需要手动配置 TensorRT 8.4：

1. 观看 TensorRT 8.4 安装教程视频。
2. 安装完 cuDNN 后，将 TensorRT 的相关文件**替换**到 CUDA 的安装目录中。
3. **重要提示**：此处仅进行物理文件替换，暂不要进行任何 `pip` 安装操作。

## 3. 虚拟环境搭建

强烈建议使用 Conda 隔离开发环境，避免全局包冲突。

### 3.1 创建与激活环境

```bash
# 创建名为 car 的环境，指定 Python 3.11
conda create -n car python=3.11

# 激活环境
conda activate car

### 3.2 核心深度学习库安装

#安装 Ultralytics：
pip install ultralytics==8.2.2

#配置 PyTorch
conda install pytorch==2.2.2 torchvision==0.17.2 torchaudio==2.2.2 pytorch-cuda=11.8 -c pytorch -c nvidia
```

### 3.3 其他依赖包安装
pip install -r requirements.txt


## 4. 效果展示图
![900d09f8a1dae08db9146a7913e461b6](https://github.com/user-attachments/assets/112b791d-e6be-446b-8469-e11e0a256578)

