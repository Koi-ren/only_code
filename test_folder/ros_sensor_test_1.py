#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import serial
import serial.tools.list_ports
import time
import math
import pandas as pd
import struct
import platform
import threading
import csv
import sys
import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float32


#변수 및 리스트--------------------gps---------------------------------------------gps------------------------------------

# 시리얼 포트 설정 (하나의 아두이노만 사용)
ser = serial.Serial('COM30', 115200)
time.sleep(2)  # 시리얼 통신 초기화 대기

speed_set = 40.0
steering_angle_set = 0

# GPS 관련 변수
tolerance = 0.00300
lat, lon = None, None

#변수 및 리스트--------------------imu---------------------------------------------imu------------------------------------

key = 0
flag = 0
buff = {}
angularVelocity = [0, 0, 0]
acceleration = [0, 0, 0]
magnetometer = [0, 0, 0]
angle_degree = [0, 0, 0]
pub_flag = [True, True]
python_version = platform.python_version()[0]

#변수 ------------------------------라이다--------------------------------------------라이다------------------------------

right_object, mid_object, left_object, lidar_stop_car = False, False, False, False
lidar_Front_is_OK = True

#계산 및 저장 설정 부 ----------------------------------------------------------------------------------------------------

#IMU센서 이중 적분
#순서대로~ 샘플링 시간 간격 (초), 속도, 거리, 이전 가속도
dt, imu_velocity, imu_distance, prev_accel = 0.00666, {0:0, 1:0, 2:0}, {0:0, 1:0, 2:0}, [0, 0, 0] # 150Hz 샘플링

# gps+imu 융합 좌표 저장
gps_imu_save_path = "C:/Users/plane/Desktop/park_ws/gps+imu_drive/gps+imu_coordinates.csv"

#경로 계획 좌표 읽기
planning_csv_path = "C:/Users/plane/Desktop/park_ws/gps+imu_drive/stadium_planning.csv"

# CSV 파일 읽기
planning_data = pd.read_csv(planning_csv_path)

# 위도와 경도 데이터 추출
planning_point_data = planning_data['Point Number'].tolist()
lat_data = planning_data['Latitude'].tolist()
lon_data = planning_data['Longitude'].tolist()
previous_planning_point_number = 0
planning_point_number = 0

time_limit =  300#주행 중단 시간(s)

with open(gps_imu_save_path, mode='w', newline='') as gps_file:
    gps_writer = csv.writer(gps_file)
    gps_writer.writerow(["Point Number", "Latitude", "Longitude"])

def save_to_csv(file_path, Point_number, Latitude, Longitude):
    """좌표 데이터를 CSV에 저장하는 함수"""
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([Point_number, Latitude, Longitude])

def publisher(speed, angle):
    rospy.init_node('sensor_publisher')
    speed_pub = rospy.Publisher('sensor_topic', Float32, queue_size=1)
    angle_pub= rospy.Publisher('sensor_topic', Float32, queue_size=1)
    rate = rospy.Rate(100)  # 100 Hz
    while not rospy.is_shutdown():
        rospy.loginfo(f"Publishing speed data: {speed}")
        rospy.loginfo(f"Publishing angle data: {angle}")
        speed_pub.publish(speed)
        angle_pub.publish(angle)
        rate.sleep()
#-------------제한시간----------------------------------------제한시간-----------------------------------------
def timeout():
    """타임아웃 함수: time_limt/60분 후에 프로그램 종료"""
    time.sleep(time_limit)
    print(f"프로그램이 {time_limit/60}분을 초과하여 종료됩니다.")
    sys.exit()

#함수정의--------------------gps---------------------------------------------gps------------------------------------

def read_gps_data(ser):
    """시리얼 포트에서 GPS 데이터를 읽어들임"""
    lat = lon = None  # None으로 초기화하여 0이 들어가는 것을 방지

    try:
        while not (lat and lon):  # 두 값 모두 유효할 때까지 반복
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                print(f"Read line from {ser.port}: {line}")  # 디버깅 메시지

                if line.startswith("Lat:"):
                    try:
                        parts = line.split()
                        if len(parts) >= 6:
                            # 위도, 경도, 고도를 파싱
                            lat = float(parts[1]) / 10000000.0
                            lon = float(parts[3]) / 10000000.0
                            # 데이터 유효성 검사
                            if not (36.11 <= lat <= 38.14 and 126 <= lon <= 129):
                                print("잘못된 데이터 범위. 다시 시도 중...")
                                lat = lon = None  # 잘못된 데이터를 무효화
                        else:
                            print("데이터 파싱 실패. 다시 시도 중...")
                    except ValueError:
                        print("데이터 파싱 오류. 다시 시도 중...")
                        lat = lon = None  # 파싱 실패 시 무효화
    except Exception as e:
        print(f"오류가 발생했습니다: {e}")
        return None, None

    return lat, lon

#함수정의--------------------imu---------------------------------------------imu------------------------------------

def find_ttyUSB():
    print("imu default serial port is COM30")
    posts = [port.device for port in serial.tools.list_ports.comports() if 'COM' in port.device]
    print("current computer connect {} ,have {} : {}".format('COM', len(posts), posts))

def checkSum(list_data, check_data):
    data = bytearray(list_data)
    crc = 0xFFFF
    for pos in data:
        crc ^= pos
        for i in range(8):
            if (crc & 1) != 0:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return hex(((crc & 0xff) << 8) + (crc >> 8)) == hex(check_data[0] << 8 | check_data[1])

def hex_to_ieee(raw_data):
    ieee_data = []
    raw_data.reverse()
    for i in range(0, len(raw_data), 4):
        data2str =hex(raw_data[i] | 0xff00)[4:6] + hex(raw_data[i + 1] | 0xff00)[4:6] + hex(raw_data[i + 2] | 0xff00)[4:6] + hex(raw_data[i + 3] | 0xff00)[4:6]
        if python_version == '2':
            ieee_data.append(struct.unpack('>f', data2str.decode('hex'))[0])
        if python_version == '3':
            ieee_data.append(struct.unpack('>f', bytes.fromhex(data2str))[0])
    ieee_data.reverse()
    return ieee_data

def handleSerialData(raw_data):
    global buff, key, pub_flag, angle_degree, magnetometer, acceleration, angularVelocity
    if python_version == '2':
        buff[key] = ord(raw_data)
    if python_version == '3':
        buff[key] = raw_data

    key += 1
    if buff[0] != 0xaa:
        key = 0
        return
    if key < 3:
        return
    if buff[1] != 0x55:
        key = 0
        return
    if key < buff[2] + 5:  # 根据数据长度位的判断, 来获取对应长度数据
        return

    else:
        data_buff = list(buff.values())  # 获取字典所以 value

        if buff[2] == 0x2c and pub_flag[0]:
            if checkSum(data_buff[2:47], data_buff[47:49]):
                data = hex_to_ieee(data_buff[7:47])
                angularVelocity = data[1:4]
                acceleration = data[4:7]
                magnetometer = data[7:10]
            else:
                print("check fail")
            pub_flag[0] = False
        elif buff[2] == 0x14 and pub_flag[1]:
            if checkSum(data_buff[2:23], data_buff[23:25]):
                data = hex_to_ieee(data_buff[7:23])
                angle_degree = data[1:4]
            else:
                print("check success")
            pub_flag[1] = False
        else:
            print("The data processing class does not provide the resolution of the" + str(buff[2]))
            print("Or data error")
            buff = {}
            key = 0

        buff = {}
        key = 0
        if pub_flag[0] == True or pub_flag[1] == True:
            return
        pub_flag[0] = pub_flag[1] = True

# --------------라이다----------------------------------------------라이다-----------------------------------------------------
def scanCallback(scan):

    #try를 사용해서 지속적으로 돌려야하는가?
    #혹은 rospy를 통해 지속적으로 데이터가 들어오는가?
    #실험적으로 알아봐야함

    global close, lidar_stop_car, right_object, mid_object, left_object, lidar_Front_is_OK
    count = int(scan.scan_time / scan.time_increment)

    rospy.loginfo("I heard a laser scan %s[%d]:" % (scan.header.frame_id, count))

    right_obj, mid_obj, left_obj, close = 0, 0, 0, 0
    right_close, mid_close, left_close = 0, 0, 0
    for i in range(count):
        degree = RAD2DEG(scan.angle_min + scan.angle_increment * i)
        dist = scan.ranges[i]
        if (165.0 <= degree <= 180.0) or (-180.0 <= degree <= -165.0) and (dist <= 3.0):
                mid_obj += 1
                if dist <= 1.0:
                    mid_close += 1
        if (135.0 <= degree <= 165.0) and (dist <= 3.0):
                right_obj += 1
                if dist <= 1.0:
                    right_close += 1
        if (-165.0 <= degree <= -135) and (dist <= 3.0):
                left_obj += 1
                if dist <= 1.0:
                    left_close += 1

        if right_object >= 93:
            right_object = True
        else: 
            right_object = False
        if mid_obj >= 93:
            mid_object = True
        else:
            mid_object = False
        if left_obj >= 93:
            left_object = True
        else:
            left_object = False 

        if (mid_close >= 50) or ((mid_close >= 30) and ((right_close >= 40) or (left_close >= 40))):
            lidar_stop_car = True 
        else: 
            lidar_stop_car = False
            

#----------계산 파트---------------------------------------------------계산 파트------------------------------------------------

def RAD2DEG(x):
    return x * 180.0 / math.pi

def calculate_distance(lat1, lon1, lat2, lon2):
    """거리 계산 함수 (Haversine 공식)"""
    R = 6371.0  # 지구 반지름 (km)
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distance = R * c
    return distance

def is_within_tolerance(lat1, lon1, lat_target, lon_target, tolerance):
    """주어진 좌표가 목표 좌표의 오차 범위 내에 있는지 확인합니다."""
    distance = calculate_distance(lat1, lon1, lat_target, lon_target)
    return distance <= tolerance

def calculate_bearing(lat1, lon1, lat2, lon2):
    """각도 계산 함수 (북쪽을 0도, 동쪽을 90도로 설정)"""
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlon = lon2_rad - lon1_rad

    x = math.sin(dlon) * math.cos(lat2_rad)
    y = math.cos(lat1_rad) * math.sin(lat2_rad) - (math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(dlon))

    initial_bearing = math.atan2(x, y)
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360
    return compass_bearing

def heading_degree_found():
    global  heading_degree
    heading = math.atan2(magnetometer[1],magnetometer[0])
    declination_angle = (-9.0 + (-0.0 / 60.0)) / (180 / math.pi)
    heading += declination_angle
    if heading < 0:
        heading += 2 * math.pi
    if heading > 2 * math.pi:
        heading -= 2 * math.pi
    heading_degree = heading * 180 / math.pi

def euclidean_distance():
    global imu_euclidean_distance
    """
    (0, 0)에서 (x, y)까지의 유클리드 거리 계산 함수
    :param x: x축으로 이동한 거리
    :param y: y축으로 이동한 거리
    :return: (0, 0)에서 (x, y)까지의 거리
    """
    imu_euclidean_distance = math.sqrt((imu_distance[0]**2  )+ imu_distance[1]**2)

def update_velocity_and_distance_trapezoid():
    global dt, imu_velocity, imu_distance
    
    """
    트라페zoid 적분법을 사용하여 속도와 이동 거리를 업데이트하는 함수
    :param acceleration: 현재 가속도 샘플 (x, y, z)
    :param prev_accel: 이전 가속도 샘플 (x, y, z)
    :param velocity: 현재 속도 (딕셔너리 형태)
    :param distance: 현재 이동 거리 (딕셔너리 형태)
    :param dt: 샘플링 시간 간격
    """
    imu_velocity[0] = (((acceleration[0]*-9.8) + 0.07) + ((prev_accel[0]*-9.8) + 0.07) / 2) * dt
    imu_velocity[1] = (((acceleration[1]*-9.8) + 0.37) + ((prev_accel[1]*-9.8) / 2) + 0.37) * dt

    # 거리 업데이트 (적분)
    imu_distance[0] = imu_velocity[0] * dt
    imu_distance[1] = imu_velocity[1] * dt
    euclidean_distance()

def update_position(lat, lon, distance, heading):
    R = 6371000
    
    # 방위각을 라디안으로 변환
    heading_rad = math.radians(heading)
    
    # 거리 변화량 계산
    delta_lat = distance * math.cos(heading_rad) / R
    delta_lon = distance * math.sin(heading_rad) / (R * math.cos(math.radians(lat)))
    
    # 새로운 좌표 계산
    plus_lat = math.degrees(delta_lat)
    plus_lon = math.degrees(delta_lon)
    
    return plus_lat, plus_lon

def calculate_angle(start_angle, target_angle):
    # 시계 방향 각도 차이 계산
    clockwise_diff = (target_angle - start_angle + 360) % 360
    # 반시계 방향 각도 차이 계산
    counterclockwise_diff = (start_angle - target_angle + 360) % 360
    
    # 시계 방향이 더 짧으면 +로 표시 (시계 방향) 
    if clockwise_diff <= counterclockwise_diff:
        return float(clockwise_diff)
    # 반시계 방향이 더 짧으면 -로 표시 (반시계 방향)
    else:
        return -float(counterclockwise_diff)
    
#쓰레드_실행함수_정의--------------------gps---------------------------------------------gps------------------------------------

def gps_part():
    global lat, lon
    while True:
        lat_yet, lon_yet = read_gps_data(ser)
        if lat_yet is not None and lon_yet is not None:
            lat, lon = lat_yet, lon_yet
            time.sleep(1)

def imu_part():
    find_ttyUSB()

    port = "COM23"
    baudrate = 921600

    try:
        hf_imu = serial.Serial(port=port, baudrate=baudrate, timeout=0.5)

        if hf_imu.isOpen():
            print("imu sensor serial open success...")
        else:
            hf_imu.open()
            print("imu sensor serial open success...")
    except Exception as e:
        print("Exception:"+str(e))
        print("imu sensor serial open fail")
        exit(0)
    else:

        while True:
            try:
                buff_count = hf_imu.inWaiting()
            except Exception as e:
                print("Exception:" + str(e))
                print("imu lost connection, poor contact or broken wire")
                exit(0)
            else:
                if buff_count > 0:
                    buff_data = hf_imu.read(buff_count)
                    for i in range(0, buff_count):
                        handleSerialData(buff_data[i])
            time.sleep(0.01)

def lidar_part():
    rospy.Subscriber("/scan", LaserScan, scanCallback)

#------------------------실행함수-------------------------------실행함수------------------------------

if __name__ == "__main__":

    i = 0
    prev_lat, prev_lon = None, None
    planning_point_number = 0
    point_number = 0
    rospy.init_node('Gps+imu+lidar_drive start')

    part_gps = threading.Thread(target=gps_part, daemon=True)
    part_imu = threading.Thread(target=imu_part, daemon=True)
    part_lidar = threading.Thread(target=lidar_part, daemon=True)
    timer_thread = threading.Thread(target=timeout, daemon=True)
    
    part_gps.start()
    part_imu.start()
    part_lidar.start()
    timer_thread.start()

    while lat is None or lon is None:
        print("Waiting for GPS data...")
        time.sleep(1)  # GPS 데이터 수신 대기

    heading_degree_found()

    while heading_degree is None:
        print("Waiting for heading degree data...")
        time.sleep(1)  # heading_degree 데이터 수신 대기

    rospy.wait_for_message("/scan", LaserScan)
    print("lidar Ready ---------------")

    print("driving_start")

    time.sleep(1)

    while True:
        time.time()
        if lidar_stop_car == True:
            try:
                publisher(0.0, 0.0)
            except rospy.ROSInterruptException:
                pass
        else:
            while mid_object == True and right_object == True and left_object == False:
                try:
                    publisher(0.0, 0.0)
                except rospy.ROSInterruptException:
                    pass
            while mid_object == True and left_object == True and right_object == False:        
                try:
                    publisher(0.0, 0.0)
                except rospy.ROSInterruptException:
                    pass
            try:
                point_number += 1
                update_velocity_and_distance_trapezoid()
                heading_degree_found()
                
    #                save_to_csv(gps_imu_save_path, i, imu_lat, imu_lon)
                if prev_lat != lat or prev_lon != lon:
                    #imu 데이터 드리프트를 막기위한 속도 및 거리초기화
                    imu_distance[0], imu_distance[1] = 0, 0
                    imu_velocity[0], imu_velocity[1] = 0, 0
                    #새로운 좌표값에 대응, 이전 위도, 이전 경도, imu로 더할 좌표값 업데이트
                    prev_lat, imu_lat, prev_lon, imu_lon = lat, lat, lon, lon
                
    #                if lat is not None and lon is not None:
    #                    print(f"gps + imu 좌표: {imu_lat}, {imu_lon}")
                print(f"heading_degree: {heading_degree}")
            
                lat_closest_value = min(lat_data, key=lambda x: abs(x- imu_lat))
                lon_closest_value = min(lon_data, key=lambda x: abs(x- imu_lon))

                lat_index = lat_data.index(lat_closest_value)
                lon_index = lon_data.index(lon_closest_value)

                if prev_lat == lat or prev_lon == lon:
                    plus_imu_lat, plus_imu_lon = update_position(lat, lon, imu_euclidean_distance, heading_degree)
                    imu_lat += plus_imu_lat
                    imu_lon += plus_imu_lon

                #소수점 11자리에서 올림 -> folium으로 디버깅할 때 값이 제대로 입력이 안되기 때문
                imu_lat = round(imu_lat, 11)
                imu_lon = round(imu_lon, 11)

                save_to_csv(gps_imu_save_path, i, imu_lat, imu_lon)

                if lat_index == lon_index:
                    # 현재 GPS 좌표가 계획된 좌표의 오차 범위 내에 있는지 확인합니다.
                    if is_within_tolerance(imu_lat, imu_lon, lat_closest_value, lon_closest_value, tolerance):
                        planning_point_number = planning_point_data[lat_index]
                        previous_planning_point_number = planning_point_number
                        planning_point_data_bool = True
    #                        print(f"가장 근사한 좌표는:\n포인트 넘버: {planning_point_number}, 위도: {lat_closest_value}, 경도: {lon_closest_value}")
                    else:
                        planning_point_number = previous_planning_point_number
                        planning_point_data_bool = False
    #                        print(f"경로에서 벗어났거나 GPS 오차범위에 들어가지 않았습니다.")
                elif lat_index <= lon_index:
                    if is_within_tolerance(imu_lat, imu_lon, lat_closest_value, lon_closest_value, tolerance):
                        planning_point_number = planning_point_data[lat_index]
                        previous_planning_point_number = planning_point_number
                        planning_point_data_bool = True
    #                        print(f"가장 근사한 좌표는:\n포인트 넘버: {planning_point_number}, 위도: {lat_closest_value}, 경도: {lon_data[lat_index]}")
                    else:
                        planning_point_number = previous_planning_point_number
                        planning_point_data_bool = False
    #                        print(f"경로에서 벗어났거나 GPS 오차범위에 들어가지 않았습니다.")

                elif lon_index <= lat_index:
                    if is_within_tolerance(imu_lat, imu_lon, lat_closest_value, lon_closest_value, tolerance):
                        planning_point_number = planning_point_data[lon_index]
                        previous_planning_point_number = planning_point_number
                        planning_point_data_bool = True
    #                        print(f"가장 근사한 좌표는:\n포인트 넘버: {planning_point_number}, 위도: {lat_data[lon_index]}, 경도: {lon_closest_value}")
                    else:
                        planning_point_number = previous_planning_point_number
                        planning_point_data_bool = False
    #                        print(f"경로에서 벗어났거나 GPS 오차범위에 들어가지 않았습니다.")
                else:
                    planning_point_number = previous_planning_point_number
                    planning_point_data_bool = False
    #                    print(f"경로에서 벗어났거나 GPS 오차범위에 들어가지 않았습니다.")

                next_planning_point_number = planning_point_number + 2
                previous_planning_point_number = planning_point_number

                if planning_point_number >= len(lat_data) - 2 or planning_point_number == len(lon_data) - 2:
                    print("목적지입니다. 주행을 종료합니다")
                    try:
                        publisher(0.0, 0.0)
                    except rospy.ROSInterruptException:
                        pass
                    sys.exit()
                    break

                if planning_point_data_bool == False:
                    if previous_planning_point_number == 0:
                        print(f"경로에서 벗어났거나 GPS 오차범위에 들어가지 않았습니다.")
                        first_target_bearing = calculate_bearing(imu_lat, imu_lon, lat_data[1], lon_data[1])
                        first_remain_distance = calculate_distance(imu_lat, imu_lon, lat_data[1], lon_data[1])
                        first_angle_to_move = calculate_angle(heading_degree, first_target_bearing)
                        if abs(first_angle_to_move) >= 43.0:
                            if  first_angle_to_move < 0.0:
                                real_steering_angle = -43.0
                            else :
                                real_steering_angle = 43.0
                        else:
                            real_steering_angle =  first_angle_to_move
                        print(f"가장 근사한 좌표는:\n포인트 넘버: {planning_point_number} \n 다음 포인트까지남은 거리: {first_remain_distance*1000}m, 다음 포인트로의 방위각{first_target_bearing}")
                    
                if planning_point_data_bool == True:
                    print("현재 경로에 위치합니다") 
                    target_bearing = calculate_bearing(lat_data[planning_point_number], lon_data[planning_point_number], lat_data[next_planning_point_number], lon_data[next_planning_point_number])
                    remain_distance = calculate_distance(lat_data[planning_point_number], lon_data[planning_point_number], lat_data[next_planning_point_number], lon_data[next_planning_point_number])
                    angle_to_move = calculate_angle(heading_degree, target_bearing)
                    if abs(angle_to_move) >= 43.0:
                        if angle_to_move < 0.0:
                            real_steering_angle = -43.0
                        else :
                            real_steering_angle = 43.0
                    else:
                        real_steering_angle = angle_to_move
                    print(f"가장 근사한 좌표는:\n포인트 넘버: {planning_point_number} \n 다음 포인트까지남은 거리: {remain_distance*1000}m, 다음 포인트로의 각도{real_steering_angle}")

                    try:
                        real_steering_angle = -real_steering_angle
                        publisher(speed_set, real_steering_angle)
                    except rospy.ROSInterruptException:
                        pass
                        time.sleep(0.1)
                    except KeyboardInterrupt:
                        print("프로그램이 종료되었습니다.")
                        
            except Exception as e:
                print(f"오류 발생: {e}")
                try:
                    publisher(0.0, 0.0)
                except rospy.ROSInterruptException:
                    pass
                continue