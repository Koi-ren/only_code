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

# 파라미터 설정
k = 0.1  # 순수 추적 제어기의 전방 감도
Lfc = 2.0  # [m] 전방 거리
Kp = 1.0  # 속도 비례 제어 이득
dt = 0.1  # [s] 시뮬레이션 시간 간격
WB = 2.9  # [m] 차량의 축간 거리

class gps_part:

    # 시리얼 포트 설정 및 초기화
    def __init__(self, port='COM30', baudrate=115200):
        # 시리얼 포트 설정 및 초기화
        self.ser = serial.Serial(port, baudrate)
        self.lat, self.lon = 0, 0
        self.lock = threading.Lock()
        time.sleep(2)  # 시리얼 포트 초기화 대기

    def read_gps_data(self):
        """시리얼 포트에서 GPS 데이터를 읽어들임"""
        with self.lock:
            self.lat, self.lon = None, None
        try:
            while not (self.lat and self.lon):
                if self.ser.in_waiting > 0:
                    line = self.ser.readline().decode('utf-8').strip()
                    print(f"Read line from {self.ser.port}: {line}")
                    if line.startswith("Lat:"):
                        parts = line.split()
                        if len(parts) >= 6:
                            self.lat, self.lon = float(parts[1]) / 10000000.0, float(parts[3]) / 10000000.0
                            if not (35.11 <= self.lat <= 35.14 and 128 <= self.lon <= 130):
                                self.lat, self.lon = None, None
                                print("잘못된 데이터 범위. 다시 시도 중...")
        except Exception as e:
            print(f"오류 발생: {e}")
            return None, None
        with self.lock:
            return self.lat, self.lon

    def gps_start(self):
        while True:
            lat_yet, lon_yet = self.read_gps_data()
            if lat_yet is not None and lon_yet is not None:
                with self.lock:
                    self.lat, self.lon = lat_yet, lon_yet
            time.sleep(1)

#기존 prev_accel = acceleration.copy() -> 
# self.prev_accel = self.acceleration.copy()로 변경
# 위치 고려할 것
class Imu_part:

    def __init__(self):
        # IMU 센서 초기화
        self.key = 0
        self.flag = 0
        self.buff = {}
        self.angularVelocity = [0, 0, 0]
        self.acceleration = [0, 0, 0]
        self.magnetometer = [0, 0, 0]
        self.angle_degree = [0, 0, 0]
        self.pub_flag = [True, True]
        self.python_version = platform.python_version()[0]
        self.prev_accel = [0, 0, 0]
        self.lock = threading.Lock()

    def find_ttyUSB(self):
        print("IMU default serial port is COM30")
        ports = [port.device for port in serial.tools.list_ports.comports() if 'COM' in port.device]
        print(f"Current connected ports: {ports}")

    def hex_to_ieee(self, raw_data):
        ieee_data = []
        raw_data.reverse()
        for i in range(0, len(raw_data), 4):
            data2str = ''.join([hex(b | 0xff00)[4:6] for b in raw_data[i:i+4]])
            ieee_data.append(struct.unpack('>f', bytes.fromhex(data2str))[0])
        ieee_data.reverse()
        return ieee_data

    def checkSum(self, data_list, check_data):
        crc = 0xFFFF
        for pos in bytearray(data_list):
            crc ^= pos
            for _ in range(8):
                if crc & 1:
                    crc = (crc >> 1) ^ 0xA001
                else:
                    crc >>= 1
        return hex((crc & 0xff) << 8 | crc >> 8) == hex(check_data[0] << 8 | check_data[1])

    def handleSerialData(self, raw_data):
        self.buff[self.key] = ord(raw_data) if self.python_version == '2' else raw_data
        self.key += 1
        if self.buff[0] != 0xaa or self.key < 3 or self.buff[1] != 0x55 or self.key < self.buff[2] + 5:
            return
        data_buff = list(self.buff.values())
        if self.buff[2] == 0x2c and self.pub_flag[0] and self.checkSum(data_buff[2:47], data_buff[47:49]):
            data = self.hex_to_ieee(data_buff[7:47])
            self.angularVelocity, self.acceleration, self.magnetometer = data[1:4], data[4:7], data[7:10]
            self.pub_flag[0] = False
        elif self.buff[2] == 0x14 and self.pub_flag[1] and self.checkSum(data_buff[2:23], data_buff[23:25]):
            self.angle_degree = self.hex_to_ieee(data_buff[7:23])[1:4]
            self.pub_flag[1] = False
        
        self.key, self.buff = 0, {}
        self.prev_accel = self.acceleration.copy()
        
        with self.lock:
            return self.acceleration, self.magnetometer, self.angle_degree

    def imu_start(self):
        self.find_ttyUSB()
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
                    self.handleSerialData(i)
        

class motor_control:

    # 모터 및 조향 초기 값
    def __init__(self):
        self.speed = 50
        self.steering_angle_set = 0

    # 모터 제어 함수
    def send_motor_speed(self, speed):
        # 모터 속도 설정
        print(f"Sent Motor Speed: {speed}")
        self.stop_motors()

    # 조향 각도 설정
    def send_steering_angle(self, angle):
        print(f"Sent Steering Angle: {angle}")

    # 모터 정지
    def stop_motors(self):
        self.send_motor_speed(0)

    # 조향 중립 설정
    def stop_steering(self):
        self.send_steering_angle(0)

class Calculation:

    #사용시에는 다음과 같이 할 것
    #calc = Calculation(magnetometer=[1, 0])  # 예시 자기장 값
    #calc.heading_degree_found()

    def __init__(self, magnetometer = None, acceleration = None, prev_accel = None):
        self.magnetometer = magnetometer if magnetometer is not None else [0, 0, 0]
        self.acceleration = acceleration if acceleration is not None else [0, 0, 0]
        self.prev_accel = prev_accel if prev_accel is not None else [0, 0, 0]
        self.imu_velocity, self.imu_distance = [0, 0, 0], [0, 0, 0]
        self.heading_degrees, self.imu_euclidean_distance, self.dt, self.plus_lat, self.plus_lon, self.lat = 0, 0, 150, 0, 0, 0  # 초기값 설정

    def calculate_distance(self, lat1, lon1, lat2, lon2):
        R = 6371.0
        lat1_rad, lon1_rad = map(math.radians, [lat1, lon1])
        lat2_rad, lon2_rad = map(math.radians, [lat2, lon2])
        dlat, dlon = lat2_rad - lat1_rad, lon2_rad - lon1_rad
        a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
        return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # 오차 범위 내 좌표 확인 함수
    def is_within_tolerance(self, lat1, lon1, lat_target, lon_target, tolerance = None):
        return self.calculate_distance(lat1, lon1, lat_target, lon_target) <= tolerance
    
    def heading_degree_found(self):
        self.heading = math.atan2(self.magnetometer[1], self.magnetometer[0]) + (-8.0 + (-29.0 / 60.0)) / (180 / math.pi)
        self.heading = self.heading % (2 * math.pi)
        self.heading_degrees = self.heading * 180 / math.pi

    def update_velocity_and_distance_trapezoid(self):
        
        self.imu_velocity[0] = (((self.acceleration[0]*-9.8) + 0.07) + ((self.prev_accel[0]*-9.8) + 0.07) / 2) * self.dt
        self.imu_velocity[1] = (((self.acceleration[1]*-9.8) + 0.37) + ((self.prev_accel[1]*-9.8) / 2) + 0.37) * self.dt

        # 거리 업데이트 (적분)
        self.imu_distance[0] = self.imu_velocity[0] * self.dt
        self.imu_distance[1] = self.imu_velocity[1] * self.dt

    def euclidean_distance(self):

        self.imu_euclidean_distance = math.sqrt((self.imu_distance[0]**2  )+ self.imu_distance[1]**2)

    def update_position(self, lat):
        R = 6371000
        self.lat = lat
        
        # 방위각을 라디안으로 변환
        heading_rad = math.radians(self.heading_degrees)
        
        # 거리 변화량 계산
        delta_lat = self.imu_euclidean_distance * math.cos(heading_rad) / R
        delta_lon = self.imu_euclidean_distance * math.sin(heading_rad) / (R * math.cos(math.radians(self.lat)))
        
        # 새로운 좌표 계산
        self.plus_lat = math.degrees(delta_lat)
        self.plus_lon = math.degrees(delta_lon)
        
        return self.plus_lat, self.plus_lon
    
class Car_State:

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

class Car_State_save:
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

def proportional_control(target, current):
    """
    비례 제어를 사용하여 제어 입력(가속도)을 계산합니다.
    """
    a = Kp * (target - current)
    return a
    
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