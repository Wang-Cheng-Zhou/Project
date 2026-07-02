import cv2
import os

# 获取脚本目录，拼接视频文件路径和输出路径
script_dir = os.path.dirname(os.path.abspath(__file__))
video_path = os.path.join(script_dir, '1.mp4')
output_path = os.path.join(script_dir, 'output.avi')

# 打开视频文件
cap = cv2.VideoCapture(video_path)

# 检查视频是否成功打开
if not cap.isOpened():
    print(f"Error: Could not open video at {video_path}")
    exit()

# 设置视频编码器为 XVID
fourcc = cv2.VideoWriter.fourcc(*'XVID')
# 获取原视频的帧率
fps = cap.get(cv2.CAP_PROP_FPS)
# 获取原视频的帧宽高
size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
# 创建视频写入器
out = cv2.VideoWriter(output_path, fourcc, fps, size)

while True:
    # 逐帧读取视频
    ret, frame = cap.read()
    # 读取失败表示视频结束
    if not ret:
        print("视频播放完毕")
        break

    # 在每一帧上添加文字
    cv2.putText(frame, "Hello, OpenCV!", (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # 将处理后的帧写入输出视频
    out.write(frame)
    # 显示当前帧
    cv2.imshow('frame', frame)

    # 按 'q' 键提前退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放视频读取器和写入器
cap.release()
out.release()
# 关闭所有 OpenCV 窗口
cv2.destroyAllWindows()
