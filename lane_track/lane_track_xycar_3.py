#!/usr/bin/env python
# -*- coding: utf-8 -*- # 한글 주석쓰려면 이거 해야함
import rospy, rospkg, time
import cv2,math # opencv 사용
import numpy as np
from cv_bridge import CvBridge
from xycar_motor.msg import xycar_motor
from sensor_msgs.msg import Image
import signal
import sys
import os

#--------------------------------
def signal_handler(sig, frame):
    import time
    time.sleep(3)
    os.system('killall -9 python rosout')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

image = np.empty(shape=[0])
bridge = CvBridge()
pub = None
Width = 320
Height = 240
Offset = 160
Gap = 40

cam = False
cam_debug = True

sub_f = 0
time_c = 0

def img_callback(data):
    global image   
    global sub_f 
    global time_c

    sub_f += 1
    if time.time() - time_c > 1:
        #print("pub fps :", sub_f)
        time_c = time.time()
        sub_f = 0

    image = bridge.imgmsg_to_cv2(data, "bgr8")

def drive(Angle, Speed): 
    global pub

    msg = xycar_motor()
    msg.angle = Angle
    msg.speed = Speed

    pub.publish(msg)    

#--------------------------------

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

def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap): # 허프 변환
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
    #line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    #draw_lines(line_img, lines)

    return lines

def get_fitline(img, f_lines): # 대표선 구하기   
    lines = np.squeeze(f_lines)
    lines = lines.reshape(lines.shape[0]*2,2)
    rows,cols = img.shape[:2]
    output = cv2.fitLine(lines,cv2.DIST_L2,0, 0.01, 0.01)
    vx, vy, x, y = output[0], output[1], output[2], output[3]
    x1, y1 = int(((img.shape[0]-1)-y)/vy*vx + x) , img.shape[0]-1
    x2, y2 = int(((img.shape[0]/2+100)-y)/vy*vx + x) , int(img.shape[0]/2+100)
    
    result = [x1,y1,x2,y2]
    return result

def draw_fit_line(img, lines, color=[255, 0, 0], thickness=10): # 대표선 그리기
        cv2.line(img, (lines[0], lines[1]), (lines[2], lines[3]), color, thickness)

def weighted_img(img, initial_img, a=1, b=1., c=0.): # 두 이미지 operlap 하기
    return cv2.addWeighted(initial_img, a, img, b, c)

# get average m, b of line, sum of x, y, mget lpos, rpos
def get_line_pos(img, lines, left=False, right=False):
    global Width, Height
    global Offset, Gap, cam_debug

    x_sum = 0.0
    y_sum = 0.0
    m_sum = 0.0

    size = len(lines)
    
    m = 0
    b = 0

    if size != 0:
        for line in lines:
            x1, y1, x2, y2 = line[0]

            x_sum += x1 + x2
            y_sum += y1 + y2
            m_sum += float(y2 - y1) / float(x2 - x1)

        x_avg = x_sum / (size * 2)
        y_avg = y_sum / (size * 2)

        m = m_sum / size
        b = y_avg - m * x_avg

    if m == 0 and b == 0:
        if left:
            pos = 0
        elif right:
            pos = Width
    else:
        y = Gap / 2

        pos = (y - b) / m

        if cam_debug:
            b += Offset
            xs = (Height - b) / float(m)
            xe = ((Height/2) - b) / float(m)

            cv2.line(img, (int(xs), Height), (int(xe), (Height/2)), (255, 0,0), 3)

    return img, int(pos)

def process_image(img):
    global Width
    global offset, Gap
    global cam, bam_debug

    height, width = image.shape[:2]
    #gray
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    blur_gray = cv2.GaussianBlur(gray, (3, 3), 0)

    low_threshold = 70
    high_threshold = 210
    canny_img = cv2.Canny(blur_gray, low_threshold, high_threshold, 3)

    vertices = np.array([[(50,height),(width/2-45, height/2+60), (width/2+45, height/2+60), (width-50,height)]], dtype=np.int32)
    ROI_img = region_of_interest(canny_img, vertices) # ROI 설정

    line_arr = hough_lines(ROI_img, 1, 1 * np.pi/180, 30, 10, 20) # 허프 변환
    left_line_x = []
    left_line_y = []
    right_line_x = []
    right_line_y = []
    for line_arr in line_arr:
        for x1, y1, x2, y2 in line_arr:
            slope = (y2 - y1) / (x2 - x1) # <-- Calculating the slope.
            if math.fabs(slope) < 0.6: # <-- Only consider extreme slope
                continue
            if slope <= 0: # <-- If the slope is negative, left group.
                left_line_x.extend([x1, x2])
                left_line_y.extend([y1, y2])
            else: # <-- Otherwise, right group.
                right_line_x.extend([x1, x2])
                right_line_y.extend([y1, y2])

    # 필터링된 직선 버리기
    temp = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)
    L_lines, R_lines = L_lines[:,None], R_lines[:,None]
    # 왼쪽, 오른쪽 각각 대표선 구하기
    left_fit_line = get_fitline(image,L_lines)
    right_fit_line = get_fitline(image,R_lines)
    # 대표선 그리기
    draw_fit_line(temp, left_fit_line)
    draw_fit_line(temp, right_fit_line)

    cvresult = weighted_img(temp, image) # 원본 이미지에 검출된 선 overlap
    if cam:
         cv2.imshow('calibration', img)
         cv2.imshow('cvresult',cvresult)

    img, lpos = get_line_pos(img, left_fit_line, left=True)
    img, rpos = get_line_pos(img, right_fit_line, right=True)

    if cam_debug:
        # draw lines
        img = draw_lines(img, left_lines)
        img = draw_lines(img, right_lines)
        img = cv2.line(img, (115, 117), (205, 117), (0,255,255), 2)

        # draw rectangle
        img = draw_rectangle(img, lpos, rpos, offset=Offset)
        img = cv2.rectangle(img, (0, Offset), (Width, Offset+Gap), (0, 255, 0), 2)

        # show image
        cv2.imshow('cam_debug', img)

    return lpos, rpos, True
def start():
    global pub
    global image
    global cap
    global Width, Height

    rospy.init_node('xycar_c1')
    pub = rospy.Publisher('xycar_motor', xycar_motor, queue_size=1)

    image_sub = rospy.Subscriber("/usb_cam/image_raw", Image, img_callback)
    print ("---------- Xycar C1 HD v1.0 ----------")
    time.sleep(3)

    #sq = rospy.Rate(30)

    t_check = time.time()
    f_n = 0

    while not rospy.is_shutdown():

        while not image.size == (Width*Height*3):
            continue

        f_n += 1
        if (time.time() - t_check) > 1:
            #print("fps : ", f_n)
            t_check = time.time()
            f_n = 0

        img = image.copy()
        lpos, rpos, go = process_image(img)

        center = (lpos + rpos) / 2
        angle = -(Width/2 - center)

        drive(angle, 10)

        cv2.waitKey(1)
        #sq.sleep()


if __name__ == '__main__':
    start()
