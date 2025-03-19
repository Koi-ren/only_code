#이미지 스케일(크기 호은 사이즈) 변환

import cv2
import numpy as np

img = cv2.imread('C:/new/slope_test.jpg')
img_scaled = cv2.resize(img,None,fx = 1.2, fy = 1.2, interpolation = cv2.INTER_LINEAR)
cv2.imshow('Scaling - Lineaar Interpolation', img_scaled)
img_scaled = cv2.resize(img, (400, 450), interpolation = cv2.INTER_AREA)
cv2.imshow('Scaling - skewed Size', img_scaled)
cv2.waitKey()