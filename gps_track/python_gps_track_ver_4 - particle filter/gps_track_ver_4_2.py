import serial
import time
import openpyxl
import random
import numpy as np
import math

# 기본적인 입자 필터 설정
NUM_PARTICLES = 1000  # 입자 수
particles = []  # 입자 리스트
weights = []  # 가중치 리스트
initial_latitude = None  # 초기 위치를 None으로 설정
initial_longitude = None

# 입자 초기화 함수
def initialize_particles(lat, lon, num_particles):
    particles = []
    for _ in range(num_particles):
        particle = [lat + random.uniform(-0.0001, 0.0001), lon + random.uniform(-0.0001, 0.0001)]
        particles.append(particle)
    return particles

# 가중치 업데이트 함수
def update_weights(particles, lat, lon):
    global weights
    weights = []
    for particle in particles:
        distance = np.sqrt((lat - particle[0]) ** 2 + (lon - particle[1]) ** 2)
        weight = np.exp(-distance ** 2 / 0.0001)  # Gaussian 분포를 사용한 가중치 계산
        weights.append(weight)
    
    weights = np.array(weights)
    weights /= weights.sum()

# 입자 위치 업데이트 함수
def resample_particles(particles, weights):
    indices = np.random.choice(range(len(particles)), size=len(particles), p=weights)
    new_particles = [particles[i] for i in indices]
    return new_particles

# 현재 위치 추정 함수
def estimate_position(particles, weights):
    lat_est = np.average([p[0] for p in particles], weights=weights)
    lon_est = np.average([p[1] for p in particles], weights=weights)
    return lat_est, lon_est

# 거리 계산 함수 (Haversine 공식)
def calculate_distance(lat1, lon1, lat2, lon2):
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

# 각도 계산 함수 (북쪽을 0도, 동쪽을 90도로 설정)
def calculate_bearing(lat1, lon1, lat2, lon2):
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

# 좌표 데이터를 엑셀에 저장하는 함수
def save_to_excel(sheet, latitude, longitude, altitude, distance, bearing, point_number):
    sheet.append([f"{point_number}", f"{latitude}", f"{longitude}", f"{altitude}", f"{distance}", f"{bearing}"])

# 시리얼 포트 설정
serial_port = 'COM6'
baud_rate = 9600

# 엑셀 파일 및 워크북 초기화
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

ser = serial.Serial(serial_port, baud_rate)
point_number = 0
corrected_point_number = 0
particles_initialized = False  # 입자 초기화 여부 확인

prev_latitude = None
prev_longitude = None

try:
    while True:
        line = ser.readline().decode('utf-8').strip()
        
        if line.startswith("Lat:"):
            try:
                parts = line.split()
                latitude = float(parts[1]) / 10000000.0
                longitude = float(parts[3]) / 10000000.0
                altitude = float(parts[5])
                
                # 거리와 각도 계산
                distance = calculate_distance(prev_latitude, prev_longitude, latitude, longitude) if prev_latitude is not None and prev_longitude is not None else 0
                bearing = calculate_bearing(prev_latitude, prev_longitude, latitude, longitude) if prev_latitude is not None and prev_longitude is not None else 0
                
                prev_latitude = latitude
                prev_longitude = longitude
                
                point_number += 1
                save_to_excel(raw_sheet, latitude, longitude, altitude, distance, bearing, point_number)
                raw_workbook.save(raw_save_path)
                print(f"현재 위치를 저장 중입니다. 저장횟수: {point_number}")
                # 입자 필터 적용
                if not particles_initialized:
                    initial_latitude = latitude
                    initial_longitude = longitude
                    particles = initialize_particles(initial_latitude, initial_longitude, NUM_PARTICLES)
                    particles_initialized = True

                update_weights(particles, latitude, longitude)
                particles = resample_particles(particles, weights)
                est_lat, est_lon = estimate_position(particles, weights)
                est_alt = altitude  # 고도는 원본 값 그대로 사용

                # 입자 필터를 적용한 거리와 각도 계산
                est_distance = calculate_distance(prev_latitude, prev_longitude, est_lat, est_lon)
                est_bearing = calculate_bearing(prev_latitude, prev_longitude, est_lat, est_lon)

                corrected_point_number += 1
                save_to_excel(corrected_sheet, est_lat, est_lon, est_alt, est_distance, est_bearing, corrected_point_number)
                corrected_workbook.save(corrected_save_path)
                print(f"현재 보정된 위치를 저장 중입니다. 저장횟수: {corrected_point_number}")

            except ValueError:
                print("현재 위치를 저장하고 있지 않습니다")

        time.sleep(1)

except KeyboardInterrupt:
    print("Program terminated by user")

finally:
    ser.close()
    raw_workbook.save(raw_save_path)
    corrected_workbook.save(corrected_save_path)
    print(f"원본 좌표 엑셀 파일이 '{raw_save_path}'에 저장되었습니다.")
    print(f"보정된 좌표 엑셀 파일이 '{corrected_save_path}'에 저장되었습니다.")
