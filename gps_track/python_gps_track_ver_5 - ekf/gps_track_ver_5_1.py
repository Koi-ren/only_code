import serial
import numpy as np
import math
import openpyxl
import time
from filterpy.kalman import ExtendedKalmanFilter
from filterpy.common import Q_discrete_white_noise

# 시리얼 포트 설정 (하나의 아두이노만 사용)
ser = serial.Serial('COM30', 115200)

# 엑셀 파일 설정
raw_save_path = "C:/Users/plane/Desktop/park_ws/gps_track/raw_coordinates.xlsx"
corrected_save_path = "C:/Users/plane/Desktop/park_ws/gps_track/corrected_coordinates.xlsx"

raw_workbook = openpyxl.Workbook()
raw_sheet = raw_workbook.active
raw_sheet.title = "Raw Coordinates"
raw_sheet.append(["Point Number", "Latitude", "Longitude", "Altitude", "Distance (km)", "Bearing (degrees)"])

corrected_workbook = openpyxl.Workbook()
corrected_sheet = corrected_workbook.active
corrected_sheet.title = "Corrected Coordinates"
corrected_sheet.append(["Point Number", "Latitude", "Longitude", "Altitude", "Distance (km)", "Bearing (degrees)"])

point_number = 0
corrected_point_number = 0

def Hx(x):
    """상태 벡터에서 관측 변수를 계산"""
    return np.array([x[0], x[1]])

def HJacobian_at_state(x):
    """상태 벡터에서 자코비안 행렬 계산"""
    return np.array([[1, 0, 0, 0], [0, 1, 0, 0]])

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

def ekf_predict(ekf, avg_lat, avg_lon):
    """EKF 예측 및 업데이트"""
    ekf.predict()
    z = np.array([avg_lat, avg_lon])
    ekf.update(z, HJacobian_at_state, Hx)

def ekf_initialize():
    """EKF 초기화 함수"""
    ekf = ExtendedKalmanFilter(dim_x=4, dim_z=2)
    ekf.x = np.array([0., 0., 0., 0.])  # 초기 상태: [위도, 경도, 위도 속도, 경도 속도]
    ekf.P *= 1000.  # 초기 공분산
    ekf.F = np.eye(4)  # 상태 전이 행렬
    ekf.H = np.array([[1, 0, 0, 0], [0, 1, 0, 0]])  # 측정 행렬
    ekf.R = np.eye(2) * 0.1  # 측정 잡음
    ekf.Q = Q_discrete_white_noise(dim=4, dt=1, var=0.1)  # 프로세스 잡음
    return ekf

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

def save_to_excel(sheet, latitude, longitude, altitude, distance, bearing, point_number):
    """좌표 데이터를 엑셀에 저장하는 함수"""
    sheet.append([f"{point_number}", f"{latitude}", f"{longitude}", f"{altitude}", f"{distance}", f"{bearing}"])

previous_lat_lon = (0, 0)
ekf = ekf_initialize()
time.sleep(5)

while True:
    try:
        # 아두이노로부터 데이터 읽기
        lat1, lon1, alt1 = read_gps_data(ser)

        # GPS 데이터가 유효한지 확인
        if lat1 is not None and lon1 is not None:
            avg_lat, avg_lon, avg_alt = lat1, lon1, alt1

            # EKF 예측 및 업데이트
            ekf_predict(ekf, avg_lat, avg_lon)
            estimated_pos = ekf.x[:2]  # 위도와 경도만 추출

            point_number += 1
            if point_number == 1:  # 첫 번째 좌표에서는 거리와 각도 계산을 생략
                previous_lat_lon = (avg_lat, avg_lon)
            else:
                distance = calculate_distance(avg_lat, avg_lon, previous_lat_lon[0], previous_lat_lon[1])
                bearing = calculate_bearing(avg_lat, avg_lon, previous_lat_lon[0], previous_lat_lon[1])
                save_to_excel(raw_sheet, avg_lat, avg_lon, avg_alt, distance, bearing, point_number)

            # 보정된 좌표 데이터 저장
            corrected_point_number += 1
            save_to_excel(corrected_sheet, estimated_pos[0], estimated_pos[1], 0, 0, 0, corrected_point_number)

            if point_number % 10 == 0:
                try:
                    corrected_workbook.save(corrected_save_path)
                    print(f"보정된 데이터 저장 횟수: {corrected_point_number}")
                    raw_workbook.save(raw_save_path)
                    print(f"원본 데이터 저장 횟수: {point_number}")
                except PermissionError:
                    print("파일 저장 권한 오류 발생. 엑셀 파일이 열려있지 않은지 확인하세요.")
                except Exception as e:
                    print(f"파일 저장 중 오류 발생: {e}")

            previous_lat_lon = estimated_pos  # 현재 위치를 기준점으로 업데이트

        time.sleep(1)  # 1초 간격으로 데이터 수집

    except KeyboardInterrupt:
        print("프로그램이 종료되었습니다.")
        break
    except Exception as e:
        print(f"오류 발생: {e}")
        continue
