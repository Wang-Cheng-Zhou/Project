import cv2
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
img_path = os.path.join(script_dir, 'lenna.jpg')
img = cv2.imread(img_path, 1)  # Load an image from file

if img is None:
    raise FileNotFoundError(f'Cannot read image: {img_path}')

cv2.imshow('img', img)
cv2.imwrite(os.path.join(script_dir, 'lenna01.jpg'), img)

cv2.waitKey(0)
cv2.destroyAllWindows()
print(img.shape)
