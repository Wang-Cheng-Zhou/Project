import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# 打印调试信息
print("=== 程序开始执行 ===")
print(f"OpenCV 版本: {cv2.__version__}")

# 获取当前脚本所在的目录路径
script_dir = os.path.dirname(os.path.abspath(__file__))
print(f"脚本目录: {script_dir}")

# 拼接图片文件的完整路径
img_path = os.path.join(script_dir, 'lenna.jpg')
print(f"图片路径: {img_path}")

# 输出目录
output_dir = os.path.join(script_dir, 'output')
os.makedirs(output_dir, exist_ok=True)
print(f"结果文件将保存到: {output_dir}")

# 检查文件是否存在
if not os.path.exists(img_path):
    print(f"错误：图片文件不存在！请检查路径: {img_path}")
    print("当前目录下的文件列表:")
    print(os.listdir(script_dir))
    raise FileNotFoundError(f'图片文件不存在: {img_path}')

print("图片文件存在，继续执行...")

# 以灰度模式读取图片并检查是否成功
img = cv2.imread(img_path, 0)
if img is None:
    print(f"错误：无法读取灰度图片: {img_path}")
    raise FileNotFoundError(f'无法读取灰度图片: {img_path}')

print(f"灰度图片读取成功，尺寸: {img.shape}")

# 打印灰度图的尺寸（高度, 宽度）
print(f"灰度图尺寸: {img.shape}")

# 以彩色模式读取同一张图片
img1 = cv2.imread(img_path)
if img1 is None:
    print(f"错误：无法读取彩色图片: {img_path}")
    raise FileNotFoundError(f'无法读取彩色图片: {img_path}')

print(f"彩色图片读取成功，尺寸: {img1.shape}")

# 将 BGR 彩色图转换为灰度图
gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

# 分离 B、G、R 三个通道
b, g, r = cv2.split(img1)
print(f"b通道尺寸: {b.shape}")
print(f"g通道尺寸: {g.shape}")
print(f"r通道尺寸: {r.shape}")

# 通过索引方式分别提取 B、G、R 三个通道
b1 = img1[:, :, 0]
g1 = img1[:, :, 1]
r1 = img1[:, :, 2]
print(f"b通道的尺寸: {b1.shape}")
print(f"g通道的尺寸: {g1.shape}")
print(f"r通道的尺寸: {r1.shape}")

# 计算彩色图 B 通道的直方图
print("计算彩色图 B 通道的直方图...")
img_hist = cv2.calcHist([img1], [0], None, [256], [0, 256])
print("直方图计算完成")

# 绘制直方图折线
plt.figure(figsize=(10, 6))
plt.plot(img_hist)
plt.title("B 通道直方图")
plt.xlabel("像素值")
plt.ylabel("像素数量")
plt.xlim([0, 256])
plt.grid(True)
plt.savefig(os.path.join(output_dir, 'b_channel_histogram.png'))
print("已保存 B 通道直方图: b_channel_histogram.png")
plt.close()

# 对灰度图进行直方图均衡化
print("进行直方图均衡化...")
equ_img = cv2.equalizeHist(img)
print("直方图均衡化完成")

# 绘制均衡化后图像的直方图
plt.figure(figsize=(10, 6))
plt.hist(equ_img.ravel(), bins=256, range=(0, 256))
plt.title("均衡化后灰度图直方图")
plt.xlabel("像素值")
plt.ylabel("像素数量")
plt.grid(True)
plt.savefig(os.path.join(output_dir, 'equalized_gray_histogram.png'))
print("已保存均衡化后灰度图直方图: equalized_gray_histogram.png")
plt.close()

# 将原灰度图与均衡化后的图像水平拼接
print("拼接图像...")
res = np.hstack((img, equ_img))
print("图像拼接完成")
result_path = os.path.join(output_dir, 'res.png')
cv2.imwrite(result_path, res)
print(f"已保存拼接图像: {result_path}")

# 计算并显示彩色通道的直方图
print("计算彩色通道直方图...")
chans = cv2.split(img1)
colors = ("b", "g", "r")
plt.figure(figsize=(12, 8))
plt.title("Color Histogram")
plt.xlabel("Bins")
plt.ylabel("# of Pixels")

for (chan, color) in zip(chans, colors):
    hist = cv2.calcHist([chan], [0], None, [256], [0, 256])
    plt.plot(hist, color=color)
    plt.xlim([0, 256])

plt.grid(True)
plt.legend(colors)
plt.savefig(os.path.join(output_dir, 'color_histogram.png'))
print("已保存彩色通道直方图: color_histogram.png")
plt.close()
print("=== 程序执行完成 ===")