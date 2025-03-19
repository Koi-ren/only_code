#이미지 위치를 옮기기 (중앙으로)

import cv2
import numpy as np

img = cv2.imread('C:/new/slope_test.jpg')
num_rows, num_cols = img.shape[:2]

translation_matrix = np.float32([[1,0,70], [0,1,110]])
img_translation = cv2.warpAffine(img, translation_matrix, ( num_cols + 70, num_rows + 110))
#translation_matrix = np.float32([[1,0,-30], [0,1,-50]])
#img_translation = cv2.warpAffine(img_translation, translation_matrix, (num_cols + 70 +30, num_rows + 110 + 50))
cv2.imshow('Traslation', img_translation)
cv2.waitKey()