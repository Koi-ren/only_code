import serial
import time
import openpyxl
import numpy as np
import math
import matplotlib.pyplot as plt

# EKF 파라미터
Q = np.diag([
    0.1,  # x축 위치의 분산
    0.1,  # y축 위치의 분산
    np.deg2rad(1.0),  # yaw 각도의 분산
    1.0  # 속도의 분산
]) ** 2  # 예측 상태 공분산
R = np.diag([0.5, 0.5]) ** 2  # 관측 x, y 위치의 공분산

DT = 0.1  # 시간 간격 [s]

# EKF 초기화
xEst = np.zeros((4, 1))  # 초기 상태 추정
PEst = np.eye(4)  # 초기 공분산 추정

def motion_model(x, u):
    F = np.array([[1.0, 0, 0, 0],
                  [0, 1.0, 0, 0],
                  [0, 0, 1.0, 0],
                  [0, 0, 0, 0]])

    B = np.array([[DT * math.cos(x[2, 0]), 0],
                  [DT * math.sin(x[2, 0]), 0],
                  [0.0, DT],
                  [1.0, 0.0]])

    x = F @ x + B @ u

    return x

def observation_model(x):
    H = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0]
    ])

    z = H @ x

    return z

def jacob_f(x, u):
    yaw = x[2, 0]
    v = u[0, 0]
    jF = np.array([
        [1.0, 0.0, -DT * v * math.sin(yaw), DT * math.cos(yaw)],
        [0.0, 1.0, DT * v * math.cos(yaw), DT * math.sin(yaw)],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0]])

    return jF

def jacob_h():
    jH = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0]
    ])

    return jH

def ekf_estimation(xEst, PEst, z, u):
    xPred = motion_model(xEst, u)
    jF = jacob_f(xEst, u)
    PPred = jF @ PEst @ jF.T + Q

    jH = jacob_h()
    zPred = observation_model(xPred)
    y = z - zPred
    S = jH @ PPred @ jH.T + R
    K = PPred @ jH.T @ np.linalg.inv(S)
    xEst = xPred + K @ y
    PEst = (np.eye(len(xEst)) - K @ jH) @ PPred
    return xEst, PEst

def decimal_to_dms(decimal):
    degrees = int(decimal)
    minutes_full = abs(decimal - degrees) * 60
    minutes = int(minutes_full)
    seconds = (minutes_full - minutes) * 60
    return degrees, minutes, seconds

def create_excel_with_dms(sheet, latitude, longitude, point_number):
    lat_deg, lat_min, lat_sec = decimal_to_dms(latitude)
    lon_deg, lon_min, lon_sec = decimal_to_dms(longitude)

    lat_direction = "N" if lat_deg >= 0 else "S"
    lon_direction = "E" if lon_deg >= 0 else "W"
    
    lat_deg = abs(lat_deg)
    lon_deg = abs(lon_deg)

    sheet.append([
        f"{point_number}",
        f"{lat_deg}°{lat_min}'{lat_sec:.2f}\"", lat_direction,
        f"{lon_deg}°{lon_min}'{lon_sec:.2f}\"", lon_direction
    ])

# 시리얼 포트 초기화
serial_port = 'COM6'
baud_rate = 9600

# 엑셀 초기화
save_path = "C:/Users/plane/Desktop/park_ws/gps_track/way_point_coordinates.xlsx"
workbook = openpyxl.Workbook()
sheet = workbook.active
sheet.title = "Coordinates"
sheet.append(["Point Number", "Latitude", "Direction", "Longitude", "Direction"])

# 시리얼 포트 열기
ser = serial.Serial(serial_port, baud_rate)

# 포인트 번호
point_number = 0

# 데이터 이력 초기화
hxEst = xEst
hxTrue = np.zeros((4, 1))  # 실제 상태 이력
hxDR = np.zeros((4, 1))  # 사망 추적 이력
hz = np.zeros((2, 1))  # GPS 측정값 이력

try:
    while True:
        line = ser.readline().decode('utf-8').strip()

        if line.startswith("Lat:"):
            try:
                parts = line.split()
                latitude = float(parts[1]) / 10000000.0
                longitude = float(parts[3]) / 10000000.0
                altitude = float(parts[5])
                button_signal = int(parts[-1])

                if button_signal == 1:
                    point_number += 1
                    create_excel_with_dms(sheet, latitude, longitude, point_number)
                    workbook.save(save_path)

                    # 위도와 경도를 상태 공간으로 변환
                    z = np.array([[latitude], [longitude]])
                    u = np.array([[1.0], [0.0]])  # 가정된 일정한 속도와 yaw 각속도

                    xEst, PEst = ekf_estimation(xEst, PEst, z, u)

                    # 이력 업데이트
                    hxEst = np.hstack((hxEst, xEst))
                    hxDR = np.hstack((hxDR, xEst))  # 사망 추적 업데이트 가능
                    hxTrue = np.hstack((hxTrue, xEst))  # 실제 상태 업데이트 가능
                    hz = np.hstack((hz, z))

                    # 플로팅
                    plt.cla()
                    plt.plot(hz[0, :], hz[1, :], ".g", label="GPS Measurements")
                    plt.plot(hxTrue[0, :].flatten(), hxTrue[1, :].flatten(), "-b", label="True Path")
                    plt.plot(hxDR[0, :].flatten(), hxDR[1, :].flatten(), "-k", label="Dead Reckoning")
                    plt.plot(hxEst[0, :].flatten(), hxEst[1, :].flatten(), "-r", label="EKF Estimation")
                    plt.legend()
                    plt.axis("equal")
                    plt.grid(True)
                    plt.pause(0.001)

            except ValueError:
                print("GPS 데이터 파싱 오류")

        time.sleep(1)

except KeyboardInterrupt:
    print("사용자에 의해 프로그램 종료")

finally:
    ser.close()
    workbook.save(save_path)
    print(f"엑셀 파일이 '{save_path}'에 저장되었습니다.")
