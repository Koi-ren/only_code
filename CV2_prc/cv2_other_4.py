import cv2

img = cv2.imread('C:/new/cars.png',cv2.IMREAD_GRAYSCALE)

cv2.imshow('car', img[120:270, 270:460])

cv2.waitKey()