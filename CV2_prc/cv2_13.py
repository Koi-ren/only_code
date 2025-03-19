#투상 변환 3 (영상 와핑)

import cv2
import numpy as np
import math

img = cv2.imread('C:/new/slope_test.jpg', cv2.IMREAD_GRAYSCALE)
rows, cols = img.shape[:2]

#------------------------------#
# Vertical wave
#------------------------------#

img_output = np.zeros(img.shape, dtype = img.dtype)

for i in range(rows):
    for j in range(cols):
        offset_x = int(25.0*math.sin(2*3.14*i/180))
        offset_y = 0
        if i + offset_x < rows: #여기서 i를 j로 바꾸면 사진의 반만 변환되고 나머지 반은 삭제됨
            img_output[i,j] = img[i,(j + offset_x)%cols]
        else:
            img_output[i,j] = 0

cv2.imshow('Input', img)
cv2.imshow('Vertical wave', img_output)

#------------------------------#
# Horizontal wave
#------------------------------#

img_output = np.zeros(img.shape, dtype = img.dtype)

for i in range(rows):
    for j in range(cols):
        offset_x = 0
        offset_y = int(16.0*math.sin(2*3.14*j/150))
        if i + offset_y < rows:
            img_output[i,j] = img[(i+offset_y)%rows,j]
        else:
            img_output[i,j] = 0

cv2.imshow('Horizontal wave', img_output)

#------------------------------#
# Both horizontal and vertical
#------------------------------#

img_output = np.zeros(img.shape, dtype = img.dtype)

for i in range(rows):
    for j in range(cols):
        offset_x = int(20.0*math.sin(2*3.14*i/150))
        offset_y = int(20.0*math.cos(2*3.14*j/150))
        if i + offset_y < rows and j + offset_x < cols:
            img_output[i,j] = img[(i + offset_y)%rows, (j +offset_x)%cols]
        else:
            img_output[i,j] = 0

cv2.imshow('Multidirection wave', img_output)

#------------------------------#
# Concave effect
#------------------------------#

img_output = np.zeros(img.shape, dtype = img.dtype)

for i in range(rows):
    for j in range(cols):
        offset_x = int(128.0*math.sin(2*3.14*i/(2*cols)))
        offset_y = 0
        if j + offset_x < cols:
            img_output[i,j] = img[i,(j + offset_x)%cols]
        else:
            img_output[i,j] = 0

cv2. imshow('Concave', img_output)

cv2.waitKey()