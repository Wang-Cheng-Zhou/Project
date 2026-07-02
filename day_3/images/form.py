import os
import cv2
import numpy as np


def perspective_transformation():
    # 获取脚本目录，拼接图片路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, "lenna.jpg")
    # 读取原图
    image_original = cv2.imread(image_path)
    if image_original is None:
        print(f"Error: Could not load image at {image_path}")
        return
    # 获取原图高宽
    H, W = image_original.shape[:2]
    cv2.imshow("Original Image", image_original)

    # 原图中的四个角点
    points1 = np.array([[56, 65], [368, 52], [28, 387], [389, 390]], dtype=np.float32)
    # 目标矩形区域的四个角点
    points2 = np.array([[0, 0], [300, 0], [0, 300], [300, 300]], dtype=np.float32)
    # 计算透视变换矩阵
    mat_perspective = cv2.getPerspectiveTransform(points1, points2)
    # 应用透视变换，校正为俯视视角
    image_perspective = cv2.warpPerspective(image_original, mat_perspective, (W, H))

    cv2.imshow("Perspective Transformation", image_perspective)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def morphology_process():
    # 获取脚本目录，拼接图片路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, "lenna.jpg")
    # 读取原图
    img_ori = cv2.imread(image_path)
    if img_ori is None:
        print(f"Error: Could not load image at {image_path}")
        return
    cv2.imshow("Original Image", img_ori)
    cv2.waitKey(0)

    # 定义 5x5 的矩形卷积核
    kernel = np.ones((5, 5), np.uint8)
    # 腐蚀操作：去除细小噪点
    img_corrosion = cv2.erode(img_ori, kernel, iterations=1)
    cv2.imshow("Corrosion Image", img_corrosion)
    cv2.waitKey(0)

    # 膨胀操作：扩大亮区域
    img_dilation = cv2.dilate(img_ori, kernel, iterations=1)
    cv2.imshow("Dilation Image", img_dilation)
    cv2.waitKey(0)

    # 以灰度模式读取图片
    img_ori02 = cv2.imread(image_path, 0)
    if img_ori02 is None:
        print(f"Error: Could not load grayscale image at {image_path}")
        return
    # 开运算：先腐蚀后膨胀，去除小噪点
    img_open = cv2.morphologyEx(img_ori02, cv2.MORPH_OPEN, kernel)
    cv2.imshow("Opening Image", img_open)
    cv2.waitKey(0)

    # 闭运算：先膨胀后腐蚀，填充小孔洞
    img_close = cv2.morphologyEx(img_ori02, cv2.MORPH_CLOSE, kernel)
    cv2.imshow("Closing Image", img_close)
    cv2.waitKey(0)


# 执行透视变换和形态学处理
perspective_transformation()
morphology_process()


def img_sharpening():
    # 获取脚本目录，拼接图片路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, "lenna.jpg")
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Could not load image at {image_path}")
        return

    # 转换为浮点型以避免溢出
    img_float = img.astype(np.float32)

    # 计算 x 和 y 方向的 Sobel 梯度
    x = cv2.Sobel(img_float, cv2.CV_16S, 1, 0)
    y = cv2.Sobel(img_float, cv2.CV_16S, 0, 1)

    # 取绝对值并转换回 uint8
    absX = cv2.convertScaleAbs(x)
    absY = cv2.convertScaleAbs(y)

    # 按权重合并两个方向的梯度，得到边缘增强图像
    dst = cv2.addWeighted(absX, 0.5, absY, 0.5, 0)

    # 显示原图与锐化结果
    cv2.imshow("Original", img)
    cv2.imshow("Sharpened", dst)
    cv2.waitKey(0)

    def cotour_process():
        # 创建 400x400 的黑色背景图
        img = np.zeros((400, 400), np.uint8)
        # 绘制一个白色填充矩形
        cv2.rectangle(img, (100, 100), (300, 300), 255, -1)
        cv2.imshow("Original", img)
        cv2.waitKey(0)

        # 创建另一张黑色背景图用于绘制轮廓
        img2 = np.zeros((400, 400), np.uint8)
        # 定义矩形轮廓的四个顶点
        cnt = np.array([[[100, 100], [300, 100], [300, 300], [100, 300]]], np.int32)
        # 计算最小外接矩形
        rect = cv2.minAreaRect(cnt)
        # 获取最小外接矩形的四个顶点
        box = cv2.boxPoints(rect)
        # 转换为整数坐标
        box = np.array(box, dtype=np.int32)
        # 绘制轮廓
        cv2.drawContours(img2, [box], 0, 255, 2)
        cv2.imshow("Contour", img2)
        cv2.waitKey(0)