#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#=============================================
# 본 프로그램은 자이트론에서 제작한 것입니다.
# 상업 라이센스에 의해 제공되므로 무단배포 및 상업적 이용을 금합니다.
#=============================================
#=============================================
# 함께 사용되는 각종 파이썬 패키지들의 import 선언부
#=============================================
import numpy as np
import cv2, rospy, time, math
from sensor_msgs.msg import Image
from xycar_motor.msg import xycar_motor
from cv_bridge import CvBridge

#=============================================
# 프로그램에서 사용할 변수, 저장공간 선언부
#=============================================
motor = None  # 모터 노드 변수
Fix_Speed = 17  # 모터 속도 고정 상수값 
new_angle = 0  # 모터 조향각 초기값
new_speed = Fix_Speed  # 모터 속도 초기값
bridge = CvBridge()  # OpenCV 함수를 사용하기 위한 브릿지 
image = np.empty(shape=[0])  # 카메라 이미지를 담을 변수
motor_msg = xycar_motor()  # 카메라 토픽 메시지
width, height = 320, 240  # 카메라 이미지 가로x세로 크기
Blue = (255,0,0) # 파란색
Green = (0,255,0) # 녹색
Red = (0,0,255) # 빨간색
Yellow = (0,255,255) # 노란색
View_Center = width//2  # 화면의 중앙값 = 카메라 위치
mark = np.zeros((10, 10), dtype=int)
thresholds = np.array([2, 5, 8])

#=============================================
# 차선 인식 프로그램에서 사용할 상수 선언부
#=============================================
CAM_FPS = 30  # 카메라 FPS 초당 30장의 사진을 보냄
ROI_START_ROW = height  # 차선을 찾을 ROI 영역의 시작 Row값
ROI_END_ROW = int(height/2+60)  # 차선을 찾을 ROT 영역의 끝 Row값
ROI_height = ROI_END_ROW - ROI_START_ROW  # ROI 영역의 세로 크기  
L_ROW = 190  # 차선의 위치를 찾기 위한 ROI 안에서의 기준 Row값 

#=============================================
# 콜백함수 - USB 전방카메라 토픽을 처리하는 콜백함수.
#=============================================
def usbcam_callback(data):
    global image
    image = bridge.imgmsg_to_cv2(data, "bgr8")

#=============================================
# 모터 토픽을 발행하는 함수.  
#=============================================
def drive(angle, speed):
    motor_msg.angle = angle
    motor_msg.speed = speed
    motor.publish(motor_msg)

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
    global mark
    #  BGR 제한 값
    bgr_threshold = [blue_threshold, green_threshold, red_threshold]

    # BGR 제한 값보다 작으면 검은색으로
    thresholds = (image[:,:,0] < bgr_threshold[0]) \
                | (image[:,:,1] < bgr_threshold[1]) \
                | (image[:,:,2] < bgr_threshold[2])
    mark[thresholds, :] = [0, 0, 0]
    return mark

    
#=============================================
# 카메라 영상 이미지에서 차선을 찾아 그 위치를 반환하는 코드
#=============================================
def lane_detect():

    global image
    global mark

    image = image.copy() # 자이카 캠에서 받은 이미지 읽기
    display_img = image # 이미지 높이, 너비
    prev_x_left = 0
    prev_x_right = width
    
    # img(원본이미지)의 특정영역(ROI Area)을 잘라내기
    vertices = np.array([[(50,height),(width/2-45, height/2+60), (width/2+45, height/2+60), (width-50,height)]], dtype=np.int32)
    roi_img = region_of_interest(image, vertices, (0,0,255)) # vertices에 정한 점들 기준으로 ROI 이미지 생성

    line_draw_img = roi_img.copy()

    #=========================================
    # 원본 칼라이미지를 그레이 회색톤 이미지로 변환하고 
    # 블러링 처리를 통해 노이즈를 제거한 후에 (약간 뿌옇게, 부드럽게)
    # Canny 변환을 통해 외곽선 이미지로 만들기
    #=========================================

    gray = cv2.cvtColor(roi_img, cv2.COLOR_BGR2GRAY)
    blur_gray = cv2.GaussianBlur(gray,(5, 5), 0)
    edge_img = cv2.Canny(np.uint8(blur_gray), 60, 75)

    cv2.imshow("Lane Detection Canny Image", edge_img)
    # 잘라낸 이미지에서 HoughLinesP 함수를 사용하여 선분들을 찾음
    all_lines = cv2.HoughLinesP(edge_img, 1, math.pi/180,50,50,20)
    
    if all_lines is None:
        return False, 0, 0

    #=========================================
    # 선분들의 기울기 값을 각각 모두 구한 후에 리스트에 담음. 
    # 기울기의 절대값이 너무 작은 경우 (수평선에 가까운 경우)
    # 해당 선분을 빼고 담음. 
    #=========================================
    slopes = []
    filtered_lines = []

    for line in all_lines:
        x1, y1, x2, y2 = line[0]

        if (x2 == x1):
            slope = 1000.0
        else:
            slope = float(y2-y1) / float(x2-x1)
    
        if 0.2 < abs(slope):
            slopes.append(slope)
            filtered_lines.append(line[0])

    if len(filtered_lines) == 0:
        return False, 0, 0

    #=========================================
    # 왼쪽 차선에 해당하는 선분과 오른쪽 차선에 해당하는 선분을 구분하여 
    # 각각 별도의 리스트에 담음.
    #=========================================
    left_lines = []
    right_lines = []

    for j in range(len(slopes)):
        Line = filtered_lines[j]
        slope = slopes[j]

        x1,y1, x2,y2 = Line

        # 기울기 값이 음수이고 화면의 왼쪽에 있으면 왼쪽 차선으로 분류함
        # 기준이 되는 X좌표값 = (화면중심값 - Margin값)
        Margin = 0
        
        if (slope < 0) and (x2 < width/2-Margin):
            left_lines.append(Line.tolist())

        # 기울기 값이 양수이고 화면의 오른쪽에 있으면 오른쪽 차선으로 분류함
        # 기준이 되는 X좌표값 = (화면중심값 + Margin값)
        elif (slope > 0) and (x1 > width/2+Margin):
            right_lines.append(Line.tolist())

    # 디버깅을 위해 차선과 관련된 직선과 선분을 그리기 위한 도화지 준비
    line_draw_img = roi_img.copy()
    
    # 왼쪽 차선에 해당하는 선분은 빨간색으로 표시
    for line in left_lines:
        x1,y1, x2,y2 = line
        cv2.line(line_draw_img, (x1,y1), (x2,y2), Red, 2)

    # 오른쪽 차선에 해당하는 선분은 노란색으로 표시
    for line in right_lines:
        x1,y1, x2,y2 = line
        cv2.line(line_draw_img, (x1,y1), (x2,y2), Yellow, 2)

    #=========================================
    # 왼쪽/오른쪽 차선에 해당하는 선분들의 데이터를 적절히 처리해서 
    # 왼쪽차선의 대표직선과 오른쪽차선의 대표직선을 각각 구함.
    # 기울기와 Y절편값으로 표현되는 아래와 같은 직선의 방적식을 사용함.
    # (직선의 방정식) y = mx + b (m은 기울기, b는 Y절편)
    #=========================================

    # 왼쪽 차선을 표시하는 대표직선을 구함        
    m_left, b_left = 0.0, 0.0
    x_sum, y_sum, m_sum = 0.0, 0.0, 0.0

    # 왼쪽 차선을 표시하는 선분들의 기울기와 양끝점들의 평균값을 찾아 대표직선을 구함
    size = len(left_lines)
    if size != 0:
        for line in left_lines:
            x1, y1, x2, y2 = line
            x_sum += x1 + x2
            y_sum += y1 + y2
            if(x2 != x1):
                m_sum += float(y2-y1)/float(x2-x1)
            else:
                m_sum += 0                
            
        x_avg = x_sum / (size*2)
        y_avg = y_sum / (size*2)
        m_left = m_sum / size
        b_left = y_avg - m_left * x_avg

        if m_left != 0.0:
            #=========================================
            # (직선 #1) y = mx + b 
            # (직선 #2) y = 0
            # 위 두 직선의 교점의 좌표값 (x1, 0)을 구함.           
            x1 = int((0.0 - b_left) / m_left)

            #=========================================
            # (직선 #1) y = mx + b 
            # (직선 #2) y = ROI_height
            # 위 두 직선의 교점의 좌표값 (x2, ROI_height)을 구함.               
            x2 = int((ROI_height - b_left) / m_left)

            # 두 교점, (x1,0)과 (x2, ROI_height)를 잇는 선을 그림
            cv2.line(line_draw_img, (x1,0), (x2,ROI_height), Blue, 2)

    # 오른쪽 차선을 표시하는 대표직선을 구함      
    m_right, b_right = 0.0, 0.0
    x_sum, y_sum, m_sum = 0.0, 0.0, 0.0

    # 오른쪽 차선을 표시하는 선분들의 기울기와 양끝점들의 평균값을 찾아 대표직선을 구함
    size = len(right_lines)
    if size != 0:
        for line in right_lines:
            x1, y1, x2, y2 = line
            x_sum += x1 + x2
            y_sum += y1 + y2
            if(x2 != x1):
                m_sum += float(y2-y1)/float(x2-x1)
            else:
                m_sum += 0     
       
        x_avg = x_sum / (size*2)
        y_avg = y_sum / (size*2)
        m_right = m_sum / size
        b_right = y_avg - m_right * x_avg

        if m_right != 0.0:
            #=========================================
            # (직선 #1) y = mx + b 
            # (직선 #2) y = 0
            # 위 두 직선의 교점의 좌표값 (x1, 0)을 구함.           
            x1 = int((0.0 - b_right) / m_right)

            #=========================================
            # (직선 #1) y = mx + b 
            # (직선 #2) y = ROI_height
            # 위 두 직선의 교점의 좌표값 (x2, ROI_height)을 구함.               
            x2 = int((ROI_height - b_right) / m_right)

            # 두 교점, (x1,0)과 (x2, ROI_height)를 잇는 선을 그림
            cv2.line(line_draw_img, (x1,0), (x2,ROI_height), Blue, 2)

    #=========================================
    # 차선의 위치를 찾기 위한 기준선(수평선)은 아래와 같음.
    #   (직선의 방정식) y = L_ROW 
    # 위에서 구한 2개의 대표직선, 
    #   (직선의 방정식) y = (m_left)x + (b_left)
    #   (직선의 방정식) y = (m_right)x + (b_right)
    # 기준선(수평선)과 대표직선과의 교점인 x_left와 x_right를 찾음.
    #=========================================

    #=========================================        
    # 대표직선의 기울기 값이 0.0이라는 것은 직선을 찾지 못했다는 의미임
    # 이 경우에는 교점 좌표값을 기존 저장해 놨던 값으로 세팅함 
    #=========================================
    if m_left == 0.0:
        x_left = prev_x_left  # 변수에 저장해 놓았던 이전 값을 가져옴

    #=========================================
    # 아래 2개 직선의 교점을 구함
    # (직선의 방정식) y = L_ROW  
    # (직선의 방정식) y = (m_left)x + (b_left)
    #=========================================
    else:
        x_left = int((L_ROW - b_left) / m_left)
                        
    #=========================================
    # 대표직선의 기울기 값이 0.0이라는 것은 직선을 찾지 못했다는 의미임
    # 이 경우에는 교점 좌표값을 기존 저장해 놨던 값으로 세팅함 
    #=========================================
    if m_right == 0.0:
        x_right = prev_x_right  # 변수에 저장해 놓았던 이전 값을 가져옴	
	
    #=========================================
    # 아래 2개 직선의 교점을 구함
    # (직선의 방정식) y = L_ROW  
    # (직선의 방정식) y = (m_right)x + (b_right)
    #=========================================
    else:
        x_right = int((L_ROW - b_right) / m_right)
       
    #=========================================
    # 대표직선의 기울기 값이 0.0이라는 것은 직선을 찾지 못했다는 의미임
    # 이 경우에 반대쪽 차선의 위치 정보를 이용해서 내 위치값을 정함 
    #=========================================
    if m_left == 0.0 and m_right != 0.0:
        x_left = x_right - 380

    if m_left != 0.0 and m_right == 0.0:
        x_right = x_left + 380

    # 이번에 구한 값으로 예전 값을 업데이트 함			
    prev_x_left = x_left
    prev_x_right = x_right
	
    # 왼쪽 차선의 위치와 오른쪽 차선의 위치의 중간 위치를 구함
    x_midpoint = (x_left + x_right) // 2 

    #=========================================
    # 디버깅용 이미지 그리기
    # (1) 수평선 그리기 (직선의 방정식) y = L_ROW 
    # (2) 수평선과 왼쪽 대표직선과의 교점 위치에 작은 녹색 사각형 그리기 
    # (3) 수평선과 오른쪽 대표직선과의 교점 위치에 작은 녹색 사각형 그리기 
    # (4) 왼쪽 교점과 오른쪽 교점의 중점 위치에 작은 파란색 사각형 그리기
    # (5) 화면의 중앙점 위치에 작은 빨간색 사각형 그리기 
    #=========================================
    cv2.line(line_draw_img, (0,L_ROW), (width,L_ROW), Yellow, 2)
    cv2.rectangle(line_draw_img, (x_left-5,L_ROW-5), (x_left+5,L_ROW+5), Green, 4)
    cv2.rectangle(line_draw_img, (x_right-5,L_ROW-5), (x_right+5,L_ROW+5), Green, 4)
    cv2.rectangle(line_draw_img, (x_midpoint-5,L_ROW-5), (x_midpoint+5,L_ROW+5), Blue, 4)
    cv2.rectangle(line_draw_img, (View_Center-5,L_ROW-5), (View_Center+5,L_ROW+5), Red, 4)

    # 위 이미지를 디버깅용 display_img에 overwrite해서 화면에 디스플레이 함
    display_img[0:320, 0:width] = line_draw_img
    #display_img[ROI_START_ROW:ROI_END_ROW, 0:width] = line_draw_img
    cv2.imshow("Lanes positions", display_img)
    cv2.imshow("line_draw", line_draw_img)
    cv2.waitKey(1)

    return True, x_left, x_right

#=============================================
# 실질적인 메인 함수 
#=============================================
def start():

    global motor, new_speed, new_angle 
    
    LANE_DRIVE = 1
    FINISH = 9
    drive_mode = LANE_DRIVE
    
    #=========================================
    # 노드를 생성하고, 구독/발행할 토픽들을 선언합니다.
    #=========================================
    rospy.init_node('Track_Driver')
    motor = rospy.Publisher('xycar_motor', xycar_motor, queue_size=1)
    rospy.Subscriber("/usb_cam/image_raw/",Image,usbcam_callback)
    
    #=========================================
    # Launch 파일에서 speed 속도값 읽어들이기 
    #=========================================
    spd = rospy.get_param("~speed", 18)
    new_speed = spd

    #=========================================
    # 첫번째 토픽이 도착할 때까지 기다립니다.
    #=========================================
    rospy.wait_for_message("/usb_cam/image_raw/", Image)
    print("Camera Ready --------------")
    drive(0,0)

    #=========================================
    # 메인 루프 
    #=========================================
    while not rospy.is_shutdown():
    
        # ======================================
        # 차선을 보고 주행합니다.
        # ======================================
        while drive_mode == LANE_DRIVE:
            found, x_left, x_right = lane_detect()
            if found:
                x_midpoint = (x_left + x_right) // 2
                new_angle = (x_midpoint - View_Center)
                drive(new_angle, new_speed)
            else:
                drive(new_angle, new_speed)

#=============================================
# 메인 함수
# 가장 먼저 호출되는 함수로 여기서 start() 함수를 호출함.
# start() 함수가 실질적인 메인 함수임. 
#=============================================
if __name__ == '__main__':
    start()
