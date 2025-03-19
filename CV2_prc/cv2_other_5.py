import cv2
import numpy as np

#img = cv2.imread('C:/new/cars.png')
#img = cv2.imread('C:/new/road.png')
img = cv2.imread('C:/new/solidWhiteCurve.jpg')
h = img.shape[0]
w = img.shape[1]

print('The image dimension is %d * %d' %(w ,h))

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

lower_white = np.array([0,0,200])
upper_white = np.array([179, 255, 255])

#lower_white = np.array([140,21,214])
#upper_white = np.array([150, 20, 200])a

mask = cv2.inRange(hsv, lower_white, upper_white)

cv2.imshow('img', img)
cv2.imshow('line', mask)

cv2.waitKey()