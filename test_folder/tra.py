# -*- coding: utf-8 -*- # 한글 주석쓰려면 이거 해야함
import cv2 # opencv 사용
import numpy as np

Green = (0,255,0)

def region_of_interest(img, vertices, color3=(255,255,255), color1=255): # ROI 셋팅

    mask = np.zeros_like(img) # mask = img와 같은 크기의 빈 이미지
    
    if len(img.shape) > 2: # Color 이미지(3채널)라면 :
        color = color3
    else: # 흑백 이미지(1채널)라면 :
        color = color1
        
    # vertices에 정한 점들로 이뤄진 다각형부분(ROI 설정부분)을 color로 채움 
    cv2.fillPoly(mask, vertices, color)
    
    # 이미지와 color로 채워진 ROI를 합침
    ROI_image = cv2.bitwise_and(img, mask)
    return ROI_image

def mark_img(img, blue_threshold=200, green_threshold=200, red_threshold=200): # 흰색 차선 찾기

    #  BGR 제한 값
    bgr_threshold = [blue_threshold, green_threshold, red_threshold]

    # BGR 제한 값보다 작으면 검은색으로
    thresholds = (image[:,:,0] < bgr_threshold[0]) \
                | (image[:,:,1] < bgr_threshold[1]) \
                | (image[:,:,2] < bgr_threshold[2])
    mark[thresholds] = [0,0,0]
    return mark

image = cv2.imread('C:/new/solidWhiteCurve.jpg') # 이미지 읽기
height, width = image.shape[:2] # 이미지 높이, 너비

# 사다리꼴 모형의 Points
vertices = np.array([[(100,height),(width/2-45, height/2+100), (width/2+45, height/2+60), (width-50,height)]], dtype=np.int32)
roi_img = region_of_interest(image, vertices, (0,0,255)) # vertices에 정한 점들 기준으로 ROI 이미지 생성
cv2.imshow('roi', roi_img)
line_draw_img = roi_img.copy()
gray = cv2.cvtColor(roi_img, cv2.COLOR_BGR2GRAY)
blur_gray = cv2.GaussianBlur(gray,(5, 5), 0)
edge_img = cv2.Canny(np.uint8(blur_gray), 60, 75)
all_lines = cv2.HoughLinesP(edge_img, 1, np.pi/180,50,50,20)
for line in all_lines:
    x1, y1, x2, y2 = line[0]
    cv2.line(line_draw_img, (x1, y1), (x2, y2), Green, 2)

cv2.imshow("roi area lines", line_draw_img)

cv2.waitKey(0) 