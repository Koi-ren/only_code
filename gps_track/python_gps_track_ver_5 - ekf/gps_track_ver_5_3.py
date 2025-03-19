import sys
import serial
import time
import numpy as np
import math
import openpyxl
import time
import pandas as pd

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

def read_gps_data(ser):
    """시리얼 포트에서 GPS 데이터를 읽어들임"""
    lat1 = lon1 = alt1 = None  # None으로 초기화하여 0이 들어가는 것을 방지

    try:
        while not (lat1 and lon1 and alt1):  # 세 값 모두 유효할 때까지 반복
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                print(f"Read line from {ser.port}: {line}")  # 디버깅 메시지

                if line.startswith("Lat:"):
                    try:
                        parts = line.split()
                        if len(parts) >= 6:
                            # 위도, 경도, 고도를 파싱
                            lat1 = float(parts[1]) / 10000000.0
                            lon1 = float(parts[3]) / 10000000.0
                            alt1 = float(parts[5])

                            # 데이터 유효성 검사
                            if not (-90 <= lat1 <= 90 and -180 <= lon1 <= 180 and alt1 >= 0):
                                print("잘못된 데이터 범위. 다시 시도 중...")
                                lat1 = lon1 = alt1 = None  # 잘못된 데이터를 무효화
                        else:
                            print("데이터 파싱 실패. 다시 시도 중...")
                    except ValueError:
                        print("데이터 파싱 오류. 다시 시도 중...")
                        lat1 = lon1 = alt1 = None  # 파싱 실패 시 무효화

    except Exception as e:
        print(f"오류가 발생했습니다: {e}")
        return None, None, None

    return lat1, lon1, alt1

def calculate_angle(start_angle, target_angle):
    # 시계 방향 각도 차이 계산
    clockwise_diff = (target_angle - start_angle + 360) % 360
    # 반시계 방향 각도 차이 계산
    counterclockwise_diff = (start_angle - target_angle + 360) % 360
    
    # 시계 방향이 더 짧으면 +로 표시 (시계 방향) 
    if clockwise_diff <= counterclockwise_diff:
        return float(clockwise_diff), '+'
    # 반시계 방향이 더 짧으면 -로 표시 (반시계 방향)
    else:
        return -float(counterclockwise_diff), '-'

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

def is_within_tolerance(lat1, lon1, lat_target, lon_target, tolerance):
    """주어진 좌표가 목표 좌표의 오차 범위 내에 있는지 확인합니다."""
    distance = calculate_distance(lat1, lon1, lat_target, lon_target)
    return distance <= tolerance

while True:
    try:
        # 아두이노로부터 데이터 읽기
        lat1, lon1, alt1 = read_gps_data(ser)

        # GPS 데이터가 유효한지 확인
        if lat1 is not None and lon1 is not None:
            avg_lat, avg_lon, avg_alt = lat1, lon1, alt1

            lat_closest_value = min(lat_data, key=lambda x: abs(x- lat1))
            lon_closest_value = min(lon_data, key=lambda x: abs(x- lon1))

            lat_index = lat_data[lat_data == lat_closest_value].index[0]
            lon_index = lon_data[lon_data == lon_closest_value].index[0]
                
            if lat_index == lon_index:
                # 현재 GPS 좌표가 계획된 좌표의 오차 범위 내에 있는지 확인합니다.
                if is_within_tolerance(lat1, lon1, lat_closest_value, lon_closest_value, tolerance):
                    planning_point_number = planning_point_data[lat_index]
                    previous_planning_point_number = planning_point_number
                    planning_point_data_bool = True
                    print(f"가장 근사한 좌표는:\n포인트 넘버: {planning_point_number}, 위도: {lat_closest_value}, 경도: {lon_closest_value}")
                else:
                    planning_point_number = previous_planning_point_number
                    planning_point_data_bool = False
                    print(f"경로에서 벗어났거나 GPS 오차범위에 들어가지 않았습니다.")

            elif lat_index <= lon_index:
                if is_within_tolerance(lat1, lon1, lat_closest_value, lon_closest_value, tolerance):
                    planning_point_number = planning_point_data[lat_index]
                    previous_planning_point_number = planning_point_number
                    planning_point_data_bool = True
                    print(f"가장 근사한 좌표는:\n포인트 넘버: {planning_point_number}, 위도: {lat_closest_value}, 경도: {lon_data[lat_index]}")
                else:
                    planning_point_number = previous_planning_point_number
                    planning_point_data_bool = False
                    print(f"경로에서 벗어났거나 GPS 오차범위에 들어가지 않았습니다.")

            elif lon_index <= lat_index:
                if is_within_tolerance(lat1, lon1, lat_closest_value, lon_closest_value, tolerance):
                    planning_point_number = planning_point_data[lon_index]
                    previous_planning_point_number = planning_point_number
                    planning_point_data_bool = True
                    print(f"가장 근사한 좌표는:\n포인트 넘버: {planning_point_number}, 위도: {lat_data[lon_index]}, 경도: {lon_closest_value}")
                else:
                    planning_point_number = previous_planning_point_number
                    planning_point_data_bool = False
                    print(f"경로에서 벗어났거나 GPS 오차범위에 들어가지 않았습니다.")
            else:
                planning_point_number = previous_planning_point_number
                planning_point_data_bool = False
                print(f"경로에서 벗어났거나 GPS 오차범위에 들어가지 않았습니다.")

            first_lat_value = lat_data[0]
            first_lon_value = lon_data[0]

            if point_number == 0:  # 첫 번째 좌표에서는 거리와 각도 계산을 생략
                previous_lat_lon_data = (avg_lat, avg_lon)
                bearing = calculate_bearing(avg_lat, avg_lon, first_lat_value, first_lon_value)
                if abs(lon_closest_value) == lon_data[0] and abs(lat_closest_value) == lat_data[0]:
                    point_number = 1
            else:
                bearing = calculate_bearing(avg_lat, avg_lon, previous_lat_lon_data[0], previous_lat_lon_data[1])
                point_number += 1
            angle_to_move, direction_sign = calculate_angle(bearing, bearing_data[planning_point_number + 1])

            if planning_point_data_bool == False:
                print(f"현재 가장 가까운 스타팅 포인트로 이동합니다")
            else:
                print(f"다음 포인트: {planning_point_number + 1}")
            print(f"다음 포인트로 가는 방위 각도: {angle_to_move}")

            if abs(angle_to_move) >= 43:
                if angle_to_move < 0:
                    real_steering_angle = 43
                else:
                    real_steering_angle = -43
            else:
                real_steering_angle = angle_to_move

            send_motor_speed(speed)
            send_steering_angle(real_steering_angle)

            if point_number >= 426:
                stop_motors()
                print("프로그램을 종료합니다.")
                sys.exit()  # 프로그램 종료

            previous_lat_lon_data = (lat1, lon1)

            time.sleep(1)

    except KeyboardInterrupt:
        print("프로그램이 종료되었습니다.")
        break

    except Exception as e:
        print(f"오류 발생: {e}")
        continue