#이미지 위치를 옮기기(트렌스레이션(translation))

import cv2
import numpy as np

img = cv2.imread('C:/new/slope_test.jpg')
num_rows, num_cols = img.shape[:2]

translation_matrix = np.float32([ [1,0,70], [0,1,110] ])
img_translation = cv2.warpAffine(img, translation_matrix, (num_cols, num_rows))
cv2.imshow('translation', img_translation)
cv2.waitKey()