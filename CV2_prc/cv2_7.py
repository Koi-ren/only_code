#이미지 회전 (안짤리게 중앙쪽으로)

import cv2
import numpy as np

img = cv2.imread('C:/new/slope_test.jpg')
num_rows, num_cols = img.shape[:2]

translation_matrix = np.float32([ [1,0,int(0.5*num_cols)], [0,1,int(0.5*num_rows)] ])
#2*num_cols, 2*num_rows))
rotation_matrix = cv2.getRotationMatrix2D((num_cols, num_rows), 30, 0.5)
img_translation = cv2.warpAffine(img, translation_matrix, (2*num_cols, 2*num_rows))
img_rotation = cv2.warpAffine(img_translation, rotation_matrix, (3*num_cols, 3*num_rows))

cv2.imshow('Roatation', img_rotation)
cv2.waitKey()