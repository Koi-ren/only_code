#엣지 탐지

import cv2
import numpy as np

img = cv2.imread('C:/new/slope_test.jpg', cv2.IMREAD_GRAYSCALE)
rows, cols = img.shape[:2]

sobel_horizontal = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize = 5)  #수평 엣지 탐지
sobel_vertical = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize = 5)  #수직 엣지 탐지
laplacian = cv2.Laplacian(img, cv2.CV_64F)  #양방향 2차 미분
canny = cv2.Canny(img, 50, 240)

cv2.imshow('Original', img)
#cv2.imshow('Sobel horizontal', sobel_horizontal)
#cv2.imshow('Sobel vertical', sobel_vertical)
#cv2.imshow('laplacian', laplacian)
cv2.imshow('canny edge', canny)

cv2.waitKey(0)
