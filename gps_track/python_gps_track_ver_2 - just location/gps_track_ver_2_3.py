#너무나도 큰 오차에 필터값 수정 필요

import serial
import time
import openpyxl
import numpy as np
from filterpy.kalman import KalmanFilter

def decimal_to_dms(decimal):
    degrees = int(decimal)
    minutes_full = abs(decimal - degrees) * 60
    minutes = int(minutes_full)
    seconds = (minutes_full - minutes) * 60
    return degrees, minutes, seconds

def create_excel_with_dms(sheet, latitude, longitude, point_number):
    # DMS 변환
    lat_deg, lat_min, lat_sec = decimal_to_dms(latitude)
    lon_deg, lon_min, lon_sec = decimal_to_dms(longitude)

    lat_direction = "N" if lat_deg >= 0 else "S"
    lon_direction = "E" if lon_deg >= 0 else "W"
    
    lat_deg = abs(lat_deg)
    lon_deg = abs(lon_deg)

    # 도분초 값을 엑셀에 추가
    sheet.append([
        f"{point_number}",
        f"{lat_deg}°{lat_min}'{lat_sec:.2f}\"", lat_direction,
        f"{lon_deg}°{lon_min}'{lon_sec:.2f}\"", lon_direction
    ])

def initialize_kalman_filter():
    kf = KalmanFilter(dim_x=4, dim_z=2)
    dt = 1.0  # Time step

    # State transition matrix
    kf.F = np.array([[1, 0, dt, 0],
                     [0, 1, 0, dt],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]])

    # Measurement function
    kf.H = np.array([[1, 0, 0, 0],
                     [0, 1, 0, 0]])

    # Measurement uncertainty
    kf.R *= 10  # You may need to adjust this value

    # Covariance matrix
    kf.P *= 1000  # Initial covariance estimate

    # Process noise
    kf.Q = np.array([[1, 0, 0, 0],
                     [0, 1, 0, 0],
                     [0, 0, 0.1, 0],
                     [0, 0, 0, 0.1]])

    return kf

# 시리얼 포트 설정
serial_port = 'COM6'  # 본인 시리얼 통신 포트 확인하고 설정
baud_rate = 9600  # 시리얼 통신 속도 설정

# 엑셀 파일 및 워크북 초기화
save_path = "C:/Users/plane/Desktop/park_ws/gps_track/way_point_coordinates.xlsx"
workbook = openpyxl.Workbook()
sheet = workbook.active
sheet.title = "Coordinates"

# 헤더 추가
sheet.append(["Point Number", "Latitude", "Direction", "Longitude", "Direction"])

# 시리얼 포트 열기
ser = serial.Serial(serial_port, baud_rate)

# 포인트 번호 초기화
point_number = 0

# Kalman Filter 초기화
kf = initialize_kalman_filter()

try:
    while True:
        # GPS 데이터 수신
        line = ser.readline().decode('utf-8').strip()

        # GPS 데이터 파싱
        if line.startswith("Lat:"):
            try:
                # 경도와 위도 추출
                parts = line.split()
                latitude = float(parts[1]) / 10000000.0  # 데이터 형식을 좌표식으로 맞춤
                longitude = float(parts[3]) / 10000000.0
                altitude = float(parts[5])
                button_signal = int(parts[-1])  # 버튼 신호가 마지막 부분에 위치하므로 마지막 값 사용

                # Kalman Filter 적용
                z = np.array([latitude, longitude])
                kf.predict()
                kf.update(z)
                filtered_lat, filtered_lon = kf.x[0], kf.x[1]

                if button_signal == 1:
                    point_number += 1
                    create_excel_with_dms(sheet, float(filtered_lat), float(filtered_lon), point_number)

                    # 수신한 데이터 출력
                    print('------------------------------------------------------------------------------------------------')
                    print(f"Latitude: {filtered_lat}, Longitude: {filtered_lon}, Altitude: {altitude}, Point: {point_number}")
                    print('------------------------------------------------------------------------------------------------')

                    # 엑셀 파일 저장 (중간에 저장하여 데이터 손실 방지)
                    workbook.save(save_path)

            except ValueError:
                print("현재 위치를 저장하고 있지 않습니다")

        # 1초 대기
        time.sleep(1)

except KeyboardInterrupt:
    print("Program terminated by user")

finally:
    ser.close()
    workbook.save(save_path)
    print(f"엑셀 파일이 '{save_path}'에 저장되었습니다.")
