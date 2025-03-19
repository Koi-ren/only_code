import serial
import time
import openpyxl
import random
import numpy as np

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

# 좌표 데이터를 엑셀에 저장하는 함수
def save_to_excel(sheet, latitude, longitude, altitude, point_number):
    sheet.append([f"{point_number}", f"{latitude}", f"{longitude}", f"{altitude}"])

# 시리얼 포트 설정
serial_port = 'COM6'
baud_rate = 9600

# 엑셀 파일 및 워크북 초기화
raw_save_path = "C:/Users/plane/Desktop/park_ws/gps_track/raw_coordinates.xlsx"
corrected_save_path = "C:/Users/plane/Desktop/park_ws/gps_track/corrected_coordinates.xlsx"
button_corrected_save_path = "C:/Users/plane/Desktop/park_ws/gps_track/button_corrected_coordinates.xlsx"

raw_workbook = openpyxl.Workbook()
raw_sheet = raw_workbook.active
raw_sheet.title = "Raw Coordinates"
raw_sheet.append(["Point Number", "Latitude", "Longitude", "Altitude"])

corrected_workbook = openpyxl.Workbook()
corrected_sheet = corrected_workbook.active
corrected_sheet.title = "Corrected Coordinates"
corrected_sheet.append(["Point Number", "Latitude", "Longitude", "Altitude"])

button_corrected_workbook = openpyxl.Workbook()
button_corrected_sheet = button_corrected_workbook.active
button_corrected_sheet.title = "Button Corrected Coordinates"
button_corrected_sheet.append(["Point Number", "Latitude", "Longitude", "Altitude"])

ser = serial.Serial(serial_port, baud_rate)
point_number = 0
particles_initialized = False  # 입자 초기화 여부 확인

try:
    while True:
        latitudes = []
        longitudes = []
        altitudes = []
        button_signal = None  # 버튼 신호 초기화

        # 5초 동안 5개의 데이터를 수집
        for _ in range(5):
            line = ser.readline().decode('utf-8').strip()
            
            if line.startswith("Lat:"):
                try:
                    parts = line.split()
                    latitude = float(parts[1]) / 10000000.0
                    longitude = float(parts[3]) / 10000000.0
                    altitude = float(parts[5])
                    
                    # 버튼 신호 처리
                    if "Button_Signal:" in line:
                        button_signal_str = line.split("Button_Signal:")[1].strip()
                        button_signal = int(button_signal_str)
                    
                    latitudes.append(latitude)
                    longitudes.append(longitude)
                    altitudes.append(altitude)
                    
                    point_number += 1
                    save_to_excel(raw_sheet, latitude, longitude, altitude, point_number)
                    raw_workbook.save(raw_save_path)
                
                except ValueError:
                    print("현재 위치를 저장하고 있지 않습니다")

            time.sleep(1)

        # 입자 필터 적용하여 위치 보정
        for latitude, longitude in zip(latitudes, longitudes):
            if not particles_initialized and initial_latitude is not None and initial_longitude is not None:
                particles = initialize_particles(initial_latitude, initial_longitude, NUM_PARTICLES)
                particles_initialized = True

            if particles_initialized:
                update_weights(particles, latitude, longitude)
                particles = resample_particles(particles, weights)

        est_lat = None
        est_lon = None
        est_alt = None

        if particles_initialized:
            # Check if latitudes and longitudes are non-empty before estimating
            if latitudes and longitudes:
                est_lat, est_lon = estimate_position(particles, weights)
            
            # Check if altitudes is non-empty before calculating mean
            if altitudes:
                est_alt = np.mean(altitudes)  # 고도는 평균값으로 보정

            point_number += 1
            save_to_excel(corrected_sheet, est_lat, est_lon, est_alt, point_number)
            corrected_workbook.save(corrected_save_path)

        # 버튼이 눌렸는지 확인
        if button_signal == 1:
            if not particles_initialized:
                # 초기 입자 필터 설정
                initial_latitude = latitude
                initial_longitude = longitude
                particles = initialize_particles(initial_latitude, initial_longitude, NUM_PARTICLES)
                particles_initialized = True

            # Check if estimated values are available before saving
            if est_lat is not None and est_lon is not None and est_alt is not None:
                save_to_excel(button_corrected_sheet, est_lat, est_lon, est_alt, point_number)
                button_corrected_workbook.save(button_corrected_save_path)

                # 보정된 좌표값과 포인트 넘버를 콘솔에 출력
                print('------------------------------------------------------------------------------------------------')
                print(f"Latitude: {est_lat}, Longitude: {est_lon}, Altitude: {est_alt}, Point: {point_number}")
                print('------------------------------------------------------------------------------------------------')

except KeyboardInterrupt:
    print("Program terminated by user")

finally:
    ser.close()
    raw_workbook.save(raw_save_path)
    corrected_workbook.save(corrected_save_path)
    button_corrected_workbook.save(button_corrected_save_path)
    print(f"원본 좌표 엑셀 파일이 '{raw_save_path}'에 저장되었습니다.")
    print(f"보정된 좌표 엑셀 파일이 '{corrected_save_path}'에 저장되었습니다.")
    print(f"버튼으로 보정된 좌표 엑셀 파일이 '{button_corrected_save_path}'에 저장되었습니다.")
