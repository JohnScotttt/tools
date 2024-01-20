# 导入cv2库
import cv2
import numpy as np
from paddleocr import PaddleOCR

# 读取图片文件
img = cv2.imread("receipt_photo.jpg")

# 转换为灰度图像
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 使用高斯滤波去除噪声
blur = cv2.GaussianBlur(gray, (5, 5), 0)

# 使用Canny算法检测边缘
edges = cv2.Canny(blur, 50, 150)

cv2.imshow("Edge", edges)
cv2.imwrite("edges.jpg", edges)
cv2.waitKey(0)

# 使用findContours函数找到轮廓
contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 找到最大的轮廓，假设它是文档的轮廓
max_area = 0
max_contour = None
for contour in contours:
    area = cv2.contourArea(contour)
    if area > max_area:
        max_area = area
        max_contour = contour


# 绘制轮廓并显示图片
cv2.drawContours(img, [max_contour], -1, (0, 255, 0), 3)
cv2.imshow("Contour", img)
cv2.imwrite("contour.jpg", img)
cv2.waitKey(0)

# 获取轮廓的四个顶点，并按照左上，右上，右下，左下的顺序排序
points = max_contour.reshape(-1, 2)
sums = points.sum(axis=1)
diffs = points[:, 0] - points[:, 1]
tl = points[sums.argmin()]
bl = points[diffs.argmin()]
br = points[sums.argmax()]
tr = points[diffs.argmax()]
src = np.array([tl, tr, br, bl], dtype="float32")

# 计算目标图片的宽度和高度
width = max(int(np.sqrt((tl[0] - tr[0]) ** 2 + (tl[1] - tr[1]) ** 2)), int(np.sqrt((bl[0] - br[0]) ** 2 + (bl[1] - br[1]) ** 2)))
height = max(int(np.sqrt((tl[0] - bl[0]) ** 2 + (tl[1] - bl[1]) ** 2)), int(np.sqrt((tr[0] - br[0]) ** 2 + (tr[1] - br[1]) ** 2)))
dst = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]], dtype="float32")

# 计算透视变换矩阵并进行变换
M = cv2.getPerspectiveTransform(src, dst)
warped = cv2.warpPerspective(img, M, (width, height))

# 显示变换后的图片
cv2.imshow("Warped", warped)
cv2.imwrite("warped.jpg", warped)
cv2.waitKey(0)

# ocr
ocr = PaddleOCR(use_angle_cls=True, lang="ch")
ocr_img = "warped.jpg"
result = ocr.ocr(ocr_img, cls=True)

# 写文件
with open(file="result.txt", mode="w", encoding="utf-8") as txt:
    for line in result[0]:
        txt.write(line[1][0]+"\n")

