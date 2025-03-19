import serial
import time
import csv

# 시리얼 포트 설정
serial_port = 'COM30'  # 본인 시리얼 통신 포트 확인하고 설정
baud_rate = 115200  # 시리얼 통신 속도 설정

gps_save_path = "C:/Users/plane/Desktop/park_ws/gps+imu_drive/bunsudae_2.csv"

def save_to_csv(file_path, Point_number, Latitude, Longitude):
    """좌표 데이터를 CSV에 저장하는 함수"""
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([Point_number, Latitude, Longitude])

def read_gps_data(ser):
    """시리얼 포트에서 GPS 데이터를 읽어들임"""
    lat = lon = None  # None으로 초기화하여 0이 들어가는 것을 방지

    try:
        while not (lat and lon):  # 두 값 모두 유효할 때까지 반복
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                print(f"Read line from {ser.port}: {line}")  # 디버깅 메시지

                if line.startswith("Lat:"):
                    try:
                        parts = line.split()
                        if len(parts) >= 6:
                            # 위도, 경도, 고도를 파싱
                            lat = float(parts[1]) / 10000000.0
                            lon = float(parts[3]) / 10000000.0
                            # 데이터 유효성 검사
                            if not (35.11 <= lat <= 35.14 and 128 <= lon <= 130):
                                print("잘못된 데이터 범위. 다시 시도 중...")
                                lat = lon = None  # 잘못된 데이터를 무효화
                        else:
                            print("데이터 파싱 실패. 다시 시도 중...")
                    except ValueError:
                        print("데이터 파싱 오류. 다시 시도 중...")
                        lat = lon = None  # 파싱 실패 시 무효화
    except Exception as e:
        print(f"오류가 발생했습니다: {e}")
        return None, None

    return lat, lon

# 시리얼 포트 열기
ser = serial.Serial(serial_port, baud_rate)

# 포인트 번호 초기화
point_number = 0
i = 0

try:
    while True:
        i += 1

        # GPS 데이터를 읽어옴
        lat, lon = read_gps_data(ser)

        if lat and lon:
            print(f"포인트: {i} 위도: {lat}, 경도: {lon}")
            save_to_csv(gps_save_path, i, lat, lon)

        # 1초 대기
        time.sleep(1)

except KeyboardInterrupt:
    print("Program terminated by user")

finally:
    ser.close()
    print(f"csv 파일이 '{gps_save_path}'에 저장되었습니다.")
