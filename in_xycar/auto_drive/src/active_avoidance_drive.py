#!/usr/bin/env python3
# -*- coding: utf-8 -*- 1
#=============================================
# 패키지 및 모듈 선언부
# #=============================================
import numpy as np
import cv2, rospy, time, math
from sensor_msgs.msg import Image, LaserScan
from xycar_motor.msg import xycar_motor
from cv_bridge import CvBridge

#lidar_module----------------------------------
import lidar_12m, lidar_10m, lidar_5m, lidar_1m
import array_set as aset
import detect
#----------------------------------------------

#=============================================
# 프로그램에서 사용할 변수, 저장공간 선언부
#=============================================
motor = None  # 모터 노드 변수
Fix_Speed = 15  # 모터 속도 고정 상수값 
new_angle = 0  # 모터 조향각 초기값
new_speed = Fix_Speed  # 모터 속도 초기값
bridge = CvBridge()  # OpenCV 함수를 사용하기 위한 브릿지 
image = np.empty(shape=[0])  # 카메라 이미지를 담을 변수
motor_msg = xycar_motor()  # 카메라 토픽 메시지
WIDTH, HEIGHT = 640, 480  # 카메라 이미지 가로x세로 크기
Blue =  (255,0,0) # 파란색
Green = (0,255,0) # 녹색
Red =   (0,0,255) # 빨간색
Yellow = (0,255,255) # 노란색
stopline_num = 1 # 정지선 발견때마다 1씩 증가
View_Center = WIDTH//2  # 화면의 중앙값 = 카메라 위치
pub = None
Width = 640
Gap = 40
cam = False
cam_debug = True
sub_f = 0
time_c = 0
Offset = 160
close = None
right = False
mid = False
left = False

#=============================================
# 콜백함수 - USB 카메라 토픽을 받아서 처리하는 콜백함수
#=============================================
def usbcam_callback(data):
    global image   
    global sub_f 
    global time_c

    sub_f += 1
    if time.time() - time_c > 1:
        #print("pub fps :", sub_f)
        time_c = time.time()
        sub_f = 0

    image = bridge.imgmsg_to_cv2(data, "bgr8")
#=============================================
# 신호등 인식
#=============================================
def check_traffic_sign():
    # 원본이미지를 복제한 후에 특정영역(ROI Area)을 잘라내기
    cimg = image.copy()
    Center_X, Center_Y = 160, 70  # ROI 영역의 중심위치 좌표 
    XX, YY = 150, 40  # 위 중심 좌표에서 좌우로 XX, 상하로 YY만큼씩 벌려서 ROI 영역을 잘라냄   

    # ROI 영역에 녹색 사각형으로 테두리를 쳐서 표시함 
    cv2.rectangle(cimg, (Center_X-XX, Center_Y-YY), (Center_X+XX, Center_Y+YY) , Green, 2)
	
    # 원본 이미지에서 ROI 영역만큼 잘라서 roi_img에 담음 
    roi_img = cimg[Center_Y-YY:Center_Y+YY, Center_X-XX:Center_X+XX]

    # roi_img 칼라 이미지를 회색 이미지로 바꾸고 노이즈 제거를 위해 블러링 처리를 함  
    img = cv2.cvtColor(roi_img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(img, (5, 5), 0)

    # Hough Circle 함수를 이용해서 이미지에서 원을 (여러개) 찾음 
    circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 1, 20,
                  param1=40, param2=20, minRadius=15, maxRadius=25)

    # 디버깅을 위해서 Canny 처리를 했을때의 모습을 화면에 표시함
    # 위 HoughCircles에서 param1, param2에 사용했던 값을 아래 canny에서 똑같이 적용해야 함. 순서 조심.
    canny = cv2.Canny(blur, 20, 40)
    cv2.imshow('Canny image used by HoughCircles', canny)
    cv2.waitKey(1)

    # 이미지에서 원이 발견됐다면 아래 if 안으로 들어가서 신호등 찾는 작업을 진행함  
    if circles is not None:

        circles = np.round(circles[0, :]).astype("int")

        # 원 중심의 X좌표값으로 소팅 - 화면의 왼쪽부터 순서대로 정리 
        circles = sorted(circles, key=lambda circle: circle[0])

        # 가장 밝은 원을 찾을 때 사용할 변수 선언 (가장밝은원 = max원)
        max_mean_value = 0
        max_mean_value_circle = None
        max_mean_value_index = None

        # 발견된 원들에 대해서 루프를 돌면서 하나씩 처리 
 	    # 원의 중심좌표, 반지름. 내부밝기 정보를 구해서 화면에 출력  
        for i, (x, y, r) in enumerate(circles):
            x1 = x - (r//2)
            y1 = y - (r//2)
            x2 = x + (r//2)
            y2 = y + (r//2)
            roi = img[y1:y2, x1:x2]
            mean_value = np.mean(roi)
            print("Circle {i} at ({x},{y}), radius={r}: mean value={mean_value}")
			
            # 이번 원의 밝기가 기존 max원보다 밝으면 이번 원을 max원으로 지정  
            if mean_value > max_mean_value:
                max_mean_value = mean_value
                max_mean_value_circle = (x, y, r)
                max_mean_value_index = i
                
            # 찾은 원을 녹색으로 그리고, 원 안에 작은 빨간색 사각형(밝기를 계산할 영역 표시)을 그림 
            cv2.circle(cimg, (x+Center_X-XX, y+Center_Y-YY), r, Green, 2)
            cv2.rectangle(cimg, (x1+Center_X-XX, y1+Center_Y-YY), (x2+Center_X-XX, y2+Center_Y-YY), Red, 2)

        # 가장 밝은 원(max원)을 찾았으면 그 원의 정보를 화면에 출력 
        if max_mean_value_circle is not None:
            (x, y, r) = max_mean_value_circle
            print(" --- Circle {max_mean_value_index} has the biggest mean value")

        # 신호등 찾기 결과가 표시된 이미지를 화면에 출력
        cv2.imshow('Circles Detected', cimg)
     
        # 찾은 원 중에서 오른쪽 3번째 원이 가장 밝으면 (파란색 신호등) True 리턴 
        if (i == 2) and (max_mean_value_index == 2):
            print("Traffic Sign is Blue...!")
            return True
        
        # 그렇지 않으면 (파란색 신호등이 아니면) False 반환 
        else:
            print("Traffic Sign is NOT Blue...!")
            return False

    # 신호등 찾기 결과가 표시된 이미지를 화면에 출력
    cv2.imshow('Circles Detected', cimg)

    # 원본 이미지에서 원이 발견되지 않았다면 False 리턴   
    #print("Can't find Traffic Sign...!")
    return False

#=============================================
# 콜백함수 - 라이다 콜백마다 거리 및 각도 값 반환
#=============================================
def RAD2DEG(x):
    return x * 180.0 / math.pi

def scanCallback(scan):
    global close, right, mid, left
    count = int(scan.scan_time / scan.time_increment)
    rospy.loginfo("I heard a laser scan %s[%d]:" % (scan.header.frame_id, count))
    
    len_12_1 = aset.array_mid_1
    len_10_1 = aset.array_mid_2
    len_5_1 = aset.array_mid_3
    len_1_1 = aset.array_mid_4
    close = 0
    right_obj_1 = aset.array_mid_1
    mid_obj_1 = aset.array.mid_2
    left_obj_1 = awet.array.mid_3
    
    for i in range(count):
        degree = RAD2DEG(scan.angle_min + scan.angle_increment * i)
        dist = scan.ranges[i]

        if (165.000000 <= degree <= 180.000000) or (-180.000000 <= degree < -165.000000):
            if (dist<0.35 or dist<0.5):
                close+=1
            elif (0.500000 < dist <= 1.000000):
                len_1_1 = lidar_1m.detect(degree)
            elif (1.000000 < dist <= 5.000000):
                len_5_1 = lidar_5m.detect(degree)
            elif (5.000000 < dist <= 10.000000):
                len_10_1 = lidar_10m.detect(degree)
            elif (10.000000 < dist <= 12.000000):
                len_12_1 = lidar_12m.detect(degree)
        if(-180.000000 < degree < -164.000000) and (dist < 0.350000):
            mid_obj_1.append(1)
        
        if(164.000000 < degree < 180.000000) and (dist < 0.350000):
            mid_obj_1.append(1)
        
        if(-164.000000 < degree <= -129.000000) and (dist < 0.370000):
            left_obj_1.append(1)
        
        if(129.000000 <= degree < 164.000000) and (dist < 0.370000):
            right_obj_1.append(1)
             
        right_obj_2 = len(right_obj_1)
        mid_obj_2 = len(mid_obj_1)
        left_obj_2 = len(left_obj_1)
        
        if right_obj_2 >= 108:
            right = True
        if mid_obj_2 >= 99:
            mid = True
        if left_obj_2 >= 108:
            left = True      
                       
        len_12_2 = len(len_12_1)
        len_10_2 = len(len_10_1)
        len_5_2 = len(len_5_1)
        len_1_2 = len(len_1_1)
        
    if close >=1:
        print("so close")
    else:
        #객체의 크기는 10cm + α 로 설정.
        result = detect.judge(len_12_2, len_10_2, len_5_2, len_1_2)
    
        if result is not None:
            dist_1, dist_2 = result
            if 0.5 <= dist_1 and 1.0 <= dist_2:
                print(f'Obstacle detected {dist_1:.1f} ~ {dist_2:.1f} meters ahead, directly in front. Prepare to decelerate.')
            else:
                 print('No object on your front')
        else:
            print('result is None')

def lidar_drive():
    global new_angle, new_speed, close

    # ¾ÕÂÊ °¡±îÀÌ¿¡ Àå¾Ö¹°ÀÌ ÀÖÀ¸¸é Â÷·® ¸ØÃã
    if close >=1:
        new_angle = new_angle
        new_speed = 0
        print("Car Brake, Stop! ")

    # ¿ÞÂÊÀÌ ¿À¸¥ÂÊº¸´Ù ¸Ö¸® ÀÖÀ¸¸é ÀÖÀ¸¸é ÁÂÈ¸Àü ÁÖÇà
    else:
        new_angle = 0
        new_speed = Fix_Speed
        print("Go Straight ")

    # ¸ðÅÍ¿¡ ÁÖÇà¸í·É ÅäÇÈÀ» º¸³½´Ù
    drive(new_angle, new_speed)
#=============================================
# 모터 토픽을 발행하는 함수 
#=============================================
def drive(Angle, Speed): 
    global pub

    msg = xycar_motor()
    msg.angle = Angle
    msg.speed = Speed

    pub.publish(msg)
#=============================================
# 차량을 정차시키는 함수  
# 입력으로 지속시간을 받아 그 시간동안 속도=0 토픽을 모터로 보냄.
# 지속시간은 0.1초 단위임. 만약 15이면 1.5초가 됨.
#=============================================
def stop_car(duration):
    for i in range(int(duration)): 
        drive(angle=0, speed=0)
        time.sleep(0.1)
#=============================================
# 차량을 이동시키는 함수 
# 입력으로 조향각과 속도, 지속시간을 받아 차량을 이동시킴.
# 지속시간은 0.1초 단위임. 만약 15이면 1.5초가 됨. 
#=============================================
def move_car(move_angle, move_speed, duration):
    for i in range(int(duration)): 
        drive(move_angle, move_speed)
        time.sleep(0.1)

#=============================================
# 정지선이 있는지 체크해서 True/False 값을 반환하는 함수
#=============================================

def check_stopline():
    global stopline_num

    # image(원본이미지)의 특정영역(ROI Area)을 잘라내기
    roi_img = image[160:240, 0:320]
    cv2.imshow("ROI Image", roi_img)

    # HSV 포맷으로 변환하고 V채널에 대해 범위를 정해서 흑백이진화 이미지로 변환
    hsv_image = cv2.cvtColor(roi_img, cv2.COLOR_BGR2HSV) 
    upper_white = np.array([255, 255, 255])
    lower_white = np.array([0, 0, 180])
    binary_img = cv2.inRange(hsv_image, lower_white, upper_white)

    # 흑백이진화 이미지에서 특정영역을 잘라내서 정지선 체크용 이미지로 만들기
    stopline_check_img = binary_img[50:60, 134:221] 
    
    # 흑백이진화 이미지를 칼라이미지로 바꾸고 정지선 체크용 이미지 영역을 녹색사각형으로 표시
    img = cv2.cvtColor(binary_img, cv2.COLOR_GRAY2BGR)
    cv2.rectangle(img, (100,50),(220,60),Green,3)
    cv2.imshow('Stopline Check', img)
    cv2.waitKey(1)
    
    # 정지선 체크용 이미지에서 흰색 점의 개수 카운트하기
    stopline_count = cv2.countNonZero(stopline_check_img)
    
    # 사각형 안의 흰색 점이 기준치 이상이면 정지선을 발견한 것으로 한다
    if stopline_count > 600:
        print("Stopline Found...! -", stopline_num)
        stopline_num = stopline_num + 1
        return True
    
    else:
        return False

#=============================================
# 카메라 이미지에서 차선을 찾아 그 위치를 반환하는 함수
#=============================================
def draw_lines(img, lines):
    for line in lines:
        x1, y1, x2, y2 = line[0]
        img = cv2.line(img, (x1, y1+Offset), (x2, y2+Offset), (0, 255, 0), 2)
    return img
def draw_rectangle(img, lpos, rpos, offset=0):
    center = (lpos + rpos) / 2

    cv2.rectangle(img, (lpos - 2, 7 + offset),
                       (lpos + 2, 12 + offset),
                       (0, 255, 0), 2)
    cv2.rectangle(img, (rpos - 2, 7 + offset),
                       (rpos + 2, 12 + offset),
                       (0, 255, 0), 2)
    cv2.rectangle(img, (center-2, 7 + offset),
                       (center+2, 12 + offset),
                       (0, 255, 0), 2)    
    cv2.rectangle(img, (157, 7 + offset),
                       (162, 12 + offset),
                       (0, 0, 255), 2)
    return img
def divide_left_right(lines):
    global Width

    low_slope_threshold = 0
    high_slope_threshold = 10

    # calculate slope & filtering with threshold
    slopes = []
    new_lines = []

    for line in lines:
        x1, y1, x2, y2 = line[0]

        if x2 - x1 == 0:
            slope = 0
        else:
            slope = float(y2-y1) / float(x2-x1)
        
        if low_slope_threshold < abs(slope) < high_slope_threshold:
            slopes.append(slope)
            new_lines.append(line[0])

    # divide lines left to right
    left_lines = []
    right_lines = []
    th = 25

    for j in range(len(slopes)):
        Line = new_lines[j]
        slope = slopes[j]

        x1, y1, x2, y2 = Line

        if (slope < 0) and (x2 < Width/2 - th):
            left_lines.append([Line.tolist()])
        elif (slope > 0) and (x1 > Width/2 + th):
            right_lines.append([Line.tolist()])

    return left_lines, right_lines

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

# show image and return lpos, rpos
def lane_detect():
    global Width
    global image
    global Offset, Gap
    global cam, cam_debug
    
    frame = image.copy() # 이미지처리를 위한 카메라 원본이미지 저장

    # gray
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    roi = gray[Offset : Offset+Gap, 0 : Width]

    # blur
    kernel_size = 3
    standard_deviation_x = 1.5     #Kernel standard deviation along X-axis
    blur_gray = cv2.GaussianBlur(roi, (kernel_size, kernel_size), standard_deviation_x)

    # canny edge
    low_threshold = 70
    high_threshold = 150
    edge_img = cv2.Canny(np.uint8(blur_gray), low_threshold, high_threshold, kernel_size)

    # HoughLinesP
    all_lines = cv2.HoughLinesP(edge_img, 1, math.pi/180,30,30,10)

    if cam:
        cv2.imshow('calibration', frame)
    # divide left, right lines
    if all_lines is None:
        return (Width)/2, (Width)/2, False
    left_lines, right_lines = divide_left_right(all_lines)

    # get center of lines
    frame, lpos = get_line_pos(frame, left_lines, left=True)
    frame, rpos = get_line_pos(frame, right_lines, right=True)

    if cam_debug:
        # draw lines
        frame = draw_lines(frame, left_lines)
        frame = draw_lines(frame, right_lines)
        frame = cv2.line(frame, (115, 117), (205, 117), (0,255,255), 2)

        # draw rectangle
        frame = draw_rectangle(frame, lpos, rpos, offset=Offset)
        frame = cv2.rectangle(frame, (0, Offset), (Width, Offset+Gap), (0, 255, 0), 2)

        # show image
        cv2.imshow('cam_debug', frame)

    return True, lpos, rpos
#=============================================
# 실질적인 메인 함수 
#=============================================
def start():

    global motor, image, close, right, mid, left
    global new_angle, new_speed
    
    TRAFFIC_SIGN = 1
    LANE_DRIVE = 2
    FINISH = 3
	
    # 처음에 어떤 미션부터 수행할 것인지 여기서 결정합니다. 
    drive_mode = TRAFFIC_SIGN
    

    rospy.init_node('Active_avoidance_drive')
    motor = rospy.Publisher('xycar_motor', xycar_motor, queue_size=10)
    rospy.Subscriber("/usb_cam/image_raw/",Image,usbcam_callback, queue_size=10)
    rospy.Subscriber("/scan", LaserScan, scanCallback)


    rospy.wait_for_message("/usb_cam/image_raw/", Image)
    print("Camera Ready --------------")
    rospy.wait_for_message("/scan", LaserScan)
    print("lidar Ready ---------------")

    print("======================================")
    print("... START ACTIVE AVOIDANCE DRIVING ...")
    print("======================================")
	
    # 일단 차량이 움직이지 않도록 정지상태 유지.  
    stop_car(20) # 2초 동안 정차.
	
    #=========================================
    # 메인 루프 
    #=========================================
    while not rospy.is_shutdown():

        # ======================================
        # 출발선에서 신호등 탐색.
        # 일단 정차해 있다가 파란색 불이 켜지면 출발.
        # 신호등을 찾으면 능동 회피 주행 시작.
        # ======================================
        while drive_mode == TRAFFIC_SIGN:
		
            # 앞에 있는 신호등에 파란색 불이 켜졌는지 체크.  
            result = check_traffic_sign()
			
            if (result == True):
                # 신호등이 파란불이면 미로주행 LANE_DRIVE로 모드 전환.
                drive_mode = LANE_DRIVE
                print ("----- lane track driving Start... -----")
                
        # ======================================
        # 차선을 보고 주행.
        # 라이다 스캐닝 중 장애물이 최소거리까지 접근 시 회피 주행 시작.
        # ======================================
        while drive_mode == LANE_DRIVE:
		
            # 카메라 이미지에서 차선의 위치 추적. 
            found, x_left, x_right = lane_detect()

            if close >= 1:
                #임의값임
                #오른쪽이 뚫려있을 떄
                if (left == True) and (mid == True) and (right  == False):
                    stop_car(10)
                    drive(30, 10)
                    time.sleep(3)
                    drive(-30, 10)
                    time.sleep(6)
                    drive(30, 10)
                    time.sleep(3)

                #왼쪽이 뚫려있을 떄
                if (left == False) and (mid == True) and (right == True):
                    stop_car(10)
                    drive(-30, 10)
                    time.sleep(3)
                    drive(30, 10)
                    time.sleep(6)
                    drive(-30, 10)
                    time.sleep(3)
			
            if found:
                # 차선인식이 됐으면 차선의 위치정보로 조향각을 결정. 
                new_angle = (((x_left + x_right) //2 ) - 160 ) 

                if ( -30 < new_angle < 30 ):
                    new_speed = 12
                else: 
                    new_speed = 8 

                drive(new_angle, new_speed)  
				
            else:
                # 차선인식이 안됐으면 기존 값을 사용하여 주행.
                drive(new_angle, new_speed)
            
            # 정지선 인식 활성화.  
            result = check_stopline()
			
            if (result == True):
                # 신호등이 파란불이면 미로주행 LANE_DRIVE로 모드 전환.
                drive_mode = FINISH
                print ("----- lane track driving Start... -----")
        # ======================================
        # 주행을 끝냅니다. 
        # ======================================
        if drive_mode == FINISH:
           
            # 차량을 정지시키고 모든 작업을 마침.
            stop_car(10) # 1초간 정차 
            print ("----- End of active driving -----")
            stop_car(200) # 20초 정차로 만일의 사태 대비
            return            

#=============================================
# 메인함수를 호출.
# start() 함수가 실질적인 메인함수.
#=============================================
if __name__ == '__main__':
    start()