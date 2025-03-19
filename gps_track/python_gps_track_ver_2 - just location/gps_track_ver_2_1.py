#미완
import serial
import time
import openpyxl
import os

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
        f"{point_number}\"",
        f"{lat_deg}°{lat_min}'{lat_sec:.2f}\"", lat_direction,
        f"{lon_deg}°{lon_min}'{lon_sec:.2f}\"", lon_direction
    ])

# 시리얼 포트 설정
serial_port = 'COM6'  # 본인 시리얼 통신 포트 확인하고 설정
baud_rate = 9600  # 시리얼 통신 속도 설정

# 엑셀 파일 및 워크북 초기화
save_path = "C:/Users/plane/Desktop/park_ws/gps_track/way_point_coordinates.xlsx"
workbook = openpyxl.Workbook()
sheet = workbook.active
sheet.title = "Coordinates"

# 헤더 추가
sheet.append(["Point Number", "Latitude", "Direction", "Longitude", "Direction",])

# 시리얼 포트 열기
ser = serial.Serial(serial_port, baud_rate)

# 포인트 번호 초기화
point_number = 0

try:
    while True:
        # GPS 데이터 수신
        line = ser.readline().decode('utf-8').strip()

        # GPS 데이터 파싱
        if line.startswith("Lat:"):
            try:
                # 경도와 위도 추출
                latitude = float(line.split()[1]) / 10000000.0  # 데이터 형식을 좌표식으로 맞춤
                longitude = float(line.split()[3]) / 10000000.0
                altitude = float(line.split()[5])
                button_signal = int(line.split()[7])

                if button_signal == 1:
                    point_number += 1
                    create_excel_with_dms(sheet, latitude, longitude, point_number)

                    # 수신한 데이터 출력
                    print(f"Latitude: {latitude}, Longitude: {longitude}, Altitude: {altitude}, Point: {point_number}")

                    # 엑셀 파일 저장 (중간에 저장하여 데이터 손실 방지)
                    workbook.save(save_path)

            except ValueError:
                print("Invalid data format:", line)

        # 1초 대기
        time.sleep(1)

except KeyboardInterrupt:
    print("Program terminated by user")

finally:
    ser.close()
    workbook.save(save_path)
    print(f"엑셀 파일이 '{save_path}'에 저장되었습니다.")
