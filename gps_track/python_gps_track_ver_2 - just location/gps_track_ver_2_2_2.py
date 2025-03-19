import serial
import time
import openpyxl
import os
import math

def decimal_to_dms(decimal):
    degrees = int(decimal)
    minutes_full = abs(decimal - degrees) * 60
    minutes = int(minutes_full)
    seconds = (minutes_full - minutes) * 60
    return degrees, minutes, seconds

def create_excel_with_dms(sheet, latitude, longitude, distance, point_number):
    # DMS 변환
    lat_deg, lat_min, lat_sec = decimal_to_dms(latitude)
    lon_deg, lon_min, lon_sec = decimal_to_dms(longitude)

    lat_direction = "N" if lat_deg >= 0 else "S"
    lon_direction = "E" if lon_deg >= 0 else "W"
    
    lat_deg = abs(lat_deg)
    lon_deg = abs(lon_deg)

    # 도분초 값을 엑셀에 추가, 거리 추가
    sheet.append([
        f"{point_number}",
        f"{lat_deg}°{lat_min}'{lat_sec:.2f}\"", lat_direction,
        f"{lon_deg}°{lon_min}'{lon_sec:.2f}\"", lon_direction,
        f"{distance:.4f} km"
    ])

def dms_to_decimal(degrees, minutes, seconds, direction):
    decimal = degrees + minutes / 60 + seconds / 3600
    if direction in ['S', 'W']:
        decimal = -decimal
    return decimal

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # 지구의 반지름 (km)

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

# 시리얼 포트 설정
serial_port = 'COM6'  # 본인 시리얼 통신 포트 확인하고 설정
baud_rate = 9600  # 시리얼 통신 속도 설정

# 엑셀 파일 및 워크북 초기화
save_path = "C:/Users/plane/Desktop/park_ws/gps_track/way_point_coordinates_2_2_2.xlsx"
workbook = openpyxl.Workbook()
sheet = workbook.active
sheet.title = "Coordinates"

# 헤더 추가
sheet.append(["Point Number", "Latitude", "Direction", "Longitude", "Direction", "Distance (km)"])

# 시리얼 포트 열기
ser = serial.Serial(serial_port, baud_rate)

# 포인트 번호 초기화
point_number = 0
last_latitude = None
last_longitude = None

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

                if button_signal == 1:
                    point_number += 1

                    # 이전 좌표가 존재하면 거리를 계산
                    if last_latitude is not None and last_longitude is not None:
                        distance = haversine(last_latitude, last_longitude, latitude, longitude)
                    else:
                        distance = 0.0  # 첫 번째 지점은 거리 0으로 설정

                    # 엑셀에 데이터 추가
                    create_excel_with_dms(sheet, latitude, longitude, distance, point_number)

                    # 현재 좌표를 마지막 좌표로 업데이트
                    last_latitude = latitude
                    last_longitude = longitude

                    # 수신한 데이터 출력
                    print('------------------------------------------------------------------------------------------------')
                    print(f"Latitude: {latitude}, Longitude: {longitude}, Altitude: {altitude}, Point: {point_number}, Distance: {distance:.2f} km")
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
