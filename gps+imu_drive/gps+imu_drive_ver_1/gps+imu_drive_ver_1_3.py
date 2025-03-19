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

# 시리얼 포트 설정 및 초기화
ser = serial.Serial('COM30', 115200)
time.sleep(2)

# 모터 및 조향 초기 값
speed = 50
steering_angle_set = 0

# GPS 관련 변수
current_index = 0
tolerance = 0.000900
previous_lat_lon_data = (0, 0)

# 플래닝 데이터 읽기
planing_data = pd.read_excel('C:/Users/plane/Desktop/park_ws/gps_track/gps_drive/fix_planning_data.xlsx')
lat_data, lon_data, bearing_data = planing_data['lat'], planing_data['lon'], planing_data['bearing']

# IMU 센서 초기화
key, flag, buff = 0, 0, {}
angularVelocity, acceleration, magnetometer, angle_degree = [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]
pub_flag = [True, True]
python_version = platform.python_version()[0]

#IMU센서 이중 적분
#순서대로~ 샘플링 시간 간격 (초), 속도, 거리, 이전 가속도
dt, imu_velocity, imu_distance, prev_accel = 0.00666, {0:0, 1:0, 2:0}, {0:0, 1:0, 2:0}, [0, 0, 0] # 100Hz 샘플링

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
    global buff, key, angle_degree, magnetometer, acceleration, angularVelocity, pub_flag
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


    prev_accel = acceleration.copy()
    time.sleep(0.1)

def heading_degree_found():
    global heading_degrees
    heading = math.atan2(magnetometer[1], magnetometer[0]) + (-8.0 + (-29.0 / 60.0)) / (180 / math.pi)
    heading = heading % (2 * math.pi)
    heading_degrees = heading * 180 / math.pi

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
    imu_velocity[0] += (((acceleration[0]*-9.8) + 0.07) + ((prev_accel[0]*-9.8) + 0.07) / 2) * dt
    imu_velocity[1] += (((acceleration[1]*-9.8) + 0.37) + ((prev_accel[1]*-9.8) / 2) + 0.37) * dt
    imu_velocity[2] += ((acceleration[2]*-9.8 + prev_accel[2]*-9.8 - 9.81 * 2) / 2) * dt  # 중력 보정 포함

    # 거리 업데이트 (적분)
    imu_distance[0] += imu_velocity[0] * dt
    imu_distance[1] += imu_velocity[1] * dt
    imu_distance[2] += imu_velocity[2] * dt

# GPS 및 IMU 쓰레드 실행
def gps_part():
    global lat, lon
    lat_yet, lon_yet = read_gps_data(ser)
    if lat_yet is not None and lon_yet is not None:
        lat, lon = lat_yet, lon_yet

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

    prev_lat, prev_lon = None, None
    time.sleep(6)  # 초기화 대기 시간
    while True:
        
        part_heading = threading.Thread(target=heading_degree_found, daemon=True)
        part_calculated_distance = threading.Thread(target= update_velocity_and_distance_trapezoid, daemon=True)

        part_heading.start()
        part_calculated_distance.start()
        
        part_heading.join()  # 스레드 완료 대기
        part_calculated_distance.join()  # 스레드 완료 대기

        if lat is not None and lon is not None:
            print(f"GPS 좌표: {lat}, {lon}")
        else:
            print(f"GPS 신호 수신 못함")

        if prev_lat != lat or prev_lon != lon:
            imu_distance[0], imu_distance[1], imu_distance[2] = 0, 0, 0
            imu_velocity[0], imu_velocity[1], imu_distance[2] = 0, 0, 0

        print(f"angle_degree: {angle_degree}")
        print(f"magnetometer: {magnetometer}")
        print(f"acceleration: {acceleration}")
        print(f"angularVelocity: {angularVelocity}")
        print(f"heading_degree: {heading_degrees}")
        print("Calculated Distance (in meters):")
        print(f"X: {imu_distance[0]:.4f} meters")
        print(f"Y: {imu_distance[1]:.4f} meters")
        print(f"Z: {imu_distance[2]:.4f} meters")
        print("\n")
        
        #print(prev_accel)
        prev_lat, prev_lon = lat, lon
if __name__ == "__main__":
    # GPS 및 IMU 스레드 시작
    part_gps = threading.Thread(target=gps_part, daemon=True)
    part_imu = threading.Thread(target=imu_part, daemon=True)

    part_gps.start()
    part_imu.start()

    # 메인 루프 실행
    main_loop()