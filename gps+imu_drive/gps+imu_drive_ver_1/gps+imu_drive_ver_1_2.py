#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import serial
import serial.tools.list_ports
import numpy as np
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
    global key, buff, pub_flag, angularVelocity, acceleration, magnetometer, angle_degree
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

def heading_degree_found():
    global heading_degrees
    heading = math.atan2(magnetometer[1], magnetometer[0]) + (-8.0 + (-29.0 / 60.0)) / (180 / math.pi)
    heading = heading % (2 * math.pi)
    heading_degrees = heading * 180 / math.pi

def calculate_distance(accel):
    global imu_distance

    for i in range(len(accel['x'])):

        dt = 0.01
        velocity = {'x': 0, 'y': 0, 'z': 0}
        imu_distance = {'x': 0, 'y': 0, 'z': 0}
        # 속도 업데이트 (적분)
        velocity['x'] += accel['x'][i] * dt
        velocity['y'] += accel['y'][i] * dt
        velocity['z'] += (accel['z'][i] - 9.81) * dt  # 중력 보정

        # 거리 업데이트 (적분)
        imu_distance['x'] += velocity['x'] * dt
        imu_distance['y'] += velocity['y'] * dt
        imu_distance['z'] += velocity['z'] * dt

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
part_gps = threading.Thread(target = gps_part, daemon = True)
part_imu = threading.Thread(target = imu_part, daemon = True)
part_gps.start()
part_imu.start()

if __name__ == "__main__":
    time.sleep(6)
    while True:
        part_heading = threading.Thread(target = heading_degree_found, daemon = True)
        part_calculated_distance = threading.Thread(target = calculate_distance, daemon = True)

        part_heading.start()
        part_calculated_distance.start()
        
        if lat is not None and lon is not None:
            print(f"GPS 좌표: {lat}, {lon}")
        print(f"angle_degree: {angle_degree}")
        print(f"magnetometer: {magnetometer}")
        print(f"acceleration: {acceleration}")
        print(f"angularVelocity: {angularVelocity}")
        print(f"heading_degree: {heading_degrees}")
        print("Calculated Distance (in meters):")
        print(f"X: {imu_distance['x']:.4f} meters")
        print(f"Y: {imu_distance['y']:.4f} meters")
        print(f"Z: {imu_distance['z']:.4f} meters")
        print("\n")
