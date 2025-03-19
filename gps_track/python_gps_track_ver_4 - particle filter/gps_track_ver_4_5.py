#Arduion_gps_track_ver_4_2에서 좌표값을 제대로 파싱 못받음

import serial
import numpy as np
import random
import math
import openpyxl
import time

# 시리얼 포트 설정
ser1 = serial.Serial('COM6', 115200)  # 첫 번째 아두이노 (포트 변경 필요)
ser2 = serial.Serial('COM29', 115200)  # 두 번째 아두이노 (포트 변경 필요)

# 입자 수 설정 및 초기화
NUM_PARTICLES = 1000
particles = np.zeros((NUM_PARTICLES, 2))  # (x, y) 위치 입자 생성
weights = np.ones(NUM_PARTICLES) / NUM_PARTICLES  # 초기 가중치 동일하게 설정

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

def read_gps_data(ser):
    """시리얼 포트에서 두 개의 GPS 데이터를 읽어들임"""
    lat1 = lon1 = alt1 = 0.0
    lat2 = lon2 = alt2 = 0.0

    try:
        # Read lines from serial
        line = ser.readline().decode('utf-8').strip()

        if "GNSS_1:" in line:
            # Read GNSS_1 data
            lat_line = ser.readline().decode('utf-8').strip()
            lon_line = ser.readline().decode('utf-8').strip()
            alt_line = ser.readline().decode('utf-8').strip()

            lat1 = float(lat_line.split("Lat: ")[1].split(" Long: ")[0])
            lon1 = float(lon_line.split("Long: ")[1].split(" Alt: ")[0])
            alt1 = float(alt_line.split("Alt: ")[1])

        line = ser.readline().decode('utf-8').strip()
        if "GNSS_2:" in line:
            # Read GNSS_2 data
            lat_line = ser.readline().decode('utf-8').strip()
            lon_line = ser.readline().decode('utf-8').strip()
            alt_line = ser.readline().decode('utf-8').strip()

            lat2 = float(lat_line.split("Lat: ")[1].split(" Long: ")[0])
            lon2 = float(lon_line.split("Long: ")[1].split(" Alt: ")[0])
            alt2 = float(alt_line.split("Alt: ")[1])

    except Exception as e:
        print(f"오류가 발생했습니다: {e}")

    return lat1, lon1, alt1, lat2, lon2, alt2


def initialize_particles_with_random_gps(measurements):
    """입자의 초기 위치를 랜덤하게 GPS 측정값으로 설정"""
    global particles
    for i in range(NUM_PARTICLES):
        lat, lon = random.choice(measurements)
        particles[i, 0] = lat
        particles[i, 1] = lon

def particle_filter(particles, weights, measurements):
    """입자 필터 업데이트"""
    for i in range(NUM_PARTICLES):
        # 예측 단계: 최근 위치에서 작은 범위 내로 이동
        particles[i, 0] += random.gauss(0, 0.000001)  # 이동 범위 조정
        particles[i, 1] += random.gauss(0, 0.000001)

    # 입자의 가중치 업데이트
    for i in range(NUM_PARTICLES):
        # 측정값과의 유클리드 거리 계산
        distances = [np.sqrt((particles[i, 0] - m[0])**2 + (particles[i, 1] - m[1])**2) for m in measurements]
        weights[i] = np.exp(-np.min(distances) / 0.01)  # 가중치 계산 (범위 조정)

    # 가중치가 모두 0이 될 경우를 방지
    if np.sum(weights) == 0:
        weights[:] = 1.0 / NUM_PARTICLES
    else:
        weights /= np.sum(weights)  # 가중치 정규화
    
    return particles, weights

def resample_particles(particles, weights):
    """가중치에 따라 입자 리샘플링"""
    cumulative_sum = np.cumsum(weights)
    cumulative_sum[-1] = 1.0  # 작은 오차 방지
    indexes = np.searchsorted(cumulative_sum, np.random.rand(NUM_PARTICLES))

    # 입자 리샘플링
    particles[:] = particles[indexes]
    weights.fill(1.0 / NUM_PARTICLES)
    return particles, weights

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

while True:
    try:
        # 두 개의 아두이노로부터 데이터 읽기
        lat1_1, lon1_1, alt1_1, lat1_2, lon1_2, alt1_2 = read_gps_data(ser1)
        lat2_1, lon2_1, alt2_1, lat2_2, lon2_2, alt2_2 = read_gps_data(ser2)
        
        # 네 개의 좌표 데이터를 리스트로 저장
        measurements = [
            (lat1_1, lon1_1), 
            (lat1_2, lon2_2),
            (lat2_1, lon2_1),
            (lat2_2, lon2_2)
        ]

        # 입자 초기화: GPS 데이터 중 랜덤하게 선택
        initialize_particles_with_random_gps(measurements)

        # 원본 데이터 저장
        point_number += 1
        for m in measurements:
            distance = calculate_distance(m[0], m[1], previous_lat_lon[0], previous_lat_lon[1])  # 기준점으로부터 거리 계산
            bearing = calculate_bearing(m[0], m[1], previous_lat_lon[0], previous_lat_lon[1])  # 기준점으로부터 각도 계산
            save_to_excel(raw_sheet, m[0], m[1], 0, distance, bearing, point_number)
        raw_workbook.save(raw_save_path)

        print(f"원본 데이터 저장 횟수: {point_number}")

        # 입자 필터 단계
        particles, weights = particle_filter(particles, weights, measurements)
        particles, weights = resample_particles(particles, weights)

        # 위치 추정: 가중치 평균 위치 계산
        estimated_pos = np.average(particles, axis=0, weights=weights)
        print(f"추정된 위치: Lat: {estimated_pos[0]}, Lon: {estimated_pos[1]}")

        # 보정된 좌표 데이터 저장
        corrected_point_number += 1
        save_to_excel(corrected_sheet, estimated_pos[0], estimated_pos[1], 0, 0, 0, corrected_point_number)
        corrected_workbook.save(corrected_save_path)

        print(f"보정된 데이터 저장 횟수: {corrected_point_number}")

        # 현재 위치를 기준점으로 업데이트
        previous_lat_lon = estimated_pos

        time.sleep(1)  # 1초 간격으로 데이터 수집

    except KeyboardInterrupt:
        print("프로그램이 종료되었습니다.")
        break
    except Exception as e:
        print(f"오류 발생: {e}")
        continue
