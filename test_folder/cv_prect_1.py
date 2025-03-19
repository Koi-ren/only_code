import numpy as np
import cv2

#color 설정
blue_color =(255,0,0)
green_color = (0,255,0)
red_color = (0,0,255)
white_color = (255,255,255)

#points 설정
points1 = np.array([[10, 10], [170, 10],[200, 230], [70, 70], [50, 150]],np.int32)
points2 = np.array([[110, 110],[270, 110], [300, 330], [170, 170], [150, 250]], np.int32)

img = np.zeros((384,382,3), np.uint8)
#그리기
img = cv2.fillPoly(img, [points1], blue_color)
img = cv2.fillPoly(img, [points2],green_color)

cv2.imshow('fillPoly',img)
cv2.waitKey(0)