import cv2
import os

# 获取当前脚本所在的目录路径
script_dir = os.path.dirname(os.path.abspath(__file__))
# 拼接图片文件的完整路径
img_path = os.path.join(script_dir, 'lenna.jpg')
# 以彩色模式读取图片
img = cv2.imread(img_path, 1)

# 检查图片是否读取成功
if img is None:
    raise FileNotFoundError(f'Cannot read image: {img_path}')

# 在窗口中显示图片
cv2.imshow('img', img)
# 将图片保存为新文件
cv2.imwrite(os.path.join(script_dir, 'lenna01.jpg'), img)

# 等待键盘按键后关闭窗口
cv2.waitKey(0)
cv2.destroyAllWindows()
# 打印图片的尺寸信息（高度, 宽度, 通道数）
print(img.shape)
