#투상 변환 2

import cv2
import numpy as np

img = cv2.imread('C:/new/slope_test.jpg')
rows, cols = img.shape[:2]

src_points = np.float32([[0,0], [0,rows-1], [cols/2,0], [cols/2,rows-1]])
dst_poinst = np.float32([[0,100], [0,rows -101], [cols/2,0], [cols/2,rows-1]])

projective_matrix = cv2.getPerspectiveTransform(src_points, dst_poinst)
img_output = cv2.warpPerspective(img, projective_matrix, (cols,rows))

cv2.imshow('Input', img)
cv2.imshow('Output', img_output)
cv2.waitKey()
