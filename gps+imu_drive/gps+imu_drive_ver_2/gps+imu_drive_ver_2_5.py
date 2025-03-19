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
import numpy as np
import sys

#변수 및 리스트--------------------gps---------------------------------------------gps------------------------------------

# 시리얼 포트 설정 (하나의 아두이노만 사용)
ser = serial.Serial('COM30', 115200)
time.sleep(2)  # 시리얼 통신 초기화 대기

speed_set = 50
steering_angle_set = 0

# GPS 관련 변수
tolerance = 0.000500
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

#IMU센서 이중 적분
#순서대로~ 샘플링 시간 간격 (초), 속도, 거리, 이전 가속도
dt, imu_velocity, imu_distance, prev_accel = 0.00666, {0:0, 1:0, 2:0}, {0:0, 1:0, 2:0}, [0, 0, 0] # 150Hz 샘플링

# gps+imu 융합 좌표 저장
gps_imu_save_path = "C:/Users/plane/Desktop/park_ws/gps+imu_drive/gps+imu_coordinates.csv"

#경로 계획 좌표 읽기
planning_csv_path = "C:/Users/plane/Desktop/park_ws/gps+imu_drive/bunsudae_planning.csv"

# CSV 파일 읽기
planning_data = pd.read_csv(planning_csv_path)

# 위도와 경도 데이터 추출
lat_data = planning_data['Latitude'].tolist()
lon_data = planning_data['Longitude'].tolist()

#pure_pursuit 알고리즘 파라미터 설정
k = 0.1  # 순수 추적 제어기의 전방 감도
Lfc = 1.0  # [m] 전방 거리
Kp = 1.0  # 속도 비례 제어 이득
WB = 0.75  # [m] 차량의 축간 거리

time_limit = 1000000 #주행 중단 시간(s)

Bon = 0.5 #조향각 계산에서 기준이 되는 값으로, 이 값이 커지면 조향각이 작아지고, 작아지면 조향각이 커져 차량의 회전 반응이 변화
WB_k = 2 #차량의 조향 동작에서의 비례성을 높이는 역할


with open(gps_imu_save_path, mode='w', newline='') as gps_file:
    gps_writer = csv.writer(gps_file)
    gps_writer.writerow(["Point Number", "Latitude", "Longitude"])

def save_to_csv(file_path, Point_number, Latitude, Longitude):
    """좌표 데이터를 CSV에 저장하는 함수"""
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([Point_number, Latitude, Longitude])

#함수정의----------------------------motor-----------------------------motor------------------------------------

class Motor_control:
# 모터 제어 함수
    def __init__(self, speed = None, angle = None, accel = None):
        self.motor_speed = speed
        self.steering_angle = angle
        self.acceleration = accel

    def send_motor_speed(self, speed = None):
        """모터 속도 설정"""
        if speed is not None:
            self.motor_speed = speed
        print(f"Sent Motor Speed: {self.motor_speed}")

    def send_steering_angle(self, angle = None):
        """조향 각도 설정"""
        if angle is not None:
            self.motor_speed = angle
        print(f"Sent Steering Angle: {self.steering_angle}")

    def stop_motors(self):
        """모터 정지"""
        self.send_motor_speed(0)

    def stop_steering(self):
        """조향 중립 설정"""
        self.send_steering_angle(0)

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
                            if not (35.11 <= lat <= 35.14 and 128 <= lon <= 130):
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

def heading_degree_found():
    global  heading_degree
    heading = math.atan2(magnetometer[1],magnetometer[0])
    declination_angle = (-8.0 + (-29.0 / 60.0)) / (180 / math.pi)
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

class State:

    """
    차량의 상태를 나타내는 클래스입니다.
    """

    def __init__(self, lat=0.0, lon=0.0, heading_degree=0.0):
        self.lat = lat  # 차량의 X 좌표
        self.lon = lon  # 차량의 Y 좌표
        self.heading_degree = heading_degree  # 차량의 요각
        self.rear_lat, self.rear_lon = self.calculate_rear_position()

    def calculate_rear_position(self):

        # 지구 반경 (대략적인 값, km)
        EARTH_RADIUS = 6371.0 * 1000  # meters
        # 위도 1도는 111.32 km, 경도 1도는 위도에 따라 다름
        delta_lat = (WB / EARTH_RADIUS) * math.cos(self.heading_degree)
        delta_lon = (WB / EARTH_RADIUS) * math.sin(self.heading_degree) / math.cos(math.radians(self.lat))
        
        # 후륜의 위도와 경도 계산 (현재 위치에서 이동)
        rear_lat = self.lat - math.degrees(delta_lat)
        rear_lon = self.lon - math.degrees(delta_lon)

        return rear_lat, rear_lon

    def update(self, lat, lon, heading_degree):
        """
        가속도와 조향각에 따라 차량의 상태를 업데이트합니다.
        """
        self.lat = lat  # 차량의 X 좌표
        self.lon = lon  # 차량의 Y 좌표
        self.heading_degree = heading_degree
        self.rear_lat, self.rear_lon = self.calculate_rear_position()

    def calc_distance(self, lat, lon):
        """
        후축에서 주어진 점까지의 거리를 계산합니다.
        """
        rear_lat = self.rear_lat
        rear_lon = self.rear_lon
        distance = calculate_distance(rear_lat, rear_lon, lat, lon)
        return distance
    
class TargetCourse:
    """
    목표 경로를 나타내는 클래스입니다.
    """

    def __init__(self, c_lat, c_lon):

        self.c_lat = c_lat  # 경로의 X 좌표
        self.c_lon = c_lon  # 경로의 Y 좌표
        self.old_nearest_point_index = None  # 가장 가까운 점의 인덱스
        self.imu_speed = None

    def search_target_index(self, state):
        """
        현재 상태를 기반으로 경로에서 목표 인덱스를 검색합니다.
        """
        if self.old_nearest_point_index is None:
            # 경로에서 가장 가까운 점의 인덱스를 찾습니다.
            ind = 0
            distances = []

            for ic_lat, ic_lon in zip(self.c_lat, self.c_lon):
                # 하버사인 공식을 사용하여 두 지점 사이의 거리 계산
                distance = state.calc_distance(ic_lon, ic_lat)
                distances.append(distance)

            # 가장 가까운 점의 인덱스를 찾습니다.
            self.old_nearest_point_index = np.argmin(distances)
        else:
            ind = self.old_nearest_point_index
            distance_this_index = state.calc_distance(self.c_lat[ind], self.c_lon[ind])
            while True:
                distance_next_index = state.calc_distance(self.c_lat[ind + 1], self.c_lon[ind + 1])
                if distance_this_index < distance_next_index:
                    break
                ind = ind + 1 if (ind + 1) < len(self.c_lat) else ind
                distance_this_index = distance_next_index
            self.old_nearest_point_index = ind

        #Lf = k * self.imu_speed + Lfc  # 차량 속도에 기반한 전방 거리 업데이트
        Lf = 2.5
        # 전방 거리가 목표 점까지의 거리보다 클 때까지 목표 점 인덱스를 찾습니다.
        while Lf > state.calc_distance(self.c_lat[ind], self.c_lon[ind]):
            if (ind + 1) >= len(self.c_lat):
                break  # 목표를 초과하지 않도록 함
            ind += 1
        
        target_lat = self.c_lat[ind]
        target_lon = self.c_lon[ind]

        if is_within_tolerance(state.lat, state.lon, target_lat, target_lon, tolerance=0.001):
            print(f"목표에 도달했습니다. (lat: {target_lat}, lon: {target_lon}, index: {ind})")
            ind = len(self.c_lat) - 1  # 마지막 인덱스로 설정하여 멈추도록 함

        return ind, Lf
    
def pure_pursuit_steer_control(state, trajectory, pind):
    """
    순수 추적 제어를 사용하여 조향각을 계산합니다.
    """
    ind, _ = trajectory.search_target_index(state)

    if pind >= ind:
        ind = pind

    if ind < len(trajectory.c_lat):
        tt = trajectory.c_lat[ind]
        tn = trajectory.c_lon[ind]
    else:  # 목표 방향으로
        tt = trajectory.c_lat[-1]
        tn = trajectory.c_lon[-1]
        ind = len(trajectory.c_lat) - 1

    target_degree = calculate_bearing(state.rear_lat, state.rear_lon, tt, tn)
    alpha = target_degree - state.heading_degree
    # 각도를 -180도에서 180도 범위로 조정
    print(f"point to point degree & index: {alpha}, {ind}")

    return alpha, ind


#쓰레드_실행함수_정의--------------------gps---------------------------------------------gps------------------------------------

def gps_part():
    global lat, lon

    lat_yet, lon_yet = read_gps_data(ser)
    # GPS 데이터가 유효한지 확인
    if lat_yet is not None and lon_yet is not None:
        lat, lon = lat_yet, lon_yet

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

part_gps = threading.Thread(target=gps_part, daemon=True)
part_imu = threading.Thread(target=imu_part, daemon=True)

part_gps.start()
part_imu.start()

if __name__ == "__main__":

    i = 0
    starting_degree = None
    prev_lat, prev_lon = None, None

    while lat is None or lon is None:
        print("Waiting for GPS data...")
    time.sleep(1)  # GPS 데이터 수신 대기

    c_lat = lat_data
    c_lon = lon_data

    runtime = 0.0

    update_velocity_and_distance_trapezoid()
    heading_degree_found()

    while heading_degree is None:
        print("Waiting for heading degree data...")
        time.sleep(1)  # heading_degree 데이터 수신 대기

    state = State(lat = lat, lon = lon, heading_degree = heading_degree)
    target_course = TargetCourse(c_lat, c_lon)
    target_ind, _ = target_course.search_target_index(state)

    Motor = Motor_control(speed = 0, angle = steering_angle_set)
    Motor.send_motor_speed()
    Motor.send_steering_angle()
    time.sleep(6)

    while True:
        try:
            heading_degree_found()

            update_velocity_and_distance_trapezoid()
            heading_degree_found()

    #            if lat is not None and lon is not None:
    #                print(f"GPS 좌표: {lat}, {lon}")
    #            else:
    #                print(f"GPS 신호 수신 못함")

            if prev_lat == lat or prev_lon == lon:
                plus_imu_lat, plus_imu_lon = update_position(lat, lon, imu_euclidean_distance, heading_degree)
                imu_lat += plus_imu_lat
                imu_lon += plus_imu_lon

                #소수점 11자리에서 올림 -> folium으로 디버깅할 때 값이 제대로 입력이 안되기 때문
                imu_lat = round(imu_lat, 11)
                imu_lon = round(imu_lon, 11)
                
    #                save_to_csv(gps_imu_save_path, i, imu_lat, imu_lon)

            if prev_lat != lat or prev_lon != lon:
                #imu 데이터 드리프트를 막기위한 속도 및 거리초기화
                imu_distance[0], imu_distance[1] = 0, 0
                imu_velocity[0], imu_velocity[1] = 0, 0
                #새로운 좌표값에 대응, 이전 위도, 이전 경도, imu로 더할 좌표값 업데이트
                prev_lat, imu_lat, prev_lon, imu_lon = lat, lat, lon, lon
            
    #            if lat is not None and lon is not None:
    #                print(f"gps + imu 좌표: {imu_lat}, {imu_lon}")
            print(f"heading_degree: {heading_degree}")
                
    #            state.update(lat = imu_lat, lon = imu_lon, heading_degree = heading_degree)  # 제어 입력에 따라 차량 상태 업데이트
            new_angle, target_ind = pure_pursuit_steer_control(state, target_course, target_ind)
            state.update(lat = imu_lat, lon = imu_lon, heading_degree = heading_degree)

            if abs(new_angle) >= 43:
                if new_angle < 0:
                    real_steering_angle = 43.0
                else:
                    real_steering_angle = -43.0
            else:
                real_steering_angle = new_angle

            Motor.steering_angle(real_steering_angle)

            Motor.send_motor_speed(speed_set)
            Motor.send_steering_angle()
            runtime += dt
    #            print(f"주행 시간: {runtime}")

            if runtime == time_limit:
                print("주행 시간 끝나 프로그램을 종료합니다.")
                Motor.stop_motors()
                Motor.stop_steering()
                sys.exit()
                break

        except KeyboardInterrupt:
            print("프로그램이 종료되었습니다.")
            Motor.stop_motors()
            Motor.stop_steering()
            break

        except Exception as e:
            print(f"오류 발생: {e}")
            Motor.stop_motors()
            Motor.stop_steering()
            continue