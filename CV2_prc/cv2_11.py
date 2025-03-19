#투상 변환 1 (사각형이 그려진 종이가 기울어지면 사각형이 사다리꼴로 보이는 것과 같은 이치의 변환)

import cv2
import numpy as np

img = cv2.imread('C:/new/slope_test.jpg')
rows, cols = img.shape[:2]

src_points = np.float32([[0,0], [cols-1,0], [0,rows-1], [cols-1,rows-1]])
dst_poinst = np.float32([[0,0], [cols-1,0], [int(0.33*cols),rows-1], [int(0.66*cols),rows-1]])

projective_matrix = cv2.getPerspectiveTransform(src_points, dst_poinst)
img_output = cv2.warpPerspective(img, projective_matrix, (cols,rows))

cv2.imshow('Input', img)
cv2.imshow('Output', img_output)
cv2.waitKey()
