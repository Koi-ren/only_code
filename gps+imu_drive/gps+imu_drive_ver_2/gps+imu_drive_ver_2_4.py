#!/usr/bin/env python3
# -*- coding:utf-8 -*-

#모듈 임포트
import serial
import serial.tools.list_ports
import time
import math
import struct
import platform
import threading
import csv
import numpy as np
import pandas as pd

# 시리얼 포트 설정 및 초기화
ser = serial.Serial('COM30', 115200)
time.sleep(2)

# 모터 및 조향 초기 값
speed = 50
steering_angle_set = 0

# GPS 관련 변수
tolerance = 0.000900

# IMU 센서 초기화
key, flag, buff = 0, 0, {}
angularVelocity, acceleration, magnetometer, angle_degree = [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]
pub_flag = [True, True]
python_version = platform.python_version()[0]

#IMU센서 이중 적분
#순서대로~ 샘플링 시간 간격 (초), 속도, 거리, 이전 가속도
dt, imu_velocity, imu_distance, prev_accel = 0.00666, {0:0, 1:0, 2:0}, {0:0, 1:0, 2:0}, [0, 0, 0] # 150Hz 샘플링

# gps+imu 융합 좌표 저장
gps_imu_save_path = "C:/Users/plane/Desktop/park_ws/gps+imu_drive/gps+imu_coordinates.csv"

#경로 계획 좌표 읽기
planing_data = pd.read_excel('C:/Users/plane/Desktop/park_ws/gps_track/gps_drive/fix_planning_data.xlsx')
lat_data, lon_data = planing_data['lat'], planing_data['lon']

#pure_pursuit 알고리즘 파라미터 설정
k = 0.1  # 순수 추적 제어기의 전방 감도
Lfc = 2.0  # [m] 전방 거리
Kp = 1.0  # 속도 비례 제어 이득
WB = 0.75  # [m] 차량의 축간 거리

with open(gps_imu_save_path, mode='w', newline='') as gps_file:
    gps_writer = csv.writer(gps_file)
    gps_writer.writerow(["Point Number", "Latitude", "Longitude"])

def save_to_csv(file_path, Point_number, Latitude, Longitude):
    """좌표 데이터를 CSV에 저장하는 함수"""
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([Point_number, Latitude, Longitude])

# 모터 제어 함수
def send_motor_speed(speed):
    """모터 속도 설정"""
    print(f"Sent Motor Speed: {speed}")
    stop_motors()

def send_steering_angle(angle):
    """조향 각도 설정"""
    print(f"Sent Steering Angle: {angle}")

def stop_motors():
    """모터 정지"""
    send_motor_speed(0)

def stop_steering():
    """조향 중립 설정"""
    send_steering_angle(0)

# GPS 데이터 읽기 함수
def read_gps_data(ser):
    """시리얼 포트에서 GPS 데이터를 읽어들임"""
    lat, lon = None, None
    try:
        while not (lat and lon):
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                print(f"Read line from {ser.port}: {line}")
                if line.startswith("Lat:"):
                    parts = line.split()
                    if len(parts) >= 6:
                        lat, lon = float(parts[1]) / 10000000.0, float(parts[3]) / 10000000.0
                        if not (35.11 <= lat <= 35.14 and 128 <= lon <= 130):
                            lat, lon = None, None
                            print("잘못된 데이터 범위. 다시 시도 중...")
    except Exception as e:
        print(f"오류 발생: {e}")
        return None, None
    return lat, lon

# 거리 계산 함수 (Haversine 공식)
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1_rad, lon1_rad = map(math.radians, [lat1, lon1])
    lat2_rad, lon2_rad = map(math.radians, [lat2, lon2])
    dlat, dlon = lat2_rad - lat1_rad, lon2_rad - lon1_rad
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

# 오차 범위 내 좌표 확인 함수
def is_within_tolerance(lat1, lon1, lat_target, lon_target, tolerance):
    return calculate_distance(lat1, lon1, lat_target, lon_target) <= tolerance

# IMU 관련 함수
def find_ttyUSB():
    print("IMU default serial port is COM30")
    ports = [port.device for port in serial.tools.list_ports.comports() if 'COM' in port.device]
    print(f"Current connected ports: {ports}")

def hex_to_ieee(raw_data):
    ieee_data = []
    raw_data.reverse()
    for i in range(0, len(raw_data), 4):
        data2str = ''.join([hex(b | 0xff00)[4:6] for b in raw_data[i:i+4]])
        ieee_data.append(struct.unpack('>f', bytes.fromhex(data2str))[0])
    ieee_data.reverse()
    return ieee_data

def checkSum(data_list, check_data):
    crc = 0xFFFF
    for pos in bytearray(data_list):
        crc ^= pos
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    return hex((crc & 0xff) << 8 | crc >> 8) == hex(check_data[0] << 8 | check_data[1])

def handleSerialData(raw_data):
    global key, buff, pub_flag, angularVelocity, acceleration, magnetometer, angle_degree, prev_accel
    buff[key] = ord(raw_data) if python_version == '2' else raw_data
    key += 1
    if buff[0] != 0xaa or key < 3 or buff[1] != 0x55 or key < buff[2] + 5:
        return
    data_buff = list(buff.values())
    if buff[2] == 0x2c and pub_flag[0] and checkSum(data_buff[2:47], data_buff[47:49]):
        data = hex_to_ieee(data_buff[7:47])
        angularVelocity, acceleration, magnetometer = data[1:4], data[4:7], data[7:10]
        pub_flag[0] = False
    elif buff[2] == 0x14 and pub_flag[1] and checkSum(data_buff[2:23], data_buff[23:25]):
        angle_degree = hex_to_ieee(data_buff[7:23])[1:4]
        pub_flag[1] = False
    key, buff = 0, {}

    prev_accel = acceleration.copy()

def heading_degree_found():
    global heading_degrees
    heading = math.atan2(magnetometer[1], magnetometer[0]) + (-8.0 + (-29.0 / 60.0)) / (180 / math.pi)
    heading = heading % (2 * math.pi)
    heading_degrees = heading * 180 / math.pi
    return heading_degrees

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
    # 트라페zoid 적분법으로 속도 업데이트
    #imu_velocity[0] += (((acceleration[0]*-9.8) + 0.07) + ((prev_accel[0]*-9.8) + 0.07) / 2) * dt
    #imu_velocity[1] += (((acceleration[1]*-9.8) + 0.37) + ((prev_accel[1]*-9.8) / 2) + 0.37) * dt

    # 거리 업데이트 (적분)
    #imu_distance[0] += imu_velocity[0] * dt
    #imu_distance[1] += imu_velocity[1] * dt
    #euclidean_distance()
    
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

def euclidean_distance():
    global imu_euclidean_distance
    """
    (0, 0)에서 (x, y)까지의 유클리드 거리 계산 함수
    :param x: x축으로 이동한 거리
    :param y: y축으로 이동한 거리
    :return: (0, 0)에서 (x, y)까지의 거리
    """
    imu_euclidean_distance = math.sqrt((imu_distance[0]**2  )+ imu_distance[1]**2)

class State:

    """
    차량의 상태를 나타내는 클래스입니다.
    """

    def __init__(self, x=0.0, y=0.0, yaw=0.0, v=0.0):
        self.x = x  # 차량의 X 좌표
        self.y = y  # 차량의 Y 좌표
        self.yaw = yaw  # 차량의 요각
        self.v = v  # 차량의 속도
        self.rear_x = self.x - ((WB / 2) * math.cos(self.yaw))  # 후축의 X 좌표
        self.rear_y = self.y - ((WB / 2) * math.sin(self.yaw))  # 후축의 Y 좌표

    def update(self, a, delta):
        """
        가속도와 조향각에 따라 차량의 상태를 업데이트합니다.
        """
        self.x += self.v * math.cos(self.yaw) * dt
        self.y += self.v * math.sin(self.yaw) * dt
        self.yaw += self.v / WB * math.tan(delta) * dt
        self.v += a * dt
        self.rear_x = self.x - ((WB / 2) * math.cos(self.yaw))
        self.rear_y = self.y - ((WB / 2) * math.sin(self.yaw))

    def calc_distance(self, point_x, point_y):
        """
        후축에서 주어진 점까지의 거리를 계산합니다.
        """
        dx = self.rear_x - point_x
        dy = self.rear_y - point_y
        return math.hypot(dx, dy)
    
class States:
    """
    차량의 상태 이력을 저장하는 클래스입니다.
    """

    def __init__(self):
        self.x = []  # X 좌표 리스트
        self.y = []  # Y 좌표 리스트
        self.yaw = []  # 요각 리스트
        self.v = []  # 속도 리스트
        self.t = []  # 시간 리스트

    def append(self, t, state):
        """
        현재 상태와 시간을 이력에 추가합니다.
        """
        self.x.append(state.x)
        self.y.append(state.y)
        self.yaw.append(state.yaw)
        self.v.append(state.v)
        self.t.append(t)

class TargetCourse:
    """
    목표 경로를 나타내는 클래스입니다.
    """

    def __init__(self, cx, cy):
        self.cx = cx  # 경로의 X 좌표
        self.cy = cy  # 경로의 Y 좌표
        self.old_nearest_point_index = None  # 가장 가까운 점의 인덱스

    def search_target_index(self, state):
        """
        현재 상태를 기반으로 경로에서 목표 인덱스를 검색합니다.
        """
        if self.old_nearest_point_index is None:
            # 경로에서 가장 가까운 점의 인덱스를 찾습니다.
            dx = [state.rear_x - icx for icx in self.cx]
            dy = [state.rear_y - icy for icy in self.cy]
            d = np.hypot(dx, dy)
            ind = np.argmin(d)
            self.old_nearest_point_index = ind
        else:
            ind = self.old_nearest_point_index
            distance_this_index = state.calc_distance(self.cx[ind], self.cy[ind])
            while True:
                distance_next_index = state.calc_distance(self.cx[ind + 1], self.cy[ind + 1])
                if distance_this_index < distance_next_index:
                    break
                ind = ind + 1 if (ind + 1) < len(self.cx) else ind
                distance_this_index = distance_next_index
            self.old_nearest_point_index = ind

        Lf = k * state.v + Lfc  # 차량 속도에 기반한 전방 거리 업데이트

        # 전방 거리가 목표 점까지의 거리보다 클 때까지 목표 점 인덱스를 찾습니다.
        while Lf > state.calc_distance(self.cx[ind], self.cy[ind]):
            if (ind + 1) >= len(self.cx):
                break  # 목표를 초과하지 않도록 함
            ind += 1

        return ind, Lf
    
def pure_pursuit_steer_control(state, trajectory, pind):
    """
    순수 추적 제어를 사용하여 조향각을 계산합니다.
    """
    ind, Lf = trajectory.search_target_index(state)

    if pind >= ind:
        ind = pind

    if ind < len(trajectory.cx):
        tx = trajectory.cx[ind]
        ty = trajectory.cy[ind]
    else:  # 목표 방향으로
        tx = trajectory.cx[-1]
        ty = trajectory.cy[-1]
        ind = len(trajectory.cx) - 1

    alpha = math.atan2(ty - state.rear_y, tx - state.rear_x) - state.yaw
    delta = math.atan2(2.0 * WB * math.sin(alpha) / Lf, 1.0)

    return delta, ind


def proportional_control(target, current):
    """
    비례 제어를 사용하여 제어 입력(가속도)을 계산합니다.
    """
    a = Kp * (target - current)
    return a

# GPS 및 IMU 쓰레드 실행
def gps_part():
    global lat, lon
    while True:
        lat_yet, lon_yet = read_gps_data(ser)
        if lat_yet is not None and lon_yet is not None:
            lat, lon = lat_yet, lon_yet
            time.sleep(1)

def imu_part():
    find_ttyUSB()
    try:
        hf_imu = serial.Serial(port="COM23", baudrate=921600, timeout=0.5)
        if not hf_imu.isOpen():
            hf_imu.open()
    except Exception as e:
        print(f"IMU 센서 오류: {e}")
        exit(0)
    while True:
        buff_count = hf_imu.inWaiting()
        if buff_count > 0:
            for i in hf_imu.read(buff_count):
                handleSerialData(i)

# 쓰레드 시작
def main_loop():
    i = 0
    prev_lat, prev_lon = None, None

    cx = lat_data
    cy = lon_data

    lastIndex = len(cx) - 1
    time = 0.0

    heading_degrees = heading_degree_found()
    target_speed = 6.0 / 3.6  # [m/s] 목표 속도
    target_course = TargetCourse(cx, cy)
    state = State(x = lat, y = lon, yaw = heading_degrees, v = 0.0)
    target_ind, _ = target_course.search_target_index(state)
    time.sleep(6)  # 초기화 대기 시간

    while True and lastIndex > target_ind:
        i += 1
        #내부 쓰레드
        part_heading = threading.Thread(target=heading_degree_found, daemon=True)
        part_calculated_distance = threading.Thread(target= update_velocity_and_distance_trapezoid, daemon=True)

        part_heading.start()
        part_calculated_distance.start()
        
        part_heading.join()  # 쓰레드 완료 대기
        part_calculated_distance.join()  # 쓰레드 완료 대기

        if lat is not None and lon is not None:
            print(f"GPS 좌표: {lat}, {lon}")
        else:
            print(f"GPS 신호 수신 못함")

        if prev_lat == lat or prev_lon == lon:
            plus_imu_lat, plus_imu_lon = update_position(lat, lon, imu_euclidean_distance, heading_degrees)
            imu_lat += plus_imu_lat
            imu_lon += plus_imu_lon

            #소수점 11자리에서 올림 -> folium으로 디버깅할 때 값이 제대로 입력이 안되기 때문
            imu_lat = round(imu_lat, 11)
            imu_lon = round(imu_lon, 11)
            
            save_to_csv(gps_imu_save_path, i, imu_lat, imu_lon)

        if prev_lat != lat or prev_lon != lon:
            #imu 데이터 드리프트를 막기위한 속도 및 거리초기화
            imu_distance[0], imu_distance[1] = 0, 0
            imu_velocity[0], imu_velocity[1] = 0, 0
            #새로운 좌표값에 대응, 이전 위도, 이전 경도, imu로 더할 좌표값 업데이트
            prev_lat, imu_lat, prev_lon, imu_lon = lat, lat, lon, lon
        
        if lat is not None and lon is not None:
            print(f"gps + imu 좌표: {imu_lat}, {imu_lon}")

        ai = proportional_control(target_speed, state.v)
        di, target_ind = pure_pursuit_steer_control(state, target_course, target_ind)

        state(ai, di)

        time += dt
        time.sleep(0.00666)

if __name__ == "__main__":
    # GPS 및 IMU 스레드 시작
    part_gps = threading.Thread(target=gps_part, daemon=True)
    part_imu = threading.Thread(target=imu_part, daemon=True)

    part_gps.start()
    part_imu.start()

    print("경로 추적 시작")
    main_loop()