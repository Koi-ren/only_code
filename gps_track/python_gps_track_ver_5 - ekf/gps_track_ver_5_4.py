import sys
import serial
import time
import numpy as np
import math
import pandas as pd

# 시리얼 포트 설정 (하나의 아두이노만 사용)
try:
    ser = serial.Serial('COM30', 115200)
    time.sleep(2)  # 시리얼 통신 초기화 대기
    if not ser.is_open:
        raise Exception("시리얼 포트를 열 수 없습니다.")
    print("시리얼 포트가 성공적으로 열렸습니다.")
except Exception as e:
    print(f"시리얼 포트 연결 실패: {e}")
    sys.exit()

speed = 50
steering_angle_set = 0
tolerance = 0.000020

previous_planning_point_number = 0
previous_lat_lon_data = (0, 0)

# 엑셀 파일에서 데이터 읽어오기
print("엑셀 파일에서 경로 데이터를 읽는 중...")
planing_data = pd.read_excel('C:/Users/plane/Desktop/park_ws/gps_track/gps_drive/path_planning_data.xlsx')
planning_point_data = np.array(planing_data['point_number'])
lat_data = np.array(planing_data['lat'])
lon_data = np.array(planing_data['lon'])
bearing_data = np.array(planing_data['bearing'])
print("경로 데이터 로드 완료.")

def send_motor_speed(speed):
    """ 구동 모터 속도 값을 아두이노로 전송 """
    data = f"{speed}\n"
    ser.write(data.encode())  # 시리얼로 전송
    print(f"Sent Motor Speed: {speed}")

def send_steering_angle(angle):
    """ 조향 각도 값을 아두이노로 전송 """
    data = f"{angle}\n"
    ser.write(data.encode())  # 시리얼로 전송
    print(f"Sent Steering Angle: {angle}")

def stop_motors():
    """ 모터를 정지시키기 위해 속도 0을 아두이노로 전송 """
    send_motor_speed(0)
    print("Motors stopped.")

def stop_steering():
    """ 조향을 중앙으로 맞추기 위해 각도 0을 아두이노로 전송 """
    send_steering_angle(0)
    print("Steering centered.")

def read_gps_data(ser):
    """시리얼 포트에서 GPS 데이터를 읽어들임"""
    lat1 = lon1 = alt1 = None
    print("GPS 데이터를 읽는 중...")
    try:
        while not (lat1 and lon1 and alt1):  # 유효한 데이터가 나올 때까지 반복
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                print(f"Read line from {ser.port}: {line}")
                if line.startswith("Lat:"):
                    try:
                        parts = line.split()
                        if len(parts) >= 6:
                            lat1 = float(parts[1]) / 10000000.0
                            lon1 = float(parts[3]) / 10000000.0
                            alt1 = float(parts[5])
                            # 데이터 유효성 체크
                            if not (-90 <= lat1 <= 90 and -180 <= lon1 <= 180 and alt1 >= 0):
                                lat1 = lon1 = alt1 = None
                                print("GPS 데이터 범위 오류. 유효하지 않은 값입니다.")
                        else:
                            print("GPS 데이터 파싱 실패.")
                    except ValueError:
                        print("GPS 데이터 파싱 오류.")
                        lat1 = lon1 = alt1 = None
    except Exception as e:
        print(f"GPS 데이터 읽기 오류: {e}")
        return None, None, None
    print(f"GPS 데이터 수신 성공: 위도={lat1}, 경도={lon1}, 고도={alt1}")
    return lat1, lon1, alt1

def calculate_angle(start_angle, target_angle):
    """ 시계/반시계 방향 각도 계산 """
    clockwise_diff = (target_angle - start_angle + 360) % 360
    counterclockwise_diff = (start_angle - target_angle + 360) % 360
    print(f"각도 계산: start_angle={start_angle}, target_angle={target_angle}, 시계방향={clockwise_diff}, 반시계방향={counterclockwise_diff}")
    return (clockwise_diff, '+') if clockwise_diff <= counterclockwise_diff else (-counterclockwise_diff, '-')

def calculate_bearing(lat1, lon1, lat2, lon2):
    """각도 계산 함수 (북쪽을 0도, 동쪽을 90도로 설정)"""
    lat1_rad, lon1_rad, lat2_rad, lon2_rad = map(math.radians, [lat1, lon1, lat2, lon2])
    dlon = lon2_rad - lon1_rad
    x = math.sin(dlon) * math.cos(lat2_rad)
    y = math.cos(lat1_rad) * math.sin(lat2_rad) - (math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(dlon))
    initial_bearing = math.degrees(math.atan2(x, y))
    compass_bearing = (initial_bearing + 360) % 360
    print(f"각도 계산: 위도1={lat1}, 경도1={lon1}, 위도2={lat2}, 경도2={lon2}, 각도={compass_bearing}")
    return compass_bearing

while True:
    try:
        lat1, lon1, alt1 = read_gps_data(ser)
        if lat1 is not None and lon1 is not None:
            print("가장 가까운 좌표를 찾는 중...")
            lat_closest_value = lat_data[np.abs(lat_data - lat1).argmin()]
            lon_closest_value = lon_data[np.abs(lon_data - lon1).argmin()]
            lat_index = np.where(lat_data == lat_closest_value)[0][0]
            lon_index = np.where(lon_data == lon_closest_value)[0][0]
           
            if lat_index == lon_index:
                planning_point_number = planning_point_data[lat_index]
                previous_planning_point_number = planning_point_number
                print(f"근사한 포인트 넘버: {planning_point_number}")
            else:
                planning_point_number = previous_planning_point_number
                print("경로에서 벗어났거나 GPS 오차범위에 들어가지 않았습니다.")

            # 각도 계산 및 조향각 설정
            bearing = calculate_bearing(lat1, lon1, lat_data[0], lon_data[0]) if planning_point_number == 0 else \
                      calculate_bearing(lat1, lon1, previous_lat_lon_data[0], previous_lat_lon_data[1])

            angle_to_move, direction_sign = calculate_angle(bearing, bearing_data[planning_point_number])
            real_steering_angle = max(min(angle_to_move, 43), -43)  # 각도를 -43~43도로 제한
            print(f"실제 조향각: {real_steering_angle}, 방향: {direction_sign}")
           
            send_motor_speed(speed)
            send_steering_angle(real_steering_angle)

            # 경로 종료 조건 체크
            if planning_point_number >= 426:
                stop_motors()
                print("프로그램을 종료합니다.")
                sys.exit()

            previous_lat_lon_data = (lat1, lon1)
            time.sleep(1)

    except KeyboardInterrupt:
        print("프로그램 종료 중...")
        stop_motors()
        stop_steering()
        break

    except Exception as e:
        print(f"오류 발생: {e}")
        continue