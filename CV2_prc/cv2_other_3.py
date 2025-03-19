import cv2

img = cv2.imread('C:/new/spot.png')
h = img.shape[0]
w = img.shape[1]

print('The image dimension is %d * %d' %(w ,h))

for i in range(0, h - 1):
    for j in range(0, w - 1):
        if img[i,j] == 255:
            print(i,j)

cv2.imshow('spot', img)

cv2.waitKet()