#!/usr/bin/env python
# -*- coding: utf-8 -*- # 한글 주석쓰려면 이거 해야함
import cv2 # opencv 사용
import rospy
import numpy as np

from sensor_msgs.msg import Image
from cv_bridge import CvBridge

bridge = CvBridge()
image = np.empty(shape=[0])
#===================================
#콜백함수
#===================================
def usbcam_callback(data):
    global image
    image = bridge.imgmsg_to_cv2(data, "bgr8")

#===================================
#새로운 차선 발견 코드
#===================================

def region_of_interest(img, vertices, color3=(255,255,255), color1=255): # ROI 셋팅

    global image

    img = image.copy()
    display_img = img
    
    
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

rospy.init_node('lane_track')
rospy.Subscriber("/usb_cam/image_raw/",Image,usbcam_callback, queue_size=1)

rospy.wait_for_message("/usb_cam/image_raw/", Image)
print("Camera Ready --------------")

#======================================
#자이카에서 굴러가게 하게 정보를 바꾸는 영역
#======================================

while not rospy.is_shutdown():

    image = image.copy() # 자이카 캠에서 받은 이미지 읽기
    height, width = image.shape[:2] # 이미지 높이, 너비

    # 사다리꼴 모형의 Points
    vertices = np.array([[(50,height),(width/2-45, height/2+60), (width/2+45, height/2+60), (width-50,height)]], dtype=np.int32)
    roi_img = region_of_interest(image, vertices, (0,0,255)) # vertices에 정한 점들 기준으로 ROI 이미지 생성

    mark = np.copy(roi_img) # roi_img 복사
    mark = mark_img(roi_img) # 흰색 차선 찾기

    # 흰색 차선 검출한 부분을 원본 image에 overlap 하기
    color_thresholds = (mark[:,:,0] == 0) & (mark[:,:,1] == 0) & (mark[:,:,2] > 200)
    image[color_thresholds] = [0,0,255]

    cv2.imshow('roi_white',mark) # 흰색 차선 추출 결과 출력
    cv2.imshow('result',image) # 이미지 출력
    cv2.waitKey(1) 