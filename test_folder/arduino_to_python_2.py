import serial
import time

# 시리얼 포트 설정
ser1 = serial.Serial('COM6', 115200, timeout=1)  # 첫 번째 아두이노 (포트 변경 필요)
ser2 = serial.Serial('COM29', 115200, timeout=1)  # 두 번째 아두이노 (포트 변경 필요)

def read_gps_data(ser):
    """시리얼 포트에서 GNSS 데이터를 읽어들임"""
    lat1 = lon1 = alt1 = 0.0
    lat2 = lon2 = alt2 = 0.0

    try:
        # Arduino로부터 데이터를 한 줄씩 읽고, 디코드
        line = ser.readline().decode('utf-8').strip()

        if "GNSS_1" in line:
            # GNSS_1 데이터 파싱
            lat_line = ser.readline().decode('utf-8').strip()
            lon_line = ser.readline().decode('utf-8').strip()
            alt_line = ser.readline().decode('utf-8').strip()

            lat1 = float(lat_line.split("Lat: ")[1])
            lon1 = float(lon_line.split("Long: ")[1])
            alt1 = float(alt_line.split("Alt: ")[1])

        line = ser.readline().decode('utf-8').strip()
        if "GNSS_2" in line:
            # GNSS_2 데이터 파싱
            lat_line = ser.readline().decode('utf-8').strip()
            lon_line = ser.readline().decode('utf-8').strip()
            alt_line = ser.readline().decode('utf-8').strip()

            lat2 = float(lat_line.split("Lat: ")[1])
            lon2 = float(lon_line.split("Long: ")[1])
            alt2 = float(alt_line.split("Alt: ")[1])

    except (ValueError, IndexError) as e:
        print(f"데이터 파싱 오류: {e}")

    return lat1, lon1, alt1, lat2, lon2, alt2

while True:
    try:
        # 첫 번째 아두이노로부터 데이터 읽기
        lat1_1, lon1_1, alt1_1, lat1_2, lon1_2, alt1_2 = read_gps_data(ser1)
        print(f"첫 번째 아두이노 - GNSS_1: Lat: {lat1_1}, Lon: {lon1_1}, Alt: {alt1_1}")
        print(f"첫 번째 아두이노 - GNSS_2: Lat: {lat1_2}, Lon: {lon1_2}, Alt: {alt1_2}")

        # 두 번째 아두이노로부터 데이터 읽기
        lat2_1, lon2_1, alt2_1, lat2_2, lon2_2, alt2_2 = read_gps_data(ser2)
        print(f"두 번째 아두이노 - GNSS_1: Lat: {lat2_1}, Lon: {lon2_1}, Alt: {alt2_1}")
        print(f"두 번째 아두이노 - GNSS_2: Lat: {lat2_2}, Lon: {lon2_2}, Alt: {alt2_2}")

        time.sleep(1)

    except KeyboardInterrupt:
        print("프로그램 종료")
        break
    except Exception as e:
        print(f"오류 발생: {e}")
