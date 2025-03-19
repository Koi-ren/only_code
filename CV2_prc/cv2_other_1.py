import cv2
import numpy as np

# 점들로 이루어진 배열 생성
points = np.array([[1, 1], [2, 2], [3, 3], [4, 4]], np.int32)

# fitLine 함수 사용
line = cv2.fitLine(points, cv2.DIST_L2, 0, 0.01, 0.01)

# 추출된 선의 정보 출력
print("기울기:", line[1])
print("y절편:", line[2])
print('output[0]:',line[0])
print('output[3]:',line[3])
