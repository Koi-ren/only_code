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


#변수 및 리스트--------------------gps---------------------------------------------gps------------------------------------

# 시리얼 포트 설정 (하나의 아두이노만 사용)
ser = serial.Serial('COM3', 115200)
time.sleep(2)  # 시리얼 통신 초기화 대기

speed_set = 40.0
steering_angle_set = 0

# GPS 관련 변수
tolerance = 0.00300
lat, lon, spd = None, None, None

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

#계산 및 저장 설정 부 ----------------------------------------------------------------------------------------------------

#IMU센서 이중 적분
#순서대로~ 샘플링 시간 간격 (초), 속도, 거리, 이전 가속도
dt, imu_velocity, imu_distance, prev_accel = 0.00666, {0:0, 1:0, 2:0}, {0:0, 1:0, 2:0}, [0, 0, 0] # 150Hz 샘플링

# gps+imu 융합 좌표 저장
gps_imu_save_path = "C:/ws/gps+imu+lidar_drive/gps+imu+lidar_drive_ver_3/test_file.csv"
time_limit = 10000#주행 중단 시간(s)

with open(gps_imu_save_path, mode='w', newline='') as gps_file:
    gps_writer = csv.writer(gps_file)
    gps_writer.writerow(["Point Number", "Latitude", "Longitude"])

def save_to_csv(file_path, Point_number, Latitude, Longitude, speed):
    """좌표 데이터를 CSV에 저장하는 함수"""
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([Point_number, Latitude, Longitude, speed])
#-------------제한시간----------------------------------------제한시간-----------------------------------------
def timeout():
    """타임아웃 함수: time_limt/60분 후에 프로그램 종료"""
    time.sleep(time_limit)
    print(f"프로그램이 {time_limit/60}분을 초과하여 종료됩니다.")
    sys.exit()

#함수정의--------------------gps---------------------------------------------gps------------------------------------

def read_gps_data(ser):
    """시리얼 포트에서 GPS 데이터를 읽어들임"""
    lat = lon = spd = None  # None으로 초기화하여 0이 들어가는 것을 방지

    try:
        while not (lat and lon and spd):  # 두 값 모두 유효할 때까지 반복
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
                            spd = float(parts[5])
                            # 데이터 유효성 검사
                        else:
                            print("데이터 파싱 실패. 다시 시도 중...")
                    except ValueError:
                        print("데이터 파싱 오류. 다시 시도 중...")
                        lat = lon = spd = None  # 파싱 실패 시 무효화
    except Exception as e:
        print(f"오류가 발생했습니다: {e}")
        return None, None, None

    return lat, lon, spd

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

#----------계산 파트---------------------------------------------------계산 파트------------------------------------------------
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
    global imu_euclidean_distance, combined_speed
    """
    (0, 0)에서 (x, y)까지의 유클리드 거리 계산 함수
    :param x: x축으로 이동한 거리
    :param y: y축으로 이동한 거리
    :return: (0, 0)에서 (x, y)까지의 거리
    """
    imu_euclidean_distance = math.sqrt((imu_distance[0]**2  )+ imu_distance[1]**2)
    combined_speed = math.sqrt(imu_velocity[0]**2 + imu_velocity[1]**2)

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

def update_position(lat, distance, heading):
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

    
#쓰레드_실행함수_정의--------------------gps---------------------------------------------gps------------------------------------

def gps_part():
    global lat, lon
    while True:
        lat_yet, lon_yet, spd_yet = read_gps_data(ser)
        if lat_yet is not None and lon_yet is not None and spd_yet is not None:
            lat, lon, spd = lat_yet, lon_yet, spd_yet
            time.sleep(1)

def imu_part():
    find_ttyUSB()

    port = "COM6"
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

#------------------------실행함수-------------------------------실행함수------------------------------

if __name__ == "__main__":

    i = 0
    prev_lat, prev_lon, prev_spd = None, None, None

    part_gps = threading.Thread(target=gps_part, daemon=True)
    part_imu = threading.Thread(target=imu_part, daemon=True)
    timer_thread = threading.Thread(target=timeout, daemon=True)
    
    part_gps.start()
    part_imu.start()
    timer_thread.start()

    while lat is None or lon is None or spd is None:
        print("Waiting for GPS data...")
        time.sleep(1)  # GPS 데이터 수신 대기

    heading_degree_found()

    while heading_degree is None:
        print("Waiting for heading degree data...")
        time.sleep(1)  # heading_degree 데이터 수신 대기

    print("location_found_start")

    time.sleep(1)

    while True:
        time.time()
        try:
                update_velocity_and_distance_trapezoid()
                heading_degree_found()

                if prev_lat != lat or prev_lon != lon:
                    #imu 데이터 드리프트를 막기위한 속도 및 거리초기화
                    imu_distance[0], imu_distance[1] = 0, 0
                    imu_velocity[0], imu_velocity[1] = 0, 0
                    #새로운 좌표값에 대응, 이전 위도, 이전 경도, imu로 더할 좌표값 업데이트
                    prev_lat, imu_lat, prev_lon, imu_lon, imu_spd, prev_spd= lat, lat, lon, lon, spd, spd

                print(f"heading_degree: {heading_degree}")

                if prev_lat == lat or prev_lon == lon or prev_spd == spd:
                    plus_imu_lat, plus_imu_lon = update_position(lat, imu_euclidean_distance, heading_degree)
                    imu_lat += plus_imu_lat
                    imu_lon += plus_imu_lon
                    imu_spd += combined_speed
                
                print(f"lat: {imu_lat} \nlon: {imu_lon} \nspeed: {imu_spd}")

                save_to_csv(gps_imu_save_path, i, imu_lat, imu_lon, imu_spd)

        except KeyboardInterrupt:
            print("프로그램이 종료되었습니다.")

        except Exception as e:
            print(f"오류 발생: {e}")
            continue