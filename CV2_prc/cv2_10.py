#어파인 변환(기하학적 변환) - 거울모드

import cv2
import numpy as np

img = cv2.imread('C:/new/slope_test.jpg')
rows, cols = img.shape[:2]

src_points = np.float32([[0,0], [cols-1,0], [0,rows-1]])
dst_points = np.float32([[cols-1,0], [0,0], [cols-1, rows-1]])

affine_matrix = cv2.getAffineTransform(src_points, dst_points)
img_output = cv2.warpAffine(img, affine_matrix, (cols, rows))

cv2.imshow('Input', img)
cv2.imshow('Output', img_output)
cv2.waitKey()