# 测试 yolo26 环境
import sys

print("yolo26 环境验证成功！")
print(f"Python 路径: {sys.executable}")
print(f"Python 版本: {sys.version.split()[0]}")

import jupyterlab
print(f"JupyterLab: {jupyterlab.__version__}")

import numpy as np
print(f"NumPy: {np.__version__}")
