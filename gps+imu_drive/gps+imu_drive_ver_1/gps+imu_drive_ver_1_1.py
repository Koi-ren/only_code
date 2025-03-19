#빠진 함수: 각도 계산 함수

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

#변수 및 리스트--------------------gps---------------------------------------------gps------------------------------------

# 시리얼 포트 설정 (하나의 아두이노만 사용)
ser = serial.Serial('COM30', 115200)
time.sleep(2)  # 시리얼 통신 초기화 대기

speed = 50
steering_angle_set = 0

current_index = 0
tolerance = 0.000900

point_number = 0
corrected_point_number = 0

previous_planning_point_number = 0
previous_lat_lon_data = (0, 0)

# 엑셀 파일에서 데이터 읽어오기
planing_data = pd.read_excel('C:/Users/plane/Desktop/park_ws/gps_track/gps_drive/fix_planning_data.xlsx')
planning_point_data = planing_data['point_number']
lat_data = planing_data['lat']
lon_data = planing_data['lon']
bearing_data = planing_data['bearing']

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

#함수정의----------------------------motor-----------------------------motor------------------------------------

def send_motor_speed(speed):
    """ 구동 모터 속도 값을 아두이노로 전송 """
    data = f"{speed}\n"
    stop_motors()
    print(f"Sent Motor Speed: {speed}")

def send_steering_angle(angle):
    """ 조향 각도 값을 아두이노로 전송 """
    data = f"{angle}\n"
    print(f"Sent Steering Angle: {angle}")

def stop_motors():
    """ 모터를 정지시키기 위해 속도 0을 아두이노로 전송 """
    send_motor_speed(0)  # 모터를 완전히 멈추기 위해 0 전송
    print("Motors stopped.")

def stop_steering():
    """ 조향을 중앙으로 맞추기 위해 각도 0을 아두이노로 전송 """
    send_steering_angle(0)  # 조향을 0도로 맞추기 위해 0 전송
    print("Steering centered.")

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
    global  heading_degrees
    heading = math.atan2(magnetometer[1],magnetometer[0])
    declination_angle = (-8.0 + (-29.0 / 60.0)) / (180 / math.pi)
    heading += declination_angle
    if heading < 0:
        heading += 2 * math.pi
    if heading > 2 * math.pi:
        heading -= 2 * math.pi
    heading_degrees = heading * 180 / math.pi

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
    time.sleep(6)
    while True:
        heading_degree_found()

        # lat, lon이 제대로 초기화되었는지 확인
        if lat is not None and lon is not None:
            print(f"GPS 좌표: {lat}, {lon}")
        else:
            print("GPS 데이터를 가져오지 못했습니다.")
        print(f"angle_degree: {angle_degree}")
        print(f"maenetometer: {magnetometer}")
        print(f"acceleration: {acceleration}")
        print(f"angularVelocity: {angularVelocity}")
        #print(angle_degree, magnetometer, acceleration, angularVelocity)
        print(f"heading_degree: {heading_degrees}")
        print("\n")