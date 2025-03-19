#이미지 가져오기

import cv2

gray_img = cv2.imread('C:/new/slope_test1.jpg',cv2.IMREAD_GRAYSCALE)
cv2.imshow('Grayscale', gray_img)
cv2.imwrite('C:/new/slope_test1.jpg',gray_img)
cv2.waitKey()
