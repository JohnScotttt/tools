import argparse
import sys
import cv2
import numpy as np
from paddleocr import PaddleOCR

# parser = argparse.ArgumentParser()
# parser.add_argument('--img-path', type=str, required=True)
# args = parser.parse_args()

img = cv2.imread(sys.argv[1])
# img = cv2.imread(args.img_path)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 0)
edges = cv2.Canny(blur, 50, 150)
contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
max_area = 0
max_contour = None
for contour in contours:
    area = cv2.contourArea(contour)
    if area > max_area:
        max_area = area
        max_contour = contour
points = max_contour.reshape(-1, 2)
sums = points.sum(axis=1)
diffs = points[:, 0] - points[:, 1]
tl = points[sums.argmin()]
bl = points[diffs.argmin()]
br = points[sums.argmax()]
tr = points[diffs.argmax()]
src = np.array([tl, tr, br, bl], dtype="float32")
width = max(int(np.sqrt((tl[0] - tr[0]) ** 2 + (tl[1] - tr[1]) ** 2)), int(np.sqrt((bl[0] - br[0]) ** 2 + (bl[1] - br[1]) ** 2)))
height = max(int(np.sqrt((tl[0] - bl[0]) ** 2 + (tl[1] - bl[1]) ** 2)), int(np.sqrt((tr[0] - br[0]) ** 2 + (tr[1] - br[1]) ** 2)))
dst = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]], dtype="float32")
M = cv2.getPerspectiveTransform(src, dst)
warped = cv2.warpPerspective(img, M, (width, height))
ocr = PaddleOCR(use_angle_cls=True, lang="ch")
ocr_img = "warped.jpg"
result = ocr.ocr(ocr_img, cls=True)
with open(file="result.txt", mode="w", encoding="utf-8") as txt:
    for line in result[0]:
        txt.write(line[1][0]+"\n")